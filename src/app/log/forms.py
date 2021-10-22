from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    SelectField,
    StringField,
    HiddenField,
)
from wtforms.widgets import TextArea
from wtforms.validators import (
    InputRequired,
    Length,
)


class LogForm(FlaskForm):
    author = StringField("Author:")
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


class LogSelectionForm(FlaskForm):
    selected_log = SelectField(
        "Select Log",
        coerce=str,
        validators=[InputRequired(message="no log selected")],
    )
    submit = SubmitField("Load Log")

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
