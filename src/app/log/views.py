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
from app.log.forms import LogForm
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
        log = LogFactory.fromForm(app.config.get("CONTENT_PATH"), user, form)

        filehelper.save(log.path, log.content)
        scripthelper.run_build_script(log.path)

        return redirect(app.config["SITE"])
