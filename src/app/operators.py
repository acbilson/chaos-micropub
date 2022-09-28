import sys
import subprocess
from subprocess import CalledProcessError
from datetime import datetime
from typing import Tuple, List


def null_or_empty(v) -> bool:
    return v in [None, ""]


def compose_header(options: dict):
    option_text = "\n".join([f"{k} = {v}" for k,v in options.items()])

    now = datetime.now().isoformat()
    header = f'+++\nauthor = "Alex Bilson"\ndate = "{now}"\nlastmod = {now}\nepistemic = "sprout"\n{option_text}\n+++'
    return header


def try_run_cmd(cmds: List[str], cwd: str) -> Tuple[str, str]:
    output = None
    try:
        output = subprocess.run(cmds, capture_output=True, check=True, cwd=cwd)
    except CalledProcessError as e:
        return None, f"{e} : {e.output}"

    if "push" in cmds:
        return output.stderr.decode(), output.stdout.decode()
    else:
        return output.stdout.decode(), output.stderr.decode()


def git_pull(cwd: str) -> str:
    commands = [["git", "pull", "--rebase"]]
    for cmd in commands:
        output, error = try_run_cmd(cmd, cwd)
        print(f"command was: {cmd}")
        print(f"output was: {output}")
        print(f"error was: {error}")
        if not null_or_empty(error):
            print(f"ending with {cmd}, {error}")
            return str(error)
    return None


def git_commit(file_path, cwd: str, msg: str) -> str:
    commands = [
        ["git", "config", "user.name", "Micropub Bot"],
        ["git", "config", "user.email", "acbilson@gmail.com"],
        ["git", "add", "-v", "."],
        ["git", "commit", "-m", f'"{msg}"'],
        ["git", "push"],
    ]
    for cmd in commands:
        print(f"command was: {cmd} at {cwd}")
        output, error = try_run_cmd(cmd, cwd)
        print(f"output was: {output}")
        print(f"error was: {error}")
        if not null_or_empty(error):
            print(f"ending with {cmd}, {error}")
            return str(error)
    return None
