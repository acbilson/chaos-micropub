from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    StringField,
    HiddenField,
)
from wtforms.widgets import TextArea
from wtforms.validators import (
    InputRequired,
    Length,
)


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
