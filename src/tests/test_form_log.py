import unittest
from datetime import datetime
from app.log.forms import LogForm
from base_test import BaseTest


class LogFormTests(BaseTest):
    def test_form_missing_content(self):
        with self.app.app_context():
            form = LogForm()
            form.current_date.data = datetime.now()
            self.assertFalse(form.validate())
            self.assertEqual(form.errors.get("content"), ["No content entered"])

if __name__ == "__main__":
    unittest.main()
