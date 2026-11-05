"""Templat file WSGI untuk PythonAnywhere.

Salin isi file ini ke file WSGI di tab "Web" PythonAnywhere,
lalu ganti USERNAME dengan username akun kamu.
"""
import os
import sys

PROJECT_DIR = "/home/USERNAME/pendekin-link"

if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

os.environ["TRUST_PROXY"] = "1"
os.environ["DB_PATH"] = os.path.join(PROJECT_DIR, "links.db")

from run import app as application  # noqa: E402
