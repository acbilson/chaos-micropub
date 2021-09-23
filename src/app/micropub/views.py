from flask import (
    Blueprint,
    request,
    render_template,
    url_for,
    redirect,
    Response,
)
from flask_dance.contrib.github import github
from flask_dance.contrib.google import google
from flask import current_app as app
from pathlib import Path
import sys
import subprocess
from datetime import datetime

from ..micropub import micropub_bp
from app.micropub.forms import LogForm


@micropub_bp.route("/healthcheck", methods=["GET"])
def health():
    return Response(status=200)


@micropub_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if not app.debug and not authenticated():
            return render_template(
                "login.html",
                login_route=url_for("micropub_bp.login"),
            )
        else:
            return redirect(url_for("micropub_bp.create"))

    elif request.method == "POST":
        if app.debug:
            return redirect(url_for("micropub_bp.create"))

        if "option" in request.form and request.form["option"] == "github":
            return redirect(url_for("github.login"))

        elif "option" in request.form and request.form["option"] == "google":
            return redirect(url_for("google.login"))

        else:
            return "the selected oauth login method is unsupported", 501
    else:
        return f"{request.method} is unsupported for this endpoint", 501


@micropub_bp.route("/", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        if not app.debug and not authenticated():
            return redirect(url_for("micropub_bp.login"))
        else:
            return render_template(
                "create.html",
                create_route=url_for("micropub_bp.create"),
                script=url_for("static", filename="js/micropub.js"),
            )
    elif request.method == "POST":
        if not app.debug and not authenticated():
            return redirect(url_for("micropub_bp.login"))
        else:
            user = get_user()
            if not authorized(user):
                return f"{user} is not authorized to use this application.", 403

            if "post-type-log" in request.form:
                return redirect(url_for("micropub_bp.create_log"))
            elif "post-type-note" in request.form:
                return redirect(url_for("micropub_bp.create_note"))
            else:
                return "no post type was passed to this endpoint. aborting.", 400


@micropub_bp.route("/create/log", methods=["GET", "POST"])
def create_log():
    if request.method == "GET":
        if not app.debug and not authenticated():
            return redirect(url_for("micropub_bp.login"))
        else:
            return render_template(
                "create_log.html",
                create_route=url_for("micropub_bp.create_log"),
                script=url_for("static", filename="js/micropub.js"),
            )
    elif request.method == "POST":
        if not app.debug and not authenticated():
            return redirect(url_for("micropub_bp.login"))
        else:
            user = get_user()
            if not authorized(user):
                return f"{user} is not authorized to use this application.", 403

            form = LogForm(request.form, csrf_enabled=False)
            if not form.validate():
                return f"form could not be validated because {form.errors}. aborting.", 400
            new_file_path = create_log(form.timestamp, user, form.content.data)

            run_build_script(new_file_path)
            return redirect(app.config["SITE"])
    else:
        return f"{request.method} is unsupported for this endpoint", 501


@micropub_bp.route("/create/note", methods=["GET", "POST"])
def create_note():
    if request.method == "GET":
        if not app.debug and not authenticated():
            return redirect(url_for("micropub_bp.login"))
        else:
            return render_template(
                "create_note.html",
                create_route=url_for("micropub_bp.create_note"),
                script=url_for("static", filename="js/micropub.js"),
            )
    elif request.method == "POST":
        if not app.debug and not authenticated():
            return redirect(url_for("micropub_bp.login"))
        else:
            user = get_user()
            if not authorized(user):
                return f"{user} is not authorized to use this application.", 403

            if "content" not in request.form:
                return "no content was passed to this endpoint. aborting.", 400
            if "current_date" not in request.form:
                return "no date was passed to this endpoint. aborting.", 400

            now = datetime.fromisoformat(request.form["current_date"])
            content = request.form["content"]
            new_file_path = ""

            if "title" not in request.form:
                return "no title was passed to this endpoint. aborting.", 400
            if "tags" not in request.form:
                return "no tags were passed to this endpoint. aborting.", 400

            comments = "false"
            if "comments" in request.form and request.form["comments"] == "on":
                comments = "true"

            title = request.form["title"]

            tags = parse_to_list(request.form["tags"])

            new_file_path = create_note(now, user, content, comments, title, tags)

            run_build_script(new_file_path)
            return redirect(app.config["SITE"])
    else:
        return f"{request.method} is unsupported for this endpoint", 501


def create_log(now, user, post_content):
    filename = now.strftime("%Y%m%d-%H%M%S")
    date = now.isoformat()

    if user == "acbilson" or user == "Alexander Bilson":
        user = "Alex Bilson"

    new_file_path = Path(f"/mnt/chaos/content/logs/{filename}.md")
    content = f"""+++
author = "{user}"
date = "{date}"
+++
{post_content}
    """

    with open(new_file_path, "x") as f:
        f.write(content)

    return new_file_path


def create_note(now, user, post_content, comments, title, tags):
    filename = title.lower().replace(" ", "-")
    date = now.isoformat()

    if user == "acbilson" or user == "Alexander Bilson":
        user = "Alex Bilson"

    new_file_path = Path(f"/mnt/chaos/content/notes/{filename}.md")
    content = f"""+++
author = "{user}"
comments = {comments}
date = "{date}"
epistemic = "seedling"
tags = [{tags}]
title = "{title}"
+++
{request.form['content']}
    """

    with open(new_file_path, "x") as f:
        f.write(content)

    return new_file_path


def run_build_script(file_path):
    try:
        cmd = ["/usr/local/bin/build-site.sh", f"{file_path}"]
        completed_proc = subprocess.run(
            cmd,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
        print(completed_proc.returncode)
        if completed_proc.returncode < 0:
            print(
                "Child was terminated by signal",
                -completed_proc.returncode,
                file=sys.stderr,
            )
        else:
            print("Child returned: ", completed_proc.returncode, file=sys.stderr)
            print("Script returned: ")
            print(completed_proc.stdout, file=sys.stderr)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)


def parse_to_list(text):
    return '"' + '","'.join(text.split(" ")) + '"'


def authenticated():
    if github.authorized or google.authorized:
        return True
    else:
        print("the user is not authenticated with any supported provider")
        return False


def authorized(user):

    if app.debug:
        return True
    elif github.authorized and user == "acbilson":
        return True
    elif google.authorized and user in ["Alexander Bilson", "Amie Bilson"]:
        return True
    else:
        print(f"{user} is not authorized to use this app")


def get_user():
    if github.authorized:
        resp = github.get("/user")
        assert resp.ok
        return resp.json()["login"]
    elif google.authorized:
        resp = google.get("/oauth2/v3/userinfo")
        assert resp.ok, resp.text
        return resp.json()["name"]
