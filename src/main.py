from urllib.parse import urlparse
from app import create_app

app = create_app()

env = app.config['FLASK_ENV']
host = app.config['HOST']
port = app.config['PORT']

print(f"Flask app running in {env} at {host}:{port}")
print(f"View the site at localhost:5000")

if __name__ == "__main__":
    app.run(
        host=host,
        port=port,
        debug=(env == 'development')
        )
