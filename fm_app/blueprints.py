from flask.blueprints import Blueprint


index_blueprint = Blueprint('index', __name__)
# admin_blueprint = Blueprint('admin', __name__)
static_blueprint = Blueprint('static', __name__, static_folder='static')
auth_blueprint = Blueprint('auth', __name__)
api_health_bp = Blueprint('api_health', __name__)
api_station_bp = Blueprint('api_station', __name__)
api_music_bp = Blueprint('api_music', __name__)
api_info_bp = Blueprint('api_info', __name__)


def register_blueprints_web(app):
    from .views import main_views
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
    from .api import music_api
    app.register_blueprint(api_music_bp, url_prefix='/music')
    from .api import info_api
    app.register_blueprint(api_info_bp, url_prefix='/info')
