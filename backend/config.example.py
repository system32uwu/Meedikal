# rename to config.py

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'secretkey'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


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