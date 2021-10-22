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

from ..log import log_bp
from app.log.forms import LogForm, LogSelectionForm
from app.log import log_factory as LogFactory


@log_bp.route("/log", methods=["GET", "POST"])
def create_log():
    if exits := authorized() != None:
        return exits
    form = LogForm(request.form)

    if request.method == "GET":
        return render_template(
            "create_log.html",
            form=form,
            create_route=url_for("log_bp.create_log"),
            script=url_for("static", filename="js/micropub.js"),
        )
    else:
        if not form.validate():
            return (
                f"form could not be validated because {form.errors}. aborting.",
                400,
            )

        user = get_user()
        log = LogFactory.fromForm(user, form)

        filehelper.save(log.path, log.content)
        scripthelper.run_build_script(log.path)

        return redirect(app.config["SITE"])


@log_bp.route("/log/select", methods=["GET", "POST"])
def select_log():
    if exits := authorized() != None:
        return exits

    if request.method == "GET":
        log_path = path.join(app.config.get("CONTENT_PATH"), "logs")
        logs = filehelper.read_files(log_path)
        form = LogSelectionForm(request.form)
        form.selected_log.choices = [(log, log) for log in logs]
        return render_template(
            "select_log.html",
            form=form,
            load_route=url_for("log_bp.select_log"),
            script=url_for("static", filename="js/micropub.js"),
        )
    else:
        selectionForm = LogSelectionForm(request.form)
        # code=303 redirects as GET
        return redirect(
            url_for("log_bp.edit_log", path=selectionForm.selected_log.data),
            code=303,
        )


@log_bp.route("/log/edit", methods=["GET", "POST"])
def edit_log():
    if exits := authorized() != None:
        return exits

    if request.method == "GET":
        if "path" not in request.args:
            return f"path not present in query string {request.args}", 400

        log_path = request.args.get("path")
        with open(log_path, "r") as f:
            form = LogFactory.fromBody(log_path, f.readlines())

        return render_template(
            "edit_log.html",
            form=form,
            save_route=url_for("log_bp.edit_log"),
            script=url_for("static", filename="js/micropub.js"),
        )
    else:
        form = LogForm(request.form)
        if not form.validate():
            return (
                f"form could not be validated because {form.errors}. aborting.",
                400,
            )
        user = get_user()
        log = LogFactory.fromForm(app.config.get("CONTENT_PATH"), user, form)

        filehelper.update(log.path, log.compose())
        scripthelper.run_build_script(log.path)

        return redirect(app.config["SITE"])
