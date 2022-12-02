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


@auth_bp.route("/mastodon/auth", methods=["GET"])
@token_auth.login_required
def masto_login():
    """
    returns my mastodon authentication uri for redirection

    requires my token auth
    """
    if "redirect" not in request.args:
        return jsonify(
            success=False,
            message="missing redirect from query params",
        )

    redirect_uri = request.args.get('redirect')
    client_id = app.config.get("MASTODON_CLIENT_ID")
    host = app.config.get("MASTODON_HOST")
    scope = "write:statuses"
    return jsonify(
        authenticationUri=f"{host}/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
    )


@auth_bp.route("/mastodon/revoke", methods=["GET"])
@token_auth.login_required
def masto_revoke():
    """
    revokes the mastodon token

    requires my token auth
    """
    token = request.json.get("token")

    if null_or_empty(token):
        return jsonify(success=False, message=f"token was missing. {token}")

    client_id = app.config.get("MASTODON_CLIENT_ID")
    client_secret = app.config.get("MASTODON_CLIENT_SECRET")

    headers = {"Content-Type": "application/json"}
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "token": token,
    }

    host = app.config.get("MASTODON_HOST")

    response = requests.post(
        f"{host}/oauth/revoke", headers=headers, data=json.dumps(payload)
    )

    if not response.ok:
        return Response(
            f"token revocation failed: {str(response)}", status=HTTPStatus.FORBIDDEN
        )

    return jsonify(success=True, message="")


@auth_bp.route("/mastodon/redirect", methods=["GET"])
def masto_redirect():
    if "code" not in request.args:
        return jsonify(
            success=False,
            message="missing code from query params",
        )

    if "redirect" not in request.args:
        return jsonify(
            success=False,
            message="missing redirect from query params",
        )

    code = request.args.get("code")
    redirect_uri = request.args.get("redirect")
    client_id = app.config.get("MASTODON_CLIENT_ID")
    client_secret = app.config.get("MASTODON_CLIENT_SECRET")
    scope = "write:statuses"

    headers = {"Content-Type": "application/json"}
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "scope": scope,
    }

    host = app.config.get("MASTODON_HOST")

    response = requests.post(
        f"{host}/oauth/token", headers=headers, data=json.dumps(payload)
    )

    if not response.ok:
        return Response(
            f"token retrieval failed: {str(response)}", status=HTTPStatus.FORBIDDEN
        )

    token = response.json().get("access_token")

    if token == "":
        return Response(
            f"no token retrieved: {token}", status=HTTPStatus.INTERNAL_SERVER_ERROR
        )

    return jsonify(token=token)
