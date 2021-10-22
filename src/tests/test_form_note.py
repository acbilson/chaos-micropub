import unittest
from datetime import datetime
from app.micropub.forms import NoteForm
from base_test import BaseTest


class NoteFormTests(BaseTest):
    def get_filled_form(self):
        form = NoteForm()
        form.content = "Some test content"
        form.title = "Some Title"
        form.tags = "fake tag"
        form.comments = True
        return form

    def test_form_fails_validation(self):
        missing_fields = [
            ("content", "No content entered"),
            ("title", "No title entered"),
            ("tags", "No tags entered"),
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
