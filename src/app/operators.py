import subprocess
import toml
from subprocess import CalledProcessError
from datetime import datetime


def replace_url_suffix(path: str, suffix: str) -> str:
    return ".".join(path.split(".")[0:-1]) + suffix


def null_or_empty(v) -> bool:
    return v in [None, ""]


def compose_header(options: dict) -> str:
    option_text = "\n".join([f"{k} = {v}" for k, v in options.items()])

    now = datetime.now().isoformat()
    header = f'+++\nauthor = "Alex Bilson"\ndate = "{now}"\nlastmod = {now}\nepistemic = "sprout"\n{option_text}\n+++'
    return header


# combines top matter and content into one file
def combine_file_content(top: dict, body: list[str], photo: dict | None) -> str:
    separator = "+++\n"
    top_matter = toml.dumps(top)

    photo_entry = ""
    if photo is not None:
        add_key = lambda k, v: "" if null_or_empty(v) else f'{k}="{v}" '

        photo_entry = "\n{{< caption "
        photo_entry += add_key("caption", photo.get("caption"))
        photo_entry += add_key("alt", photo.get("alt"))
        photo_entry += add_key("src", photo.get("src"))
        photo_entry += ">}}"

    return separator + top_matter + separator + "".join(body) + photo_entry


# splits a file into its top matter and content
def split_file_content(body: list[str]) -> tuple[dict, list[str]]:
    """returns a (list, list)

    parses a list into its top matter (toml) and content (md)
    """
    is_top_matter = False
    top_matter = []
    content = []

    for line in body:
        if line == "+++\n":
            is_top_matter = not is_top_matter
            continue

        if is_top_matter and line != "+++\n":
            top_matter.append(line)
        else:
            content.append(line)

    return toml.loads("".join(top_matter)), content


def convert_to_webp(start_path: str, filename: str, new_filename: str):
    try_run_cmd(["magick", "-quality", "50", filename, new_filename], start_path)


def try_run_cmd(cmds: list[str], cwd: str) -> tuple[str | None, str]:
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
    outputs = []
    for cmd in commands:
        output, error = try_run_cmd(cmd, cwd)
        # print(f"command was: {cmd}")
        # print(f"output was: {output}")
        # print(f"error was: {error}")
        if not null_or_empty(error):
            # print(f"ending with {cmd}, {error}")
            return str(error)
        else:
            outputs.append(output)
    return "\n".join(outputs)


def git_commit(cwd: str, msg: str) -> tuple[str | None, str | None]:
    commands = [
        ["git", "config", "user.name", "Micropub Bot"],
        ["git", "config", "user.email", "acbilson@gmail.com"],
        ["git", "add", "-v", "."],
        ["git", "commit", "-m", f"{msg}"],
        ["git", "push"],
    ]
    outputs = []
    for cmd in commands:
        # print(f"command was: {cmd} at {cwd}")
        output, error = try_run_cmd(cmd, cwd)
        # print(f"output was: {output}")
        # print(f"error was: {error}")
        if not null_or_empty(error):
            # print(f"ending with {cmd}, {error}")
            return None, str(error)
        else:
            outputs.append(output)
    return "\n".join(outputs), None
