"""Note Factory

Converts data into objects of Note* type

Currently supports TOML-style content, with YAML as a possible future implementation
"""
from app.note.forms import NoteForm
from app.note.models import Note
from os import path
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
        filename=form.filename.data,
        backlinks=form.backlinks.data,
        tags=form.tags.data,
        title=form.title.data,
        date=form.current_date.data,
        lastmod=form.modified_date.data,
        epistemic=form.epistemic.data,
        content=form.content.data,
        comments=form.comments.data,
        author=user,
        aliases=form.aliases.data,
    )


def fromBody(note_path: Path, body: list) -> NoteForm:
    """returns a NoteForm obj

    converts a list of content into a NoteForm
    """
    notename = path.basename(note_path)

    top_matter, content = _parseBody(body)
    top = toml.loads("".join(top_matter))
    return NoteForm(
        title=top.get("title"),
        filename=filename,
        author=top.get("author"),
        tags=top.get("tags"),
        backlinks=top.get("backlinks") if "backlinks" in top else None,
        epistemic=top.get("epistemic"),
        current_date=top.get("date"),
        modified_date=top.get("lastmod") if "lastmod" in top else None,
        comments=top.get("comments"),
        content="".join(content),
        aliases=top.get("aliases")
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
