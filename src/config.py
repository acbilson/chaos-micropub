from os import environ

class Config:
    """Set Flask configuration variables"""
    FLASK_HOST = "0.0.0.0"
    FLASK_PORT = 80
    FLASK_ENV = environ.get("FLASK_ENV")
    SITE = environ.get('SITE')

    FLASK_SECRET_KEY = environ.get('FLASK_SECRET_KEY')
    SESSION_SECRET = environ.get('SESSION_SECRET')
    GITHUB_CLIENT_ID = environ.get('GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET = environ.get('GITHUB_CLIENT_SECRET')
    GOOGLE_CLIENT_ID = environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = environ.get('GOOGLE_CLIENT_SECRET')
