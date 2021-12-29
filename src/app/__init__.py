import logging
from flask import Flask, Response
from flask_dance.contrib.github import make_github_blueprint
from flask_dance.contrib.google import make_google_blueprint

from app.core import core_bp
from app.log import log_bp
from app.quip import quip_bp
from app.assets import assets
from app import config


def create_app(config=config.BaseConfig):
    """Initialize the core application"""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config)

    app.logger.info(app.config.get("CONTENT_PATH"))

    # required to encrypt session
    app.secret_key = app.config["FLASK_SECRET_KEY"]

    register_extensions(app)

    with app.app_context():

        # creates github flask-dance blueprint
        github_bp = make_github_blueprint(
            client_id=app.config["GITHUB_CLIENT_ID"],
            client_secret=app.config["GITHUB_CLIENT_SECRET"],
        )

        # creates google flask-dance blueprint
        google_bp = make_google_blueprint(
            client_id=app.config["GOOGLE_CLIENT_ID"],
            client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        )

        # register blueprints
        app.register_blueprint(github_bp, url_prefix="/login")
        app.register_blueprint(google_bp, url_prefix="/login")

        app.register_blueprint(core_bp)
        app.register_blueprint(log_bp)
        app.register_blueprint(quip_bp)

        @app.route("/healthcheck", methods=["GET"])
        def health():
            return Response(status=200)

        return app


def register_extensions(app):
    """Register extensions with the Flask application."""
    assets.init_app(app)
