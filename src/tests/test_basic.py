import os
import unittest

from flask import Flask
from app import create_app

class BasicTests(unittest.TestCase):

  def setUp(self):
    self.app = create_app()

  def test_create_app(self):
    self.assertEqual(type(self.app), Flask)

  def test_example(self):
    self.assertEqual(True, True)

if __name__ == "__main__":
  unittest.main()
