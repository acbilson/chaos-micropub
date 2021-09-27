import unittest
from datetime import datetime
from flask import Flask
from app import create_app


class CreateTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_create_unsupported(self):
        resp = self.app.put("/")
        self.assertEqual(resp.status, "405 METHOD NOT ALLOWED")

    def test_create_entry(self):
        resp = self.app.get("/")
        self.assertEqual(resp.status, "200 OK")
        self.assertEqual(resp.content_type, "text/html; charset=utf-8")
        self.assertGreater(resp.content_length, 0)


if __name__ == "__main__":
    unittest.main()
