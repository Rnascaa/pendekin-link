from app import create_app
from app.config import TestConfig


def shorten(client, url):
    return client.post("/api/shorten", json={"url": url})


def proxied_short_url(tmp_path, trust_proxy):
    class Cfg(TestConfig):
        DB_PATH = str(tmp_path / "proxy.db")
        TRUST_PROXY = trust_proxy

    res = create_app(Cfg).test_client().post(
        "/api/shorten",
        json={"url": "https://contoh.com"},
        headers={"Host": "pendekin.example", "X-Forwarded-Proto": "https"},
    )
    return res.get_json()["short_url"]


def test_short_url_uses_https_behind_trusted_proxy(tmp_path):
    assert proxied_short_url(tmp_path, True).startswith("https://pendekin.example/")


def test_forwarded_proto_ignored_without_trust_proxy(tmp_path):
    assert proxied_short_url(tmp_path, False).startswith("http://pendekin.example/")


def test_index_page(client):
    res = client.get("/")
    assert res.status_code == 200
    assert "Pendekin" in res.get_data(as_text=True)


def test_static_assets(client):
    assert client.get("/static/css/style.css").status_code == 200
    assert client.get("/static/js/app.js").status_code == 200


def test_shorten_random_code(client):
    res = shorten(client, "https://contoh.com/panjang")
    assert res.status_code == 201
    data = res.get_json()
    assert len(data["code"]) == 6
    assert data["url"] == "https://contoh.com/panjang"
    assert data["clicks"] == 0


def test_shorten_adds_https_scheme(client):
    res = shorten(client, "contoh.com")
    assert res.status_code == 201
    assert res.get_json()["url"] == "https://contoh.com"


def test_alias_is_ignored(client):
    res = client.post("/api/shorten", json={"url": "https://contoh.com", "alias": "promo-1"})
    assert res.status_code == 201
    code = res.get_json()["code"]
    assert code != "promo-1"
    assert len(code) == 6
    assert client.get("/promo-1").status_code == 404


def test_index_has_no_alias_field(client):
    assert 'id="alias"' not in client.get("/").get_data(as_text=True)


def test_invalid_urls(client):
    assert shorten(client, "").status_code == 400
    assert shorten(client, "ftp://contoh.com").status_code == 400
    assert shorten(client, "http://contoh.com:abc").status_code == 400
    assert shorten(client, "https://" + "a" * 2100 + ".com").status_code == 400


def test_redirect_counts_clicks(client):
    code = shorten(client, "https://contoh.com").get_json()["code"]
    res = client.get(f"/{code}")
    assert res.status_code == 302
    assert res.headers["Location"] == "https://contoh.com"
    client.get(f"/{code}")
    links = client.get("/api/links").get_json()
    assert links[0]["clicks"] == 2


def test_redirect_not_found(client):
    assert client.get("/tidakada").status_code == 404


def test_list_newest_first_and_limit(client):
    for i in range(25):
        shorten(client, f"https://contoh.com/{i}")
    links = client.get("/api/links").get_json()
    assert len(links) == 20
    assert links[0]["url"].endswith("/24")


def test_delete(client):
    code = shorten(client, "https://contoh.com").get_json()["code"]
    assert client.delete(f"/api/links/{code}").status_code == 204
    assert client.delete(f"/api/links/{code}").status_code == 404
    assert client.get(f"/{code}").status_code == 404
