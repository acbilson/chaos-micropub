from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flask configuration variables"""
    SESSION_SECRET = environ.get('SESSION_SECRET')
    SECRET_KEY = environ.get('SECRET_KEY')
    CLIENT_ID = environ.get('CLIENT_ID')
    CLIENT_SECRET = environ.get('CLIENT_SECRET')

    HOME = environ.get('HOME')
    SITE = environ.get('SITE')
    BINDING = environ.get('BINDING')
    HOST = environ.get('HOST')
    PORT = environ.get('PORT')
    CONTENT_PATH = environ.get('CONTENT_PATH')
    DEPLOY_FILE = environ.get('DEPLOY_FILE')

class ProdConfig(Config):
    FLASK_ENV = environ.get('FLASK_ENV')

class DevConfig(Config):
    FLASK_ENV = 'development'
