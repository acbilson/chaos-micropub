import os
from pathlib import Path


def read_files(dir):
    return [os.path.join(dir, name) for name in os.listdir(dir)]


def save(path: Path, content: str):
    with open(path, "x", newline="\n") as f:
        f.write(content)


def update(path: Path, content: str):
    with open(path, "w", newline="\n") as f:
        f.write(content)
