from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    StringField,
    RadioField,
    SelectField,
    HiddenField,
    BooleanField,
)
from wtforms.widgets import TextArea
from wtforms.validators import (
    InputRequired,
    Length,
    AnyOf,
)


class LoginForm(FlaskForm):
    option = RadioField(
        "Action",
        choices=[
            ("github", "Github"),
            ("google", "Google"),
        ],
    )
    submit = SubmitField("Login")

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)


class SelectForm(FlaskForm):
    action = RadioField(
        "Action",
        choices=[
            ("create_log", "Create Log"),
            ("create_note", "Create Note"),
            ("select_note", "Edit Note"),
        ],
    )
    submit = SubmitField("Select")

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)


class LogForm(FlaskForm):
    content = StringField(
        "Content",
        widget=TextArea(),
        validators=[InputRequired(message="No content entered")],
    )
    current_date = HiddenField(
        "Current Date", validators=[Length(min=1, max=25, message="No date entered")]
    )
    submit = SubmitField("Publish!")

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)


class NoteForm(FlaskForm):
    content = StringField(
        "Content",
        widget=TextArea(),
        validators=[InputRequired(message="No content entered")],
    )
    current_date = HiddenField("Current Date")
    modified_date = StringField("Modified Date")
    author = StringField("Author:")
    title = StringField(
        "Title:", validators=[InputRequired(message="No title entered")]
    )
    tags = StringField("Tags:", validators=[InputRequired(message="No tags entered")])
    epistemic = StringField("Epistemic:")
    backlinks = StringField("Backlinks:")
    comments = BooleanField("Allow Comments?")
    submit = SubmitField("Publish!")

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)


class NoteSelectionForm(FlaskForm):
    selected_note = SelectField(
        "Select Note",
        coerce=str,
        validators=[InputRequired(message="no note selected")],
    )
    submit = SubmitField("Load Note")

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
