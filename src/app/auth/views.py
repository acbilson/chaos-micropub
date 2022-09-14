import os
from os import path
from datetime import datetime, timedelta
import requests
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
from flask_httpauth import HTTPTokenAuth

from ..auth import auth_bp

token_auth = HTTPTokenAuth()

@token_auth.verify_token
def verify_token(token):
    print("verifying token in micropub")
    if token == null:
        return False
    authorized = requests.get("http://localhost:7000/auth", headers={'Authorization': f"Bearer {token}"})
    print(authorized)
    return True

@token_auth.verify_token
@auth_bp.route("/read", methods=["GET"])
def read():
    file_type, file_name = request.args.get("type"), request.args.get("name")
    if None in (file_type, file_name):
        return Response(
        "missing either type or name from query params",
        status=HTTPStatus.BAD_REQUEST,
        )

    type_path = os.path.join(app.config["CONTENT_PATH"], file_type)

    if not os.path.exists(type_path):
        raise Exception(f"{type_path} does not exist")

    all_matches = [];
    for root, _, files in os.walk(type_path):
        matches = [os.path.join(root,f) for f in files if f.startswith(file_name)]
        all_matches += matches

    my_file_path = all_matches[0] if len(all_matches) else ""
    my_file_content = ""
    if my_file_path != "":
        with open(my_file_path, "r") as my_file:
            my_file_content = my_file.readlines()

    return jsonify(
            my_file_path=my_file_path,
            my_file_content=my_file_content,
            matches=all_matches
            )

@token_auth.verify_token
@auth_bp.route("/update", methods=["POST"])
def update():
    body = request.json()
    content = body.get("content")
    return jsonify(content=content)
