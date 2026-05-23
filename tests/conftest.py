import os
import tempfile

import pytest

import database.db as db_module
from app import app as flask_app


@pytest.fixture
def app():
    """
    Yield a Flask app wired to a fresh temp SQLite DB.
    DB_PATH is patched so every get_db() call inside the test
    hits the temp file, not the real spendly.db.
    """
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    original_path = db_module.DB_PATH
    db_module.DB_PATH = db_path

    with flask_app.app_context():
        db_module.init_db()
        db_module.create_user("Test User", "test@example.com", "password123")

    flask_app.config["TESTING"] = True

    yield flask_app

    db_module.DB_PATH = original_path
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()
