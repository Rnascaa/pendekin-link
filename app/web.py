"""Blueprint halaman web dan redirect."""
feat/web-ui
from flask import Blueprint, abort, redirect, render_template
from flask import Blueprint, abort, redirect
main

from . import services

bp = Blueprint("web", __name__)


feat/web-ui
@bp.get("/")
def index():
    return render_template("index.html")

main
@bp.get("/<code>")
def follow(code):
    url = services.resolve_and_count(code)
    if url is None:
        abort(404)
    return redirect(url, code=302)
