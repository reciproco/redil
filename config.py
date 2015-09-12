# -*- coding: utf-8 -*-
import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    API_USERS = { os.environ['API_USER'] : os.environ['API_PASSWORD'] }
#    REDIS_URL = None
#    REDIS_HOST = 'localhost'
#    REDIS_PORT = 6379
#    REDIS_PASSWORD = None
#    REDIS_DB = 0
#    RQ_POLL_INTERVAL = 2500  #: Web interface poll period for updates in ms

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ['TEST_DATABASE_URL']
