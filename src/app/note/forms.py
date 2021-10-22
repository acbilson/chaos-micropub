from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    StringField,
    SelectField,
    HiddenField,
    BooleanField,
)
from wtforms.widgets import TextArea
from wtforms.validators import (
    InputRequired,
)


class NoteForm(FlaskForm):
    content = StringField(
        "Content",
        widget=TextArea(),
        validators=[InputRequired(message="No content entered")],
    )
    author = StringField("Author:")
    title = StringField(
        "Title:", validators=[InputRequired(message="No title entered")]
    )
    tags = StringField("Tags:", validators=[InputRequired(message="No tags entered")])
    epistemic = StringField("Epistemic:")
    backlinks = StringField("Backlinks:")
    comments = BooleanField("Allow Comments?")
    notename = StringField("Note Name:")
    current_date = StringField("Published:")
    modified_date = StringField("Last Edited:")
    aliases = HiddenField("Aliases")
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
