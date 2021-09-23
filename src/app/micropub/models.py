from os import path
from datetime import datetime


class LogFile():

  def __init__(self, path, form, user):
    self.path = path
    self.body = form.content.data
    self.timestamp = datetime.fromisoformat(form.current_date.data) if form.current_date.data else None
    self.date = self.timestamp.isoformat()
    self.filename = self.timestamp.strftime("%Y%m%d-%H%M%S")
    self.user = "Alex Bilson" if (user == "acbilson" or user == "Alexander Bilson") else user
    self.content = self.compose()

  def save(self):
    save_path = path.join(self.path, f"{self.filename}.md")
    with open(save_path, "x") as f:
        f.write(self.content)

  def compose(self):
    return f"""+++
author = "{self.user}"
date = "{self.date}"
+++
{self.body}"""


class NoteFile():

  def __init__(self, path, form, user):
    self.path = path
    self.body = form.content.data
    self.timestamp = datetime.fromisoformat(form.current_date.data) if form.current_date.data else None
    self.date = self.timestamp.isoformat()
    self.user = "Alex Bilson" if (user == "acbilson" or user == "Alexander Bilson") else user
    self.title = form.title.data
    self.filename = self.title.lower().replace(" ", "-")
    self.tags = '"' + '","'.join(form.tags.data.split(" ")) + '"'
    self.comments = "true" if form.comments.data == "on" else "false"
    self.content = self.compose()

  def save(self):
    save_path = path.join(self.path, f"{self.filename}.md")
    with open(save_path, "x") as f:
        f.write(self.content)
    return save_path

  def compose(self):
    return f"""+++
author = "{self.user}"
comments = {self.comments}
date = "{self.date}"
epistemic = "seedling"
tags = [{self.tags}]
title = "{self.title}"
+++
{self.body}"""
