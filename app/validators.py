"""Validasi dan normalisasi input."""
from urllib.parse import urlparse

from flask import current_app


def normalize_url(url: str) -> str:
    """Tambahkan https:// jika pengguna tidak menulis skema."""
    url = url.strip()
    if url and "://" not in url:
        url = "https://" + url
    return url


def is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        parsed.port  # memicu ValueError jika port tidak valid
    except ValueError:
        return False
    return (
        parsed.scheme in ("http", "https")
        and bool(parsed.hostname)
        and len(url) <= current_app.config["MAX_URL_LENGTH"]
    )
