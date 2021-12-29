import toml
from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    StringField,
    SelectField,
    HiddenField,
)
from wtforms.widgets import TextArea
from wtforms.validators import InputRequired, ValidationError


class QuipForm(FlaskForm):
    author = StringField("Author:")
    content = StringField(
        "Content",
        widget=TextArea(),
        validators=[InputRequired(message="No content entered")],
    )
    filename = StringField("File Name:")
    current_date = StringField("Published:")
    modified_date = StringField("Last Edited:")

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


class QuipSelectionForm(FlaskForm):
    selected_quip = SelectField(
        "Select Quip",
        coerce=str,
        validators=[InputRequired(message="no quip selected")],
    )
    submit = SubmitField("Load Quip")

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
