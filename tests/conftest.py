import pytest

from app import create_app
from app.config import TestConfig


@pytest.fixture()
def client(tmp_path):
    class Cfg(TestConfig):
        DB_PATH = str(tmp_path / "test.db")

    app = create_app(Cfg)
    return app.test_client()
