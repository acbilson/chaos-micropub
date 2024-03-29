import os
import json
import requests
from pathlib import Path

from flask import Response, request, jsonify
from flask import current_app as app
from ..file import file_bp

from app.auth import token_auth
from app.operators import (
    combine_file_content,
    split_file_content,
    null_or_empty,
    git_pull,
    git_commit,
    convert_to_webp,
    replace_url_suffix,
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
    content_path: str = app.config.get("CONTENT_PATH")
    strip_first_slash = lambda x: x.strip("/") if x[0] == os.path.sep else x
    abs_path = os.path.join(content_path, f"{strip_first_slash(file_path)}.md")

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
        content=dict(path=file_path, frontmatter=front_matter, body="".join(body)),
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

    content_path: str = app.config.get("CONTENT_PATH")
    strip_first_slash = lambda x: x.strip("/") if x[0] == os.path.sep else x
    abs_path = os.path.join(content_path, f"{strip_first_slash(file_path)}.md")

    if not os.path.exists(abs_path):
        return jsonify(
            success=False,
            message=f"The file {file_path} to update does not exist. Please use /file POST to create.",
        )

    git_pull(content_path)

    content = combine_file_content(front_matter, body, photo=None)
    with open(abs_path, "w", newline="\n") as my_file:
        my_file.write(content)

    _, git_error = git_commit(
        content_path,
        f"edited {os.path.basename(abs_path)}",
    )

    if git_error is not None:
        return jsonify(
            success=False,
            message=git_error,
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

    content_path: str = app.config.get("CONTENT_PATH")
    strip_first_slash = lambda x: x.strip("/") if x[0] == os.path.sep else x
    abs_path = os.path.join(content_path, f"{strip_first_slash(file_path)}.md")

    if os.path.exists(abs_path):
        return jsonify(
            success=False,
            message="The file already exists. Please use /file PUT to update.",
        )

    git_pull(content_path)

    # TODO: abstract syndication somehow
    is_syndicated = False
    syn_msg = ""
    token: str = data.get("token")
    if (
        front_matter.get("syndicate") in ["true", "True", "yes", "Yes", True]
        and token != ""
    ):
        host = app.config.get("MASTODON_HOST")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        payload = {"status": body}

        # TODO: create a Mastodon API layer
        # TODO: figure out how to submit a photo and alt-text when it exists.
        response = requests.post(
            f"{host}/api/v1/statuses", data=json.dumps(payload), headers=headers
        )

        if response.ok:
            front_matter["syndicated"] = {
                "mastodon": f"{host}/@acbilson/{response.json().get('id')}"
            }
            is_syndicated = True
        else:
            syn_msg = f"status: {str(response)}, reason: {response.reason}, txt: {response.text}"

    photo: dict[str, str] | None = None
    if front_matter.get("photo"):
        photo = dict(
            src=replace_url_suffix(front_matter.get("photo"), ".webp"),
            alt=front_matter.get("photoAlt"),
            caption=front_matter.get("photoCaption"),
        )

        # removes photo attributes from front_matter
        front_matter.pop("photo")

        if front_matter.get("photoAlt"):
            front_matter.pop("photoAlt")

        if front_matter.get("photoCaption"):
            front_matter.pop("photoCaption")

    content = combine_file_content(front_matter, body, photo)
    with open(abs_path, "x", newline="\n") as my_file:
        my_file.write(content)

    _, git_error = git_commit(
        content_path,
        f"added {os.path.basename(abs_path)}",
    )
    if git_error is not None:
        return jsonify(
            success=False,
            message=git_error,
            content=dict(path=file_path, body=content, frontmatter=front_matter),
        )

    # TODO: clean up response messaging
    message = "created"
    if is_syndicated and syn_msg == "":
        message += " and syndicated"
    elif not is_syndicated and syn_msg != "":
        message += f" but syndication returned {syn_msg}"
    elif not is_syndicated and token == "":
        message += " but not syndicated (and no token)"
    else:
        message += " but not syndicated"

    return jsonify(
        success=True,
        message=message,
        content=dict(
            path=file_path, body=content, frontmatter=front_matter, token=token
        ),
    )


@file_bp.route("/photo", methods=["POST"])
@token_auth.login_required
def create_photo():
    photo = request.files.get("photo")

    if photo is None:
        return jsonify(success=False, message=f"photo was missing. {photo}")

    # store photo to image path
    photo_path = os.path.join(app.config["IMAGE_PATH"], photo.filename)
    photo.save(photo_path)

    # convert the file to WebP
    new_filename = str(Path(photo.filename).with_suffix(".webp"))
    convert_to_webp(app.config["IMAGE_PATH"], photo.filename, new_filename)

    # remove original
    os.remove(photo_path)

    return jsonify(success=True, message="", content=dict(filename=new_filename))
