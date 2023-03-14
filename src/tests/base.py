import unittest
import os
from os import environ
from app.config import LocalTestConfig, DockerTestConfig
from app.operators import try_run_cmd

if environ.get("IS_DOCKER"):
    CONTENT_PATH = DockerTestConfig.CONTENT_PATH
    REPO_PATH = DockerTestConfig.REPO_PATH
    IMAGE_PATH = DockerTestConfig.IMAGE_PATH
else:
    CONTENT_PATH = LocalTestConfig.CONTENT_PATH
    REPO_PATH = LocalTestConfig.REPO_PATH
    IMAGE_PATH = LocalTestConfig.IMAGE_PATH

READ_FILE = "read_file.md"
UPDATE_FILE = "update_file.md"
CREATE_FILE = "create_file.md"


class InitializeRepo(unittest.TestCase):
    def setUp(self):
        # generate the origin repo
        os.makedirs(REPO_PATH)
        try_run_cmd(["git", "init", "--bare"], REPO_PATH)

        # clones content from bare origin
        try_run_cmd(["git", "clone", REPO_PATH, CONTENT_PATH], ".")

        # creates image storage location
        os.makedirs(IMAGE_PATH)

        # creates a few test files
        content = (
            '+++\nauthor = "Alex Bilson"\n+++\nThis is some test content to read\n'
        )
        with open(os.path.join(CONTENT_PATH, READ_FILE), "w") as f:
            f.write(content)

        content = (
            '+++\nauthor = "Alex Bilson"\n+++\nThis is some test content to update\n'
        )
        with open(os.path.join(CONTENT_PATH, UPDATE_FILE), "w") as f:
            f.write(content)

        # commits my files to origin
        try_run_cmd(["git", "add", "-v", "."], CONTENT_PATH)
        try_run_cmd(["git", "commit", "-m", f'"adds initial files"'], CONTENT_PATH)
        try_run_cmd(["git", "push"], CONTENT_PATH)

    def tearDown(self):
        try_run_cmd(["rm", "-rf", CONTENT_PATH], ".")
        try_run_cmd(["rm", "-rf", REPO_PATH], ".")
        try_run_cmd(["rm", "-rf", IMAGE_PATH], ".")
