#!/usr/bin/python3
from urllib.request import Request, urlopen
from urllib import error
import sys
import json
import base64
sys.path.append("/home/vkobryn/Projects/mistofm")
import config
from fm_app import constants

api_base_url = config.API_URL
api_ices_health_url = api_base_url + constants.API_STATION_HEALTH_PATH
api_ices_restart_url = api_base_url + constants.API_RESTART_ICES_PATH
creds = base64.b64encode('{}:{}'.format(config.API_USERNAME,
                                        config.API_PASSWORD).encode('ascii'))
try:
    health_req = Request(api_ices_health_url)
    health_req.add_header('Authorization',
                          'Basic ' + creds.decode("ascii"))
    health_resp = json.loads(str(urlopen(health_req).read(), 'utf-8'))
    if health_resp.get(constants.API_ERROR_TEXT):
        print(health_resp.get('message'))
        exit(-1)
    stations = health_resp.get('stations')
    if not stations:
        print("Api didn't return any station")
    for station in stations:
        if station['active'] and not station['running']:
            try:
                restart_ices_req = Request('%s/%s' % (api_ices_restart_url,
                                                      station['id']))
                restart_ices_req.add_header(
                    'Authorization',
                    'Basic %s:%s' % (config.API_USERNAME, config.API_PASSWORD))
                restart_ices_resp = json.loads(str(urlopen(restart_ices_req).read(),
                                                   'utf-8'))
                if restart_ices_resp.get(constants.API_ERROR_TEXT):
                    print("Can't restart ices via API")
                    print(restart_ices_resp.get('message'))
                    exit(-1)
            except error.HTTPError as e:
                print(e.code)

except error.HTTPError as e:
    print(e.code)
