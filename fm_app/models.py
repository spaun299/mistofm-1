from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, \
    String, Boolean, DateTime, Table, UniqueConstraint
from flask import g, flash, current_app
import datetime
import config
from utils import copy_file, move_file, delete_file, run_cli_script, file_exists
import os
from .errors import IcesException
import xml.etree.ElementTree as ET


Base = declarative_base()

station_image_table = Table('station_image', Base.metadata,
                            Column('station_id', Integer, ForeignKey('station.id')),
                            Column('image_id', Integer, ForeignKey('image.id')))


class Station(Base):

    __tablename__ = 'station'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(30), nullable=False)
    stream_url_music = Column(VARCHAR(200), nullable=False)
    stream_url_free_channel = Column(VARCHAR(200))
    description_html = Column(VARCHAR(500))
    cr_tm = Column(DateTime, nullable=False)
    images = relationship('Image', secondary=station_image_table, backref="stations")

    def __init__(self, name=None, stream_url=None, description_html=None,
                 stream_url_free_channel=None):
        self.name = name
        self.stream_url = stream_url
        self.stream_url_free_channel = stream_url_free_channel
        self.description_html = description_html
        self.cr_tm = datetime.datetime.now()

    def __repr__(self):
        return self.name


class Image(Base):

    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    image_url = Column(String)
    name = Column(String, unique=True)
    stored_on_server = Column(Boolean, default=False)

    def __init__(self, image_url=None, name=None, stored_on_server=False, image_data=None):
        self.image_url = image_url
        self.name = name
        self.stored_on_server = stored_on_server
        self.image_data = image_data

    def __repr__(self):
        return self.name or self.image_url

    def rename_filename_to_id(self, tmp_filename):
        folder_path = config.IMAGES_PATH
        os.rename(folder_path + tmp_filename, folder_path + str(self.id))

    def get_stored_image_url(self, file_ext):
        return r'/{folder_path}{id}.{file_ext}'.format(folder_path=config.IMAGES_PATH,
                                                       id=self.id, file_ext=file_ext)

    def get_image_path(self):
        return '{root}/{images_url}'.format(
            root=current_app.root_path, images_url=self.image_url)

    def remove_picture(self):
        delete_file(self.get_image_path())

    def change_upload_image_url(self):
        self.image_url = config.IMAGES_PATH + str(self.id)
        self.stored_on_server = True


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String)
    user_type = Column(String, default="admin")

    def __init__(self, nickname=None, password=None, user_type=None, email=None):
        self.nickname = nickname
        self.password = password
        self.user_type = user_type
        self.email = email

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def has_confirmed_email(self):
        return True

    def get_id(self):
        return self.id


class Music(Base):
    __tablename__ = 'music'
    id = Column(Integer, primary_key=True)
    song_name = Column(String, nullable=False)
    playlists = relationship('Playlist', secondary='playlist_music',
                             back_populates='songs', lazy='dynamic')

    def __init__(self, song_name=None, songs=[]):
        self.song_name = song_name
        self.songs = songs

    @property
    def songs(self):
        return self.song_name

    @songs.setter
    def songs(self, song_names):
        multiple_songs = []
        for val in song_names:
            multiple_songs.append(Music(val))
        g.db.add_all(multiple_songs)

    def delete_song(self):
        delete_file(config.MUSIC_PATH + self.song_name)

    def __repr__(self):
        return self.song_name


class StationIces(Base):
    __tablename__ = 'station_ices'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(100), nullable=False)
    genre = Column(VARCHAR(50), nullable=False)
    description = Column(String, nullable=False)
    bitrate = Column(Integer, nullable=False, default=128)
    crossfade = Column(Integer, nullable=False, default=10)
    server_host = Column(VARCHAR(200), nullable=False, default='localhost')
    server_port = Column(Integer, nullable=False, default=8000)
    server_rotocol = Column(VARCHAR(20), nullable=False, default='http')
    server_mountpoint = Column(VARCHAR(100), nullable=False)
    active = Column(Boolean, default=True)

    def __init__(self, name=None, genre=None, description=None, bitrate=128,
                 crossfade=10, active=True, server_host=None, server_port=None,
                 server_rotocol=None, server_mountpoint=None, password=None, **kwargs):
        self.name = name
        self.genre = genre
        self.description = description
        self.bitrate = bitrate
        self.crossfade = crossfade
        self.active = active
        self.server_host = server_host
        self.server_port = server_port
        self.server_rotocol = server_rotocol
        self.server_mountpoint = server_mountpoint
        # Note: password will not be saved into the database.
        # It's just for creating isec config file
        self.password = password
        self.ices_config_path = None
        self.ices_pid_folder = None
        self.ices_playlist_module = None

    def __repr__(self):
        return self.name

    def get_ices_conf_path(self):
        return '{folder}{id}_ices.xml'.format(folder=config.ICES_CONFIGS_PATH,
                                              id=self.id)

    def get_playlist_module_path(self):
        return '%s_playlist.py' % self.id

    def start_ices(self):
        run_cli_script(
            '{ices_path} -c {config_path} & echo $1 > {pid_path}'.format(
                ices_path=config.ICES_PROGRAMM_PATH,
                config_path=self.ices_config_path,
                pid_path=self.ices_pid_folder))

    def stop_ices(self):
        pass

    def restart_ices(self):
        self.stop_ices()
        self.start_ices()

    def save(self):
        ices_tmp_conf = ices_conf_perm_path = None
        try:
            g.db.add(self)
            # flush session to get id
            g.db.flush()
            self.ices_pid_folder = self.get_pid_path()
            self.ices_config_path = self.get_ices_conf_path()
            self.ices_playlist_module = self.get_playlist_module_path()
            ices_conf_name = '%s_ices.xml' % self.id
            ices_tmp_conf = copy_file(config.ICES_BASE_CONFIG_PATH, config.TMP_FOLDER,
                                      ices_conf_name)
            self.fill_ices_config(ices_tmp_conf)
            ices_conf_perm_path = config.ICES_CONFIGS_PATH + ices_conf_name
            move_file(ices_tmp_conf, ices_conf_perm_path)
            copy_file(config.ICES_PYTHON_BASE_MODULE_PATH,
                      config.ICES_PYTHON_MODULES_PATH, "%s_playlist.py" % self.id)
            g.db.commit()
            self.start_ices()
            if not self.running():
                msg = "Ices station was saved and configured, " \
                      "but can't run. Please see logs"
                flash(msg)
                raise IcesException(msg)
        except Exception as e:
            g.db.rollback()
            try:
                # Delete all created files if something went wrong
                self.delete_ices_from_file_system(ices_tmp_conf)
            except OSError:
                pass
            finally:
                raise Exception(e)

    def delete_ices_from_file_system(self, tmp_file=None):
        files = [self.ices_playlist_module, self.ices_config_path]
        if tmp_file:
            files.append(tmp_file)
        for fname in files:
            if file_exists(fname):
                delete_file(fname)

    def get_pid_path(self):
        return config.ICES_PID_FOLDER + '%s_ices.pid' % self.id

    def running(self):
        return file_exists(self.ices_pid_folder)

    def fill_ices_config(self, base_config):
        tree = ET.parse(base_config)
        root = tree.getroot()
        playlist, _, stream = root
        playlist.find('Module').text = self.ices_playlist_module[:-3]
        playlist.find('Crossfade').text = str(self.crossfade)
        stream[0].find('Hostname').text = self.server_host
        stream[0].find('Port').text = str(self.server_port)
        stream[0].find('Password').text = str(self.password)
        stream[0].find('Protocol').text = self.server_rotocol
        stream.find('Mountpoint').text = self.server_mountpoint
        stream.find('Name').text = self.name
        stream.find('Genre').text = self.genre
        stream.find('Description').text = self.description
        stream.find('Bitrate').text = str(self.bitrate)
        tree.write(base_config)


class Playlist(Base):
    __tablename__ = 'playlist'
    id = Column(Integer, primary_key=True)
    station_id = Column(Integer, ForeignKey(StationIces.id))
    name = Column(VARCHAR(50), nullable=False, unique=True)
    randomize = Column(Boolean, default=False)
    play_from_hour = Column(Integer, nullable=False)
    play_to_hour = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)
    station_ices = relationship(StationIces, backref='playlists')
    songs = relationship(Music, secondary='playlist_music', back_populates='playlists',
                         lazy='dynamic')

    def __init__(self, name=None, randomize=False, play_from_hour=None, play_to_hour=None,
                 active=True, station_ices=None):
        self.name = name
        self.randomize = randomize
        self.active = active
        self.play_from_hour = play_from_hour
        self.play_to_hour = play_to_hour
        self.station_ices = station_ices

    def __repr__(self):
        return self.name

    def save(self):
        if self.active:
            self.validate_playlist()
        g.db.add(self)
        g.db.commit()

    def validate_playlist(self):
        # TODO: check if play_from_hour and play_to_hour don't cross with other playlists in that station
        pass


class PlaylistMusic(Base):
    __tablename__ = 'playlist_music'
    id = Column(Integer, primary_key=True)
    song_id = Column(Integer, ForeignKey('music.id'), nullable=False)
    playlist_id = Column(Integer, ForeignKey('playlist.id'), nullable=False)
    # order = Column(Integer, nullable=False)
    song = relationship(Music, backref='playlist_assoc')
    playlist = relationship(Playlist, backref='music_assoc')
    __table_args__ = (#UniqueConstraint('song_id', 'playlist_id', 'order',
                      #                 name='unique_order'),
                      UniqueConstraint('song_id', 'playlist_id',
                                       name='unique_song_playlist_pair'),)

    def __init__(self, song=None, playlist=None):
        self.song = song
        self.playlist = playlist
        # self.order = order

    def __repr__(self):
        return 'Playlist:%s|Song:%s' % (self.playlist.name, self.song.song_name)
