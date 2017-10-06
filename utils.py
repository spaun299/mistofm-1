from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
import shutil
import subprocess
import shlex


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


def copy_file(source_path, dest_folder, filename):
    dest_path = dest_folder + filename
    shutil.copyfile(source_path, dest_folder + filename)
    return dest_path


def delete_file(file_path):
    os.remove(file_path)


def move_file(source_path, dest_path):
    shutil.move(source_path, dest_path)


def file_exists(file_path):
    return True if os.path.exists(file_path) else False


def run_cli_script(script_with_args: str):
    args = shlex.split(script_with_args)
    subprocess.Popen(args, shell=True)
