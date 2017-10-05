from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, \
    String, Boolean, DateTime, Table, UniqueConstraint
from flask import g
import datetime
import config
import os


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

    def remove_picture(self, image_name):
        os.remove(config.IMAGES_PATH + image_name)

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

    def __init__(self, song_name):
        self.song_name = song_name

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
    server_host = Column(VARCHAR(200), nullable=False)
    server_port = Column(Integer, nullable=False)
    server_rotocol = Column(VARCHAR(20), nullable=False, default='http')
    server_mountpoint = Column(VARCHAR(100), nullable=False)
    active = Column(Boolean, default=True)

    def __init__(self, name=None, genre=None, description=None, bitrate=128,
                 crossfade=10, active=True, server_host=None, server_port=None,
                 server_rotocol=None, server_mountpoint=None, password=None):
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

    def __repr__(self):
        return self.name

    def save(self):
        # TODO: Create new config file for ices with name id_ices.xml
        g.db.add(self)
        # flush session to get id
        g.db.flush()
        g.db.commit()


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
        if list(map(lambda hour: hour not in range(1, 24),
                    [self.play_from_hour, self.play_to_hour])):
            raise ValueError('play_from_hour and play_to_hour should be from 1 to 24')


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
                                       name='unique_song_playlist_pair'))

    def __init__(self, song=None, playlist=None):
        self.song = song
        self.playlist = playlist
        # self.order = order

    def __repr__(self):
        return 'Playlist:%s|Song:%s' % (self.playlist.name, self.song.song_name)
