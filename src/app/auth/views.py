from os import path
from datetime import datetime, timedelta
import jwt
from http import HTTPStatus
from flask import (
    Response,
    request,
    render_template,
    url_for,
    redirect,
    jsonify
)
from flask import current_app as app
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from ..auth import auth_bp

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    username_match = username == 'alex'
    password_match = password == 'example'
    if username_match and password_match:
        return username


@token_auth.verify_token
def verify_token(token):
    data = jwt.decode(token, 'my-secret-key', algorithms=["HS256"])
    id, exp = data.get("id"), data.get("exp")
    return id


def generate_token():
    obj = dict(
        id='alex', exp=datetime.utcnow() + timedelta(minutes=20)
    )
    return jwt.encode(obj, 'my-secret-key', algorithm="HS256")


@auth_bp.route("/authenticate", methods=["GET"])
@token_auth.login_required
def authenticate():
    return Response(status=HTTPStatus.OK)


@auth_bp.route("/login", methods=["GET"])
@basic_auth.login_required
def login():
    return jsonify(token=generate_token())
