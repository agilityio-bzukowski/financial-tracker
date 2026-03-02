# External Integrations

**Analysis Date:** 2026-03-02

## APIs & External Services

**AI/LLM Services:**
- Anthropic Claude - AI analysis and insights (optional)
  - SDK/Client: `anthropic ^0.83.0`
  - Auth: `ANTHROPIC_API_KEY` environment variable
  - Config: `backend/src/app/core/config.py` - `anthropic_api_key` setting
  - Status: Configured but not actively integrated in current codebase

- OpenAI - Alternative AI provider (optional)
  - SDK/Client: `openai ^1.0.0`
  - Auth: `OPENAI_API_KEY` environment variable
  - Config: `backend/src/app/core/config.py` - `openai_api_key` setting
  - Status: Configured but not actively integrated in current codebase

- Ollama - Local LLM inference (optional)
  - Base URL: `OLLAMA_BASE_URL` environment variable (default: http://localhost:11434)
  - Status: Infrastructure URL configured, awaiting feature integration

## Data Storage

**Databases:**
- PostgreSQL 16
  - Connection: `DATABASE_URL` environment variable
  - Format: `postgresql://user:password@localhost:5432/financial_tracker`
  - Client: SQLAlchemy 2.0.46 ORM (`backend/src/app/db/session.py`)
  - Schemas: `backend/src/app/db/schema.py` - User, Category, Transaction entities
  - Migrations: Alembic 1.18.4 (`backend/alembic/`)

**File Storage:**
- Local filesystem only - No cloud storage integration present

**Caching:**
- None - No caching layer configured (Redis, Memcached, etc.)

**Session Storage:**
- Browser localStorage - JWT token storage (`frontend/src/lib/api-client.ts`)

## Authentication & Identity

**Auth Provider:**
- Custom JWT-based authentication
  - Implementation: `backend/src/app/services/auth.py`
  - Token Generation: `backend/src/app/core/security.py` - `create_access_token()`
  - Algorithm: HS256 (configurable via `JWT_ALGORITHM` setting)
  - Token Expiry: 30 days (configurable via `JWT_EXPIRE_DAYS` setting)
  - Secret Key: `backend/src/app/core/config.py` - `secret_key` (MUST change in production)

**Password Management:**
- Hashing: passlib with bcrypt (`backend/src/app/core/security.py`)
- Validation: `verify_password()` function
- Registration: `backend/src/app/services/auth.py` - `register()` endpoint

**Frontend Auth:**
- Token Storage: localStorage with key "token"
- Auto-Injection: Axios interceptor adds Bearer token to all requests (`frontend/src/lib/api-client.ts`)
- Auth Redirect: Auto-redirect to `/auth/login` on 401 responses

**Email/Password Reset (Infrastructure only):**
- SMTP configured but not implemented:
  - `SMTP_HOST` - Email server host
  - `SMTP_PORT` - Port (default: 587)
  - `SMTP_USER` - Credentials
  - `SMTP_PASSWORD` - Credentials
  - `SMTP_FROM` - Sender email

## Monitoring & Observability

**Error Tracking:**
- None - No error tracking service (Sentry, etc.) integrated

**Logs:**
- Console logging via Python logging (built-in)
- Frontend: Browser console (Vite dev server + production)

**Health Checks:**
- Backend: `GET /health` endpoint returns `{"status": "ok"}` (`backend/src/app/main.py`)
- Database: Docker Compose health check via `pg_isready` command

## CI/CD & Deployment

**Hosting:**
- Not configured - Development-only setup

**CI Pipeline:**
- None - No GitHub Actions, GitLab CI, or other CI service configured

**Build Commands:**
- Frontend: `pnpm build` - Type-check + Vite production build
- Backend: Poetry handles packaging (no explicit build command)

**Container Orchestration:**
- Docker Compose for local development only
- No Kubernetes or cloud deployment configuration

## Environment Configuration

**Required Environment Variables:**

Frontend:
- `VITE_API_URL` - API base URL (default: http://localhost:8000/api)

Backend:
- `DATABASE_URL` - PostgreSQL connection string (required)
- `ANTHROPIC_API_KEY` - Claude API key (optional, empty by default)
- `OPENAI_API_KEY` - OpenAI API key (optional, empty by default)

Optional (with defaults):
- `OLLAMA_BASE_URL` - Ollama server (default: http://localhost:11434)
- `JWT_ALGORITHM` - Token algorithm (default: HS256)
- `JWT_EXPIRE_DAYS` - Token expiry (default: 30)
- `SECRET_KEY` - JWT signing key (default: "change-me-in-production")
- `FRONTEND_URL` - For password reset emails (default: http://localhost:5173)
- SMTP settings (optional, for email delivery)

**Secrets Location:**
- `.env` file (git-ignored)
- Docker Compose hardcoded for PostgreSQL (development only)

## Webhooks & Callbacks

**Incoming:**
- None - No webhook endpoints implemented

**Outgoing:**
- None - No webhook delivery to external services

## API Architecture

**Frontend to Backend Communication:**
- HTTP REST API via axios client (`frontend/src/lib/api-client.ts`)
- Base URL: `http://localhost:8000/api` (development)
- CORS: Enabled for all origins in FastAPI (`backend/src/app/main.py`)
  - `allow_origins=["*"]`
  - `allow_credentials=True`
  - `allow_methods=["*"]`
  - `allow_headers=["*"]`

**Backend Endpoints:**
- `/api/auth` - Authentication (register, login) (`backend/src/app/api/auth.py`)
- `/api/users` - User management (`backend/src/app/api/users.py`)
- `/api/transactions` - Transaction CRUD (`backend/src/app/api/transactions.py`)
- `/api/categories` - Category management (`backend/src/app/api/categories.py`)
- `/health` - Health check endpoint

**Error Handling:**
- HTTP Status Codes: 200, 401 (auth), 409 (conflict), 500 (server error)
- 401 Responses trigger client-side logout and redirect to `/auth/login`

---

*Integration audit: 2026-03-02*
