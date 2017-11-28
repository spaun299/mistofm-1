from ..blueprints import index_blueprint
from flask import render_template, g, abort, Markup
from ..models import Station, HtmlHeader
from flask import Markup


@index_blueprint.route('/')
@index_blueprint.route('/<string:name>')
def station(name=None):
    stations = g.db.query(Station).all()
    html_tags = g.db.query(HtmlHeader).all()
    station_obj = None
    if name:
        for st in stations:
            if st.name == name:
                station_obj = st
                break
    else:
        if stations:
            station_obj = stations[0]
    if not station_obj:
        abort(404), 404
    station_obj.description_html = Markup(station_obj.description_html)
    return render_template('index.html', station=station_obj,
                           stations=[st.name for st in stations],
                           html_tags=[Markup(tag.html_tag) for tag in
                                      html_tags])


@index_blueprint.route('/contact_us')
def contact_us():
    stations = g.db.query(Station).all()
    html_tags = g.db.query(HtmlHeader).all()
    return render_template('contact.html',
                           stations=[st.name for st in stations],
                           html_tags=[Markup(tag.html_tag) for tag in
                                      html_tags])
