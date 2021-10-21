from flask import current_app as app
from flask_dance.contrib.github import github
from flask_dance.contrib.google import google


def authenticated() -> bool:
    return github.authorized or google.authorized


def authorized(user) -> bool:
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
