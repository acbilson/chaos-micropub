"""Note Factory

Converts data into objects of Note* type

Currently supports TOML-style content, with YAML as a possible future implementation
"""
from app.note.forms import NoteForm
from app.note.models import Note
from pathlib import Path
from datetime import datetime
import toml


def fromForm(base_path: Path, user: str, form: NoteForm) -> Note:
    """returns a Note obj

    converts a NoteForm obj into a Note
    """
    user = "Alex Bilson" if user == "acbilson" or user == "Alexander Bilson" else user
    return Note(
        base_path=base_path,
        backlinks=form.backlinks.data,
        tags=form.tags.data,
        title=form.title.data,
        date=form.current_date.data,
        lastmod=form.modified_date.data,
        epistemic=form.epistemic.data,
        content=form.content.data,
        comments=form.comments.data,
        author=user,
    )


def fromBody(base_path: Path, body: list) -> NoteForm:
    """returns a NoteForm obj

    converts a list of content into a NoteForm
    """
    top_matter, content = _parseBody(body)
    top = toml.loads("".join(top_matter))
    return NoteForm(
        title=top["title"],
        author=top["author"],
        tags=top["tags"],
        backlinks=top["backlinks"] if "backlinks" in top else None,
        epistemic=top["epistemic"],
        current_date=top["date"],
        modified_date=top["lastmod"] if "lastmod" in top else datetime.now(),
        comments="true" if "comments" in top else "false",
        content="".join(content),
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
