import unittest
from datetime import datetime
from app.micropub.forms import NoteForm
from app.micropub import note_factory as NoteFactory
from base_test import BaseTest


class NoteFactoryTests(BaseTest):
    def setUp(self):
        super().setUp()
        with open(
            "/mnt/chaos/content/notes/add-snippets-to-your-text-input.md", "r"
        ) as f:
            self.content = f.readlines()

    def test_factory_creates_form_from_body(self):
        with self.app.app_context():
            note = NoteFactory.fromBody("/mnt/chaos/content", self.content)
            self.assertEqual(note.title.data, "Add Snippets to Your Text Input")
            self.assertEqual(note.author.data, "Alex Bilson")
            self.assertEqual(note.tags.data, ["snippet", "javascript", "software"])
            self.assertEqual(note.current_date.data, "2021-06-11T20:05:50")
            self.assertGreater(len(str(note.modified_date.data)), 0)
            self.assertGreater(len(note.content.data), 0)

    def test_factory_creates_note_from_form(self):
        with self.app.app_context():
            form = NoteForm()
            form.author.data = "Alex Bilson"
            form.title.data = "Test Title"
            form.content.data = "Test Content"
            form.current_date.data = datetime.now().isoformat()
            form.modified_date.data = datetime.now().isoformat()
            form.comments.data = True
            form.tags.data = ["fake", "tag"]

            note = NoteFactory.fromForm("/mnt/chaos/content", "Alex Bilson", form)

            self.assertEqual(note.title, "Test Title")
            self.assertEqual(note.author, "Alex Bilson")
            self.assertEqual(note.tags, ["fake", "tag"])
            self.assertEqual(str(note.path), "/mnt/chaos/content/notes/test-title.md")
            self.assertGreater(len(str(note.date)), 0)
            self.assertGreater(len(str(note.lastmod)), 0)
            self.assertGreater(len(note.content), 0)


if __name__ == "__main__":
    unittest.main()
