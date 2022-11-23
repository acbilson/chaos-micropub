import os
from os import path
from datetime import datetime, timedelta
import jwt
import json
import requests
from http import HTTPStatus
from flask import (
    Response,
    make_response,
    request,
    redirect,
    render_template,
    url_for,
    redirect,
    jsonify,
)
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
    obj = dict(id="alex", exp=datetime.utcnow() + timedelta(minutes=60))
    return jwt.encode(obj, app.config.get("FLASK_SECRET_KEY"), algorithm="HS256")


@auth_bp.route("/auth", methods=["GET"])
@token_auth.login_required
def authenticate():
    return Response(status=HTTPStatus.OK)


@auth_bp.route("/token", methods=["GET"])
@basic_auth.login_required
def login():
    return jsonify(token=generate_token())


@auth_bp.route("/mastoauth", methods=["GET"])
@token_auth.login_required
def masto_login():
    client_id = "8MOfoRYQVmPOLRDjO-tE90X8EU7ZQwwAOyg8RkDtv08"
    redirect_uri = "http://localhost:5000/masto_redirect"
    scope = "write:statuses"
    return redirect(
        f"https://indieweb.social/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
    )


@auth_bp.route("/masto_redirect", methods=["GET"])
def masto_redirect():
    if "code" not in request.args:
        return

    code = request.args.get("code")
    client_id = "8MOfoRYQVmPOLRDjO-tE90X8EU7ZQwwAOyg8RkDtv08"
    client_secret = "lsLLQZEVbTQG4qirgtPTWFhpixcHacwHUiyVIyq4vq4"
    redirect_uri = "http://localhost:5000/masto_redirect"
    scope = "write:statuses"
    code = request.args.get("code")

    headers = {"Content-Type": "application/json"}
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "scope": scope,
    }
    print(payload)
    response = requests.post(
        "https://indieweb.social/oauth/token", headers=headers, data=json.dumps(payload)
    )

    print(response)
    print(response.json())
    token = response.json().get("access_token")
    resp = make_response()
    resp.set_cookie("masto_token", value=token)
    return resp
