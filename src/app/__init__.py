import logging
from flask import Flask, Response
from flask_cors import CORS

from app.file import file_bp
from app.auth import auth_bp
from app import config


def create_app(config=config.BaseConfig):
    """Initialize the core application"""
    app = Flask(__name__, instance_relative_config=False)
    cors = CORS(app)
    app.config.from_object(config)

    app.logger.info(app.config.get("CONTENT_PATH"))

    # required to encrypt session
    app.secret_key = app.config["FLASK_SECRET_KEY"]

    with app.app_context():

        # register blueprints
        app.register_blueprint(file_bp)
        app.register_blueprint(auth_bp)

        @app.route("/healthcheck", methods=["GET"])
        def health():
            return Response(status=200)

        return app
