import unittest
from unittest import mock
from unittest.mock import Mock
from app.config import TestConfig
from base_test import BaseTest


class CreateNoteTests(BaseTest):
    def test_create_note_missing_request_data(self):
        bodies = [
            dict(),
            dict(content="a fake post here"),
            dict(content="a fake post here", current_date="2021-01-01T12:12:12"),
            dict(
                content="a fake post here",
                current_date="2021-01-01T12:12:12",
                title="A Fake Title",
            ),
            dict(
                content="a fake post here",
                current_date="2021-01-01T12:12:12",
                title="A Fake Title",
                tags="['fake', 'false',]",
            ),
        ]

        for body in bodies:
            resp = self.client.post("/", data=body)
            self.assertEqual(resp.status, "400 BAD REQUEST")

    @mock.patch("app.core.helpers.filehelper.save")
    @mock.patch("app.core.helpers.scripthelper.run_build_script")
    def test_create_note_file_output(self, mock_build, mock_save):
        # setup
        data = dict(
            content="a fake post here",
            current_date="2021-01-01T12:12:12",
            title="A Fake Title",
            tags="['fake', 'false',]",
            comments="on",
        )
        resp = self.client.post("/note", data=data)
        self.assertEqual(resp.status, "302 FOUND", resp.data)
        self.assertEqual(resp.location, TestConfig.SITE)
        self.assertEqual(len(mock_save.call_args), 2)

        path, content = mock_save.call_args[0]
        self.assertTrue(str(path).endswith(".md"))
        self.assertTrue(data.get("content") in content)
        self.assertTrue(data.get("current_date") in content)
        self.assertTrue(data.get("title") in content)
        self.assertTrue("epistemic" in content)


if __name__ == "__main__":
    unittest.main()
