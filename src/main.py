from urllib.parse import urlparse
from app import create_app

app = create_app()

env = app.config['FLASK_ENV']
site = app.config['SITE']
host = app.config['HOST']
port = app.config['PORT']

print(f"Flask app running in {env} mode at {host}:{port}")
print(f"View the site at {site}")

if __name__ == "__main__":
    app.run(
        host=host,
        port=port,
        debug=(env == 'development')
        )
