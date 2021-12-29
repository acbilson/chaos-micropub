# TODO: fix test and create dir when missing
import unittest
from datetime import datetime
from app.log.forms import LogForm
from app.log import log_factory as LogFactory
from base_test import BaseTest


class LogFactoryTests(BaseTest):
    def setUp(self):
        super().setUp()
        with open("/mnt/chaos/content/logs/2020/06/20200627-132146.md", "r") as f:
            self.content = f.readlines()

    def test_factory_creates_form_from_body(self):
        with self.app.app_context():
            log = LogFactory.fromBody(
                "/mnt/chaos/content/logs/2020/06/20200627-132146.md", self.content
            )
            self.assertEqual(log.author.data, "Alex Bilson")
            self.assertGreater(len(str(log.current_date.data)), 0)
            self.assertGreater(len(str(log.modified_date.data)), 0)
            self.assertGreater(len(log.content.data), 0)

    def test_factory_creates_log_from_form(self):
        with self.app.app_context():
            form = LogForm()
            form.filename.data = "20200627-533924"
            form.author.data = "Alex Bilson"
            form.content.data = "Test Content"
            form.current_date.data = datetime.fromisoformat("2020-06-27T18:53:39.240457").isoformat()
            form.modified_date.data = datetime.now().isoformat()

            log = LogFactory.fromForm("/mnt/chaos/content", "Alex Bilson", form)

            self.assertEqual(log.author, "Alex Bilson")
            self.assertEqual(str(log.path), "/mnt/chaos/content/logs/2020/06/20200627-533924.md")
            self.assertGreater(len(str(log.date)), 0)
            self.assertGreater(len(str(log.lastmod)), 0)
            self.assertGreater(len(log.content), 0)


if __name__ == "__main__":
    unittest.main()
