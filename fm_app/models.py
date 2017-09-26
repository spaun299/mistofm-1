from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR

Base = declarative_base()


class Station(Base):
    __tablename__ = 'station'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(30))
    stream_url = Column(VARCHAR(200))
    description_html = Column(VARCHAR(500))
