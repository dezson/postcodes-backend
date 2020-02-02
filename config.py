import os


class Config:
    TESTING = True
    DEBUG = True
    THREADS_PER_PAGE = 2

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'prod.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'not secret'


class TestingConfig:
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test!'
