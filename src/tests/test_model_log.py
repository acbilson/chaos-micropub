import unittest
from app.micropub.models import Log


class LogTests(unittest.TestCase):
    def test_model_composes(self):
        expected = """+++
author = "Alex Bilson"
date = "2021-09-23T18:53:39.240457"
+++
Test Content"""

        log = Log(
            base_path="/path/here",
            date="2021-09-23T18:53:39.240457",
            author="Alex Bilson",
            content="Test Content",
        )
        result = log.compose()
        self.assertEqual(expected, result)
