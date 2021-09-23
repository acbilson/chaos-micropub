import unittest
from unittest.mock import create_autospec
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import Field
from app.micropub.models import NoteFile


class NoteFileTests(unittest.TestCase):
    def setUp(self):
      self.form = create_autospec(FlaskForm)

      self.form.content = create_autospec(Field)
      self.form.content.data = "Test content"

      self.form.current_date = create_autospec(Field)
      self.form.current_date.data = "2021-09-23T18:53:39.240457"

      self.form.title = create_autospec(Field)
      self.form.title.data = "Test Title"

      self.form.title = create_autospec(Field)
      self.form.title.data = "Test Title"

      self.form.tags = create_autospec(Field)
      self.form.tags.data = "fake tags"

      self.form.comments = create_autospec(Field)
      self.form.comments.data = "on"

    def test_model_composes_file(self):
        expected = """+++
author = "Alex Bilson"
comments = true
date = "2021-09-23T18:53:39.240457"
epistemic = "seedling"
tags = ["fake","tags"]
title = "Test Title"
+++
Test content"""

        model = NoteFile("a/path/here", self.form, "acbilson")
        content = model.compose()
        self.assertEqual(content, expected)


    def test_model_sets_filename(self):
        expected = "test-title"
        model = NoteFile("a/path/here", self.form, "acbilson")
        self.assertEqual(model.filename, expected)

if __name__ == "__main__":
    unittest.main()
