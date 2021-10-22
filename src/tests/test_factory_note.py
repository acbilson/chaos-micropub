import unittest
from app.micropub import note_factory as NoteFactory
from base_test import BaseTest


class NoteFactoryTests(BaseTest):
    def setUp(self):
        super().setUp()
        with open(
            "/mnt/chaos/content/notes/add-snippets-to-your-text-input.md", "r"
        ) as f:
            self.content = f.readlines()

    def test_factory_creates_note_form_from_content(self):
        with self.app.app_context():
            note = NoteFactory.fromBody(
                "/mnt/chaos/content/notes", "Test User", self.content
            )
            self.assertEqual(note.title.data, "Add Snippets to Your Text Input")
            self.assertEqual(note.tags.data, ["snippet", "javascript", "software"])
            self.assertEqual(note.current_date.data, "2021-06-11T20:05:50")
            self.assertGreater(len(note.content.data), 0)


if __name__ == "__main__":
    unittest.main()
