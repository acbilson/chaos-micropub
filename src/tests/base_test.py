import unittest
from app import create_app
from app.config import TestConfig


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.client = self.app.test_client()