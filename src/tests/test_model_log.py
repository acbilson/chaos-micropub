import unittest
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
