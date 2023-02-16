from os import environ


class BaseConfig(object):
    """Set Flask configuration variables"""

    FLASK_HOST = "0.0.0.0"
    FLASK_PORT = 5000
    FLASK_ENV = environ.get("FLASK_ENV")
    FLASK_DEBUG = environ.get("FLASK_DEBUG")
    SITE = environ.get("SITE")
    # TODO: figure out why this doesn't work in prod
    CONTENT_PATH = environ.get("CONTENT_PATH") or "/mnt/chaos/content"
    IMAGE_PATH = environ.get("IMAGE_PATH") or "/mnt/images/alexbilson"

    ADMIN_USER = environ.get("ADMIN_USER")
    ADMIN_PASSWORD = environ.get("ADMIN_PASSWORD")

    FLASK_SECRET_KEY = environ.get("FLASK_SECRET_KEY")
    SESSION_SECRET = environ.get("SESSION_SECRET")

    MASTODON_HOST = environ.get("MASTODON_HOST")
    MASTODON_CLIENT_ID = environ.get("MASTODON_CLIENT_ID")
    MASTODON_CLIENT_SECRET = environ.get("MASTODON_CLIENT_SECRET")


class LocalTestConfig(object):
    """Set Flask test configuration variables"""

    FLASK_HOST = "0.0.0.0"
    FLASK_PORT = 80
    FLASK_ENV = "testing"
    SITE = "http://localhost"
    REPO_PATH = "/tmp/test_micropub_repo"
    CONTENT_PATH = "/tmp/test_micropub_content"
    IMAGE_PATH = "/tmp/test_micropub_images"

    ADMIN_USER = "alex"
    ADMIN_PASSWORD = "example"

    FLASK_SECRET_KEY = "my secret test key"
    SESSION_SECRET = "my secret test session"

    MASTODON_HOST = "https://indieweb.social"
    MASTODON_CLIENT_ID = "masto client id"
    MASTODON_CLIENT_SECRET = "masto client secret"


class DockerTestConfig(object):
    """Set Flask Docker test configuration variables"""

    FLASK_HOST = "0.0.0.0"
    FLASK_PORT = 80
    FLASK_ENV = "docker"
    SITE = "http://localhost"
    REPO_PATH = "/mnt/repo"
    CONTENT_PATH = "/mnt/test/content"
    IMAGE_PATH = "/mnt/images/alexbilson"

    ADMIN_USER = "alex"
    ADMIN_PASSWORD = "example"

    FLASK_SECRET_KEY = "my secret test key"
    SESSION_SECRET = "my secret test session"

    MASTODON_HOST = "https://indieweb.social"
    MASTODON_CLIENT_ID = "masto client id"
    MASTODON_CLIENT_SECRET = "masto client secret"
