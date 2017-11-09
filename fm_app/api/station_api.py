from ..blueprints import api_station_bp
from ..models import StationIces
from flask import abort
from flask import g
from ..decorators import authorization_required_api
from utils import json_response


@api_station_bp.route('/restart', methods=['POST', ])
@authorization_required_api
def restart_stations():
    for station in g.db.query(StationIces).filter_by(
            active=True).all():
        try:
            station.restart_ices()
        except Exception:
            abort(500)
    return json_response(status='ok')


@api_station_bp.route('/restart/<int:station_id>',
                      methods=['POST', ])
@authorization_required_api
def restart_station(station_id):
    station = g.db.query(StationIces).filter_by(
        id=station_id, active=True).first()
    if not station:
        abort(404)
    try:
        station.restart_ices()
    except Exception:
        abort(500)
    return json_response(status='ok')
