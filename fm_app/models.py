from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, \
    String, Boolean, DateTime, Table
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
    stream_url = Column(VARCHAR(200), nullable=False)
    description_html = Column(VARCHAR(500))
    cr_tm = Column(DateTime, nullable=False)
    images = relationship('Image', secondary=station_image_table, backref="stations")

    def __init__(self, name=None, stream_url=None, description_html=None):
        self.name = name
        self.stream_url = stream_url
        self.description_html = description_html
        self.cr_tm = datetime.datetime.now()

    def __repr__(self):
        return self.name


class Image(Base):

    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    image_url = Column(String)
    name = Column(String)
    stored_on_server = Column(Boolean, default=False)

    def __init__(self, image_url=None, name=None, stored_on_server=False, image_data=None):
        self.image_url = image_url
        self.name = name
        self.stored_on_server = stored_on_server
        self.image_data = image_data

    def __repr__(self):
        return self.image_url

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
