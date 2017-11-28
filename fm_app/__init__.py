from flask import Flask, g, render_template
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_login import LoginManager, current_user
from flask_user import UserManager, SQLAlchemyAdapter
import config
from .blueprints import register_blueprints_web, \
    register_blueprints_admin, register_blueprints_api
from flask_sqlalchemy import SQLAlchemy
import logging
from logging.handlers import TimedRotatingFileHandler
from sqlalchemy import event
from utils import get_database_uri, get_db_session, capitalize_string, \
    json_response, current_year
from .models import Station, Image, User, Playlist, PlaylistMusic, Music, \
    StationIces, HtmlHeader
from .admin import StationView, ImageView, IndexView, AdminView,\
    StationIcesView, PlaylistView, PlaylistMusicView, MusicView
import os
from .errors import IcesException


def get_base_app():
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
    app.logger.debug("Add before request handlers")
    app.before_request(lambda: load_db_session(db_url))
    return app


def init_app_web():
    app = get_base_app()
    app.logger.debug("Register blueprints")
    register_blueprints_web(app)
    app.teardown_request(app_teardown)
    app.jinja_env.globals.update(capitalize_string=capitalize_string)
    app.jinja_env.globals.update(current_year=current_year)

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


def init_app_admin():
    app = get_base_app()
    app.logger.debug("Run ices modules")
    run_ices_modules(app.config['SQLALCHEMY_DATABASE_URI'])
    app.before_request(get_current_user)
    app.logger.debug("Register blueprints")
    register_blueprints_admin(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.user_loader(load_user)
    user_db = SQLAlchemy(app)
    db_adapter = SQLAlchemyAdapter(user_db, type('UserModel',
                                                 (user_db.Model, User), {}))
    user_manager = UserManager(db_adapter, app)
    admin = Admin(name="Mistofm", template_mode="bootstrap3",
                  index_view=IndexView(url=config.ADMIN_URL_PREFIX))
    admin.init_app(app)
    db_session, connection, engine = get_db_session(app.config.get('SQLALCHEMY_DATABASE_URI'))

    # remove db session each time when close connection in
    # order to refresh data and get new session
    @app.teardown_request
    def teardown(err):
        db_session.remove()
        connection.close()
        engine.dispose()
        db = getattr(g, 'db', None)
        sql_connection = getattr(g, 'db_connection', None)
        g_engine = getattr(g, 'engine', None)
        if db is not None:
            if err:
                db.rollback()
            db.remove()
        if sql_connection:
            sql_connection.close()
        if g_engine:
            g_engine.dispose()
        return err
    admin.add_view(StationView(Station, db_session))
    admin.add_view(ImageView(Image, db_session))
    admin.add_view(MusicView(Music, db_session))
    admin.add_view(PlaylistView(Playlist, db_session))
    admin.add_view(StationIcesView(StationIces, db_session))
    admin.add_view(PlaylistMusicView(PlaylistMusic, db_session))
    admin.add_view(AdminView(HtmlHeader, db_session))
    admin.add_link(MenuLink(name='Logout', category='', url="/logout"))
    return app


def init_app_api():
    app = get_base_app()
    app.logger.debug("Register blueprints")
    register_blueprints_api(app)
    app.teardown_request(app_teardown)

    @app.errorhandler(400)
    def error_400(err):
        app.logger.debug("Bad request")
        return json_response(err=True, message='Bad request', code=400), 400

    @app.errorhandler(401)
    def error_401(err):
        app.logger.warning("Not authorized access")
        return json_response(err=True, message='Not authorized', code=401), 401

    @app.errorhandler(404)
    def error_404(err):
        app.logger.debug("Page not found")
        return json_response(err=True, message='Not found', code=404), 404

    @app.errorhandler(405)
    def error_405(err):
        app.logger.debug("Method not allowed")
        return json_response(err=True, message='Method not allowed', code=405), 405

    @app.errorhandler(500)
    def error_500(err):
        app.logger.error("Internal server error.\n%s" % str(err))
        return json_response(err=True, message='Internal server error', code=500), 500
    return app


def app_teardown(err):
    db = getattr(g, 'db', None)
    sql_connection = getattr(g, 'db_connection', None)
    g_engine = getattr(g, 'engine', None)
    if db is not None:
        if err:
            db.rollback()
        db.remove()
    if sql_connection:
        sql_connection.close()
    if g_engine:
        g_engine.dispose()
    return err


def load_user(_id):
    return g.db.query(User).filter_by(id=int(_id)).one()


def get_current_user():
    g.user = current_user


def configure_logger(app):
    log_handler = TimedRotatingFileHandler(config.LOG_PATH, "midnight",
                                           backupCount=config.LOG_ROTATE_COUNT)
    log_handler.setLevel(logging.WARNING)
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [File:%(name)s] [Message:%(message)s]')
    log_handler.setFormatter(formatter)
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.WARNING)
    werkzeug_logger.addHandler(log_handler)
    app.logger.addHandler(log_handler)


def load_db_session(db_url):
    db_session, connection, engine = get_db_session(db_url)
    g.db = db_session
    g.db_connection = connection
    g.engine = engine


def run_ices_modules(db_url):
    session, connection, engine = get_db_session(db_url)
    for station in session.query(StationIces).filter_by(active=True).all():
        if not station.running:
            station.start_ices()
    session.remove()
    connection.close()
    engine.dispose()


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
