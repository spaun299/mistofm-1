from flask import Flask, g
from flask_admin import Admin
from flask.ext.login import LoginManager, current_user
from flask_user import login_required, UserManager, SQLAlchemyAdapter
import config
from .blueprints import register_blueprints
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
import logging
from logging.handlers import TimedRotatingFileHandler
from utils import get_database_uri
from .models import Station, Image, User
from .admin import StationView, ImageView


def init_app():
    app = Flask(__name__)
    app.config.from_object(config)
    configure_logger(app)
    app.before_request(load_db_session)
    app.before_request(get_current_user)
    register_blueprints(app)
    login_manager = LoginManager(app)
    login_manager.user_loader(load_user)
    user_db = SQLAlchemy(app)
    db_adapter = SQLAlchemyAdapter(user_db, type('UserModel',
                                                 bases=(user_db.Model, User)))
    user_manager = UserManager(db_adapter, app)
    init_admin_panel(app)
    return app


def load_user(_id):
    return g.db.query(User).filter_by(id=int(_id)).one()


def get_current_user():
    g.user = current_user


def configure_logger(app):
    log_handler = TimedRotatingFileHandler(config.LOG_PATH, "midnight",
                                           backupCount=config.LOG_ROTATE_COUNT)
    log_handler.setLevel(logging.INFO)
    if not config.DEBUG:
        werkzeug_logger = logging.getLogger('werkzeug')
        werkzeug_logger.setLevel(logging.INFO)
        werkzeug_logger.addHandler(log_handler)
    app.logger.addHandler(log_handler)


def load_db_session():
    db_session = get_db_session()
    g.db = db_session


def get_db_session():
    try:
        db_config_fields = (config.DB_HOST, config.DB_USERNAME,
                            config.DB_PASSWORD, config.DB_NAME)
    except AttributeError as e:
        raise ValueError(e)
    for field in db_config_fields:
        if not field:
            raise ValueError("Please specify '%s' in config file" % field)
    engine = create_engine(get_database_uri(*db_config_fields),
                           echo=False)
    engine.connect()
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    return db_session


def init_admin_panel(app):
    admin = Admin(name="Mistofm", template_mode="bootstrap3")
    admin.init_app(app)
    db_session = get_db_session()

    # remove db session each time when close connection in
    # order to refresh data and get new session
    @admin.app.teardown_request
    def app_teardown(resp):
        db_session.remove()
        return resp
    admin.add_view(StationView(Station, db_session))
    admin.add_view(ImageView(Image, db_session))
