import unittest
from datetime import datetime
from flask_wtf import Form
from flask import Flask
from app import create_app
from app.micropub.forms import LogForm

class LogFormTests(unittest.TestCase):
    def setUp(self):
      app = create_app()
      app.config["WTF_CSRF_ENABLED"] = False
      self.app = app

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
