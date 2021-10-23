import os

class Config(object):
    DEBUG =  False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.path.join(os.getcwd(), '')

class Production(Config):
    pass
