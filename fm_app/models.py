from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, \
    String, Boolean, DateTime, Table, UniqueConstraint
from flask import flash, current_app
import datetime
import config
from utils import copy_file, move_file, delete_file, run_cli_script, file_exists, kill_process, get_pid_by_args, \
    get_hours_from_timeframe
import os
from .errors import IcesException, PlaylistException
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
    metadata_url = Column(VARCHAR(200))
    description_html = Column(VARCHAR(500))
    cr_tm = Column(DateTime, nullable=False)
    images = relationship('Image', secondary=station_image_table, backref="stations")

    def __init__(self, name=None, stream_url=None, description_html=None,
                 stream_url_free_channel=None, metadata_url=None):
        self.name = name
        self.stream_url = stream_url
        self.stream_url_free_channel = stream_url_free_channel
        self.description_html = description_html
        self.cr_tm = datetime.datetime.now()
        self.metadata_url = metadata_url

    def __repr__(self):
        return self.name


class Image(Base):

    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    image_url = Column(String)
    name = Column(String, unique=True, nullable=False)
    stored_on_server = Column(Boolean, default=False)

    def __init__(self, image_url=None, name=None, stored_on_server=False, image_data=None):
        self.image_url = image_url
        self.name = name
        self.stored_on_server = stored_on_server
        self.image_data = image_data

    def __repr__(self):
        return self.name or self.image_url

    @property
    def image_path(self):
        return '{root}/{images_url}'.format(
            root=current_app.root_path, images_url=self.image_url)

    def rename_filename_to_id(self, tmp_filename):
        folder_path = config.IMAGES_PATH
        os.rename(folder_path + tmp_filename, folder_path + str(self.id))

    def get_stored_image_url(self, file_ext):
        return r'/{folder_path}{id}.{file_ext}'.format(folder_path=config.IMAGES_PATH,
                                                       id=self.id, file_ext=file_ext)

    def remove_picture(self):
        delete_file(self.image_path)

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

    def __repr__(self):
        return self.nickname

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

    def __init__(self, song_name=None, songs=[], playlists=[]):
        self.song_name = song_name
        self.songs = songs
        self.playlists = playlists

    def __repr__(self):
        return self.song_name

    # @property
    # def songs(self):
    #     return self.song_name
    #
    # @songs.setter
    # def songs(self, song_names):
    #     multiple_songs = []
    #     for val in song_names:
    #         multiple_songs.append(Music(val, playlists=self.playlists))
    #     g.db.add_all(multiple_songs)

    def delete_song(self):
        try:
            delete_file(config.MUSIC_PATH + self.song_name)
        except OSError:
            pass


class StationIces(Base):
    __tablename__ = 'station_ices'
    id = Column(Integer, primary_key=True)
    jingle_id = Column(Integer, ForeignKey(Music.id))
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
    play_jingle_after_songs_count = Column(Integer, default=5)
    jingle = relationship('Music', backref='stations')

    def __init__(self, name=None, genre=None, description=None, bitrate=128,
                 crossfade=10, active=True, server_host=None, server_port=None,
                 server_rotocol=None, server_mountpoint=None, password=None,
                 jingle=None, play_jingle_after_songs_count=None, **kwargs):
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
        self.jingle = jingle
        self.play_jingle_after_songs_count = play_jingle_after_songs_count
        # Note: password will not be saved into the database.
        # It's just for creating isec config file
        self.password = password

    def __repr__(self):
        return self.name

    @property
    def ices_config_path(self):
        return self.get_ices_conf_path()

    @property
    def ices_playlist_module(self):
        return 'playlist_%s.py' % self.id


    @property
    def pid(self):
        _pid = get_pid_by_args('ices', self.ices_config_path)
        return _pid

    @property
    def running(self):
        return True if self.pid else False

    @property
    def status(self):
        return 'ON' if self.running else 'OFF'

    def get_ices_conf_path(self):
        return '{folder}{id}_ices.xml'.format(folder=config.ICES_CONFIGS_PATH,
                                              id=self.id)

    @property
    def playlist_module_path(self):
        return config.ICES_PYTHON_MODULES_PATH + self.ices_playlist_module

    def start_ices(self):
        if not self.running:
            run_cli_script(
                '{bash_script} {ices_path} {config_path}'.format(
                    bash_script=config.BASH_RUN_ICES,
                    ices_path=config.ICES_PROGRAMM_PATH,
                    config_path=self.ices_config_path))
        else:
            raise IcesException("Ices station %s already is running" % self.name)

    def stop_ices(self):
        if self.running:
            try:
                kill_process(self.pid)
            except Exception as e:
                raise IcesException("Can't stop ices station %s." % self.name, err=e)
        else:
            raise IcesException("Can't stop ices station %s. Process already stopped" % self.name)

    def restart_ices(self):
        try:
            self.stop_ices()
        except IcesException:
            pass
        self.start_ices()

    def create(self, session):
        ices_tmp_conf = None
        try:
            ices_conf_name = '%s_ices.xml' % self.id
            ices_tmp_conf = copy_file(config.ICES_BASE_CONFIG_PATH, config.TMP_FOLDER,
                                      ices_conf_name)
            self.fill_ices_config(ices_tmp_conf)
            ices_conf_perm_path = config.ICES_CONFIGS_PATH + ices_conf_name
            move_file(ices_tmp_conf, ices_conf_perm_path)
            copy_file(config.ICES_PYTHON_BASE_MODULE_PATH,
                      config.ICES_PYTHON_MODULES_PATH, "playlist_%s.py" % self.id)
            session.commit()
            if self.active:
                self.start_ices()
                if not self.running:
                    msg = "Ices station was saved and configured, " \
                          "but can't run. Please see logs"
                    flash(msg)
                    raise IcesException(msg)
        except Exception as e:
            session.rollback()
            try:
                # Delete all created files if something went wrong
                self.delete_ices_from_file_system(ices_tmp_conf)
            except OSError:
                pass
            finally:
                raise Exception(e)

    def edit(self, session):
        backup_conf_name = 'ices_%s_backup_xml' % self.id
        copy_file(self.ices_config_path, config.TMP_FOLDER, backup_conf_name)
        try:
            self.fill_ices_config(self.ices_config_path)
        except Exception as e:
            move_file(backup_conf_name, self.ices_config_path)
            session.rollback()
        finally:
            delete_file(config.TMP_FOLDER + backup_conf_name)
            if self.active:
                try:
                    self.restart_ices()
                except IcesException as e:
                    if 'Process already stopped' in e.message:
                        pass
                if not self.running:
                    msg = "Ices station was saved and configured, " \
                          "but can't run. Please see logs"
                    flash(msg)
                    raise IcesException(msg)
            else:
                self.stop_ices()

    def delete_ices_from_file_system(self, tmp_file=None):
        files = [self.playlist_module_path, self.playlist_module_path + 'c', self.ices_config_path]
        if tmp_file:
            files.append(tmp_file)
        for fname in files:
            if file_exists(fname):
                delete_file(fname)

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
                 active=True, station_ices=None, songs=[]):
        self.name = name
        self.randomize = randomize
        self.active = active
        self.play_from_hour = play_from_hour
        self.play_to_hour = play_to_hour
        self.station_ices = station_ices
        self.songs = songs

    def __repr__(self):
        return self.name

    def create(self):
        pass

    def validate(self):
        # TODO: check if play_from_hour and play_to_hour don't cross with other playlists in that station
        if self.active:
            try:
                station_playlists = [playlist for playlist in self.station_ices.playlists
                                     if playlist.active and playlist.id != self.id]
            except AttributeError:
                station_playlists = None
            if station_playlists:
                default_err_message = "Playlist is crossing with playlist '%s'." \
                                      "Choose another time frames"
                self_hours_list = get_hours_from_timeframe(self.play_from_hour, self.play_to_hour)
                for station_playlist in station_playlists:
                    if station_playlist.play_from_hour == self_hours_list[0] \
                          or station_playlist.play_to_hour == self_hours_list[-1]:
                        raise PlaylistException(default_err_message % station_playlist)
                    station_hours_list = get_hours_from_timeframe(
                        station_playlist.play_from_hour, station_playlist.play_to_hour)[1:-1]
                    if any(hour in self_hours_list for hour in station_hours_list) \
                            or any(hour in station_hours_list for hour in self_hours_list):
                        raise PlaylistException(default_err_message % station_playlist)


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


class HtmlHeader(Base):
    __tablename__ = 'html_header'
    id = Column(Integer, primary_key=True)
    html_tag = Column(String, unique=True, nullable=False)

    def __init__(self, html_tag=None):
        self.html_tag = html_tag

    def __repr__(self):
        return self.html_tag
