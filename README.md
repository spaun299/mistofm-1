# mistofm
Python 3.4.3 - PostgreSQL 4.2 - Flask 0.12.2


Installation

1:) Install python
sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get update
sudo apt-get install python3.4
2:) Install postgres
sudo add-apt-repository "deb https://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main"
wget --quiet -O - https://postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install postgresql-9.4
3:) Install pip
sudo apt-get install pip3
4:) Install psycopg2 dependencies
sudo apt-get install libpq-dev
5:) Install requirements
pip install -r requirements.txt
