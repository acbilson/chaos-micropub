import os
from os import path
from datetime import datetime, timedelta
import requests
from http import HTTPStatus
from flask import Response, request, render_template, url_for, redirect, jsonify
from flask import current_app as app
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from ..file import file_bp

from app.auth import token_auth
from app.operators import (
    compose_header,
    combine_file_content,
    split_file_content,
    null_or_empty,
    git_pull,
    git_commit,
)


@file_bp.route("/file", methods=["GET"])
@token_auth.login_required
def read():
    if "path" not in request.args:
        return jsonify(
            success=False,
            message="missing path from query params",
        )

    file_path = request.args.get("path")
    strip_first_slash = lambda x: x.strip("/") if x[0] == os.path.sep else x
    abs_path = os.path.join(
        app.config.get("CONTENT_PATH"), f"{strip_first_slash(file_path)}.md"
    )

    if not os.path.exists(abs_path):
        return jsonify(success=False, message=f"{abs_path} does not exist")

    matches = [
        f
        for f in os.listdir(os.path.dirname(abs_path))
        if f.startswith(os.path.basename(abs_path))
    ]

    if len(matches) == 0:
        return Response(
            success=False,
            message=f"There were no matches",
        )

    if len(matches) > 2:
        return Response(
            success=False, message=f"There were too many matches", result=matches
        )

    content = []
    first_match_abs_path = os.path.join(os.path.dirname(abs_path), matches[0])
    with open(first_match_abs_path, "r") as my_file:
        content = my_file.readlines()

    front_matter, body = split_file_content(content)

    return jsonify(
        success=True,
        message="",
        content=dict(filepath=file_path, frontmatter=front_matter, body="".join(body)),
    )


@file_bp.route("/file", methods=["PUT"])
@token_auth.login_required
def update():
    data = request.json
    file_path, front_matter, body = (
        data.get("path"),
        data.get("frontmatter"),
        data.get("body"),
    )

    if null_or_empty(front_matter):
        return jsonify(
            success=False, message=f"front_matter was missing. {front_matter}"
        )

    if null_or_empty(body):
        return jsonify(success=False, message=f"body were missing. {body}")

    if null_or_empty(file_path):
        return jsonify(success=False, message=f"file path was missing. {file_path}")

    strip_first_slash = lambda x: x.strip("/") if x[0] == os.path.sep else x
    abs_path = os.path.join(
        app.config.get("CONTENT_PATH"), f"{strip_first_slash(file_path)}.md"
    )

    if not os.path.exists(abs_path):
        return jsonify(
            success=False,
            message=f"The file {file_path} to update does not exist. Please use /file POST to create.",
        )

    git_pull(app.config.get("CONTENT_PATH"))

    content = combine_file_content(front_matter, body)
    with open(abs_path, "w", newline="\n") as my_file:
        my_file.write(content)

    git_message = git_commit(
        file_path,
        app.config.get("CONTENT_PATH"),
        f"edited {os.path.basename(file_path)}",
    )

    if git_message is not None:
        return jsonify(
            success=False,
            message=git_message,
            result=dict(path=file_path, front_matter=front_matter, body=body),
        )

    return jsonify(
        success=True,
        message="",
        content=dict(path=file_path, body=body, frontmatter=front_matter),
    )


@file_bp.route("/file", methods=["POST"])
@token_auth.login_required
def create():
    data = request.json
    file_path, front_matter, body = (
        data.get("path"),
        data.get("frontmatter"),
        data.get("body"),
    )

    if null_or_empty(front_matter):
        return jsonify(
            success=False, message=f"front matter was missing. {front_matter}"
        )

    if null_or_empty(body):
        return jsonify(success=False, message=f"body were missing. {body}")

    if null_or_empty(file_path):
        return jsonify(success=False, message=f"file path was missing. {file_path}")

    strip_first_slash = lambda x: x.strip("/") if x[0] == os.path.sep else x
    abs_path = os.path.join(
        app.config.get("CONTENT_PATH"), f"{strip_first_slash(file_path)}.md"
    )

    if os.path.exists(abs_path):
        return jsonify(
            success=False,
            message="The file to create already exists. Please use /file PUT to update.",
        )

    git_pull(app.config.get("CONTENT_PATH"))

    content = combine_file_content(front_matter, body)
    with open(abs_path, "x", newline="\n") as my_file:
        my_file.write(content)

    git_message = git_commit(
        file_path,
        app.config.get("CONTENT_PATH"),
        f"added {os.path.basename(file_path)}",
    )
    if git_message is not None:
        return jsonify(
            success=False,
            message=git_message,
            content=dict(path=file_path, body=body, frontmatter=front_matter),
        )

    return jsonify(
        success=True,
        message="",
        content=dict(path=file_path, body=body, frontmatter=front_matter),
    )
