import unittest
from pathlib import Path
from app.quip.models import Quip


class QuipTests(unittest.TestCase):
    def test_model_composes(self):
        expected = """+++
author = "Alex Bilson"
date = "2021-09-23T18:53:39.240457"
lastmod = "2021-09-23T18:53:39.240457"
aliases = [ "/note/example/alias",]
+++
Test Content"""

        quip = Quip(
            base_path="/path/here",
            filename="20211229-212916.md",
            aliases=["/note/example/alias"],
            date="2021-09-23T18:53:39.240457",
            lastmod="2021-09-23T18:53:39.240457",
            author="Alex Bilson",
            content="Test Content",
        )
        result = quip.compose()
        self.assertEqual(expected, result)

    def test_model_path(self):
        expected = Path("/path/here/quips/20211229-212916.md")
        quip = Quip(
            base_path="/path/here",
            filename="20211229-212916.md",
            aliases=["/note/example/alias"],
            date="2021-09-23T18:53:39.240457",
            lastmod="2021-09-23T18:53:39.240457",
            author="Alex Bilson",
            content="Test Content",
        )
        self.assertEqual(expected, quip.path)
