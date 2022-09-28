import sys
import subprocess
from datetime import datetime
from typing import Tuple, List


def null_or_empty(v) -> bool:
    return v in [None, ""]


def compose_header(options):
    option_text = map(options, lambda x: f"{x.label} = {x.value}").join("\n")

    now = datetime.now()
    header = f'+++\nauthor = "Alex Bilson"\ndate = {now()}\nlastmod = {now}\nepistemic = "sprout"\n{option_text}\n+++'
    return header


def try_run_cmd(cmds: List[str]) -> Tuple[str, str]:
    output = None
    try:
        output = subprocess.run(cmds, capture_output=True, check=True)
    except Exception as e:
        #import pdb; pdb.set_trace()
        return None, str(e)

    return output.stdout.decode(), output.stderr.decode()


def git_pull() -> str:
    commands = [["git", "rebase", "master"]]
    for cmd in commands:
        output, error = try_run_cmd(cmd)
        print(f"command was: {cmd}")
        print(f"output was: {output}")
        print(f"error was: {error}")
        if not null_or_empty(error):
            print(f"ending with {cmd}, {error}")
            return str(error)
    return None


def git_commit(file_path, msg: str) -> str:
    commands = [
        ["git", "config", "user.name", "Micropub Bot"],
        ["git", "config", "user.email", "acbilson@gmail.com"],
        ["git", "add", "."],
        ["git", "commit", "-m", msg],
        ["git", "push"],
    ]
    for cmd in commands:
        output, error = try_run_cmd(cmd)
        print(f"command was: {cmd}")
        print(f"output was: {output}")
        print(f"error was: {error}")
        if not null_or_empty(error):
            print(f"ending with {cmd}, {error}")
            return str(error)
    return None
