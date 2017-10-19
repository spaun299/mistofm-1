from flask import Flask, g, render_template, current_app
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_login import LoginManager, current_user
from flask_user import UserManager, SQLAlchemyAdapter
import config
from .blueprints import register_blueprints
from flask_sqlalchemy import SQLAlchemy
import logging
from logging.handlers import TimedRotatingFileHandler
from sqlalchemy import event
from utils import get_database_uri, get_db_session
from .models import Station, Image, User, Playlist, PlaylistMusic, Music, \
    StationIces, HtmlHeader
from .admin import StationView, ImageView, IndexView, AdminView,\
    StationIcesView, PlaylistView, PlaylistMusicView, MusicView
import os
from .errors import IcesException


def init_app():
    app = Flask(__name__)
    app.config.from_object(config)
    create_necessary_folders()
    try:
        db_config_fields = (app.config.get('DB_HOST'), app.config.get('DB_USERNAME'),
        app.config.get('DB_PASSWORD'), app.config.get('DB_NAME'))
    except AttributeError as e:
        raise ValueError(e)
    for field in db_config_fields:
        if not field:
            raise ValueError("Please specify '%s' in config file" % field)
    db_url = get_database_uri(*db_config_fields)
    app.config.update(dict(SQLALCHEMY_DATABASE_URI=db_url))
    configure_logger(app)
    app.logger.debug("Run ices modules")
    run_ices_modules(db_url)
    app.logger.debug("Add before request handlers")
    app.before_request(lambda: load_db_session(db_url))
    app.before_request(get_current_user)
    app.teardown_request(teardown_request)
    app.logger.debug("Register blueprints")
    register_blueprints(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.user_loader(load_user)
    user_db = SQLAlchemy(app)
    db_adapter = SQLAlchemyAdapter(user_db, type('UserModel',
                                                 (user_db.Model, User), {}))
    user_manager = UserManager(db_adapter, app)
    app.logger.debug("Init admin panel")
    init_admin_panel(app)

    @app.errorhandler(404)
    def handle_404(err):
        return render_template("error.html", code=404,
                               message="Page not found",
                               stations=[st.name for st in
                                         g.db.query(Station.name).all()])

    @app.errorhandler(500)
    def handle_500(err):
        app.logger.error("Internal server error. %s" % str(err))
        return render_template("error.html", message="Server error", code=500)
    return app


def load_user(_id):
    return g.db.query(User).filter_by(id=int(_id)).one()


def get_current_user():
    g.user = current_user


def configure_logger(app):
    log_handler = TimedRotatingFileHandler(config.LOG_PATH, "midnight",
                                           backupCount=config.LOG_ROTATE_COUNT)
    log_handler.setLevel(logging.ERROR)
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.ERROR)
    werkzeug_logger.addHandler(log_handler)
    app.logger.addHandler(log_handler)


def load_db_session(db_url):
    db_session, connection = get_db_session(db_url)
    g.db = db_session
    g.db_connection = connection


def teardown_request(err):
    db = getattr(g, 'db', None)
    sql_connection = getattr(g, 'db_connection', None)
    if db is not None:
        if err:
            db.rollback()
        db.remove()
    if sql_connection:
        sql_connection.close()


def run_ices_modules(db_url):
    session, connection = get_db_session(db_url)
    for station in session.query(StationIces).filter_by(active=True).all():
        if not station.running:
            station.start_ices()
    session.remove()
    connection.close()


def init_admin_panel(app):
    admin = Admin(name="Mistofm", template_mode="bootstrap3",
                  index_view=IndexView(url=config.ADMIN_URL_PREFIX))
    admin.init_app(app)
    db_session, connection = get_db_session(app.config.get('SQLALCHEMY_DATABASE_URI'))

    # remove db session each time when close connection in
    # order to refresh data and get new session
    @admin.app.teardown_request
    def app_teardown(resp):
        db_session.remove()
        connection.close()
        return resp
    admin.add_view(StationView(Station, db_session))
    admin.add_view(ImageView(Image, db_session))
    admin.add_view(MusicView(Music, db_session))
    admin.add_view(PlaylistView(Playlist, db_session))
    admin.add_view(StationIcesView(StationIces, db_session))
    admin.add_view(PlaylistMusicView(PlaylistMusic, db_session))
    admin.add_view(AdminView(HtmlHeader, db_session))
    admin.add_link(MenuLink(name='Logout', category='', url="/logout"))


def create_necessary_folders():
    folders = (config.IMAGES_PATH, config.MUSIC_PATH,
               config.ICES_CONFIGS_PATH, config.TMP_FOLDER)
    for folder in folders:
        os.makedirs(folder, exist_ok=True)


@event.listens_for(Image, 'after_delete')
def delete_image(mapper, connection, target):
    if target.stored_on_server:
        try:
            target.remove_picture()
        except OSError:
            pass


@event.listens_for(StationIces, 'after_delete')
def delete_station(mapper, connection, target):
    try:
        target.stop_ices()
    except IcesException as e:
        if 'Process already stopped' in e.message:
            pass
    target.delete_ices_from_file_system()


@event.listens_for(Music, 'after_delete')
def delete_music(mapper, connection, target):
    target.delete_song()
