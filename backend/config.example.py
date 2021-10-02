# rename to config.py

class Config(object):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SAMESITE = 'Strict'
    JSON_SORT_KEYS = False
    AUTH_METHOD = 'cookie' # store jwt in session during production
    SECRET_KEY = 'secretkey' # used to sign and verify jwt tokens
    DATABASE = 'meedikal.db'
    UPLOAD_FOLDER = 'images/'
    Admin = {
        'ci': None,
        'name1': None,
        'surname1': None,
        'sex': None,
        'birthdate': None,
        'location': None,
        'email': None,
        'password': None,
        'name2': None,
        'surname2': None,
        'genre': None,
        'active': 1,
        'photoUrl': None
    }

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEBUG = True

class DevelopmentConfig(Config):
    DEBUG = True
    ENV= "development"
    AUTH_METHOD = 'headers' # store jwt in local storage, only during development
class TestingConfig(Config):
    TESTING = True