"""Blueprint REST API (/api/...)."""
from flask import Blueprint, jsonify, request

from . import services, validators

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.post("/shorten")
def shorten():
    data = request.get_json(silent=True) or {}
    url = validators.normalize_url(data.get("url") or "")

    if not validators.is_valid_url(url):
        return jsonify(error="URL tidak valid. Gunakan alamat http:// atau https://."), 400

    row = services.create_link(url)
    return jsonify(services.link_to_dict(row)), 201


@bp.get("/links")
def list_links():
    return jsonify([services.link_to_dict(r) for r in services.list_links()])


@bp.delete("/links/<code>")
def delete_link(code):
    if not services.delete_link(code):
        return jsonify(error="Link tidak ditemukan."), 404
    return "", 204
