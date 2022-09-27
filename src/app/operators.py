import sys
import subprocess
from datetime import datetime
from typing import Tuple, List

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
        return None, str(e)

    return output.stdout.decode(), output.stderr.decode()

def git_commit(file_path) -> str:
    commands = [
        ["git", "config", "user.name", "Micropub Bot"],
        ["git", "config", "user.email", "acbilson@gmail.com"],
        ["git", "add", "."],
        ["git", "commit", "-m", "This is a test"],
            ]
    for cmd in commands:
        output, error = try_run_cmd(cmd)
        print(f"command was: {cmd}")
        print(f"output was: {output}")
        print(f"error was: {error}")
        if error not in [None, ""]:
            print(f"ending with {cmd}, {error}")
            return str(error)
    return None
