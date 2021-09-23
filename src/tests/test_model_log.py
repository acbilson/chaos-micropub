import unittest
from unittest.mock import create_autospec
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import Field
from app.micropub.models import LogFile
from helpers import mock_field


class LogFileTests(unittest.TestCase):
    def setUp(self):
      self.form = create_autospec(FlaskForm)
      self.form.content = mock_field(Field, "Test content")
      self.form.current_date = mock_field(Field, "2021-09-23T18:53:39.240457")

    def test_model_composes_file(self):
        expected = """+++
author = "Alex Bilson"
date = "2021-09-23T18:53:39.240457"
+++
Test content"""
        model = LogFile("a/path/here", self.form, "acbilson")
        content = model.compose()
        self.assertEqual(content, expected)

if __name__ == "__main__":
    unittest.main()
