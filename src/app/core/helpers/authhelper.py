from flask import redirect, url_for, Response
from flask import current_app as app
from flask_dance.contrib.github import github
from flask_dance.contrib.google import google


def authorized() -> Response:
    if not app.debug and not _authenticated():
        return redirect(url_for("micropub_bp.login"))
    user = get_user()
    if not _authorized(user):
        return f"{user} is not authorized to use this application.", 403
    return None


def _authenticated() -> bool:
    return github.authorized or google.authorized


def _authorized(user) -> bool:
    return (
        app.debug
        or (github.authorized and user == "acbilson")
        or (google.authorized and user in ["Alexander Bilson", "Amie Bilson"])
    )


def get_user() -> str:
    if github.authorized:
        resp = github.get("/user")
        assert resp.ok
        return resp.json()["login"]
    elif google.authorized:
        resp = google.get("/oauth2/v3/userinfo")
        assert resp.ok, resp.text
        return resp.json()["name"]
    else:
        return None
