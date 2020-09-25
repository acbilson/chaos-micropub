from flask import Flask

def create_app():
    """Initialize the core application"""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # required to encrypt session
    app.secret_key = app.config['SECRET_KEY']

    with app.app_context():
        # import parts of the app
        from .micropub import micropub
        from .auth import auth

        # register blueprints
        app.register_blueprint(micropub.micropub_bp)
        app.register_blueprint(auth.auth_bp)

        return app

