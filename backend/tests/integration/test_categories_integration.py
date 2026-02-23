def test_list_categories_empty(client_with_test_db):
    resp = client_with_test_db.get("/api/categories/")
    assert resp.status_code == 200
    assert resp.json() == []


def test_create_category(client_with_test_db):
    resp = client_with_test_db.post(
        "/api/categories/",
        json={"name": "Food", "type": "expense"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Food"
    assert data["type"] == "expense"


def test_delete_category(client_with_test_db):
    create_resp = client_with_test_db.post(
        "/api/categories/",
        json={"name": "Travel", "type": "expense"},
    )
    category_id = create_resp.json()["id"]

    resp = client_with_test_db.delete(f"/api/categories/{category_id}")
    assert resp.status_code == 204

    resp = client_with_test_db.get(f"/api/categories/{category_id}")
    assert resp.status_code == 404
