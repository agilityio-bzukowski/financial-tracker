# Testing Patterns

**Analysis Date:** 2026-03-02

## Test Framework

**Runner:**
- pytest (Python backend tests)
- Config: `backend/pyproject.toml` with `testpaths = ["tests"]`
- No frontend testing framework configured (no vitest/jest/playwright)

**Assertion Library:**
- pytest assertions (standard `assert` statements)
- unittest.mock for mocking

**Run Commands:**
```bash
make test                                          # Run all backend tests
poetry run pytest tests/integration/test_users_integration.py -v  # Run single file
poetry run pytest -k "test_create_account" -v     # Run by test name
```

## Test File Organization

**Location:**
- Backend: `backend/tests/` directory
  - `backend/tests/integration/` - full API integration tests
  - `backend/tests/unit/` - isolated unit tests
- Frontend: No test files present

**Naming:**
- Pattern: `test_*.py` for test modules
- Pattern: `test_*` prefix for test functions
- Integration tests: `test_users_integration.py`, `test_transactions_integration.py`
- Unit tests: `test_filters.py` (testing `FilterSpec` helper)

**Structure:**
```
backend/
├── tests/
│   ├── conftest.py              # Pytest fixtures
│   ├── unit/
│   │   ├── __init__.py
│   │   └── test_filters.py
│   └── integration/
│       ├── __init__.py
│       ├── test_users_integration.py
│       ├── test_transactions_integration.py
│       ├── test_categories_integration.py
│       └── test_auth_integration.py
```

## Test Structure

**Suite Organization:**
```python
# Section headers for logical grouping
# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------

def test_create_transaction(client_with_test_db):
    headers = _register_and_auth(client_with_test_db)
    resp = client_with_test_db.post("/api/transactions/", json={...}, headers=headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["description"] == "Coffee"
    assert "id" in data
```

**Patterns:**
- Setup: Arrange helpers at top (`_register_and_auth()`, `_create_transaction()`)
- Arrange: Call setup helpers to establish preconditions
- Act: Execute API call
- Assert: Verify status code and response body

**Helper Functions:**
- `_register_and_auth()` - creates user and returns auth headers
- `_create_transaction()` - creates transaction with defaults + overrides
- `_create_category()` - creates category and returns ID
- All prefixed with `_` to indicate private/internal use

## Mocking

**Framework:** unittest.mock (`from unittest.mock import MagicMock`)

**Patterns:**
```python
def test_applies_when_value_present():
    spec = FilterSpec(param="name", build=lambda v: f"name == {v}")
    query = MagicMock()
    query.filter.return_value = query  # Chain calls

    result = apply_filters(query, [spec], {"name": "Alice"})

    query.filter.assert_called_once_with("name == Alice")
    assert result is query
```

**What to Mock:**
- SQLAlchemy query chains (for unit tests)
- External dependencies that shouldn't be called in isolation
- Test utilities use MagicMock for complex query operations

**What NOT to Mock:**
- Database (real SQLite test DB created per test)
- HTTP client (TestClient from fastapi.testclient)
- External services like JWT/bcrypt (use real implementations with test fixtures)

## Fixtures and Factories

**Test Data:**
```python
# backend/tests/conftest.py
@pytest.fixture
def client_with_test_db():
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)

    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    os.unlink(db_path)
```

**Location:**
- `backend/tests/conftest.py` - shared pytest fixtures
- Fixtures provide test database and FastAPI TestClient
- Temporary SQLite databases created per test, cleaned up after

**Factory Pattern:**
- Test helpers return IDs or default payloads
- `_create_transaction()` accepts `**overrides` for flexible test data
- Example: `_create_transaction(client, headers, amount=99.99, description="Custom")`

## Coverage

**Requirements:** Not enforced - no coverage configuration in pyproject.toml

**View Coverage:**
- No coverage command configured
- Could run with `poetry run pytest --cov=app tests/`

## Test Types

**Unit Tests:**
- Scope: Single function or class in isolation
- Location: `backend/tests/unit/`
- Example: `test_filters.py` tests `FilterSpec.apply_filters()` with mocked queries
- Approach: Mocked dependencies, focused on logic
- Count: ~9 tests for filter logic

**Integration Tests:**
- Scope: Full API endpoint to database
- Location: `backend/tests/integration/`
- Example: `test_transactions_integration.py` - tests POST/PATCH/DELETE against live SQLite
- Approach: Real database, real HTTP client, uses fixtures
- Coverage:
  - Users: Create, list, get, update, delete (7 tests)
  - Transactions: Create, list, get, update, delete, restore, pagination, filtering (30+ tests)
  - Categories: Similar CRUD pattern
  - Auth: Login, registration, token validation

**E2E Tests:**
- Framework: Not used
- Frontend: No testing framework configured

## Common Patterns

**Async Testing:**
- Backend uses pytest-asyncio (`pytest-asyncio = "^1.3.0"` in pyproject.toml)
- No `@pytest.mark.asyncio` observed in current tests
- FastAPI TestClient handles async endpoints internally

**Error Testing:**
```python
def test_create_user_duplicate_email(client_with_test_db):
    payload = {"email": "bob@example.com", "name": "Bob", "password": "pass"}
    client_with_test_db.post("/api/users/", json=payload)
    resp = client_with_test_db.post("/api/users/", json=payload)
    assert resp.status_code == 409

def test_get_user_not_found(client_with_test_db):
    resp = client_with_test_db.get("/api/users/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404

def test_create_transaction_empty_description(client_with_test_db):
    headers = _register_and_auth(client_with_test_db)
    resp = client_with_test_db.post("/api/transactions/", json={
        "type": "expense",
        "description": "  ",  # Invalid
        "amount": 10.0,
        "date": "2026-01-01T00:00:00Z",
    }, headers=headers)
    assert resp.status_code == 422
```

**Permission Testing:**
```python
def test_get_transaction_wrong_user(client_with_test_db):
    headers_alice = _register_and_auth(client_with_test_db, email="alice@example.com")
    txn_id = _create_transaction(client_with_test_db, headers_alice)

    headers_bob = _register_and_auth(client_with_test_db, email="bob@example.com")
    resp = client_with_test_db.get(f"/api/transactions/{txn_id}", headers=headers_bob)
    assert resp.status_code == 404  # User cannot access another's transaction
```

**Pagination Testing:**
```python
def test_list_transactions_pagination(client_with_test_db):
    headers = _register_and_auth(client_with_test_db)

    # Create 15 transactions
    for i in range(15):
        _create_transaction(client, headers, description=f"Item {i}", amount=float(i + 1))

    # Page 1
    resp = client_with_test_db.get("/api/transactions/", headers=headers)
    data = resp.json()
    assert data["total"] == 15
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert data["total_pages"] == 2
    assert len(data["items"]) == 10

    # Page 2
    resp = client_with_test_db.get("/api/transactions/?page=2", headers=headers)
    assert len(resp.json()["items"]) == 5
```

**Filtering Testing:**
```python
def test_list_transactions_filter_by_type(client_with_test_db):
    headers = _register_and_auth(client_with_test_db)
    _create_transaction(client, headers, type="income", amount=5000)
    _create_transaction(client, headers, type="expense", amount=5)

    resp = client_with_test_db.get("/api/transactions/?type=income", headers=headers)
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["type"] == "income"

def test_list_transactions_search(client_with_test_db):
    headers = _register_and_auth(client_with_test_db)
    _create_transaction(client, headers, description="Weekly groceries")
    _create_transaction(client, headers, description="Coffee shop")

    resp = client_with_test_db.get("/api/transactions/?search=grocer", headers=headers)
    data = resp.json()
    assert data["total"] == 1
    assert "groceries" in data["items"][0]["description"].lower()
```

**Soft Delete Testing:**
```python
def test_delete_transaction(client_with_test_db):
    headers = _register_and_auth(client_with_test_db)
    txn_id = _create_transaction(client, headers)

    resp = client_with_test_db.delete(f"/api/transactions/{txn_id}", headers=headers)
    assert resp.status_code == 204

    # Soft delete - not in list
    resp = client_with_test_db.get("/api/transactions/", headers=headers)
    assert resp.json()["total"] == 0

    # Can restore
    resp = client_with_test_db.post(f"/api/transactions/{txn_id}/restore", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == txn_id
```

## Test Coverage Summary

**Backend Integration Tests:**
- Users: 7 tests covering CRUD operations
- Transactions: 30+ tests covering CRUD, filtering, pagination, soft delete, restore, validation
- Categories: Similar CRUD pattern
- Auth: Login/register validation

**Backend Unit Tests:**
- Filter logic: 9 tests for `FilterSpec` helper functions

**Frontend:**
- No tests configured or written

---

*Testing analysis: 2026-03-02*
