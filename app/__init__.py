"""Pendekin — pemendek link sederhana (Flask + SQLite)."""
from flask import Flask

from . import api, db, web
from .config import Config


def create_app(config_object=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    app.register_blueprint(api.bp)
    app.register_blueprint(web.bp)

    @app.errorhandler(404)
    def not_found(_e):
        return "Link tidak ditemukan.", 404

    feat/web-ui
    return app
=======
    return app
    main
