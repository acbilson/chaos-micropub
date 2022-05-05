"""Log Factory

Converts data into objects of Log* type

Currently supports TOML-style content, with YAML as a possible future implementation
"""
from flask import current_app as app
from app.log.forms import LogForm
from app.log.models import Log
from os import path
from pathlib import Path
import toml


def fromForm(base_path: Path, user: str, form: LogForm) -> Log:
    """returns a Log obj

    converts a LogForm obj into a Log
    """
    user = "Alex Bilson" if user == "acbilson" or user == "Alexander Bilson" else user
    return Log(
        base_path=base_path,
        filename=form.filename.data,
        date=form.current_date.data,
        lastmod=form.modified_date.data,
        content=form.content.data,
        author=user,
        aliases=form.aliases.data,
    )


def fromBody(log_path: Path, body: list) -> LogForm:
    """returns a LogForm obj

    converts a list of content into a LogForm
    """
    logname = path.basename(log_path)

    top_matter, content = _parseBody(body)
    top = toml.loads("".join(top_matter))
    return LogForm(
        author=top.get("author") if "author" in top else "Alex Bilson",
        current_date=top.get("date"),
        modified_date=top.get("lastmod") if "lastmod" in top else None,
        content="".join(content),
        logname=logname,
        aliases=top.get("aliases") if "aliases" in top else None,
    )


def _parseBody(body: list) -> tuple:
    """returns a (list, list)

    parses a list into its top matter (toml) and content (md)
    """
    is_top_matter = False
    top_matter = []
    content = []

    for line in body:
        if line == "+++\n":
            is_top_matter = not is_top_matter
            continue

        if is_top_matter and line != "+++\n":
            top_matter.append(line)
        else:
            content.append(line)

    return top_matter, content