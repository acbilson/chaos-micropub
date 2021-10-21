from pathlib import Path
import yaml

class Note():

    def __init__(self, base_path: Path, user: str):
        self.base_path = base_path
        self.user = user
        self.backlinks = []
        self.tags = []
        self.title = None
        self.date = None
        self.epistemic = None


def fromBody(base_path: Path, user: str, body: list) -> Note:
    note = Note(base_path, user)
    is_top_matter = False
    top_matter = []
    content = []
    last_key = ""

    for line in body:
        if line == "+++\n":
            is_top_matter = not is_top_matter
            continue

        if is_top_matter:
            top_matter.append(line)
        else:
            content.append(line)

    header = ''.join(top_matter)
    # TODO: figure out what obj returns from safe_load for parsing purposes
    top = yaml.safe_load(header)
    if "title" in top:
        note.title = getattr(top, "title")()
    else:
        note.title = "Test Title"
    note.body = ''.join(content)
    return note


def _parseTopMatter(line: str) -> tuple:
    if "=" not in line:
        return None, line.strip()

    lines = line.split("=")
    key = lines[0].strip()
    value = lines[1].strip()

    return key, value