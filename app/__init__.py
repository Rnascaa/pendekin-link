"""Pendekin — pemendek link sederhana (Flask + SQLite)."""
from flask import Flask

from . import api, db
from .config import Config


def create_app(config_object=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    app.register_blueprint(api.bp)

    return app