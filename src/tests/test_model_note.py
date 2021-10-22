import unittest
from app.micropub.models import Note


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
            backlinks=[],
            tags=["fake", "tag"],
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
