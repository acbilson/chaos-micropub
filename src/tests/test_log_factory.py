import unittest
from datetime import datetime
from app.log.forms import LogForm
from app.log import log_factory as LogFactory
from base_test import BaseTest


class LogFactoryTests(BaseTest):
    def setUp(self):
        super().setUp()
        with open(
            "/mnt/chaos/content/logs/20200627-132146.md", "r"
        ) as f:
            self.content = f.readlines()

    def test_factory_creates_form_from_body(self):
        with self.app.app_context():
            note = LogFactory.fromBody("/mnt/chaos/content/logs/20200627-132146.md", self.content)
            self.assertEqual(note.author.data, "Alex Bilson")
            self.assertGreater(len(str(note.current_date.data)), 0)
            self.assertGreater(len(str(note.modified_date.data)), 0)
            self.assertGreater(len(note.content.data), 0)

    def test_factory_creates_note_from_form(self):
        with self.app.app_context():
            form = LogForm()
            form.filename.data = "2021010-21324"
            form.author.data = "Alex Bilson"
            form.content.data = "Test Content"
            form.current_date.data = datetime.now().isoformat()
            form.modified_date.data = datetime.now().isoformat()

            note = LogFactory.fromForm("/mnt/chaos/content", "Alex Bilson", form)

            self.assertEqual(note.author, "Alex Bilson")
            self.assertEqual(str(note.path), "/mnt/chaos/content/logs/2021010-21324.md")
            self.assertGreater(len(str(note.date)), 0)
            self.assertGreater(len(str(note.lastmod)), 0)
            self.assertGreater(len(note.content), 0)


if __name__ == "__main__":
    unittest.main()
