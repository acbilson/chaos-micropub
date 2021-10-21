import unittest
from datetime import datetime
from flask_wtf import Form
from flask import Flask
from app import create_app
from app.micropub.forms import NoteForm


class NoteFormTests(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config["WTF_CSRF_ENABLED"] = False
        self.app = app

    def get_filled_form(self):
        form = NoteForm()
        form.content = "Some test content"
        form.current_date = datetime.now()
        form.title = "Some Title"
        form.tags = "fake tag"
        form.comments = "on"
        return form

    def test_form_fails_validation(self):
        missing_fields = [
            ("content", "No content entered"),
            ("current_date", "No date entered"),
            ("title", "No title entered"),
            ("tags", "No tags entered"),
            ("comments", "Comment data missing"),
        ]

        with self.app.app_context():
            for field in missing_fields:
                field_name, message = field

                form = self.get_filled_form()
                form[field_name].data = None

                self.assertFalse(form.validate())
                self.assertEqual(form.errors[field_name], [message])


if __name__ == "__main__":
    unittest.main()
