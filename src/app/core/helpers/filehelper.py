import os
from os import DirEntry
from typing import List
from pathlib import Path


def read_files(paths: List[str]) -> List[DirEntry]:
    files = []
    for path in paths:
        files += [x for x in os.scandir(path) if x.is_file()]
    return files


def save(path: Path, content: str) -> None:
    if not os.path.exists(path.parent):
        os.makedirs(path.parent)
    with open(path, "x", newline="\n") as f:
        f.write(content)


def update(path: Path, content: str) -> None:
    with open(path, "w", newline="\n") as f:
        f.write(content)
