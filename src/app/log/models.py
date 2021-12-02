import toml
from pathlib import Path
from os import path
from datetime import datetime


class Log:
    """read-only log representation"""

    def __init__(
        self,
        base_path: str,
        filename: str,
        date: str,
        lastmod: str,
        author: str,
        content: str,
        aliases: str,
    ):
        self._base_path = base_path
        self._filename = filename
        self._date = date
        self._lastmod = lastmod
        self._author = author
        self._content = content
        self._aliases = aliases
        self._folder = "logs"

    @property
    def folder(self):
        return path.join(self._folder, self.timestamp.strftime('%Y'), self.timestamp.strftime('%m'))

    @property
    def path(self):
        return Path(path.join(self._base_path, self.folder, f"{self.filename}.md"))

    @property
    def filename(self):
        if self._filename:
            return self._filename.removesuffix(".md")
        else:
            return self.timestamp.strftime("%Y%m%d-%H%M%S")

    @property
    def date(self):
        return self.timestamp.isoformat()

    @property
    def timestamp(self):
        return datetime.fromisoformat(self._date) if self._date else datetime.now()

    @property
    def lastmod(self):
        return (
            datetime.fromisoformat(self._lastmod).isoformat()
            if self._lastmod
            else datetime.now().isoformat()
        )

    @property
    def author(self):
        return self._author

    @property
    def aliases(self):
        return (
            toml.loads(f"aliases = {self._aliases}").get("aliases")
            if self._aliases
            else None
        )

    @property
    def content(self):
        return self._content.replace("\r\n", "\n")

    def compose(self):
        separator = "+++\n"
        top = {
            "author": self.author,
            "date": self.date,
            "lastmod": self.lastmod,
        }

        # adds optional tags
        if self.aliases:
            top["aliases"] = self.aliases

        top_matter = toml.dumps(top)
        return separator + top_matter + separator + self.content
