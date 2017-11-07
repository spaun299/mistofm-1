from ..blueprints import api_health_bp
from ..models import StationIces
from flask_login import login_required
from flask import g
from utils import json_response


@api_health_bp.route('/stations')
@login_required
def check_stations_status():
    stations = []
    for station in g.db.query(StationIces).all():
        stations.append(dict(
            id=station.id,
            active=station.active,
            running=station.running
        ))
    return json_response(stations=stations)
