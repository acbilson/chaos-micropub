import toml
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
    ValidationError
)


class LogForm(FlaskForm):
    author = StringField("Author:")
    content = StringField(
        "Content",
        widget=TextArea(),
        validators=[InputRequired(message="No content entered")],
    )
    logname = StringField("Log Name")

    current_date = HiddenField("Current Date")
    aliases = HiddenField("Aliases")
    submit = SubmitField("Publish!")

    def validate_aliases(form, field):
        if field.data is None or field.data == "":
            return None
        try:
            toml.loads(f"aliases = {field.data}")
        except:
            raise ValidationError("Invalid TOML syntax")


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
