import unittest
from unittest.mock import create_autospec
from pathlib import Path
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import Field
from app.micropub.models import NoteFile
from helpers import mock_field


class NoteFileTests(unittest.TestCase):
    def setUp(self):
        self.form = create_autospec(FlaskForm)
        self.form.content = mock_field(Field, "Test content")
        self.form.current_date = mock_field(Field, "2021-09-23T18:53:39.240457")
        self.form.title = mock_field(Field, "Test Title")
        self.form.tags = mock_field(Field, "fake tags")
        self.form.comments = mock_field(Field, "on")

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

        model = NoteFile("/path/here", self.form, "acbilson")
        content = model.compose()
        self.assertEqual(content, expected)

    def test_model_builds_path(self):
        expected = Path("/path/here/test-title.md")
        model = NoteFile("/path/here", self.form, "acbilson")
        self.assertEqual(model.path, expected)


if __name__ == "__main__":
    unittest.main()
