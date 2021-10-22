from pathlib import Path
from os import path
from datetime import datetime
from flask_wtf import FlaskForm


class MicropubFile:
    def __init__(self, base_path: Path, form: FlaskForm, user: str):
        self._base_path = base_path
        self._form = form
        self._user = user

    @property
    def body(self):
        return self._form.content.data

    @property
    def user(self):
        return (
            "Alex Bilson"
            if (self._user == "acbilson" or self._user == "Alexander Bilson")
            else self._user
        )

    @property
    def date(self):
        return self.timestamp.isoformat() if self.timestamp else None

    @property
    def timestamp(self):
        d = self._form.current_date.data
        return datetime.fromisoformat(d) if d else None

    @property
    def path(self):
        return Path(path.join(self._base_path, f"{self.filename}.md"))

    def save(self):
        with open(self.path, "x", newline="\n") as f:
            f.write(self.compose())
        return self.path

    def update(self):
        with open(self.path, "w", newline="\n") as f:
            f.write(self.compose())
        return self.path

    @property
    def filename(self):
        raise "not implemented"

    def compose(self):
        raise "not implemented"


class LogFile(MicropubFile):
    def __init__(self, base_path: Path, form: FlaskForm, user: str):
        super().__init__(base_path, form, user)

    @property
    def filename(self):
        return self.timestamp.strftime("%Y%m%d-%H%M%S")

    def compose(self) -> str:
        return f"""+++
author = "{self.user}"
date = "{self.date}"
+++
{self.body}""".encode(
            "utf-8"
        ).decode(
            "utf-8"
        )


class NoteFile(MicropubFile):
    def __init__(self, base_path: Path, form: FlaskForm, user: str):
        super().__init__(base_path, form, user)

    @property
    def title(self):
        return self._form.title.data

    @property
    def tags(self):
        return '"' + '","'.join(self._form.tags.data.split(" ")) + '"'

    @property
    def comments(self):
        return "true" if self._form.comments.data == "on" else "false"

    @property
    def filename(self):
        return self.title.lower().replace(" ", "-")

    def compose(self) -> str:
        return f"""+++
author = "{self.user}"
comments = {self.comments}
date = "{self.date}"
epistemic = "seedling"
tags = [{self.tags}]
title = "{self.title}"
+++
{self.body}""".encode(
            "utf-8"
        ).decode(
            "utf-8"
        )
