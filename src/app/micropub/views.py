from pathlib import Path
from datetime import datetime

from flask import (
    request,
    render_template,
    url_for,
    redirect,
    Response,
)
from flask import current_app as app

from app.micropub import filehelper

from ..micropub import micropub_bp
from app.micropub.forms import (
    LoginForm,
    LogForm,
    NoteForm,
    SelectForm,
    NoteSelectionForm,
)
from app.micropub.models import Log, Note
from app.micropub.authhelper import authenticated, authorized, get_user
from app.micropub.filehelper import read_notes
from app.micropub import scripthelper
from app.micropub import note_factory as NoteFactory
from app.micropub import log_factory as LogFactory


def _authorized() -> Response:
    if not app.debug and not authenticated():
        return redirect(url_for("micropub_bp.login"))
    user = get_user()
    if not authorized(user):
        return f"{user} is not authorized to use this application.", 403
    return None


@micropub_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if not app.debug and not authenticated():
            form = LoginForm(request.form)
            return render_template(
                "login.html",
                login_route=url_for("micropub_bp.login"),
            )
        else:
            return redirect(url_for("micropub_bp.select"))

    else:
        if app.debug:
            return redirect(url_for("micropub_bp.select"))

        form = LoginForm(request.form)
        if not form.validate():
            return f"login failed: {form.errors}", 501

        return redirect(url_for(f"{form.option.data}.login"))


@micropub_bp.route("/", methods=["GET", "POST"])
def select():
    if exits := _authorized() != None:
        return exits

    if request.method == "GET":
        form = SelectForm()
        return render_template(
            "select.html", create_route=url_for("micropub_bp.select"), form=form
        )
    else:
        form = SelectForm(request.form)
        if not form.validate():
            return (
                f"No action was passed to this endpoint {form.errors}, {form.action.data}. aborting.",
                400,
            )

        return redirect(url_for(f"micropub_bp.{form.action.data}"))


@micropub_bp.route("/log", methods=["GET", "POST"])
def create_log():
    if exits := _authorized() != None:
        return exits
    form = LogForm(request.form)

    if request.method == "GET":
        return render_template(
            "create_log.html",
            form=form,
            create_route=url_for("micropub_bp.create_log"),
            script=url_for("static", filename="js/micropub.js"),
        )
    else:
        if not form.validate():
            return (
                f"form could not be validated because {form.errors}. aborting.",
                400,
            )

        user = get_user()
        log = LogFactory.fromForm(app.config.get("CONTENT_PATH"), user, form)

        filehelper.save(log.path, log.content)
        scripthelper.run_build_script(log.path)

        return redirect(app.config["SITE"])


@micropub_bp.route("/note", methods=["GET", "POST"])
def create_note():
    if exits := _authorized() != None:
        return exits
    form = NoteForm(request.form)

    if request.method == "GET":
        return render_template(
            "create_note.html",
            form=form,
            create_route=url_for("micropub_bp.create_note"),
            script=url_for("static", filename="js/micropub.js"),
        )
    else:
        if not form.validate():
            return (
                f"form could not be validated because {form.errors}. aborting.",
                400,
            )

        user = get_user()
        note = NoteFactory.fromForm(app.config.get("CONTENT_PATH"), user, form)

        filehelper.save(note.path, note.compose())
        scripthelper.run_build_script(note.path)

        return redirect(app.config["SITE"])


@micropub_bp.route("/note/select", methods=["GET", "POST"])
def select_note():
    if exits := _authorized() != None:
        return exits

    if request.method == "GET":
        notes = read_notes("/mnt/chaos/content/notes")
        form = NoteSelectionForm(request.form)
        form.selected_note.choices = [(note, note) for note in notes]
        return render_template(
            "edit_notes.html",
            form=form,
            load_route=url_for("micropub_bp.select_note"),
            script=url_for("static", filename="js/micropub.js"),
        )
    else:
        selectionForm = NoteSelectionForm(request.form)
        # code=303 redirects as GET
        return redirect(
            url_for("micropub_bp.edit_note", path=selectionForm.selected_note.data),
            code=303,
        )


@micropub_bp.route("/note/edit", methods=["GET", "POST"])
def edit_note():
    if exits := _authorized() != None:
        return exits

    if request.method == "GET":
        if "path" not in request.args:
            return f"path not present in query string {request.args}", 400

        with open(request.args.get("path"), "r") as f:
            form = NoteFactory.fromBody(app.config.get("CONTENT_PATH"), f.readlines())

        return render_template(
            "edit_note.html",
            form=form,
            save_route=url_for("micropub_bp.edit_note"),
            script=url_for("static", filename="js/micropub.js"),
        )
    else:
        form = NoteForm(request.form)
        if not form.validate():
            return (
                f"form could not be validated because {form.errors}. aborting.",
                400,
            )
        user = get_user()
        note = NoteFactory.fromForm(app.config.get("CONTENT_PATH"), user, form)

        filehelper.update(note.path, note.compose())
        scripthelper.run_build_script(note.path)

        return redirect(app.config["SITE"])
