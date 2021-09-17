# rename to config.py

class Config(object):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SAMESITE = 'Strict'
    JSON_SORT_KEYS = False
    SECRET_KEY = 'secretkey' # used to sign and verify jwt tokens
    DATABASE = 'meedikal.db'

class ProductionConfig(Config):
    ENV= "production"
    DEBUG = False


class StagingConfig(Config):
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True
    ENV= "development"

class TestingConfig(Config):
    TESTING = True