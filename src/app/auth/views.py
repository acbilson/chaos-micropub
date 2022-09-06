from os import path
from datetime import datetime
import time
import jwt
from flask import (
    request,
    render_template,
    url_for,
    redirect,
)
from flask import current_app as app
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from ..auth import auth_bp

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(username, password):
    username_match = username == app.config["ADMIN_USER"]
    password_match = password == app.config["ADMIN_PASSWORD"]
    if username_match and password_match:
        return username

@token_auth.verify_token
def verify_token(token):
    data = jwt.decode(token, app.config["FLASK_SECRET_KEY"], algorithm=['HS256'])

def generate_token(expires_in = 600):
    return jwt.encode(dict(id=app.config["ADMIN_USER"],exp=time.time() + expires_in ), app.config["FLASK_SECRET_KEY"], algorithm='HS256')

@auth_bp.route("/authenticate", methods=["GET", "POST"])
@basic_auth.login_required
def authenticate():
    return generate_token()
