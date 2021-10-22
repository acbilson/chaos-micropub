import toml
from pathlib import Path
from os import path
from datetime import datetime


class Note:
    """read-only note representation"""

    def __init__(
        self,
        base_path: Path,
        backlinks: list,
        tags: list,
        title: str,
        date: datetime,
        lastmod: datetime,
        epistemic: str,
        author: str,
        content: str,
        comments: str,
    ):
        self._base_path = base_path
        self._backlinks = backlinks
        self._tags = tags
        self._title = title
        self._date = date
        self._lastmod = lastmod
        self._epistemic = epistemic
        self._author = author
        self._content = content
        self._comments = comments

    @property
    def path(self):
        return Path(path.join(self._base_path, "notes", f"{self.filename}.md"))

    @property
    def filename(self):
        return self.title.lower().replace(" ", "-")

    @property
    def backlinks(self):
        return self._backlinks

    @property
    def tags(self):
        return self._tags

    @property
    def title(self):
        return self._title

    @property
    def date(self):
        return self.timestamp.isoformat()

    @property
    def timestamp(self):
        return datetime.fromisoformat(self._date)

    @property
    def lastmod(self):
        return self._lastmod

    @property
    def epistemic(self):
        return self._epistemic

    @property
    def author(self):
        return self._author

    @property
    def comments(self):
        return self._comments

    @property
    def content(self):
        return self._content

    def compose(self):
        separator = "+++\n"
        top_matter = toml.dumps(
            {
                "author": self.author,
                "backlinks": self.backlinks,
                "comments": self.comments,
                "date": self.date,
                "epistemic": self.epistemic,
                "lastmod": self.lastmod,
                "tags": self.tags,
                "title": self.title,
            }
        )
        return separator + top_matter + separator + self.content
