from flask.blueprints import Blueprint


index_blueprint = Blueprint('index', __name__)
# admin_blueprint = Blueprint('admin', __name__)
static_blueprint = Blueprint('static', __name__, static_folder='static')


def register_blueprints(app):
    from .views import index_view
    app.register_blueprint(index_blueprint, url_prefix='')
    # from .views import admin_view
    # app.register_blueprint(admin_blueprint, url_prefix='/manage')
    app.register_blueprint(static_blueprint)
