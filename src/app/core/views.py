from flask import (
    request,
    render_template,
    url_for,
    redirect,
)
from flask import current_app as app

from app.core.helpers import authhelper

from ..core import core_bp
from app.core.forms import (
    LoginForm,
    SelectForm,
)


@core_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if not app.debug and not authhelper._authenticated():
            form = LoginForm(request.form)
            return render_template(
                "login.html",
                form=form,
                login_route=url_for("core_bp.login"),
            )
        else:
            return redirect(url_for("core_bp.select"))

    else:
        if app.debug:
            return redirect(url_for("core_bp.select"))

        form = LoginForm(request.form)
        if not form.validate():
            return f"login failed: {form.errors}", 501

        return redirect(url_for(form.action.data))


@core_bp.route("/", methods=["GET", "POST"])
def select():
    if (exits := authhelper.authorized()) != None:
        return exits

    if request.method == "GET":
        form = SelectForm()
        return render_template(
            "select.html", create_route=url_for("core_bp.select"), form=form
        )
    else:
        form = SelectForm(request.form)
        if not form.validate():
            return (
                f"No action was passed to this endpoint {form.errors}, {form.action.data}. aborting.",
                400,
            )

        return redirect(url_for(form.action.data))
