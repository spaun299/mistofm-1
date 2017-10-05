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
