import unittest
import base64
from os import environ
from http import HTTPStatus
from app.config import LocalTestConfig, DockerTestConfig
from app import create_app


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
