import os
from os import environ
from io import BytesIO
from http import HTTPStatus
from app.config import LocalTestConfig, DockerTestConfig
from app import create_app

from .base import InitializeRepo, IMAGE_PATH, CREATE_FILE


class CreateTests(InitializeRepo):
    def setUp(self):
        super().setUp()
        self.app = create_app(
            DockerTestConfig if environ.get("IS_DOCKER") else LocalTestConfig
        )
        self.client = self.app.test_client()

    def test_create_returns_correct_json(self):
        file_path = CREATE_FILE.split(".")[0]
        new_front_matter = dict(author="Gerry Witte")
        new_content = "This is the content of my new file"
        body = dict(path=file_path, body=new_content, frontmatter=new_front_matter)
        response = self.client.post(f"/file", json=body)

        # assert
        self.assertEqual(HTTPStatus.OK, response.status_code)
        data = response.json
        print(data)
        self.assertTrue(data.get("success"), data.get("message"))

        content = data.get("content")
        front_matter, body = content.get("frontmatter"), content.get("body")

        self.assertEqual(file_path, content.get("path"))
        self.assertIsNotNone(body)
        self.assertIsNotNone(front_matter)
        self.assertIn("content of my new file", body)
        self.assertIn("Gerry Witte", front_matter.values())

    def test_create_with_file_appends_caption(self):
        file_path = CREATE_FILE.split(".")[0]
        photo = "https://images.alexbilson.dev/photo.webp"
        photoAlt = "Alternative text for my photo"
        photoCaption = "A test photo caption"
        new_front_matter = dict(
            author="Gerry Witte",
            photo=photo,
            photoAlt=photoAlt,
            photoCaption=photoCaption,
        )
        new_content = "This is the content of my new file"
        body = dict(path=file_path, body=new_content, frontmatter=new_front_matter)
        response = self.client.post(f"/file", json=body)

        # assert
        self.assertEqual(HTTPStatus.OK, response.status_code)
        data = response.json
        self.assertTrue(data.get("success"), data.get("message"))

        content = data.get("content")
        front_matter, body = content.get("frontmatter"), content.get("body")

        self.assertEqual(file_path, content.get("path"))
        self.assertIsNotNone(body)
        self.assertIsNotNone(front_matter)
        self.assertIn("{{< caption", body)
        self.assertIn(f'caption="{photoCaption}"', body)
        self.assertIn(f'alt="{photoAlt}"', body)
        self.assertIn(f'src="{photo}"', body)

    def test_create_file_saves_to_path(self):
        filename = "photo.heic"
        image_path = (
            f"/mnt/data/{filename}"
            if environ.get("IS_DOCKER")
            else f"/Users/alexbilson/source/chaos-micropub/src/tests/test_data/{filename}"
        )
        with open(image_path, "rb") as f:
            file_content = BytesIO(f.read())
        data = dict(photo=(file_content, filename))
        response = self.client.post(
            "/photo", content_type="multipart/form-data", buffered=True, data=data
        )

        # assert
        self.assertEqual(HTTPStatus.OK, response.status_code)
        data = response.json
        self.assertTrue(data.get("success"), data.get("message"))
        new_filename = data.get("content").get("filename")
        self.assertEqual("photo.webp", new_filename)
        # ensures original is removed
        self.assertFalse(os.path.exists(os.path.join(IMAGE_PATH, filename)))
