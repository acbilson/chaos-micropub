from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Set Flask configuration variables"""
    FLASK_ENV = environ.get("FLASK_ENV")
    FLASK_SECRET_KEY = environ.get('FLASK_SECRET_KEY')
    HOST = environ.get('HOST')
    PORT = environ.get('PORT')
    SITE = environ.get('SITE')

    SESSION_SECRET = environ.get('SESSION_SECRET')
    CLIENT_ID = environ.get('CLIENT_ID')
    CLIENT_SECRET = environ.get('CLIENT_SECRET')

    CONTENT_PATH = environ.get('CONTENT_PATH')
    DEPLOY_FILE = environ.get('DEPLOY_FILE')
