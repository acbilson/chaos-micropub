from flask import Blueprint, request, render_template, url_for, redirect, session, Response
from flask_dance.contrib.github import github
from flask import current_app as app
from pathlib import Path
import sys
import pwd
import grp
import os
import subprocess
import re
from datetime import datetime

# blueprint configuration
micropub_bp = Blueprint("micropub_bp", __name__)


@micropub_bp.route("/healthcheck", methods=["GET"])
def health():
  return Response(status=200)


@micropub_bp.route("/", methods=["GET", "POST"])
def create():
  if request.method == "GET":
    if not app.debug and not github.authorized:
      return redirect(url_for("github.login"))
    else:
      return render_template('create.html',
        style=url_for("static", filename="css/micropub.css"),
        normalize_style=url_for("static", filename="css/normalize.css"),
        create_route=url_for("micropub_bp.create"),
        script=url_for("static", filename="js/micropub.js")
      )
  else:
    if not app.debug and not github.authorized:
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

      comments = ''
      if "comments" in request.form and request.form["comments"] == 'on':
        comments = 'comments = true'

      new_file_path = Path(f"/mnt/chaos/content/comments/{filename}.md")
      content = f"""+++
categories = ["{category}"]
date = "{date}"
tags = [{tags}]
{comments}
+++
{request.form['content']}
      """

      with open(new_file_path, "x") as f:
        f.write(content)

      run_build_script(new_file_path)

      return redirect(app.config["SITE"])


def run_build_script(file_path):
  try:
    cmd = ["/usr/local/bin/build-site.sh", f"{file_path}"]
    completed_proc = subprocess.run(
      cmd,
      shell=False,
      stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT,
      universal_newlines=True
    )
    if completed_proc.returncode < 0:
      print(
        "Child was terminated by signal",
        -completed_proc.returncode,
        file=sys.stderr,
      )
    else:
      print("Child returned: ", completed_proc.returncode, file=sys.stderr)
      print("Script returned: ")
      print(completed_proc.stdout, file=sys.stderr)
  except OSError as e:
    print("Execution failed:", e, file=sys.stderr)


def parse_to_list(text):
  return '"' + '","'.join(text.split(" ")) + '"'
