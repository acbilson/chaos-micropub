from os import path
from flask import (
    request,
    render_template,
    url_for,
    redirect,
)
from flask import current_app as app

from app.core.helpers import filehelper
from app.core.helpers import scripthelper
from app.core.helpers.authhelper import get_user, authorized

from ..note import note_bp
from app.note import note_factory as NoteFactory
from app.note.forms import (
    NoteForm,
    NoteSelectionForm,
)


@note_bp.route("/note", methods=["GET", "POST"])
def create_note():
    if exits := authorized() != None:
        return exits
    form = NoteForm(request.form)

    if request.method == "GET":
        return render_template(
            "create_note.html",
            form=form,
            create_route=url_for("note_bp.create_note"),
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


@note_bp.route("/note/select", methods=["GET", "POST"])
def select_note():
    if exits := authorized() != None:
        return exits

    if request.method == "GET":
        note_path = path.join(app.config.get("CONTENT_PATH"), "notes")
        notes = filehelper.read_files(note_path)
        form = NoteSelectionForm(request.form)
        form.selected_note.choices = [(note, note) for note in notes]
        return render_template(
            "select_note.html",
            form=form,
            load_route=url_for("note_bp.select_note"),
            script=url_for("static", filename="js/micropub.js"),
        )
    else:
        selectionForm = NoteSelectionForm(request.form)
        # code=303 redirects as GET
        return redirect(
            url_for("note_bp.edit_note", path=selectionForm.selected_note.data),
            code=303,
        )


@note_bp.route("/note/edit", methods=["GET", "POST"])
def edit_note():
    if exits := authorized() != None:
        return exits

    if request.method == "GET":
        if "path" not in request.args:
            return f"path not present in query string {request.args}", 400

        note_path = request.args.get("path")
        with open(note_path, "r") as f:
            form = NoteFactory.fromBody(note_path, f.readlines())

        return render_template(
            "edit_note.html",
            form=form,
            save_route=url_for("note_bp.edit_note"),
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
