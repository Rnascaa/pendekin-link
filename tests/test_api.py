def shorten(client, url, alias=None):
    payload = {"url": url}
    if alias is not None:
        payload["alias"] = alias
    return client.post("/api/shorten", json=payload)


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


def test_shorten_custom_alias(client):
    res = shorten(client, "https://contoh.com", "promo-1")
    assert res.status_code == 201
    assert res.get_json()["code"] == "promo-1"


def test_duplicate_alias(client):
    shorten(client, "https://a.com", "sama")
    res = shorten(client, "https://b.com", "sama")
    assert res.status_code == 409


def test_reserved_alias(client):
    assert shorten(client, "https://a.com", "admin").status_code == 400
    assert shorten(client, "https://a.com", "API").status_code == 400


def test_invalid_alias(client):
    assert shorten(client, "https://a.com", "a b").status_code == 400
    assert shorten(client, "https://a.com", "ab").status_code == 400


def test_invalid_urls(client):
    assert shorten(client, "").status_code == 400
    assert shorten(client, "ftp://contoh.com").status_code == 400
    assert shorten(client, "http://contoh.com:abc").status_code == 400
    assert shorten(client, "https://" + "a" * 2100 + ".com").status_code == 400


def test_redirect_counts_clicks(client):
    code = shorten(client, "https://contoh.com", "tujuan").get_json()["code"]
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
