# Pendekin

Pemendek link sederhana berbasis **Flask + SQLite**. Tempel link panjang, dapatkan link pendek, dengan alias kustom opsional, penghitung klik, dan daftar link terbaru.

## Fitur

- Link pendek acak (6 karakter) atau alias kustom
- Penghitung klik per link
- Hapus link
- Antarmuka web responsif (mendukung mode gelap)
- REST API sederhana
- Tes otomatis dengan pytest

## Struktur proyek

```
pendekin/
├── app/
│   ├── __init__.py        # create_app (app factory)
│   ├── config.py          # konfigurasi
│   ├── db.py              # koneksi & skema SQLite
│   ├── validators.py      # validasi URL & alias
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

## API

| Method   | Endpoint            | Keterangan                          |
|----------|---------------------|-------------------------------------|
| `POST`   | `/api/shorten`      | Buat link. Body: `{"url", "alias"?}` |
| `GET`    | `/api/links`        | 20 link terbaru                     |
| `DELETE` | `/api/links/<code>` | Hapus link                          |
| `GET`    | `/<code>`           | Redirect ke URL asli (302)          |

Contoh:

```bash
curl -X POST http://127.0.0.1:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://contoh.com/artikel/panjang", "alias": "promo"}'
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

> Catatan: API ini belum memiliki autentikasi, sehingga siapa pun yang bisa mengakses server dapat membuat dan menghapus link. Tambahkan autentikasi sebelum dipublikasikan ke internet.
