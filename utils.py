from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


def get_database_uri(host, username, password, db_name):
    return 'postgresql+psycopg2://{username}:{password}@{host}/{db_name}'. \
        format(**{'db_name': db_name,
                  'host': host,
                  'username': username,
                  'password': password})


def get_db_session(db_url):
    engine = create_engine(db_url,
                           echo=False)
    engine.connect()
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    return db_session
