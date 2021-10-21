"""Note Factory

Converts data into objects of Note* type

Currently supports TOML-style content, with YAML as a possible future implementation
"""
from flask import current_app as app
from app.micropub.forms import NoteForm
from pathlib import Path
import toml


class Note:
    def __init__(self, base_path: Path, user: str):
        self.base_path = base_path
        self.user = user
        self.backlinks = []
        self.tags = []
        self.title = None
        self.date = None
        self.epistemic = None
        self.author = None


def fromForm(base_path: Path, user: str, form: NoteForm) -> Note:
    """returns a Note obj

    converts a NoteForm obj into a Note
    """
    pass

    top = dict()
    for key in top.keys():
        if hasattr(form, key):
            setattr(form, key, top[key])



def fromBody(base_path: Path, user: str, body: list) -> NoteForm:
    """returns a NoteForm obj

    converts a list of content into a NoteForm
    """
    top_matter, content = _parseBody(body)
    top = toml.loads("".join(top_matter))
    form = NoteForm(meta={"csrf": False})

    form.title.data = top['title']
    form.tags.data = top['tags']
    form.current_date.data = top['date']
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
