from flask import Blueprint, request, render_template, url_for, redirect, session, Response
from flask_dance.contrib.github import github
from flask import current_app as app
from pathlib import Path
import sys
import os
import subprocess
import re
from datetime import datetime

# blueprint configuration
micropub_bp = Blueprint("micropub_bp", __name__)


@micropub_bp.route("/health", methods=["GET"])
def health():
  return Response(status=200)


@micropub_bp.route("/test", methods=["GET"])
def test():
  if not github.authorized:
    return redirect(url_for("github.login"))
  resp = github.get("/user")
  assert resp.ok
  return "You are @{login} on GitHub".format(login=resp.json()["login"])


@micropub_bp.route("/", methods=["GET", "POST"])
def create():
  if request.method == "GET":
    if not github.authorized:
      return redirect(url_for("github.login"))
    else:
      return render_template('create.html',
        style=url_for("static", filename="css/micropub.css"),
        normalize_style=url_for("static", filename="css/normalize.css"),
        create_route=url_for("micropub_bp.create"),
        script=url_for("static", filename="js/micropub.js")
      )
  else:
    if not github.authorized:
      return redirect(url_for("github.login"))
    else:
      if "content" not in request.form:
        return "no content was passed to this endpoint. aborting."
      if "current_date" not in request.form:
        return "no date was passed to this endpoint. aborting."

      now = datetime.fromisoformat(request.form["current_date"])
      filename = now.strftime("%Y%m%d-%H%M%S")
      date = now.isoformat()

      category = "personal"

      if "category" in request.form:
        category = request.form["category"]

      tags = ""

      if "tags" in request.form:
        tags = parse_to_list(request.form["tags"])

      new_file_path = Path(f"{app.config['CONTENT_PATH']}/comments/{filename}.md")
      content = f"""+++
categories = ["{category}"]
date = "{date}"
tags = [{tags}]
+++
{request.form['content']}
      """

      with open(new_file_path, "x") as f:
        f.write(content)

      run_deploy_script(filename)

      return redirect(app.config["SITE"])


def run_deploy_script(filename):
  try:
    cmd = f"{app.config['DEPLOY_FILE']} {filename}.md"
    completed_proc = subprocess.run(
      cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    if completed_proc.returncode < 0:
      print(
        "Child was terminated by signal",
        -completed_proc.returncode,
        file=sys.stderr,
      )
    else:
      print("Child returned: ", completed_proc.returncode, file=sys.stderr)
      print("Script returned: ", completed_proc.stdout, file=sys.stderr)
  except OSError as e:
    print("Execution failed:", e, file=sys.stderr)


def parse_to_list(text):
  return '"' + '","'.join(text.split(" ")) + '"'
