import os
from os import path
from datetime import datetime, timedelta
import requests
from http import HTTPStatus
from flask import Response, request, render_template, url_for, redirect, jsonify
from flask import current_app as app
from flask_httpauth import HTTPTokenAuth
from ..file import file_bp

from app.operators import compose_header, git_commit

token_auth = HTTPTokenAuth()


@token_auth.verify_token
def verify_token(token):
    resp = requests.get(
        "http://localhost:7000/auth", headers={"Authorization": f"Bearer {token}"}
    )
    return token if resp.status_code == HTTPStatus.OK else None


@file_bp.route("/file", methods=["GET"])
#@token_auth.login_required
def read():
    if "path" not in request.args:
        return jsonify(
            success=False,
            message="missing path from query params",
        )

    file_path = request.args.get("path")
    abs_path = os.path.join(app.config.get("CONTENT_PATH"), f"{file_path[1:]}.md")

    if not os.path.exists(abs_path):
        return jsonify(
                success=False,
                message=f"{abs_path} does not exist"
                       )

    matches = [f for f in os.listdir(os.path.dirname(abs_path)) if f.startswith(os.path.basename(abs_path))]

    if len(matches) == 0:
        return Response(
                success=False,
                message=f"There were no matches",
        )

    if len(matches) > 2:
        return Response(
                success=False,
                message=f"There were too many matches",
                result=matches
        )

    content = ""
    first_match_abs_path = os.path.join(os.path.dirname(abs_path), matches[0])
    with open(first_match_abs_path, "r") as my_file:
        content = my_file.read()

    git_message = git_commit(file_path)
    if git_message is not None:
        return jsonify(success=False, message=git_message, result=dict(filepath=file_path, content=content))

    return jsonify(success=True, message="", result=dict(filepath=file_path, content=content))


@file_bp.route("/file", methods=["PUT"])
#@token_auth.login_required
def update():
    body = request.json
    options, content = body.get("options"), body.get("content")

    if content in [None, ""]:
        return jsonify(
                success=False,
                message=f"content was missing. {content}"
        )

    if options in [None, ""]:
        return jsonify(
                success=False,
                message=f"options were missing. {options}"
        )

    if "filepath" not in [o.keys() for o in options]:
        return jsonify(
                success=False,
                message=f"file path was not included in options."
        )

    file_path = [o for o in options if "filepath" in o.values()][0]

    if not os.path.exists(file_path):
        return jsonify(
                success=False,
                message="The file to update does not exist. Please use /file POST to create.",
        )

    with open(file_path, "w", newline="\n") as my_file:
        my_file.write(content)

    return jsonify(success=True, message="", result=dict(options=options, content=content))


@file_bp.route("/file", methods=["POST"])
#@token_auth.login_required
def create():
    body = request.json
    options, content = body.get("options"), body.get("content")

    if content in [None, ""]:
        return jsonify(
                success=False,
            message=f"content was missing."
        )

    if options in [None, ""]:
        return jsonify(
                success=False,
            message=f"options were missing."
        )

    if "filepath" not in options.keys():
        return jsonify(
                success=False,
            message=f"file path was not included in options."
        )

    if os.path.exists(file_path):
        return jsonify(
                success=False,
            message="The file to create already exists. Please use /file PUT to update."
        )

    with open(file_path, "x", newline="\n") as my_file:
        my_file.write(f"{compose_header(options)}\ncontent")

    #run_build_script(file_path)
    return jsonify(success=True, message="", result=dict(options=options, content=content))
