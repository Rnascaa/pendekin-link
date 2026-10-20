"""Logika bisnis: akses data link."""
import secrets
import sqlite3

from flask import current_app, request

from .db import get_db


class AliasTaken(Exception):
    """Kode/alias sudah dipakai link lain."""


def generate_code() -> str:
    cfg = current_app.config
    while True:
        code = "".join(secrets.choice(cfg["ALPHABET"]) for _ in range(cfg["CODE_LENGTH"]))
        if get_link(code) is None:
            return code


def get_link(code: str):
    return get_db().execute("SELECT * FROM links WHERE code = ?", (code,)).fetchone()


def create_link(url: str, alias: str | None = None):
    """Simpan link baru. Melempar AliasTaken jika kode sudah ada."""
    db = get_db()
    code = alias or generate_code()
    try:
        db.execute("INSERT INTO links (code, url) VALUES (?, ?)", (code, url))
        db.commit()
    except sqlite3.IntegrityError as exc:  # balapan antar request
        raise AliasTaken(code) from exc
    return get_link(code)


def list_links():
    limit = current_app.config["LIST_LIMIT"]
    return get_db().execute(
        "SELECT * FROM links ORDER BY created_at DESC, rowid DESC LIMIT ?", (limit,)
    ).fetchall()


def delete_link(code: str) -> bool:
    db = get_db()
    cur = db.execute("DELETE FROM links WHERE code = ?", (code,))
    db.commit()
    return cur.rowcount > 0


def resolve_and_count(code: str) -> str | None:
    """Ambil URL tujuan dan tambah hitungan klik. None jika tidak ada."""
    db = get_db()
    row = db.execute("SELECT url FROM links WHERE code = ?", (code,)).fetchone()
    if row is None:
        return None
    db.execute("UPDATE links SET clicks = clicks + 1 WHERE code = ?", (code,))
    db.commit()
    return row["url"]


def link_to_dict(row) -> dict:
    return {
        "code": row["code"],
        "short_url": request.host_url + row["code"],
        "url": row["url"],
        "clicks": row["clicks"],
        "created_at": row["created_at"],
    }
