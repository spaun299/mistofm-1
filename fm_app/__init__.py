from flask import Flask, g
import config
from .blueprints import register_blueprints
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import logging
from logging.handlers import TimedRotatingFileHandler
from utils import get_database_uri


def init_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.logger.addHandler(get_logging_handler())
    app.before_request(load_database)
    register_blueprints(app)
    return app


def get_logging_handler():
    log_handler = TimedRotatingFileHandler(config.LOG_PATH, "midnight",
                                           backupCount=config.LOG_ROTATE_COUNT)
    log_handler.setLevel(logging.INFO)
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.INFO)
    werkzeug_logger.addHandler(log_handler)
    return log_handler


def load_database():
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
    g.sql_connection = engine.connect()
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    g.db = db_session
