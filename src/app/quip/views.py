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

from ..quip import quip_bp
from app.quip import quip_factory as QuipFactory
from app.quip.forms import (
    QuipForm,
    QuipSelectionForm,
)


@quip_bp.route("/quip", methods=["GET", "POST"])
def create_quip():
    if (exits := authorized()) != None:
        return exits
    form = QuipForm(request.form)

    if request.method == "GET":
        return render_template(
            "create_quip.html",
            form=form,
            create_route=url_for("quip_bp.create_quip"),
            script=url_for("static", filename="js/micropub.js"),
        )
    else:
        if not form.validate():
            return (
                f"form could not be validated because {form.errors}. aborting.",
                400,
            )

        user = get_user()
        quip = QuipFactory.fromForm(app.config.get("CONTENT_PATH"), user, form)

        app.logger.info(f"creating quip: {quip.path}")
        app.logger.debug(quip.compose())

        filehelper.save(quip.path, quip.compose())
        scripthelper.run_build_script(quip.path)

        return redirect(app.config["SITE"])


@quip_bp.route("/quip/select", methods=["GET", "POST"])
def select_quip():
    if (exits := authorized()) != None:
        return exits

    if request.method == "GET":
        quip_path = path.join(app.config.get("CONTENT_PATH"), "quips")
        quips = filehelper.read_files([quip_path])
        form = QuipSelectionForm(request.form)

        # sorts quip files by last modified descending
        form.selected_quip.choices = [
            (quip.path, quip.name)
            for quip in sorted(quips, key=lambda q: q.stat().st_mtime, reverse=True)
        ]

        return render_template(
            "select_quip.html",
            form=form,
            load_route=url_for("quip_bp.select_quip"),
            script=url_for("static", filename="js/micropub.js"),
        )
    else:
        selectionForm = QuipSelectionForm(request.form)
        # code=303 redirects as GET
        return redirect(
            url_for("quip_bp.edit_quip", path=selectionForm.selected_quip.data),
            code=303,
        )


@quip_bp.route("/quip/edit", methods=["GET", "POST"])
def edit_quip():
    if (exits := authorized()) != None:
        return exits

    if request.method == "GET":
        if "path" not in request.args:
            return f"path not present in query string {request.args}", 400

        quip_path = request.args.get("path")
        with open(quip_path, "r") as f:
            form = QuipFactory.fromBody(quip_path, f.readlines())

        return render_template(
            "edit_quip.html",
            form=form,
            save_route=url_for("quip_bp.edit_quip"),
            script=url_for("static", filename="js/micropub.js"),
        )
    else:
        form = QuipForm(request.form)
        if not form.validate():
            return (
                f"form could not be validated because {form.errors}. aborting.",
                400,
            )
        user = get_user()

        # nullifies lastmod so it refreshes to now
        form.modified_date.data = None

        quip = QuipFactory.fromForm(app.config.get("CONTENT_PATH"), user, form)

        app.logger.info(f"editing quip: {quip.path}")
        app.logger.debug(quip.compose())

        filehelper.update(quip.path, quip.compose())
        scripthelper.run_build_script(quip.path)

        return redirect(app.config["SITE"])
