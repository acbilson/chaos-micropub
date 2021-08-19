import unittest
from unittest import mock
from datetime import datetime
from flask import Flask
from app import create_app

class CreateLogTests(unittest.TestCase):

  def setUp(self):
    self.app = create_app().test_client()

  def test_create_log_missing_request_data(self):
    bodies = [
      dict(),
      dict(post_type="log"),
      dict(post_type="log",content="a fake post here"),
    ]

    for body in bodies:
      resp = self.app.post("/", data=body)
      self.assertEqual(resp.status, "400 BAD REQUEST")

  @mock.patch("app.open")
  @mock.patch("subprocess.run")
  def test_create_log_file_output(self, mock_open, mock_run):
    # setup
    data = dict(post_type="log",content="a fake post here",current_date="2021-01-01T12:12:12")
    pm = mock.Mock()
    pm.returncode = 1
    mock_run.return_value = pm

    resp = self.app.post("/", data=data)

  def _get_process_mock(self):
    process_mock = mock.Mock()
    process_mock.returncode.return_value = 1
    return process_mock

if __name__ == "__main__":
  unittest.main()
