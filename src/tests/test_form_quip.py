import unittest
from datetime import datetime
from app.quip.forms import QuipForm
from base_test import BaseTest


class QuipFormTests(BaseTest):
    def test_form_missing_content(self):
        with self.app.app_context():
            form = QuipForm()
            form.current_date.data = datetime.now()
            self.assertFalse(form.validate())
            self.assertEqual(form.errors.get("content"), ["No content entered"])


if __name__ == "__main__":
    unittest.main()
