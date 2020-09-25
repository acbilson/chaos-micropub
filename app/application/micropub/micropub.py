from flask import Blueprint, request, url_for, redirect, session
from flask import current_app as app
from pathlib import Path
import os
import re
from datetime import datetime

# blueprint configuration
micropub_bp = Blueprint('micropub_bp', __name__)

@micropub_bp.route('/', methods=['GET'])
def health():
    return 'Alive!'

@micropub_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        if 'access_token' not in session:
            return redirect(url_for('auth_bp.login'))

        return """
<!DOCTYPE html>
<html>
  <body>
    <form action="{}" method="POST" style="display: flex; flex-flow: column wrap;">

      <div>
          <input type="radio" name="category" value="personal">Personal</input>
          <input type="radio" name="category" value="spiritual">Spiritual</input>
          <input type="radio" name="category" value="business">Business</input>
          <input type="radio" name="category" value="technology">Technology</input>
          <input type="radio" name="category" value="resources">Resources</input>
      </div>

      <label for="tags">Tags:</label>
      <input type="text" name="tags">

      <label for="content">Content:</label>
      <textarea name="content" rows=20></textarea>

      <input id="date" type="text" name="current_date" value="" hidden>

      <button type="submit">Publish</button>
    </form>
      <script type="text/javascript" src="{}"></script>
  </body>
</html>
        """.format(url_for('micropub_bp.create'), url_for('static', filename='js/micropub.js'))
    else:
        if 'access_token' not in session:
            return redirect(url_for('auth_bp.login'))
        if 'content' not in request.form:
            return "no content was passed to this endpoint. aborting."
        if 'current_date' not in request.form:
            return "no date was passed to this endpoint. aborting."

        now = datetime.fromisoformat(request.form['current_date'])
        filename = now.strftime('%Y%m%d-%H%M%S')
        date = now.isoformat()

        category = 'personal'

        if 'category' in request.form:
            category = request.form['category']

        tags = ''

        if 'tags' in request.form:
            tags = parse_to_list(request.form['tags'])

        new_file_path = Path(f"{app.config['CONTENT_PATH']}/{filename}.md")
        content = f"""+++
categories = ["{category}"]
date = "{date}"
tags = [{tags}]
+++
{request.form['content']}
               """

        with open(new_file_path, 'x') as f:
            f.write(content)

        cmd = f"{app.config['DEPLOY_FILE']} {filename}.md"
        output = os.system(cmd)

        return redirect(app.config['HOME'])

def parse_to_list(text):
    return "\""+'","'.join(text.split(' '))+"\""
