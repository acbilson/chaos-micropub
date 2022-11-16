import os
from os import path
from datetime import datetime, timedelta
import jwt
import requests
from http import HTTPStatus
from flask import Response, request, render_template, url_for, redirect, jsonify
from flask import current_app as app
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from ..auth import auth_bp

from app.operators import (
    compose_header,
    combine_file_content,
    split_file_content,
    null_or_empty,
    git_pull,
    git_commit,
)

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    if app.debug:
        return app.config.get("ADMIN_USER")
    username_match = username == app.config.get("ADMIN_USER")
    password_match = password == app.config.get("ADMIN_PASSWORD")
    if username_match and password_match:
        return username


@token_auth.verify_token
def verify_token(token):
    if app.debug:
        return app.config.get("ADMIN_USER")
    data = jwt.decode(token, app.config.get("FLASK_SECRET_KEY"), algorithms=["HS256"])
    id, exp = data.get("id"), data.get("exp")
    return id


def generate_token():
    obj = dict(
        id='alex', exp=datetime.utcnow() + timedelta(minutes=60)
    )
    return jwt.encode(obj, app.config.get("FLASK_SECRET_KEY"), algorithm="HS256")


@auth_bp.route("/auth", methods=["GET"])
@token_auth.login_required
def authenticate():
    return Response(status=HTTPStatus.OK)


@auth_bp.route("/token", methods=["GET"])
@basic_auth.login_required
def login():
    return jsonify(token=generate_token())

