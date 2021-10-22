from urllib.parse import urlparse
from app import create_app

app = create_app()

env = app.config["FLASK_ENV"]
site = app.config["SITE"]
host = app.config["FLASK_HOST"]
port = app.config["FLASK_PORT"]

app.logger.info(f"Flask app running in {env} mode at {host}:{port}")
app.logger.info(f"View the site at {site}")

if __name__ == "__main__":
    app.run(host=host, port=port, debug=(env == "development"))
