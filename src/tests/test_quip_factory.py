import unittest
from datetime import datetime
from app.quip.forms import QuipForm
from app.quip import quip_factory as QuipFactory
from base_test import BaseTest


class QuipFactoryTests(BaseTest):
    def setUp(self):
        super().setUp()
        with open("/mnt/chaos/content/quips/20211229-212916.md", "r") as f:
            self.content = f.readlines()

    def test_factory_creates_form_from_body(self):
        with self.app.app_context():
            quip = QuipFactory.fromBody(
                "/mnt/chaos/content/quips/20211229-212916.md",
                self.content,
            )
            self.assertEqual(quip.author.data, "Alex Bilson")
            self.assertGreater(len(str(quip.current_date.data)), 0)
            self.assertGreater(len(str(quip.modified_date.data)), 0)
            self.assertGreater(len(quip.content.data), 0)

    def test_factory_creates_quip_from_form(self):
        with self.app.app_context():
            form = QuipForm()
            form.filename.data = "20211229-212916"
            form.author.data = "Alex Bilson"
            form.content.data = "Test Content"
            form.current_date.data = datetime.fromisoformat(
                "2021-12-29T15:43:54.124399"
            ).isoformat()
            form.modified_date.data = datetime.now().isoformat()

            quip = QuipFactory.fromForm("/mnt/chaos/content", "Alex Bilson", form)

            self.assertEqual(quip.author, "Alex Bilson")
            self.assertEqual(
                str(quip.path), "/mnt/chaos/content/quips/20211229-212916.md"
            )
            self.assertGreater(len(str(quip.date)), 0)
            self.assertGreater(len(str(quip.lastmod)), 0)
            self.assertGreater(len(quip.content), 0)


if __name__ == "__main__":
    unittest.main()
