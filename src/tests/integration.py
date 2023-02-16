import unittest
import base64
import subprocess
from subprocess import CalledProcessError
import os
from os import environ
import json
from io import BytesIO
from http import HTTPStatus
from flask import Flask
from app.config import LocalTestConfig, DockerTestConfig
from app import create_app
from app.operators import try_run_cmd

if environ.get("IS_DOCKER"):
    CONTENT_PATH = DockerTestConfig.CONTENT_PATH
    REPO_PATH = DockerTestConfig.REPO_PATH
    IMAGE_PATH = DockerTestConfig.IMAGE_PATH
else:
    CONTENT_PATH = LocalTestConfig.CONTENT_PATH
    REPO_PATH = LocalTestConfig.REPO_PATH
    IMAGE_PATH = LocalTestConfig.IMAGE_PATH

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
        os.makedirs(REPO_PATH)
        try_run_cmd(["git", "init", "--bare"], REPO_PATH)

        # clones content from bare origin
        try_run_cmd(["git", "clone", REPO_PATH, CONTENT_PATH], ".")

        # creates image storage location
        os.makedirs(IMAGE_PATH)

        # creates a few test files
        content = (
            '+++\nauthor = "Alex Bilson"\n+++\nThis is some test content to read\n'
        )
        with open(os.path.join(CONTENT_PATH, READ_FILE), "w") as f:
            f.write(content)

        content = (
            '+++\nauthor = "Alex Bilson"\n+++\nThis is some test content to update\n'
        )
        with open(os.path.join(CONTENT_PATH, UPDATE_FILE), "w") as f:
            f.write(content)

        # commits my files to origin
        try_run_cmd(["git", "add", "-v", "."], CONTENT_PATH)
        try_run_cmd(["git", "commit", "-m", f'"adds initial files"'], CONTENT_PATH)
        try_run_cmd(["git", "push"], CONTENT_PATH)

    def tearDown(self):
        try_run_cmd(["rm", "-rf", CONTENT_PATH], ".")
        try_run_cmd(["rm", "-rf", REPO_PATH], ".")
        try_run_cmd(["rm", "-rf", IMAGE_PATH], ".")


class ReadTests(InitializeRepo):
    def setUp(self):
        super().setUp()
        self.app = create_app(
            DockerTestConfig if environ.get("IS_DOCKER") else LocalTestConfig
        )
        self.client = self.app.test_client()

    def test_read_returns_correct_json(self):
        file_path = READ_FILE.split(".")[0]
        response = self.client.get(f"/file?path={file_path}")

        # assert
        self.assertEqual(HTTPStatus.OK, response.status_code)
        data = response.json
        self.assertTrue(data.get("success"), data.get("message"))

        content = data.get("content")
        front_matter, body = content.get("frontmatter"), content.get("body")

        self.assertEqual(file_path, content.get("path"))
        self.assertIn("test content to read", content.get("body"))
        self.assertIn("author", content.get("frontmatter"))


class UpdateTests(InitializeRepo):
    def setUp(self):
        super().setUp()
        self.app = create_app(
            DockerTestConfig if environ.get("IS_DOCKER") else LocalTestConfig
        )
        self.client = self.app.test_client()

    def test_update_returns_correct_json(self):
        file_path = UPDATE_FILE.split(".")[0]
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
        self.app = create_app(
            DockerTestConfig if environ.get("IS_DOCKER") else LocalTestConfig
        )
        self.client = self.app.test_client()

    def test_create_returns_correct_json(self):
        file_path = CREATE_FILE.split(".")[0]
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

    def test_create_with_file_appends_caption(self):
        file_path = CREATE_FILE.split(".")[0]
        new_front_matter = dict(
            author="Gerry Witte",
            photoSrc="http://images.alexbilson.dev/photo.webp",
            photoAlt="Alternative text for my photo",
            photoCaption="A test photo caption",
        )
        new_content = "This is the content of my new file"
        body = dict(path=file_path, body=new_content, frontmatter=new_front_matter)
        response = self.client.post(f"/file", json=body)

        # assert
        self.assertEqual(HTTPStatus.OK, response.status_code)
        data = response.json
        self.assertTrue(data.get("success"), data.get("message"))

        content = data.get("content")
        front_matter, body = content.get("frontmatter"), content.get("body")

        import pdb

        pdb.set_trace()
        self.assertEqual(file_path, content.get("path"))
        self.assertIsNotNone(body)
        self.assertIsNotNone(front_matter)
        self.assertIn("{{< caption", body)
        self.assertIn(f"caption=\"{new_front_matter.get('photoCaption')}\"", body)
        self.assertIn(f"alt=\"{new_front_matter.get('photoAlt')}\"", body)
        self.assertIn(f"src=\"{new_front_matter.get('photoSrc')}\"", body)

    def test_create_file_saves_to_path(self):
        filename = "photo.heic"
        with open(
            f"/Users/alexbilson/source/chaos-micropub/src/tests/test_data/{filename}",
            "rb",
        ) as f:
            file_content = BytesIO(f.read())
        data = dict(photo=(file_content, filename))
        response = self.client.post(
            "/photo", content_type="multipart/form-data", buffered=True, data=data
        )

        # assert
        self.assertEqual(HTTPStatus.OK, response.status_code)
        data = response.json
        self.assertTrue(data.get("success"), data.get("message"))
        new_filename = data.get("content").get("filename")
        self.assertEqual("photo.webp", new_filename)
        # ensures original is removed
        self.assertFalse(os.path.exists(os.path.join(IMAGE_PATH, filename)))


class AuthTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            DockerTestConfig if environ.get("IS_DOCKER") else LocalTestConfig
        )
        self.client = self.app.test_client()

    def test_basic_login_returns_token(self):
        creds = base64.b64encode(
            b"{TestConfig.ADMIN_USER}:{TestConfig.ADMIN_PASSWORD}"
        ).decode("utf-8")

        response = self.client.get(
            "/token", headers=dict(Authorization=f"Basic {creds}")
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIn("token", response.json)

    def test_auth_token_returns_ok(self):
        creds = base64.b64encode(
            b"{TestConfig.ADMIN_USER}:{TestConfig.ADMIN_PASSWORD}"
        ).decode("utf-8")
        token_resp = self.client.get(
            "/token", headers=dict(Authorization=f"Basic {creds}")
        )
        token = token_resp.json.get("token")

        response = self.client.get(
            "/auth", headers=dict(Authorization=f"Bearer {token}")
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
