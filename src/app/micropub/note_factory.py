"""Note Factory

Converts data into objects of Note* type

Currently supports TOML-style content, with YAML as a possible future implementation
"""
from app.micropub.forms import NoteForm
from app.micropub.models import Note
from pathlib import Path
from datetime import datetime
import toml


def fromForm(base_path: Path, user: str, form: NoteForm) -> Note:
    """returns a Note obj

    converts a NoteForm obj into a Note
    """
    return Note(
        base_path=base_path,
        backlinks=form.backlinks.data,
        tags=form.tags.data,
        title=form.title.data,
        date=form.current_date.data,
        lastmod=form.modified_date.data,
        epistemic=form.epistemic.data,
        content=form.content.data,
        author=user,
    )


def fromBody(base_path: Path, body: list) -> NoteForm:
    """returns a NoteForm obj

    converts a list of content into a NoteForm
    """
    top_matter, content = _parseBody(body)
    top = toml.loads("".join(top_matter))
    form = NoteForm()

    form.title.data = top["title"]
    form.author.data = top["author"]
    form.tags.data = top["tags"]
    form.current_date.data = top["date"]
    form.modified_date.data = top["lastmod"] if "lastmod" in top else datetime.now()
    form.comments.data = "true" if "comments" in top else "false"
    form.content.data = "".join(content)

    return form


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
