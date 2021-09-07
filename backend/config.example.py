# rename to config.py

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'secretkey'
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