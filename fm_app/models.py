from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
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


class Image(Base):

    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    image_url = Column(String)
    stored_on_server = Column(Boolean, default=False)

    def __init__(self, image_url="Uploaded", stored_on_server=False, image_data=None):
        print(image_url)
        self.image_url = image_url
        self.stored_on_server = stored_on_server

    def rename_filename_to_id(self, tmp_filename):
        folder_path = config.IMAGES_PATH
        os.rename(folder_path + tmp_filename, folder_path + str(self.id))

    def delete_image(self, image_name):
        os.remove(config.IMAGES_PATH + image_name)

    def change_upload_image_url(self):
        self.image_url = config.IMAGES_PATH + self.id
