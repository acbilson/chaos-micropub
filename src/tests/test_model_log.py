import unittest
from pathlib import Path
from app.log.models import Log


class LogTests(unittest.TestCase):
    def test_model_composes(self):
        expected = """+++
author = "Alex Bilson"
date = "2021-09-23T18:53:39.240457"
lastmod = "2021-09-23T18:53:39.240457"
aliases = [ "/note/example/alias",]
+++
Test Content"""

        log = Log(
            base_path="/path/here",
            filename="20210923.md",
            aliases=["/note/example/alias"],
            date="2021-09-23T18:53:39.240457",
            lastmod="2021-09-23T18:53:39.240457",
            author="Alex Bilson",
            content="Test Content",
        )
        result = log.compose()
        self.assertEqual(expected, result)

    def test_model_path(self):
        expected = Path("/path/here/logs/2021/09/20210923.md")
        log = Log(
            base_path="/path/here",
            filename="20210923.md",
            aliases=["/note/example/alias"],
            date="2021-09-23T18:53:39.240457",
            lastmod="2021-09-23T18:53:39.240457",
            author="Alex Bilson",
            content="Test Content",
        )
        self.assertEqual(expected, log.path)
