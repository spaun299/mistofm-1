from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import jsonify
from fm_app import constants
import os
import shutil
import subprocess
import shlex
import re


def get_database_uri(host, username, password, db_name):
    return 'postgresql+psycopg2://{username}:{password}@{host}/{db_name}'. \
        format(**{'db_name': db_name,
                  'host': host,
                  'username': username,
                  'password': password})


def get_db_session(db_url):
    engine = create_engine(db_url,
                           echo=False)
    sql_connection = engine.connect()
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    return db_session, sql_connection, engine


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
    subprocess.check_call(args)


def kill_process(pid):
    run_cli_script('kill -9 %s' % pid)


def get_pid_by_args(*args):
    command = "ps -eaf | grep -v grep | %s grep -v $$ | awk '{ print $2 }'" % ''.join(
        [' grep %s | ' % arg for arg in args])
    pid = re.findall(b'\d+', subprocess.check_output(['bash', '-c', command]))
    return str(pid[0], 'utf-8') if pid else None


def get_hours_from_timeframe(_from, _to):
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


def get_disc_space():
    mount_points = ['/', '/var/www/mistofm']
    partitions = []

    for mount_point in mount_points:
        try:
            partition_space = list(filter(bool, str(subprocess.check_output(
                ['bash', '-c', "df -h %s" % mount_point]),
                'utf-8').split('\n')[-2].split(" ")))
            partition_dict = dict(partition=partition_space[0],
                                  all_space=partition_space[1],
                                  used_space=partition_space[2],
                                  available_space=partition_space[3],
                                  used_percent=int(partition_space[4][:-1]),
                                  mount_point=partition_space[5])
            partitions.append(partition_dict)
        except subprocess.CalledProcessError:
            pass
    return partitions


def get_memory_usage():
    mem_swap = ["Mem", "Swap"]
    mem_swap_result = []
    for ms in mem_swap:
        memory = list(filter(bool, str(subprocess.check_output(
            ['bash', '-c', "free -m | grep %s" % ms]),
            'utf-8').replace("\n", "").split(' ')))
        memory_dict = dict(
            type=ms,
            total=int(memory[1]),
            used=int(memory[2]),
            free=int(memory[3])
        )
        if ms == "Mem":
            memory_dict['used'] = memory_dict['used'] - int(memory[6])
            memory_dict['free'] = memory_dict['free'] + int(memory[6])
        mem_swap_result.append(memory_dict)
    return mem_swap_result


def capitalize_string(val):
    return val.capitalize()


def json_response(err=False, **kwargs):
    kwargs.update({constants.API_ERROR_TEXT: True if err else False})
    return jsonify(kwargs)
