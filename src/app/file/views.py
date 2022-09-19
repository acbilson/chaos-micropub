import os
from os import path
from datetime import datetime, timedelta
import requests
from http import HTTPStatus
from flask import Response, request, render_template, url_for, redirect, jsonify
from flask import current_app as app
from flask_httpauth import HTTPTokenAuth

from ..file import file_bp
from ../operators import run_build_script

token_auth = HTTPTokenAuth()


@token_auth.verify_token
def verify_token(token):
    resp = requests.get(
        "http://localhost:7000/auth", headers={"Authorization": f"Bearer {token}"}
    )
    return token if resp.status_code == HTTPStatus.OK else None


@file_bp.route("/file<path:string>", methods=["GET"])
@token_auth.login_required
def read(file_path):
    if file_path == None:
        return Response(
            "missing path from query params",
            status=HTTPStatus.BAD_REQUEST,
        )

    abs_path = os.path.join(app.config["CONTENT_PATH"], file_path)
    abs_dir = os.path.getdir(abs_path)
    file_name = os.path.filename(abs_path)

    if not os.path.exists(abs_dir):
        raise Exception(f"{abs_dir} does not exist")

    matches = [f for f in os.listdirs(abs_dir) if f.startswith(file_name)]

    if len(matches) == 0:
        return Response(
            f"There were no matches",
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    if len(matches) > 2:
        return Response(
            f"There were too many matches",
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    content = ""
    with open(matches[0], "r") as my_file:
        content = my_file.read()

    return jsonify(filePath=file_path, fileContent=content)


@file_bp.route("/file", methods=["PUT"])
@token_auth.login_required
def update():
    body = request.json
    file_path, content = body.get("filePath"), body.get("fileContent")

    if content in [None, ""]:
        return Response(
            f"content was missing. {content}", status=HTTPStatus.BAD_REQUEST
        )

    if file_path in [None, ""]:
        return Response(
            f"file path was missing. {file_path}", status=HTTPStatus.BAD_REQUEST
        )

    if not os.path.exists(file_path):
        return Response("The file to update does not exist. Please use /file POST to create.", status=HTTPStatus.INTERNAL_SERVER_ERROR)

    with open(file_path, "w", newline="\n") as my_file:
        my_file.write(content)

    run_build_script(file_path)
    return jsonify(filePath=file_path, fileContent=content)

@file_bp.route("/file", methods=["POST"])
@token_auth.login_required
def create():
    body = request.json
    file_path, content = body.get("filePath"), body.get("fileContent")

    if content in [None, ""]:
        return Response(
            f"content was missing. {content}", status=HTTPStatus.BAD_REQUEST
        )

    if file_path in [None, ""]:
        return Response(
            f"file path was missing. {file_path}", status=HTTPStatus.BAD_REQUEST
        )

    if os.path.exists(file_path):
        return Response("The file to create already exists. Please use /file PUT to update.", status=HTTPStatus.INTERNAL_SERVER_ERROR)

    with open(file_path, "x", newline="\n") as my_file:
        my_file.write(content)

    run_build_script(file_path)
    return jsonify(filePath=file_path, fileContent=content)
