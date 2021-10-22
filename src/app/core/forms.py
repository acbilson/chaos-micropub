from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    RadioField,
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
            ("log_bp.create_log", "Create Log"),
            ("note_bp.create_note", "Create Note"),
            ("note_bp.select_note", "Edit Note"),
        ],
    )
    submit = SubmitField("Select")

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
