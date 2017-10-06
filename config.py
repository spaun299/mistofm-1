import secret_data

DEBUG = True
DB_NAME = secret_data.DB_NAME
DB_HOST = secret_data.DB_HOST
DB_USERNAME = secret_data.DB_USERNAME
DB_PASSWORD = secret_data.DB_PASSWORD
LOG_PATH = "mistofm.log"
# LOG_PATH = "/var/log/mistofm.log"
LOG_ROTATE_COUNT = 5
SECRET_KEY = secret_data.SECRET_KEY
IMAGES_PATH = "static/img/uploaded/"
ADMIN_URL_PREFIX = "/admin_mistofm"
MUSIC_PATH = "/home/vkobryn/mistofm/music_uploaded/"
ICES_CONFIGS_PATH = "/home/vkobryn/mistofm/etc/"
ICES_PROGRAMM_PATH = "/usr/local/ices/bin/ices0"
ICES_BASE_CONFIG_PATH = "/home/vkobryn/Projects/mistofm/ices_base_conf.xml"
ICES_PYTHON_MODULES_PATH = "/usr/local/ices/etc/modules/"
ICES_PYTHON_BASE_MODULE_PATH = "/home/vkobryn/Projects/mistofm/ices_base_playlist.py"
ICES_PID_FOLDER = "/tmp/ices_pid/"
STATION_JINGLE_FOLDER = "/home/vkobryn/mistofm/media/"
TMP_FOLDER = "/home/vkobryn/mistofm/tmp/"
