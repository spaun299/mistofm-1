from flask.blueprints import Blueprint


index_blueprint = Blueprint('index', __name__)
static_blueprint = Blueprint('static', __name__, static_folder='static')


def register_blueprints(app):
    from .views import index_view
    app.register_blueprint(index_blueprint, url_prefix='')
    app.register_blueprint(static_blueprint)
