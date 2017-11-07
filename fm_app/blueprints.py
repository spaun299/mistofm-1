from flask.blueprints import Blueprint


index_blueprint = Blueprint('index', __name__)
# admin_blueprint = Blueprint('admin', __name__)
static_blueprint = Blueprint('static', __name__, static_folder='static')
auth_blueprint = Blueprint('auth', __name__)
api_health_bp = Blueprint('api_health', __name__)
api_station_bp = Blueprint('api_station', __name__)


def register_blueprints_web(app):
    from .views import index_view
    app.register_blueprint(index_blueprint, url_prefix='')
    app.register_blueprint(static_blueprint)


def register_blueprints_admin(app):
    app.register_blueprint(static_blueprint)
    from .views import auth_view
    app.register_blueprint(auth_blueprint)


def register_blueprints_api(app):
    from .api import health_api
    app.register_blueprint(api_health_bp, url_prefix='/health')
    from .api import station_api
    app.register_blueprint(api_station_bp, url_prefix='/station')
