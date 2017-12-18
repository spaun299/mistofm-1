from ..blueprints import api_info_bp
from ..models import General
from utils import json_response
from flask import g


@api_info_bp.route('/general')
def general():
    general_model = g.db.query(General).one()
    return json_response(mail_main=general_model.mail_main,
                         mail_ads=general_model.mail_ads,
                         mail_support=general_model.mail_support,
                         mail_rotation=general_model.mail_rotation,
                         phone_main=general_model.phone_main,
                         phone_secondary=general_model.phone_secondary,
                         skype=general_model.skype,
                         address=general_model.address,
                         facebook_link=general_model.facebook_link,
                         instagram_link=general_model.instagram_link,
                         soundcloud_link=general_model.soundcloud_link,
                         youtube_link=general_model.youtube_link,
                         playmarket_link=general_model.playmarket_link,
                         appstore_link=general_model.appstore_link,
                         android_current_version=general_model.android_current_version,
                         ios_current_version=general_model.ios_current_version)
