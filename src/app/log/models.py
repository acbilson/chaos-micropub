import toml
from pathlib import Path
from os import path
from datetime import datetime


class Log:
    """read-only log representation"""

    def __init__(
        self,
        base_path: str,
        logname: str,
        date: datetime,
        author: str,
        content: str,
        aliases: list,
    ):
        self._base_path = base_path
        self._logname = logname
        self._date = date
        self._author = author
        self._content = content
        self._aliases = aliases
        self._folder = "logs"

    @property
    def path(self):
        if self._logname is not None:
            return path.join(self._base_path, self._folder, self._logname)
        else:
            return Path(path.join(self._base_path, self._folder, f"{self.filename}.md"))

    @property
    def filename(self):
        if self._logname is not None:
            return self._logname
        else:
            return self.timestamp.strftime("%Y%m%d-%H%M%S")

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
    def author(self):
        return self._author

    @property
    def aliases(self):
        return self._aliases

    @property
    def content(self):
        return self._content

    def compose(self):
        separator = "+++\n"
        top = {
            "author": self.author,
            "date": self.date,
        }

        # adds optional tags
        if self.aliases is not None and self.aliases != "":
            top["aliases"] = self.aliases

        top_matter = toml.dumps(top)
        return separator + top_matter + separator + self.content
