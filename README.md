![MistoFM Logo](/fm_app/static/img/logo_album.png)
## Python 3.4.3 - PostgreSQL 4.2 - Flask 0.12.2

**NOTE: EACH TIME YOU CREATE OR MODIFY DB MODELS, PLEASE CREATE NEW REVISION FILE AND COMMIT IT TO GIT**

**Installation instructions:**

1. Install python
   * sudo add-apt-repository ppa:fkrull/deadsnakes
   * sudo apt-get update
   * sudo apt-get install python3.4
   * sudo apt-get install python-dev
1. Install postgres
   * sudo add-apt-repository "deb https://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main"
   * wget --quiet -O - https://postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
   * sudo apt-get update
   * sudo apt-get install postgresql-9.4
1. Create db user and database
1. Install pip
   * sudo apt-get install pip3
1. Install psycopg2 dependencies
   * sudo apt-get install libpq-dev
1. Install application python requirements
   * pip install -r requirements.txt
1. Rename file secret_data_example.py to secret_data.py and change required parameters
1. Change sqlalchemy.url in alembic.ini file according to server configuration
1. Add project path to PYTHONPATH:
   * export PYTHONPATH=<path_to_project>
1. Create/upgrade tables for database via alembic:

   * alembic --config='/path/to/config/file' upgrade head|revision_id
1. Install Icecast2:
   * apt-get install icecast2
   * configure icecast2 server manually
1. Install ices:
   * apt-get install libshout3-dev
   * /etc/apt/sources.list -> deb http://www.deb-multimedia.org testing main non-free
   * apt-get install deb-multimedia-keyring
   * apt-get install libmp3lame-dev
   * apt-get install libxml2-dev
   * wget http://www.centova.com/clientdist/ices/ices-cc-0.4.3.tar.gz
   * tar xvzf ices-cc-0.4.3.tar.gz
   * ./configure --with-lame --without-perl --without-python --without-flac --with-xml --prefix=/usr/local/ices
   * make && make install

**COMMANDS FOR ALEMBIC:**
1. Create new revision
   * alembic --config '/path/to/config/file' revision --autogenerate -m 'revision description'
1. Upgrade your db according revision
   * alembic --config='/path/to/config/file' upgrade head|revision_id
