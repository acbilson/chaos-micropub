from pathlib import Path
from datetime import datetime

from flask import (
    Blueprint,
    request,
    render_template,
    url_for,
    redirect,
)
from flask import current_app as app

from ..micropub import micropub_bp
from app.micropub.forms import (
  LoginForm,
  LogForm,
  NoteForm,
  CreateForm,
)
from app.micropub.models import (
  LogFile,
  NoteFile,
)
from app.micropub.authhelper import (
  authenticated,
  authorized,
  get_user
)
from app.micropub import scripthelper

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

        form = LoginForm(form)
        if not form.validate():
            return f"login failed: {form.errors}", 501

        return redirect(url_for(f"{form.option.data}.login"))
    else:
        return f"{request.method} is unsupported for this endpoint", 501


@micropub_bp.route("/", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        if not app.debug and not authenticated():
            return redirect(url_for("micropub_bp.login"))
        else:
            form = CreateForm(meta={"csrf": False})
            return render_template(
                "create.html",
                create_route=url_for("micropub_bp.create"),
                form=form)
    elif request.method == "POST":
        if not app.debug and not authenticated():
            return redirect(url_for("micropub_bp.login"))
        else:
            user = get_user()
            if not authorized(user):
                return f"{user} is not authorized to use this application.", 403

            form = CreateForm(request.form, meta={"csrf": False})
            if not form.validate():
                return f"No post type was passed to this endpoint {form.errors}, {form.post_type.data}. aborting.", 400

            return redirect(url_for(f"micropub_bp.create_{form.post_type.data}"))


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

            form = LogForm(request.form, meta={"csrf": False})
            if not form.validate():
                return f"form could not be validated because {form.errors}. aborting.", 400

            log = LogFile("/mnt/chaos/content/logs", form, user)
            new_file_path = log.save()

            scripthelper.run_build_script(new_file_path)

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

            form = NoteForm(request.form, meta={"csrf": False})
            if not form.validate():
                return f"form could not be validated because {form.errors}. aborting.", 400

            note = NoteFile("/mnt/chaos/content/notes", form, user)
            new_file_path = note.save()

            scripthelper.run_build_script(new_file_path)

            return redirect(app.config["SITE"])
    else:
        return f"{request.method} is unsupported for this endpoint", 501