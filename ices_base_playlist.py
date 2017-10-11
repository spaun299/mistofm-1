#!/usr/bin/python3
import sys
import os
sys.path.append("/home/vkobryn/Projects/mistofm")
import config
import psycopg2
import psycopg2.extras
import logging
import pytz
import datetime
import utils


model = None


class Db:

    db_url = "host='{host}' dbname='{db_name}' " \
             "user='{user}' password='{password}'".format(host=config.DB_HOST, db_name=config.DB_NAME,
                                                          user=config.DB_USERNAME, password=config.DB_PASSWORD)

    def __init__(self):
        self.connection = psycopg2.connect(self.db_url)
        self.session = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def close_connection(self):
        print("Close db connection")
        self.connection.close()


class Model:
    def __init__(self, station_id):
        self.station_id = station_id
        self.timezone = pytz.timezone('Europe/Uzhgorod')

    @property
    def current_hour(self):
        return datetime.datetime.now(self.timezone).hour

    def current_playlist(self, db_cursor):
        hours_
        db_cursor.execute(""" SELECT """)


def ices_init():
    global model
    try:
        print("Getting id from module name")
        station_id = int(__name__.split('_')[0])
        print('Checking db connection')
        db = Db()
        db.close_connection()
        print("Creating model instance")
        model = Model(station_id)
        return 1
    except ValueError:
        print("Can't get station id from module name")
        return 0
    except psycopg2.DatabaseError:
        print("Can't connect to database")
        return 0


def ices_get_next(*args, **kwargs):

    db = Db()
    # TODO: run jingle if there no songs in station playlist
    return '/home/vkobryn/mistofm/media/mistofm/media/louis_fonsi_feat_daddy_yankee_-_despasito_(zf.fm).mp3'
