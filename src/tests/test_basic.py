import unittest
from flask import Flask
from app import create_app


class BasicTests(unittest.TestCase):
    def test_create_app(self):
        app = create_app()
        self.assertEqual(type(app), Flask)

    def test_healthcheck(self):
        app = create_app().test_client()
        resp = app.get("/healthcheck")
        self.assertEqual(resp.status, "200 OK")


if __name__ == "__main__":
    unittest.main()
