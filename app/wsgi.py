#from os import environ
from application import create_app

app = create_app()

env = app.config['FLASK_ENV']
host = app.config['HOST']
port = app.config['PORT']
site = app.config['SITE']
debug = True

if env == 'production':
    debug = False

print(f"Flask app running at {host}:{port} in {env}")
print(f"View the site at {site}")

if __name__ == "__main__":
    app.run(
        host=host,
        port=port,
        debug=debug
        )
