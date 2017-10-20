#!/usr/bin/python
import sys
import os
sys.path.append("/home/vkobryn/Projects/mistofm")
import config
import psycopg2
import psycopg2.extras
import pytz
import datetime
import logging
import logging.handlers
import urllib2
import urllib


logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(
    config.ICES_PLAYLIST_LOG_FILE, maxBytes=(1048576*5), backupCount=5
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

model = None


class Db:

    db_url = "host='{host}' dbname='{db_name}' " \
             "user='{user}' password='{password}'".format(host=config.DB_HOST, db_name=config.DB_NAME,
                                                          user=config.DB_USERNAME, password=config.DB_PASSWORD)

    def __init__(self):
        self.connection = psycopg2.connect(self.db_url)
        self.session = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def close_connection(self):
        logger.debug("Close db connection")
        self.connection.close()


class Model:
    def __init__(self, station_id):
        self.station_id = station_id
        self.timezone = pytz.timezone('Europe/Uzhgorod')
        self.previous_playlist_id = 0
        self.previous_song_id = 0
        # if playlist play random songs we will add each
        # played song to list in order to not play played songs
        self.played_songs_id = []
        self.station_playlists = []
        self.playlists_count = 0
        self.metadata_add_url = "{host}/metadata/add/{station_id}/".format(host=config.METADATA_URL,
                                                                           station_id=self.station_id)
        self.metadata_get_url = "{host}/metadata/get/{station_id}/".format(host=config.METADATA_URL,
                                                                           station_id=self.station_id)
        self.metadata_body = \
            {"username": config.METADATA_USERNAME,
             "password": config.METADATA_PASSWORD}

    @property
    def current_hour(self):
        return datetime.datetime.now(self.timezone).hour

    def get_hours_from_timeframe(self, _from, _to):
        hours = []
        while _from != _to:
            hours.append(_from)
            if _from == 24:
                _from = 1
            else:
                _from += 1
        else:
            hours.append(_from)
        return hours

    def set_playlists(self, db_cursor):
        db_cursor.execute(""" SELECT id, randomize, play_from_hour play_from, play_to_hour play_to 
                                  FROM playlist WHERE active=TRUE AND station_id=%s;""" % self.station_id)
        playlists = db_cursor.fetchall()
        self.playlists_count = len(playlists)
        self.station_playlists = playlists

    def current_playlist(self):
        current_hour = int(self.current_hour)
        for playlist in self.station_playlists:
            if current_hour in self.get_hours_from_timeframe(
                    playlist['play_from'], playlist['play_to'])[:-1]:
                return playlist

    def update_playlists(self, db_cursor):
        """ update station_playlists if new playlist was created """
        db_cursor.execute(""" SELECT COUNT(id) FROM playlist 
                             WHERE active=TRUE AND station_id=%s;""" % self.station_id)
        if db_cursor.fetchone()[0] != self.playlists_count:
            self.set_playlists(db_cursor)

    def get_jingle(self, db_cursor):
        db_cursor.execute(""" SELECT music.song_name FROM station_ices JOIN music
                             ON station_ices.jingle_id=music.id 
                             WHERE station_ices.id=%s LIMIT 1; """ % self.station_id)
        return db_cursor.fetchone()

    def get_song(self, db_cursor):
        playlist = self.current_playlist()
        if not playlist:
            logger.debug('There are no active playlists for the station')
            return self.get_jingle(db_cursor)['song_name'], True
        if self.previous_playlist_id != playlist['id']:
            self.previous_playlist_id = playlist['id']
            self.played_songs_id = []
        query_string = """ SELECT m.song_name AS song_name, pm.id as id FROM music m 
                          JOIN playlist_music pm ON m.id=pm.song_id
                          JOIN playlist p ON p.id=pm.playlist_id  
                          WHERE pm.playlist_id=%s AND pm.id """ % playlist['id']
        if playlist['randomize']:
            self.previous_song_id = 0
            if self.played_songs_id:
                query_string_random = query_string + """ NOT IN (%s) ORDER BY random() LIMIT 1; """ % \
                                                     ', '.join(list(map(lambda s: str(s), self.played_songs_id)))
            else:
                query_string_random = query_string + """ IS NOT NULL ORDER BY random() LIMIT 1; """
            db_cursor.execute(query_string_random)
            song = db_cursor.fetchone()
            if song:
                self.played_songs_id.append(song['id'])
                return song['song_name'], False
            else:
                query_string_random = query_string + """ > 0 ORDER BY random() LIMIT 1; """
                db_cursor.execute(query_string_random)
                song = db_cursor.fetchone()
                if song:
                    self.played_songs_id = [song['id'], ]
                    return song['song_name'], False
                else:
                    self.played_songs_id = []
                    logger.debug("Playlist %s doesn't have any songs" % playlist['name'])
        else:
            self.played_songs_id = []
            query_string_ordered = query_string + """ > %s ORDER BY pm.id LIMIT 1; """ % self.previous_song_id
            db_cursor.execute(query_string_ordered)
            song = db_cursor.fetchone()
            if song:
                self.previous_song_id = song['id']
                return song['song_name'], False
            else:
                query_string_ordered = query_string + """ > 0 ORDER BY pm.id LIMIT 1; """
                db_cursor.execute(query_string_ordered)
                song = db_cursor.fetchone()
                if song:
                    self.previous_song_id = song['id']
                    return song['song_name'], False
                else:
                    self.previous_song_id = 0
                    logger.debug("Playlist %s doesn't have any songs" % playlist['name'])
        return self.get_jingle(db_cursor)['song_name'], True


def ices_init():
    global model
    try:
        logger.debug("Getting id from module %s" % __name__)
        station_id = int(__name__.split('_')[-1])
        logger.debug('Checking db connection')
        db = Db()
        logger.debug("Creating model instance")
        model = Model(station_id)
        model.set_playlists(db.session)
        db.close_connection()
        logger.debug("Check if metadata server is running")
        try:
            urllib2.urlopen(model.metadata_get_url)
        except urllib2.HTTPError:
            logger.error("Can't connect to metadata server")
            return 0
        logger.debug("Module configured")
        return 1
    except ValueError:
        logger.debug("Can't get station id from module name")
        return 0
    except psycopg2.DatabaseError as e:
        logger.debug("Can't connect to database. Error:%s" % e)
        return 0
    except Exception as e:
        logger.debug("Unknown error:%s" % e)


def ices_get_next(*args, **kwargs):
    db = Db()
    logger.debug("Updating playlists")
    model.update_playlists(db.session)
    logger.debug("Getting song name")
    song_name, is_jingle = model.get_song(db.session)
    db.close_connection()
    logger.debug("Send metadata to server")
    if not is_jingle:
        song_name_metadata = song_name
        if song_name_metadata.endswith('.mp3'):
            song_name_metadata = song_name[:-4]
        model.metadata_body.update({"song_name": song_name_metadata})
        request = urllib2.Request(model.metadata_add_url, urllib.urlencode(model.metadata_body))
        urllib2.urlopen(request)
    return config.MUSIC_PATH + song_name
