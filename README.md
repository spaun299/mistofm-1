# mistofm
Python 3.4.3 - PostgreSQL 4.2 - Flask 0.12.2

NOTE: EACH TIME YOU CREATE OR MODIFY DB MODELS, PLEASE CREATE NEW REVISION FILE AND COMMIT IT TO GIT

Installation
sudo apt-get install python-dev
1:) Install python
sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get update
sudo apt-get install python3.4
2:) Install postgres
sudo add-apt-repository "deb https://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main"
wget --quiet -O - https://postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install postgresql-9.4
3:) Create user and database
4:) Install pip
sudo apt-get install pip3
5:) Install psycopg2 dependencies
sudo apt-get install libpq-dev
6:) Install requirements
pip install -r requirements.txt
7:) Rename file secret_data_example.py to secret_data.py and change required parameters
8:) Change sqlalchemy.url in alembic.ini file according server configuration
9:) Add project path to PYTHONPATH:
export PYTHONPATH=<path_to_project>
10:) Create/upgrade tables for database via alembic:

alembic --config='/path/to/config/file' upgrade head|revision_id

COMMANDS FOR ALEMBIC:
1:) Create new revision
alembic --config '/path/to/config/file' revision --autogenerate -m 'revision description'
2:) Upgrade your db according revision
alembic --config='/path/to/config/file' upgrade head|revision_id
