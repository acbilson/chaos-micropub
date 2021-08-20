import unittest
from flask import Flask
from app import create_app

class LoginTests(unittest.TestCase):

  def setUp(self):
    self.app = create_app().test_client()

  def test_login_unsupported(self):
    resp = self.app.put("/login")
    self.assertEqual(resp.status, "405 METHOD NOT ALLOWED")

if __name__ == "__main__":
  unittest.main()
