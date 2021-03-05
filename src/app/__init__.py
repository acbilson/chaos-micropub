from flask import Flask
from flask_dance.contrib.github import make_github_blueprint

def create_app():
    """Initialize the core application"""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # required to encrypt session
    app.secret_key = app.config['FLASK_SECRET_KEY']

    with app.app_context():

        # creates github flask-dance blueprint
        github_bp = make_github_blueprint(
            client_id=app.config['CLIENT_ID'],
            client_secret=app.config['CLIENT_SECRET'],
        )

        # import parts of the app
        from .micropub import micropub

        # register blueprints
        app.register_blueprint(github_bp, url_prefix="/login")
        app.register_blueprint(micropub.micropub_bp)

        return app

