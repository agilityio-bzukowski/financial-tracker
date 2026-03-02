# Technology Stack

**Analysis Date:** 2026-03-02

## Languages

**Primary:**
- Python 3.11+ - Backend API and services
- TypeScript 5.9 - Frontend application with strict mode enabled
- JavaScript - Frontend build tooling and scripts

**Secondary:**
- SQL - Database queries via SQLAlchemy ORM

## Runtime

**Environment:**
- Node.js v22+ (frontend development and build)
- Python 3.11+ (backend API and services)

**Package Manager:**
- **Frontend:** pnpm (monorepo-aware Node package manager)
  - Lockfile: `frontend/pnpm-lock.yaml` (present)
- **Backend:** Poetry (Python dependency management)
  - Lockfile: `backend/poetry.lock` (Poetry-managed)

## Frameworks

**Core:**
- FastAPI ^0.132.0 - Backend REST API framework (`backend/src/app/main.py`)
- React 19.2.0 - Frontend UI framework (`frontend/src/main.tsx`)
- TanStack Router 1.162.9 - File-based routing for React (`frontend/vite.config.ts`)

**UI & Styling:**
- Tailwind CSS 4.2.1 - Utility-first CSS (`frontend/src/`)
- Radix UI 1.4.3 - Accessible component primitives (ShadCN components)
- class-variance-authority 0.7.1 - Component variant management
- lucide-react 0.575.0 - Icon library

**State Management & Data:**
- TanStack React Query 5.90.21 - Server state management (`frontend/src/features/*/queries.ts`)
- SQLAlchemy 2.0.46 - Python ORM (`backend/src/app/db/schema.py`)

**Forms & Validation:**
- React Hook Form 7.71.2 - Frontend form state
- Zod 4.3.6 - TypeScript-first schema validation
- Pydantic 2.0+ - Python data validation and settings (`backend/src/app/core/config.py`)

**Dev/Build:**
- Vite 7.3.1 - Frontend build tool and dev server (`frontend/vite.config.ts`)
- @vitejs/plugin-react 5.1.1 - React plugin for Vite
- @tanstack/router-plugin 1.162.9 - File-based routing plugin
- @tailwindcss/vite 4.2.1 - Tailwind CSS Vite integration

**Testing:**
- pytest 9.0.2 - Backend test framework (`backend/pyproject.toml`)
- pytest-asyncio 1.3.0 - Async test support for backend
- httpx 0.28.1 - Async HTTP client for backend tests

**Linting & Code Quality:**
- ESLint 9.39.1 - JavaScript/TypeScript linting (`frontend/eslint.config.js`)
- typescript-eslint 8.48.0 - TypeScript ESLint rules
- eslint-plugin-react-hooks 7.0.1 - React hooks lint rules
- eslint-plugin-react-refresh 0.4.24 - React fast refresh lint rules

## Key Dependencies

**Critical:**
- FastAPI ^0.132.0 - Core backend framework
- SQLAlchemy ^2.0.46 - Database ORM enabling migrations and model-driven development
- React ^19.2.0 - Core frontend UI framework
- TanStack React Query ^5.90.21 - Server state synchronization (critical for transaction/category data)

**Infrastructure:**
- psycopg2-binary ^2.9.11 - PostgreSQL adapter for Python
- Alembic ^1.18.4 - Database migration tool (`backend/alembic/`)
- Uvicorn ^0.30.0 (standard extras) - ASGI server for FastAPI (`backend/src/app/main.py`)
- python-dotenv ^1.2.1 - Environment variable management

**Authentication & Security:**
- passlib ^1.7.4 (bcrypt) - Password hashing (`backend/src/app/core/security.py`)
- python-jose ^3.5.0 (cryptography) - JWT token generation and validation
- pydantic-settings ^2.13.1 - Type-safe configuration management

**HTTP & Networking:**
- axios ^1.13.5 - Frontend HTTP client (`frontend/src/lib/api-client.ts`)
- httpx ^0.28.1 - Backend HTTP client for async requests

**AI Integration (Optional - Config Available):**
- anthropic ^0.83.0 - Claude AI client (optional via `ANTHROPIC_API_KEY`)
- openai ^1.0.0 - OpenAI client (optional via `OPENAI_API_KEY`)

**UI & Theme:**
- next-themes ^0.4.6 - Dark/light mode theme management
- sonner ^2.0.7 - Toast notification library
- clsx ^2.1.1 - Conditional CSS class utility
- tailwind-merge ^3.5.0 - Merge Tailwind classes intelligently
- date-fns ^4.1.0 - Date utility library

**Form Utilities:**
- @hookform/resolvers ^5.2.2 - Connect Hook Form with validation libraries

## Configuration

**Environment:**
- `.env` file - Environment variable configuration
- `.env.example` - Reference template
- Backend uses `app/core/config.py` with Pydantic Settings for typed config
- Frontend uses Vite environment variables (VITE_* prefix) accessed via `import.meta.env`

**Key Environment Variables:**
- `DATABASE_URL` - PostgreSQL connection string (required)
- `AI_PROVIDER` - Provider selection: "anthropic" or "openai" (optional)
- `ANTHROPIC_API_KEY` - Claude API key (optional)
- `OPENAI_API_KEY` - OpenAI API key (optional)
- `OLLAMA_BASE_URL` - Local Ollama server URL (default: http://localhost:11434)
- `VITE_API_URL` - Frontend API base URL (default: http://localhost:8000/api)

**Build:**
- `frontend/vite.config.ts` - Vite configuration with TanStack Router and Tailwind plugins
- `frontend/tsconfig.json` - TypeScript strict mode enabled (ES2022 target, ESNext modules)
- `frontend/eslint.config.js` - Flat config ESLint with React Hooks rules
- `backend/pyproject.toml` - Poetry project configuration
- `backend/alembic.ini` - Alembic migration configuration

## Platform Requirements

**Development:**
- Node.js 22+ (verified: v22.17.0)
- Python 3.11+ (verified: 3.14.3)
- pnpm (Node package manager)
- Poetry (Python package manager)
- PostgreSQL 16 (via Docker Compose)

**Production:**
- Node.js 22+ (frontend build artifacts are static)
- Python 3.11+ runtime
- PostgreSQL 16+ database
- CORS middleware configured in FastAPI for cross-origin requests

**Local Development Stack:**
- Docker & Docker Compose - PostgreSQL database (`docker-compose.yml`)
  - Image: postgres:16-alpine
  - Port: 5432
  - Database: financial_tracker
  - Volume: `postgres_data`

---

*Stack analysis: 2026-03-02*
