import unittest
import subprocess
from subprocess import CalledProcessError
import os
import json
from http import HTTPStatus
from flask import Flask
from app.config import TestConfig
from app import create_app
from app.operators import try_run_cmd

TEST_DIR = "test_dir"
TEST_DIR_ABS = os.path.join(TestConfig.CONTENT_PATH, TEST_DIR)
REPO_DIR_ABS = "/mnt/repo/test"
READ_FILE = "read_file.md"
UPDATE_FILE = "update_file.md"
CREATE_FILE = "create_file.md"


class BasicTests(unittest.TestCase):
    def test_create_app(self):
        app = create_app()
        self.assertEqual(type(app), Flask)

    def test_healthcheck(self):
        app = create_app().test_client()
        resp = app.get("/healthcheck")
        self.assertEqual(resp.status, "200 OK")


class InitializeRepo(unittest.TestCase):
    def setUp(self):
        # generate the origin repo
        os.makedirs(REPO_DIR_ABS)
        try_run_cmd(["git", "init", "--bare"], REPO_DIR_ABS)

        # clones content from bare origin
        try_run_cmd(["git", "clone", REPO_DIR_ABS, TestConfig.CONTENT_PATH], "/mnt")

        # creates a few test files
        os.makedirs(os.path.join(TestConfig.CONTENT_PATH, TEST_DIR))
        content = (
            '+++\nauthor = "Alex Bilson"\n+++\nThis is some test content to read\n'
        )
        with open(os.path.join(TestConfig.CONTENT_PATH, TEST_DIR, READ_FILE), "w") as f:
            f.write(content)

        content = (
            '+++\nauthor = "Alex Bilson"\n+++\nThis is some test content to update\n'
        )
        with open(
            os.path.join(TestConfig.CONTENT_PATH, TEST_DIR, UPDATE_FILE), "w"
        ) as f:
            f.write(content)

        # commits my files to origin
        try_run_cmd(["git", "add", "-v", "."], TestConfig.CONTENT_PATH)
        try_run_cmd(
            ["git", "commit", "-m", f'"adds initial files"'], TestConfig.CONTENT_PATH
        )
        try_run_cmd(["git", "push"], TestConfig.CONTENT_PATH)

    def tearDown(self):
        try_run_cmd(["rm", "-rf", TestConfig.CONTENT_PATH], "/mnt")
        try_run_cmd(["rm", "-rf", REPO_DIR_ABS], "/mnt")


class ReadTests(InitializeRepo):
    def setUp(self):
        super().setUp()
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

    def test_read_returns_correct_json(self):
        file_path = os.path.join(TEST_DIR, READ_FILE.split(".")[0])
        response = self.client.get(f"/file?path={file_path}")

        # assert
        self.assertEqual(HTTPStatus.OK, response.status_code)
        data = response.json
        self.assertTrue(data.get("success"), data.get("message"))

        content = data.get("content")
        front_matter, body = content.get("frontmatter"), content.get("body")

        self.assertEqual(file_path, content.get("filepath"))
        self.assertIn("test content to read", content.get("body"))
        self.assertIn("author", content.get("frontmatter"))


class UpdateTests(InitializeRepo):
    def setUp(self):
        super().setUp()
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

    def test_update_returns_correct_json(self):
        file_path = os.path.join(TEST_DIR, UPDATE_FILE.split(".")[0])
        new_front_matter = dict(author="Bob Wiley")
        new_content = "This is what I have updated the file to"
        body = dict(path=file_path, body=new_content, frontmatter=new_front_matter)
        response = self.client.put(f"/file", json=body)

        # assert
        self.assertEqual(HTTPStatus.OK, response.status_code)
        data = response.json
        self.assertTrue(data.get("success"), data.get("message"))

        content = data.get("content")
        front_matter, body = content.get("frontmatter"), content.get("body")

        self.assertEqual(file_path, content.get("path"))
        self.assertIsNotNone(body)
        self.assertIsNotNone(front_matter)
        self.assertIn("what I have updated", body)
        self.assertIn("Bob Wiley", front_matter.values())


class CreateTests(InitializeRepo):
    def setUp(self):
        super().setUp()
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

    def test_create_returns_correct_json(self):
        file_path = os.path.join(TEST_DIR, CREATE_FILE.split(".")[0])
        new_front_matter = dict(author="Gerry Witte")
        new_content = "This is the content of my new file"
        body = dict(path=file_path, body=new_content, frontmatter=new_front_matter)
        response = self.client.post(f"/file", json=body)

        # assert
        self.assertEqual(HTTPStatus.OK, response.status_code)
        data = response.json
        self.assertTrue(data.get("success"), data.get("message"))

        content = data.get("content")
        front_matter, body = content.get("frontmatter"), content.get("body")

        self.assertEqual(file_path, content.get("path"))
        self.assertIsNotNone(body)
        self.assertIsNotNone(front_matter)
        self.assertIn("content of my new file", body)
        self.assertIn("Gerry Witte", front_matter.values())
