import unittest
from unittest import mock
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
    def test_create_note_file_output(self, mock_open, mock_sp):
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


if __name__ == "__main__":
    unittest.main()
