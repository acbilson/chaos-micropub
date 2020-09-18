from flask import Flask

# globally accessible libraries
# db = SQLAlchemy()

def create_app():
    """Initialize the core application"""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.DevConfig')

    # required to encrypt session
    app.secret_key = app.config['SECRET_KEY']

    # initialize plugins
    # db.init_app(app)

    with app.app_context():
        # import parts of the app
        from .micropub import micropub
        from .auth import auth

        # register blueprints
        app.register_blueprint(micropub.micropub_bp)
        app.register_blueprint(auth.auth_bp)

        return app

