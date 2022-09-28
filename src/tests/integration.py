import unittest
import subprocess
import os
import json
from http import HTTPStatus
from flask import Flask
from app.config import TestConfig
from app import create_app

TEST_DIR = "/Users/alexbilson/temp/test_dir"

def run_cmd(cmds):
    output = subprocess.run(cmds, capture_output=True, check=True)
    return output.stdout.decode()

class BasicTests(unittest.TestCase):
    def test_create_app(self):
        app = create_app()
        self.assertEqual(type(app), Flask)

    def test_healthcheck(self):
        app = create_app().test_client()
        resp = app.get("/healthcheck")
        self.assertEqual(resp.status, "200 OK")


class ReadTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        # create file to read
        os.makedirs(TEST_DIR)
        self.file_path = os.path.join(TEST_DIR, "test_file")
        self.file_content = (
            '+++\nauthor = "Alex Bilson"\n+++\nThis is some test content\n'
        )
        with open(f"{self.file_path}.md", "w") as f:
            f.write(self.file_content)

    def test_read_returns_correct_json(self):
        response = self.client.get(f"/file?path={self.file_path}")
        self.assertEqual(HTTPStatus.OK, response.status_code)
        data = response.json
        self.assertTrue(data.get("success"), data.get("message"))
        result = data.get("result")
        self.assertEqual(result.get("content"), self.file_content)

    def tearDown(self):
        run_cmd(["rm", "-rf", TEST_DIR])

class UpdateTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        # add folder and git init
        os.makedirs(TEST_DIR)
        run_cmd(["git", "init", TEST_DIR])

        # creates a test file and adds it
        self.file_path = os.path.join(TEST_DIR, "test_file")
        self.file_content = (
            '+++\nauthor = "Alex Bilson"\n+++\nThis is some test content\n'
        )
        with open(f"{self.file_path}.md", "w") as f:
            f.write(self.file_content)

        run_cmd(["git", "add", "."])
        run_cmd(["git", "commit", "-m", "adds a file to update"])

    def test_update_returns_correct_json(self):
        body = dict(options=dict(filepath=self.file_path), content="This is new test content")
        response = self.client.put(f"/file", json=body)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        print(response)
        data = response.json
        self.assertTrue(data.get("success"), data.get("message"))
        result = data.get("result")
        self.assertEqual(result.get("content"), self.file_content)

    def tearDown(self):
        run_cmd(["rm", "-rf", TEST_DIR])
