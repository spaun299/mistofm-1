from ..blueprints import index_blueprint
from flask import render_template


@index_blueprint.route('/')
def index():
    return render_template('index.html')
