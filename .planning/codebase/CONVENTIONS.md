# Coding Conventions

**Analysis Date:** 2026-03-02

## Naming Patterns

**Files:**
- PascalCase for React components: `TransactionList.tsx`, `AuthShell.tsx`
- camelCase for utility/hook files: `api-client.ts`, `conftest.py`
- camelCase for service/model files: `users.py`, `transactions.py`
- kebab-case for route files: `_authenticated.tsx`, `_authenticated/transactions.tsx`

**Functions:**
- camelCase for all functions: `listTransactions()`, `createUser()`, `handleRowClick()`
- Prefix React hooks with `use`: `useTransactions()`, `useLogin()`, `useDeleteTransaction()`
- Prefix event handlers with `handle`: `handleCreate()`, `handleDelete()`, `handleParamsChange()`
- Prefix API request functions with verb: `createTransaction()`, `updateUser()`, `deleteMe()`
- snake_case for Python functions: `list_users()`, `create_user()`, `get_current_user()`

**Variables:**
- camelCase in TypeScript/React: `editingTransaction`, `isError`, `onParamsChange`
- snake_case in Python: `user_id`, `page_size`, `hashed_password`
- Prefix booleans with `is` or `on`: `isPending`, `isError`, `onSuccess`

**Types:**
- PascalCase for all type/interface names: `UserCreate`, `TransactionResponse`, `ListTransactionsParams`
- Include suffix for request/response types: `CreateTransactionBody`, `UpdateTransactionBody`, `UserResponse`
- Use `Props` suffix for React component prop interfaces: `TransactionListProps`
- Use generic container names: `PaginatedResponse<T>`, `BaseModel` (Pydantic)

## Code Style

**Formatting:**
- TypeScript/React: ESLint with TypeScript support (no Prettier detected, using ESLint for consistency)
- Python: No formatter configured (likely black available but not enforced)
- 2-space indentation for TypeScript/React (Vite default)
- 4-space indentation for Python (standard)

**Linting:**
- Frontend: ESLint with configs in `frontend/eslint.config.js`
  - Extends: `@eslint/js`, `typescript-eslint`, `react-hooks`, `react-refresh`
  - Strict TypeScript checking enabled
  - ECMAScript 2020+
- Backend: No linter configured (pytest runs but no flake8/pylint in pyproject.toml)

**TypeScript Strictness:**
- `strict: true` in `frontend/tsconfig.json`
- `noUnusedLocals: true` - unused variables flagged
- `noUnusedParameters: true` - unused parameters flagged
- `noFallthroughCasesInSwitch: true` - require breaks in switch
- `noUncheckedSideEffectImports: true` - warn about side-effects on imports
- `verbatimModuleSyntax: true` - explicit type/value imports

## Import Organization

**Order:**
1. External libraries (react, axios, fastapi, sqlalchemy)
2. Type imports (from own types module)
3. Internal absolute imports (using `@/` alias in frontend)
4. Internal relative imports (./api, ./types in same feature)

**Pattern (Frontend):**
```typescript
import { useMutation } from "@tanstack/react-query"
import { useRouter } from "@tanstack/react-router"
import type { LoginRequest } from "./types"
import { authApi } from "./api"
```

**Pattern (Backend):**
```python
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import CurrentUser
from app.services.users import UsersService
```

**Path Aliases:**
- Frontend: `@/*` maps to `./src/*` in `frontend/tsconfig.json` and `frontend/vite.config.ts`
- Use absolute imports consistently: `import { apiClient } from "@/lib/api-client"`

## Error Handling

**Patterns:**
- Backend raises `HTTPException` with specific status codes: `404`, `409`, `401`, `422`
- Frontend uses axios interceptors for global error handling
- 401 responses trigger logout and redirect to `/auth/login`
- Test assertions check both status codes and response body content
- Validation errors use Pydantic field validators with clear messages

**HTTP Status Codes:**
- `201` for successful POST (created)
- `200` for successful GET/PATCH
- `204` for successful DELETE (no content)
- `401` for unauthenticated requests
- `404` for not found or access denied
- `409` for conflicts (duplicate email)
- `422` for validation errors

**Error Messages:**
- Python: Clear detail messages in HTTPException: `"User not found"`, `"Email already registered"`
- Frontend: Toast notifications with `sonner` library for user feedback
- Undo actions provided for destructive operations

## Logging

**Framework:** No centralized logging configured - uses Python exceptions and frontend console errors

**Patterns:**
- Backend: Exceptions bubble up with HTTPException (implicit logging via FastAPI)
- Frontend: Console errors from axios interceptors and React errors
- No debug logging observed - errors handled through exceptions

## Comments

**When to Comment:**
- Used for test section headers (Python): `# ---------------------------------------------------------------------------`
- Used for logical groupings in React: `/* Filters */`, `/* Content */`
- Path conflict warnings: `/me must be defined before /{user_id}` in `backend/src/app/api/users.py:31`

**JSDoc/TSDoc:**
- Not heavily used - minimal to no JSDoc annotations observed
- Type safety via TypeScript inference preferred

## Function Design

**Size:** Functions average 5-30 lines - reasonably focused

**Parameters:**
- Use named parameters for clarity: `service: TransactionsService = TransactionsServiceDep`
- Depends() pattern for FastAPI dependency injection
- Frontend: Props objects for components, individual params for hooks

**Return Values:**
- Backend services return domain models or None: `User`, `list[User]`, `None`
- API routes map to Pydantic response models
- Frontend hooks return mutation/query objects from TanStack
- Promise-based returns in API clients with `.then()` chaining for type inference

**Error Returns:**
- Backend: Raise HTTPException (never return error objects)
- Frontend: Reject promises, handle in interceptors or mutation callbacks
- No nullable/optional return patterns for errors - exceptions preferred

## Module Design

**Exports:**
- Frontend services export const objects: `export const authApi = { ... }`
- Frontend hooks export named functions: `export function useRegister() { ... }`
- Python services export classes: `class UsersService(BaseService): ...`
- Python models export Pydantic classes: `class UserCreate(BaseModel): ...`

**Barrel Files:**
- Used in `backend/src/app/models/__init__.py` and `backend/src/app/services/__init__.py`
- Frontend: Minimal barrel files, imports from specific modules
- Pattern: Import from feature subdirectories (e.g., `@/features/auth/api`)

**Feature Structure:**
- Frontend: Features organized by domain (`auth/`, `transactions/`, `categories/`)
  - Each feature has: `api.ts`, `types.ts`, `hooks.ts`, `queries.ts`, `components/`
- Backend: Organized by layer (`api/`, `services/`, `models/`, `db/`)
  - Cross-cutting: `core/` (security, config), `db/` (session, schema)

## Dependency Injection

**Frontend:**
- React Query for server state
- React Context implied but not heavily used
- Hooks as primary composition mechanism

**Backend:**
- FastAPI `Depends()` for service injection
- Pattern: Define service factory, then `Depends(get_users_service)` creates type alias
  - `UsersServiceDep = Depends(get_users_service)` used as default parameter
- Session injected via `Depends(get_db)`
- Authentication via `Depends(oauth2_scheme)` and custom `get_current_user`

---

*Convention analysis: 2026-03-02*
