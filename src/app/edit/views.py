import os
from os import path
from datetime import datetime, timedelta
import requests
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

from ..edit import edit_bp

token_auth = HTTPTokenAuth()

@token_auth.verify_token
def verify_token(token):
    resp = requests.get("http://localhost:7000/auth", headers={'Authorization': f"Bearer {token}"})
    if resp.status_code == HTTPStatus.OK:
        return token
    else:
        return None

@edit_bp.route("/read", methods=["GET"])
@token_auth.login_required
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
            filePath=my_file_path,
            fileContent=my_file_content,
            matches=all_matches
            )

@edit_bp.route("/update", methods=["POST"])
@token_auth.login_required
def update():
    body = request.json
    file_path, content = body.get("filePath"), body.get("fileContent")

    if content in [None, ""]:
        return Response(f"content was missing. {content}", status=HTTPStatus.BAD_REQUEST)

    if file_path in [None, ""]:
        return Response(f"file path was missing. {file_path}", status=HTTPStatus.BAD_REQUEST)

    with open(file_path, "w", newline="\n") as my_file:
        my_file.write(content)

    return Response(status=HTTPStatus.OK)
