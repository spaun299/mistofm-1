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
MUSIC_PATH = "/Users/apple/projects/mistofm/music_uploaded/"
ICES_CONFIGS_PATH = "/Users/apple/projects/mistofm/etc/"
ICES_PROGRAMM_PATH = "/usr/local/ices/bin/ices"
ICES_BASE_CONFIG_PATH = "/Users/apple/projects/mistofm/ices_base_conf.xml"
ICES_PYTHON_MODULES_PATH = "/usr/local/ices/etc/modules/"
ICES_PYTHON_BASE_MODULE_PATH = "/home/vkobryn/Projects/mistofm/ices_base_playlist.py"
ICES_PLAYLIST_LOG_FILE = "/Users/apple/projects/mistofm/playlist.log"
TMP_FOLDER = "/Users/apple/projects/mistofm/tmp/"
BASH_RUN_ICES = "/Users/apple/projects/mistofm/run_ices.sh"

METADATA_URL = "http://0.0.0.0:8777"
METADATA_USERNAME = secret_data.METADATA_USERNAME
METADATA_PASSWORD = secret_data.METADATA_PASSWORD
