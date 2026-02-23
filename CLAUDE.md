# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository layout

```
financial-tracker/
├── backend/          # Python FastAPI application (all backend work lives here)
│   ├── src/app/      # Application source (Poetry package root)
│   ├── alembic/      # Database migrations
│   ├── tests/        # Integration tests
│   ├── pyproject.toml
│   └── Makefile
├── frontend/         # Frontend application (all frontend work lives here)
└── docs/backend/ARCHITECTURE.md   # Authoritative design reference — read this first
```

Rules are split by project. Apply only the section that matches the directory you are working in.

## Commands

### Dependencies

Always use the Poetry CLI to manage packages — never edit `pyproject.toml` manually for dependencies.

```bash
poetry install --no-root          # install all dependencies (initial setup)
poetry add <package>              # add a runtime dependency (latest stable)
poetry add --group dev <package>  # add a dev-only dependency
poetry remove <package>           # remove a dependency
poetry update <package>           # upgrade a specific package
poetry show --outdated            # list packages with newer versions available
```

### Development

```bash
make run              # uvicorn dev server (hot-reload)
make test             # run all tests
make db-generate msg="describe change"   # alembic autogenerate migration
make db-upgrade       # apply all pending migrations
make db-downgrade     # roll back one migration
```

Run a single test file:
```bash
poetry run pytest tests/integration/test_accounts_integration.py -v
```

Run a single test by name:
```bash
poetry run pytest -k "test_create_account" -v
```

## Architecture

The detailed design reference is [`docs/backend/ARCHITECTURE.md`](docs/backend/ARCHITECTURE.md). Below is a quick orientation.

### Request flow

```
HTTP → api/<resource>.py (router) → services/<resource>.py (business logic) → db/schema.py (ORM)
                                                                              ↓
HTTP ← models/<resource>.py (Pydantic response_model serialisation) ←────────┘
```

### Layer rules

- **`db/schema.py`** — single file for all SQLAlchemy models and enums. Every model extends `Base` (provides `id`, `created_at`, `updated_at`). Deletion is always soft: set `deleted_at = datetime.now(timezone.utc)`; all queries filter `.filter(Model.deleted_at.is_(None))`.
- **`models/`** — Pydantic schemas only. Three shapes per resource: `*Create`, `*Update` (all fields `Optional`, uses `model_dump(exclude_unset=True)`), `*Response` (has `model_config = ConfigDict(from_attributes=True)`).
- **`services/`** — business logic, owns all DB queries, raises `HTTPException` directly (404 not found, 409 conflict, 400 bad request, 422 validation, 503 downstream). All extend `BaseService(session)`.
- **`api/`** — thin routers, no logic. Each file defines a local `get_*_service()` factory and `*ServiceDep = Depends(...)`. Static routes must be declared **before** parameterised routes (`/{id}`). Do not add entries to `core/deps.py`.

### Resources

| Resource | ORM model | Notes |
|---|---|---|
| `accounts` | `Account` | `AccountType` enum: checking, savings, credit_card, cash, other |
| `categories` | `Category` | `TransactionType` enum: income, expense |
| `transactions` | `Transaction` | FK to account + optional category; eager-loads both via `joinedload` |
| `settings` | `Settings` | Singleton row (`id = "default"`); use `SettingsService.get_or_create_settings()` |

### Adding a new resource — checklist

1. `db/schema.py` — add ORM model + enums; add `deleted_at` if soft-deletable
2. `make db-generate msg="add <resource>"` — create migration
3. `models/<resource>.py` — `*Create`, `*Update`, `*Response`
4. `services/<resource>.py` — extend `BaseService`
5. `api/<resource>.py` — `APIRouter`, local `get_*_service`, thin handlers
6. `main.py` — `app.include_router(<resource>.router, prefix=PREFIX)`
7. `tests/integration/test_<resource>_integration.py` — use `client_with_test_db` fixture

### Testing

Integration tests use `TestClient` with an isolated per-test SQLite database (see `tests/conftest.py`). The `client_with_test_db` fixture spins up a fresh schema, overrides `get_db`, and tears it down after the test. No external database is needed to run tests.

### src/ layout & VSCode

The package is declared as `packages = [{ include = "app", from = "src" }]` in `pyproject.toml`. Pylance requires `"python.analysis.extraPaths": ["backend/src"]` in `.vscode/settings.json` (already committed) to resolve `app.*` imports.

---

# Frontend (`frontend/`)

> All frontend work lives in the `frontend/` directory. Apply the rules below when working on any file inside it. Backend rules above do **not** apply here.

## Commands

All commands must be run from `frontend/`.

```bash
# placeholder — populate once the frontend stack is decided
```

## Architecture

> To be defined. Add stack, folder structure, and conventions here when the frontend is set up.
