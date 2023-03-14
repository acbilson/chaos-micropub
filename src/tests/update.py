from os import environ
from http import HTTPStatus
from app.config import LocalTestConfig, DockerTestConfig
from app import create_app

from .base import InitializeRepo, UPDATE_FILE


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
