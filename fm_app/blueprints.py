from flask.blueprints import Blueprint


index_blueprint = Blueprint('index', __name__)


def register_blueprints(app):
    from .views import index_view
    app.register_blueprint(index_blueprint, url_prefix='')
