from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    RadioField,
)


class LoginForm(FlaskForm):
    action = RadioField(
        "Action",
        choices=[
            ("github.login", "Github"),
            ("google.login", "Google"),
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
            ("log_bp.select_log", "Edit Log"),
            ("note_bp.create_note", "Create Note"),
            ("note_bp.select_note", "Edit Note"),
        ],
    )
    submit = SubmitField("Select")

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
