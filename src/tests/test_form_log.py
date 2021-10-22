import unittest
from datetime import datetime
from app.micropub.forms import LogForm
from base_test import BaseTest


class LogFormTests(BaseTest):
    def test_form_missing_content(self):
        with self.app.app_context():
            form = LogForm()
            form.current_date = datetime.now()
            self.assertFalse(form.validate())
            self.assertEqual(form.errors["content"], ["No content entered"])

    def test_form_missing_date(self):
        with self.app.app_context():
            form = LogForm()
            form.content = "some test content"
            self.assertFalse(form.validate())
            self.assertEqual(form.errors["current_date"], ["No date entered"])


if __name__ == "__main__":
    unittest.main()
