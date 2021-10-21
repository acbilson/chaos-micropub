import unittest
from unittest import mock
from datetime import datetime
from flask import Flask
from app import create_app
from app.config import TestConfig
from app.micropub import views


class CreateLogTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig).test_client()

    def test_create_log_missing_request_data(self):
        bodies = [
            dict(),
            dict(content="a fake post here"),
        ]

        for body in bodies:
            resp = self.app.post("/", data=body)
            self.assertEqual(resp.status, "400 BAD REQUEST")

    @mock.patch("app.micropub.models.LogFile.save")
    @mock.patch("app.micropub.scripthelper.run_build_script")
    def test_create_log_file_output(self, mock_open, mock_sp):
        # setup
        data = dict(
            content="a fake post here",
            current_date="2021-01-01T12:12:12",
        )
        resp = self.app.post("/create/log", data=data)
        self.assertEqual(resp.status, "302 FOUND", resp.data)
        self.assertEqual(resp.location, TestConfig.SITE)


if __name__ == "__main__":
    unittest.main()
