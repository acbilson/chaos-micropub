import unittest
from unittest import mock
from unittest.mock import Mock
from app.config import TestConfig
from base_test import BaseTest


class CreateQuipTests(BaseTest):
    def test_create_quip_missing_request_data(self):
        bodies = [
            dict(),
            dict(content="a fake post here"),
        ]

        for body in bodies:
            resp = self.client.post("/", data=body)
            self.assertEqual(resp.status, "400 BAD REQUEST")

    @mock.patch("app.core.helpers.filehelper.save")
    @mock.patch("app.core.helpers.scripthelper.run_build_script")
    def test_create_quip_file_output(self, mock_build, mock_save):
        # setup
        data = dict(
            content="a fake post here",
            current_date="2021-01-01T12:12:12",
        )
        resp = self.client.post("/quip", data=data)
        self.assertEqual(resp.status, "302 FOUND", resp.data)
        self.assertEqual(resp.location, TestConfig.SITE)
        self.assertEqual(len(mock_save.call_args), 2)

        path, content = mock_save.call_args[0]
        self.assertTrue(str(path).endswith(".md"))
        self.assertTrue(data.get("content") in content)
        self.assertTrue(data.get("current_date") in content)


if __name__ == "__main__":
    unittest.main()
