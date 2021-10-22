import toml
from pathlib import Path
from os import path
from datetime import datetime


class Log:
    """read-only log representation"""

    def __init__(
        self,
        base_path: Path,
        date: datetime,
        author: str,
        content: str,
    ):
        self._base_path = base_path
        self._date = date
        self._author = author
        self._content = content

    @property
    def path(self):
        return Path(path.join(self._base_path, "logs", f"{self.filename}.md"))

    @property
    def filename(self):
        return self.timestamp.strftime("%Y%m%d-%H%M%S")

    @property
    def date(self):
        return self.timestamp.isoformat()

    @property
    def timestamp(self):
        return datetime.fromisoformat(self._date)

    @property
    def author(self):
        return self._author

    @property
    def content(self):
        return self._content

    def compose(self):
        separator = "+++\n"
        top_matter = toml.dumps(
            {
                "author": self.author,
                "date": self.date,
            }
        )
        return separator + top_matter + separator + self.content
