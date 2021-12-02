import unittest
from pathlib import Path
from app.note.models import Note


class NoteTests(unittest.TestCase):
    def test_model_composes(self):
        expected = """+++
author = "Alex Bilson"
backlinks = []
comments = true
date = "2021-09-23T18:53:39.240457"
epistemic = "seedling"
lastmod = "2021-09-23T18:53:39.240457"
tags = [ "fake", "tag",]
title = "Test Title"
+++
Test Content"""

        note = Note(
            base_path="/path/here",
            filename="test-title.md",
            aliases=None,
            backlinks="[]",
            tags="['fake', 'tag']",
            title="Test Title",
            date="2021-09-23T18:53:39.240457",
            lastmod="2021-09-23T18:53:39.240457",
            epistemic="seedling",
            author="Alex Bilson",
            content="Test Content",
            comments=True,
        )
        result = note.compose()
        self.assertEqual(expected, result)

    def test_model_path(self):
        expected = Path("/path/here/notes/test-title.md")
        note = Note(
            base_path="/path/here",
            filename="test-title.md",
            aliases=None,
            backlinks="[]",
            tags="['fake', 'tag']",
            title="Test Title",
            date="2021-09-23T18:53:39.240457",
            lastmod="2021-09-23T18:53:39.240457",
            epistemic="seedling",
            author="Alex Bilson",
            content="Test Content",
            comments=True,
        )
        self.assertEqual(expected, note.path)
