from flask import Flask
import config
from .blueprints import register_blueprints


def init_app():
    app = Flask(__name__)
    app.config.from_object(config)
    register_blueprints(app)

    return app
