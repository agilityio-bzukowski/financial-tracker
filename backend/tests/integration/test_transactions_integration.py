from datetime import datetime, timezone


def _create_account(client, name="Test Account", account_type="checking"):
    resp = client.post(
        "/api/accounts/",
        json={"name": name, "type": account_type},
    )
    assert resp.status_code == 201
    return resp.json()["id"]


def test_list_transactions_empty(client_with_test_db):
    resp = client_with_test_db.get("/api/transactions/")
    assert resp.status_code == 200
    assert resp.json() == []


def test_create_transaction(client_with_test_db):
    account_id = _create_account(client_with_test_db)

    resp = client_with_test_db.post(
        "/api/transactions/",
        json={
            "account_id": account_id,
            "type": "expense",
            "amount": 50.0,
            "date": datetime.now(timezone.utc).isoformat(),
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["amount"] == 50.0
    assert data["type"] == "expense"


def test_delete_transaction(client_with_test_db):
    account_id = _create_account(client_with_test_db)

    create_resp = client_with_test_db.post(
        "/api/transactions/",
        json={
            "account_id": account_id,
            "type": "income",
            "amount": 100.0,
            "date": datetime.now(timezone.utc).isoformat(),
        },
    )
    transaction_id = create_resp.json()["id"]

    resp = client_with_test_db.delete(f"/api/transactions/{transaction_id}")
    assert resp.status_code == 204

    resp = client_with_test_db.get(f"/api/transactions/{transaction_id}")
    assert resp.status_code == 404
