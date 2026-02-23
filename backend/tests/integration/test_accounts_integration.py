def test_list_accounts_empty(client_with_test_db):
    resp = client_with_test_db.get("/api/accounts/")
    assert resp.status_code == 200
    assert resp.json() == []


def test_create_account(client_with_test_db):
    resp = client_with_test_db.post(
        "/api/accounts/",
        json={"name": "Checking", "type": "checking", "balance": 1000.0},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Checking"
    assert data["type"] == "checking"
    assert data["balance"] == 1000.0


def test_get_account(client_with_test_db):
    create_resp = client_with_test_db.post(
        "/api/accounts/",
        json={"name": "Savings", "type": "savings"},
    )
    account_id = create_resp.json()["id"]

    resp = client_with_test_db.get(f"/api/accounts/{account_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == account_id


def test_update_account(client_with_test_db):
    create_resp = client_with_test_db.post(
        "/api/accounts/",
        json={"name": "Cash", "type": "cash"},
    )
    account_id = create_resp.json()["id"]

    resp = client_with_test_db.patch(
        f"/api/accounts/{account_id}", json={"balance": 500.0}
    )
    assert resp.status_code == 200
    assert resp.json()["balance"] == 500.0


def test_delete_account(client_with_test_db):
    create_resp = client_with_test_db.post(
        "/api/accounts/",
        json={"name": "Old Account", "type": "other"},
    )
    account_id = create_resp.json()["id"]

    resp = client_with_test_db.delete(f"/api/accounts/{account_id}")
    assert resp.status_code == 204

    resp = client_with_test_db.get(f"/api/accounts/{account_id}")
    assert resp.status_code == 404


def test_get_account_not_found(client_with_test_db):
    resp = client_with_test_db.get("/api/accounts/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404
