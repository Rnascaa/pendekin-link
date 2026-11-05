"""Pendekin — pemendek link sederhana (Flask + SQLite)."""
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from . import api, db, web
from .config import Config


def create_app(config_object=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Di balik reverse proxy, skema asli (https) ada di X-Forwarded-Proto.
    # Tanpa ini short_url akan dibuat dengan http://.
    if app.config["TRUST_PROXY"]:
        app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)

    db.init_app(app)
    app.register_blueprint(api.bp)
    app.register_blueprint(web.bp)

    @app.errorhandler(404)
    def not_found(_e):
        return "Link tidak ditemukan.", 404

    return app
