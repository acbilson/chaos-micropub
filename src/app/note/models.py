import toml
from pathlib import Path
from os import path
from datetime import datetime


class Note:
    """read-only note representation"""

    def __init__(
        self,
        base_path: Path,
        notename: str,
        backlinks: list,
        tags: list,
        title: str,
        date: datetime,
        lastmod: datetime,
        epistemic: str,
        author: str,
        content: str,
        comments: str,
        aliases: list,
    ):
        self._base_path = base_path
        self._notename = notename
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
        if self._notename is not None:
            return path.join(self._base_path, self._folder, self._notename)
        else:
            return Path(path.join(self._base_path, self._folder, f"{self.filename}.md"))
            

    @property
    def filename(self):
        if self._notename is not None:
            return self._notename
        else:
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
        if self._date is not None:
            return datetime.fromisoformat(self._date)
        else:
            return datetime.now()

    @property
    def lastmod(self):
        if self._lastmod is not None and self._lastmod != "":
            return datetime.fromisoformat(self._lastmod)
        else:
            return datetime.now()

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

    @property
    def aliases(self):
        return self._aliases

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
        if self.aliases is not None and self.aliases != "":
            top["aliases"] = self.aliases

        top_matter = toml.dumps(top)
        return separator + top_matter + separator + self.content
