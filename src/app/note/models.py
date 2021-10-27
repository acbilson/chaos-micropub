import toml
from pathlib import Path
from os import path
from datetime import datetime


class Note:
    """read-only note representation"""

    def __init__(
        self,
        base_path: Path,
        filename: str,
        backlinks: str,
        tags: str,
        title: str,
        date: str,
        lastmod: str,
        epistemic: str,
        author: str,
        content: str,
        comments: str,
        aliases: str,
    ):
        self._base_path = base_path
        self._filename = filename
        self._backlinks = backlinks
        self._tags = tags
        self._title = title
        self._date = date
        self._lastmod = lastmod
        self._epistemic = epistemic
        self._author = author
        self._content = content
        self._comments = comments
        self._aliases = aliases
        self._folder = "notes"

    @property
    def path(self):
        return Path(path.join(self._base_path, self._folder, f"{self.filename}.md"))

    @property
    def filename(self):
        return self._filename if self._filename else self.title.lower().replace(" ", "-")

    @property
    def backlinks(self):
        return toml.loads(f"backlinks = {self._backlinks}").get("backlinks") if self._backlinks else None


    @property
    def tags(self):
        return toml.loads(f"tags = {self._tags}").get("tags") if self._tags else None

    @property
    def title(self):
        return self._title

    @property
    def date(self):
        return self.timestamp.isoformat()

    @property
    def timestamp(self):
        return datetime.fromisoformat(self._date) if self._date else datetime.now()

    @property
    def lastmod(self):
        return datetime.fromisoformat(self._lastmod).isoformat() if self._lastmod else datetime.now().isoformat()

    @property
    def epistemic(self):
        return self._epistemic if self._epistemic else "seedling"

    @property
    def author(self):
        return self._author

    @property
    def comments(self):
        return self._comments

    @property
    def content(self):
        return self._content

    @property
    def aliases(self):
        return toml.loads(f"aliases = {self._aliases}").get("aliases") if self._aliases else None

    def compose(self):
        separator = "+++\n"
        top = {
            "author": self.author,
            "backlinks": self.backlinks,
            "comments": self.comments,
            "date": self.date,
            "epistemic": self.epistemic,
            "lastmod": self.lastmod,
            "tags": self.tags,
            "title": self.title,
        }

        # adds optional tags 
        if self.aliases:
            top["aliases"] = self.aliases

        top_matter = toml.dumps(top)
        return separator + top_matter + separator + self.content
