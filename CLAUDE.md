# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository layout

```
financial-tracker/
├── backend/          # Python FastAPI application — see docs/backend/ARCHITECTURE.md
├── frontend/         # Frontend application
└── docs/             # Architecture and design references
```

Rules are split by project. Apply only the section that matches the directory you are working in.

---

# General Rules

## Context7

Always use Context7 when you need code generation, setup or configuration steps, or library/API documentation. Use the Context7 MCP tools to resolve library IDs and fetch docs automatically — do not wait to be asked.

## Writing Implementation Plans

Write high-quality, maintainable code while avoiding over-engineering. Be pragmatic and follow the guidelines in the docs first before blindly following industry standards.

Implementation plans must always include build, lint, and integration tests when necessary. Provide explicit test commands covering happy paths and edge cases.

## Implementation and Testing

Always include integration tests to cover important paths. Test suites must cover happy paths and edge cases. Tests should give high confidence while keeping coverage meaningful over exhaustive.

## Database Entities and Migrations

Never create migrations manually — always generate them from ORM model changes:

```bash
make db-generate msg="describe change"   # autogenerate migration from db/schema.py changes
make db-upgrade                          # apply all pending migrations
make db-downgrade                        # roll back one migration
```

---

# Backend (`backend/`)

> All backend work lives in `backend/`. For full architecture details see [`docs/backend/ARCHITECTURE.md`](docs/backend/ARCHITECTURE.md).

## Commands

### Dependencies

Always use the Poetry CLI — never edit `pyproject.toml` manually for dependencies.

```bash
poetry install --no-root          # install all dependencies (initial setup)
poetry add <package>              # add a runtime dependency
poetry add --group dev <package>  # add a dev-only dependency
poetry remove <package>           # remove a dependency
```

### Development

```bash
make run              # uvicorn dev server (hot-reload)
make test             # run all tests
```

Run a single test file:

```bash
poetry run pytest tests/integration/test_accounts_integration.py -v
```

Run a single test by name:

```bash
poetry run pytest -k "test_create_account" -v
```
