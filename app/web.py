"""Blueprint halaman web dan redirect."""
from flask import Blueprint, abort, redirect

from . import services

bp = Blueprint("web", __name__)


@bp.get("/<code>")
def follow(code):
    url = services.resolve_and_count(code)
    if url is None:
        abort(404)
    return redirect(url, code=302)
