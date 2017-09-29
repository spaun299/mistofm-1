def get_database_uri(host, username, password, db_name):
    return 'postgresql+psycopg2://{username}:{password}@{host}/{db_name}'. \
        format(**{'db_name': db_name,
                  'host': host,
                  'username': username,
                  'password': password})
