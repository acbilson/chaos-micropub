from os import environ

class Config:
    """Set Flask configuration variables"""
    FLASK_HOST = "0.0.0.0"
    FLASK_PORT = 80
    FLASK_ENV = environ.get("FLASK_ENV")
    SITE = environ.get('SITE')

    FLASK_SECRET_KEY = environ.get('FLASK_SECRET_KEY')
    SESSION_SECRET = environ.get('SESSION_SECRET')
    CLIENT_ID = environ.get('CLIENT_ID')
    CLIENT_SECRET = environ.get('CLIENT_SECRET')
