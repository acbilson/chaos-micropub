from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length


class LogForm(Form):
    content = StringField("content", validators=[InputRequired(message="No content entered")])
    current_date = StringField(
        "current_date", validators=[Length(min=1, max=25)]
    )

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.timestamp = self.get_timestamp()

    def get_timestamp(self):
        if self.current_date:
            return datetime.fromisoformat(self.current_date.data)
        else:
            return None
