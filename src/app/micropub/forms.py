from datetime import datetime
from flask_wtf import Form
from wtforms import (
  StringField,
  PasswordField,
  BooleanField,
)
from wtforms.validators import (
  InputRequired,
  Length,
  AnyOf,
)


class LoginForm(Form):
    option = StringField("option", validators=[
        InputRequired(message="Must select a login option"),
        AnyOf(["github", "google"], message="This login option is not supported")
      ])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


class LogForm(Form):
    content = StringField("content", validators=[InputRequired(message="No content entered")])
    current_date = StringField("current_date", validators=[Length(min=1, max=25)])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


class NoteForm(Form):
    content = StringField("content", validators=[InputRequired(message="No content entered")])
    current_date = StringField("current_date", validators=[Length(min=1, max=25)])
    title = StringField("title", validators=[InputRequired(message="No title entered")])
    tags = StringField("tags", validators=[InputRequired(message="No tags entered")])
    comments = StringField("comments", validators=[InputRequired(message="Comment data missing")])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

