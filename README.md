# Pendekin-link

Pemendek link sederhana berbasis **Flask + SQLite**. Tempel link panjang, dapatkan link pendek, dengan penghitung klik dan daftar link terbaru.

## Fitur

- Link pendek acak (6 karakter)
- Penghitung klik per link
- Hapus link
- Antarmuka web responsif (mendukung mode gelap)
- REST API sederhana
- Tes otomatis dengan pytest

## Struktur proyek

```
pendekin-link/
├── app/
│   ├── __init__.py        # create_app (app factory)
│   ├── config.py          # konfigurasi
│   ├── db.py              # koneksi & skema SQLite
│   ├── validators.py      # validasi URL
│   ├── services.py        # logika akses data
│   ├── api.py             # blueprint REST API (/api)
│   ├── web.py             # halaman utama & redirect
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/style.css
│       └── js/app.js
├── tests/
│   ├── conftest.py
│   └── test_api.py
├── run.py                 # titik masuk
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Menjalankan

```bash
git clone https://github.com/Rnascaa/pendekin-link.git
cd pendekin-link
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Buka http://127.0.0.1:5000

### Variabel lingkungan (opsional)

| Variabel      | Default      | Keterangan                    |
|---------------|--------------|-------------------------------|
| `DB_PATH`     | `links.db`   | Lokasi file database SQLite   |
| `HOST`        | `127.0.0.1`  | Alamat bind server            |
| `PORT`        | `5000`       | Port server                   |
| `FLASK_DEBUG` | `0`          | Set `1` untuk mode debug      |
| `TRUST_PROXY` | `0`          | Set `1` jika di balik reverse proxy, agar `short_url` memakai `https://` |

## API

| Method   | Endpoint            | Keterangan                          |
|----------|---------------------|-------------------------------------|
| `POST`   | `/api/shorten`      | Buat link. Body: `{"url"}`          |
| `GET`    | `/api/links`        | 20 link terbaru                     |
| `DELETE` | `/api/links/<code>` | Hapus link                          |
| `GET`    | `/<code>`           | Redirect ke URL asli (302)          |

Contoh:

```bash
curl -X POST http://127.0.0.1:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://contoh.com/artikel/panjang"}'
```

## Tes

```bash
pip install -r requirements-dev.txt
pytest
```

## Deploy produksi

Server bawaan Flask hanya untuk pengembangan. Untuk produksi gunakan WSGI server, misalnya:

```bash
pip install gunicorn
gunicorn "run:app"
```

### PythonAnywhere

Di tab **Consoles**, buka Bash console lalu jalankan:

```bash
git clone https://github.com/Rnascaa/pendekin-link.git
cd pendekin-link
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Lalu di tab **Web**:

1. **Add a new web app** → **Manual configuration** → pilih versi Python 3.10 atau lebih baru.
2. Isi **Virtualenv** dengan `/home/USERNAME/pendekin-link/.venv`.
3. Buka **WSGI configuration file**, ganti seluruh isinya dengan `deploy/pythonanywhere_wsgi.py`, dan ganti `USERNAME`.
4. Aktifkan **Force HTTPS**, lalu klik **Reload**.

Aplikasi tersedia di `https://USERNAME.pythonanywhere.com`. Database SQLite tersimpan di `links.db` pada folder proyek dan tidak hilang saat aplikasi di-reload.

> Catatan: API ini tidak memiliki autentikasi, sehingga siapa pun yang bisa mengakses server dapat membuat, melihat, dan menghapus link.
