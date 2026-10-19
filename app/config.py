"""Konfigurasi aplikasi."""
import os
import re
import string
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    DB_PATH = os.environ.get("DB_PATH", str(BASE_DIR / "links.db"))

    # Pembuatan kode pendek
    ALPHABET = string.ascii_letters + string.digits
    CODE_LENGTH = 6

    # Validasi
    ALIAS_RE = re.compile(r"^[A-Za-z0-9_-]{3,32}$")
    RESERVED = frozenset({"api", "links", "static", "favicon.ico", "admin"})
    MAX_URL_LENGTH = 2048

    # Daftar link terbaru di halaman utama
    LIST_LIMIT = 20


class TestConfig(Config):
    TESTING = True
