from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    RadioField,
    SelectField,
)
from wtforms.widgets import TextArea
from wtforms.validators import (
    InputRequired,
    Length,
    AnyOf,
)


class LoginForm(FlaskForm):
    option = StringField(
        "option",
        validators=[
            InputRequired(message="Must select a login option"),
            AnyOf(["github", "google"], message="This login option is not supported"),
        ],
    )

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)


class CreateForm(FlaskForm):
    post_type = RadioField("post-type", choices=[("log", "Log"), ("note", "Note")])

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)


class LogForm(FlaskForm):
    content = StringField(
        "content", validators=[InputRequired(message="No content entered")]
    )
    current_date = StringField(
        "current_date", validators=[Length(min=1, max=25, message="No date entered")]
    )

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)


class NoteForm(FlaskForm):
    content = StringField(
        "content",
        widget=TextArea(),
        validators=[InputRequired(message="No content entered")],
    )
    current_date = StringField(
        "current_date", validators=[Length(min=1, max=25, message="No date entered")]
    )
    title = StringField("title", validators=[InputRequired(message="No title entered")])
    tags = StringField("tags", validators=[InputRequired(message="No tags entered")])
    comments = StringField(
        "comments", validators=[InputRequired(message="Comment data missing")]
    )

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)


class NoteSelectionForm(FlaskForm):
    selected_note = SelectField(
        "Select Note",
        coerce=str,
        validators=[InputRequired(message="no note selected")],
    )

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
