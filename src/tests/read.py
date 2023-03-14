from os import environ
from http import HTTPStatus
from app.config import LocalTestConfig, DockerTestConfig
from app import create_app

from .base import InitializeRepo, READ_FILE


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
