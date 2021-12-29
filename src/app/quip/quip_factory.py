"""Quip Factory

Converts data into objects of Quip* type

Currently supports TOML-style content, with YAML as a possible future implementation
"""
from app.quip.forms import QuipForm
from app.quip.models import Quip
from os import path
from pathlib import Path
from datetime import datetime
import toml


def fromForm(base_path: Path, user: str, form: QuipForm) -> Quip:
    """returns a Quip obj

    converts a QuipForm obj into a Quip
    """
    user = "Alex Bilson" if user == "acbilson" or user == "Alexander Bilson" else user
    return Quip(
        base_path=base_path,
        filename=form.filename.data,
        date=form.current_date.data,
        lastmod=form.modified_date.data,
        content=form.content.data,
        author=user,
        aliases=form.aliases.data,
    )


def fromBody(quip_path: Path, body: list) -> QuipForm:
    """returns a QuipForm obj

    converts a list of content into a QuipForm
    """
    filename = path.basename(quip_path)

    top_matter, content = _parseBody(body)
    top = toml.loads("".join(top_matter))
    return QuipForm(
        author=top.get("author") if "author" in top else "Alex Bilson",
        current_date=top.get("date"),
        modified_date=top.get("lastmod") if "lastmod" in top else None,
        content="".join(content),
        filename=filename,
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
