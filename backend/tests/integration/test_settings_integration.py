def test_get_settings_creates_default(client_with_test_db):
    resp = client_with_test_db.get("/api/settings/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == "default"
    assert data["currency"] == "USD"


def test_update_settings(client_with_test_db):
    resp = client_with_test_db.patch(
        "/api/settings/", json={"currency": "EUR"}
    )
    assert resp.status_code == 200
    assert resp.json()["currency"] == "EUR"
