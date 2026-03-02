# Codebase Structure

**Analysis Date:** 2026-03-02

## Directory Layout

```
financial-tracker/
├── backend/                        # FastAPI backend service
│   ├── src/app/
│   │   ├── main.py                # FastAPI app instance and router registration
│   │   ├── api/                   # Route handlers (one file per resource)
│   │   │   ├── auth.py            # POST /auth/register, /auth/login
│   │   │   ├── users.py           # GET /users/me
│   │   │   ├── transactions.py    # CRUD endpoints for transactions
│   │   │   └── categories.py      # CRUD endpoints for categories
│   │   ├── models/                # Pydantic request/response schemas
│   │   │   ├── auth.py            # LoginRequest, RegisterRequest, TokenResponse
│   │   │   ├── user.py            # UserResponse
│   │   │   ├── transaction.py     # TransactionCreate, TransactionUpdate, TransactionResponse, TransactionFilters
│   │   │   └── category.py        # CategoryCreate, CategoryResponse
│   │   ├── services/              # Business logic layer
│   │   │   ├── base.py            # BaseService class with session
│   │   │   ├── auth.py            # AuthService (login, register)
│   │   │   ├── users.py           # UsersService
│   │   │   ├── transactions.py    # TransactionsService (queries, CRUD, filtering)
│   │   │   ├── categories.py      # CategoriesService
│   │   │   └── filters.py         # FilterSpec, apply_filters utility
│   │   ├── db/
│   │   │   ├── schema.py          # All SQLAlchemy ORM models: User, Category, Transaction
│   │   │   ├── session.py         # Engine, SessionLocal, get_db dependency
│   │   │   └── seed.py            # Default data seeding (idempotent)
│   │   └── core/
│   │       ├── config.py          # Settings (pydantic-settings from .env)
│   │       └── security.py        # JWT, password hashing, CurrentUser dependency
│   ├── tests/
│   │   ├── conftest.py            # client_with_test_db fixture
│   │   ├── integration/           # Full HTTP tests via TestClient
│   │   │   ├── test_auth_integration.py
│   │   │   ├── test_users_integration.py
│   │   │   ├── test_transactions_integration.py
│   │   │   └── test_categories_integration.py
│   │   └── unit/                  # Pure logic tests (no DB or HTTP)
│   │       └── test_filters.py
│   ├── alembic/                   # Database migrations
│   │   ├── env.py                 # Alembic configuration
│   │   └── versions/              # Auto-generated .py migration files
│   ├── Makefile                   # Build commands (run, test, db-generate, etc.)
│   └── pyproject.toml             # Poetry dependencies and project config
│
├── frontend/                       # React + TypeScript frontend
│   ├── src/
│   │   ├── main.tsx               # React 19 entry point; renders App
│   │   ├── routes/                # TanStack Router file-based routes
│   │   │   ├── __root.tsx         # Root layout: QueryClientProvider, ThemeProvider, global shell
│   │   │   ├── index.tsx          # Dashboard page
│   │   │   ├── _authenticated.tsx # Auth guard layout; checks localStorage.token
│   │   │   ├── _authenticated/
│   │   │   │   ├── index.tsx      # Dashboard page
│   │   │   │   └── transactions.tsx # Transactions page with filters
│   │   │   └── auth/
│   │   │       ├── login.tsx      # Login form
│   │   │       └── register.tsx   # Registration form
│   │   ├── features/              # Feature-scoped modules (one per backend resource)
│   │   │   ├── auth/
│   │   │   │   ├── api.ts         # loginApi, registerApi, getCurrentUserApi
│   │   │   │   ├── types.ts       # Auth-specific types (LoginCredentials, etc.)
│   │   │   │   ├── hooks.ts       # useLoginMutation, useRegisterMutation, useCurrentUser
│   │   │   │   └── components/    # AuthShell, LoginForm, RegisterForm, ErrorBanner
│   │   │   ├── transactions/
│   │   │   │   ├── api.ts         # transactionsApi with typed fetch functions
│   │   │   │   ├── queries.ts     # transactionKeys factory, useTransactions, useCreateTransaction, etc.
│   │   │   │   └── components/
│   │   │   │       ├── TransactionList.tsx
│   │   │   │       ├── TransactionTable.tsx
│   │   │   │       ├── TransactionModal.tsx
│   │   │   │       ├── TransactionForm.tsx
│   │   │   │       ├── TransactionFilterBar.tsx
│   │   │   │       └── TransactionPagination.tsx
│   │   │   ├── categories/
│   │   │   │   ├── api.ts         # categoriesApi
│   │   │   │   └── queries.ts     # categoryKeys, useCategories, useCreateCategory
│   │   │   ├── navigation/
│   │   │   │   └── components/
│   │   │   │       └── AppNavbar.tsx
│   │   │   └── dashboard/
│   │   │       ├── data/
│   │   │       │   └── mockData.ts # Demo data for dashboard
│   │   │       └── components/
│   │   │           ├── StatCards.tsx
│   │   │           ├── SpendingByCategory.tsx
│   │   │           └── RecentTransactions.tsx
│   │   ├── components/            # Shared UI components (not feature-specific)
│   │   │   ├── ui/                # ShadCN primitives (auto-generated, never hand-edit)
│   │   │   │   ├── button.tsx
│   │   │   │   ├── input.tsx
│   │   │   │   ├── table.tsx
│   │   │   │   ├── dialog.tsx
│   │   │   │   ├── form.tsx
│   │   │   │   ├── select.tsx
│   │   │   │   ├── card.tsx
│   │   │   │   └── [other primitives].tsx
│   │   │   ├── theme-provider.tsx
│   │   │   └── AppShell.tsx       # Composite components
│   │   ├── lib/
│   │   │   ├── api-client.ts      # axios instance with JWT interceptor
│   │   │   └── utils.ts           # cn() helper for class merging
│   │   ├── types/
│   │   │   └── api.ts             # TypeScript interfaces: Transaction, Category, User, PaginatedResponse<T>
│   │   ├── assets/                # Images, icons (if any)
│   │   └── routeTree.gen.ts       # Auto-generated by TanStack Router (never edit)
│   ├── index.html                 # HTML entry point
│   ├── vite.config.ts             # Vite build config
│   ├── tsconfig.json              # TypeScript config with path aliases (@/)
│   └── package.json               # pnpm dependencies and scripts
│
├── docs/                          # Project documentation
│   ├── backend/
│   │   ├── ARCHITECTURE.md        # Backend layer responsibilities
│   │   ├── CODING_PATTERNS.md     # ORM, service, router, test patterns
│   │   └── IMPLEMENTATION_CHECKLIST.md
│   └── frontend/
│       ├── ARCHITECTURE.md        # Frontend layer responsibilities, TanStack Query best practices
│       ├── CODING_PATTERNS.md     # Query hooks, form patterns, component patterns
│       └── IMPLEMENTATION_CHECKLIST.md
│
├── .planning/                     # GSD phase planning
│   └── codebase/                  # Codebase analysis documents (ARCHITECTURE.md, STRUCTURE.md, etc.)
│
├── docker-compose.yml             # PostgreSQL + pgAdmin for local dev
├── pyproject.toml                 # Python project config (Poetry)
├── CLAUDE.md                      # Instructions for Claude Code
└── README.md                      # (Empty placeholder)
```

## Directory Purposes

### Backend: `src/app/`

**Purpose:** All application code follows a layered structure with clear separation of concerns.

**Contains:**
- HTTP routing (`api/`)
- Request/response validation (`models/`)
- Business logic (`services/`)
- Data models and persistence (`db/`)
- Infrastructure (`core/`)

### Backend: `src/app/api/`

**Purpose:** HTTP endpoint definitions

**Contains:** One file per resource (auth, users, transactions, categories)

**Key files:**
- `auth.py` — Authentication endpoints (register, login)
- `transactions.py` — Transaction CRUD (GET /, POST /, GET /{id}, PATCH /{id}, DELETE /{id}, POST /{id}/restore)
- `categories.py` — Category CRUD
- `users.py` — User profile endpoints

**Pattern:** Each file defines:
```python
router = APIRouter(prefix="/resource", tags=["resource"])

def get_resource_service(db: Session = Depends(get_db)) -> ResourceService:
    return ResourceService(session=db)

ResourceServiceDep = Depends(get_resource_service)

@router.get("/")
def list_resources(current_user: CurrentUser, service: ResourceService = ResourceServiceDep):
    return service.list_resources(user_id=current_user.id)
```

### Backend: `src/app/models/`

**Purpose:** Pydantic schemas for validation and serialization

**Contains:** One file per resource

**Key files:**
- `transaction.py` — `TransactionCreate`, `TransactionUpdate`, `TransactionResponse`, `TransactionFilters`, `PaginatedTransactionResponse`
- `category.py` — `CategoryCreate`, `CategoryResponse`
- `user.py` — `UserResponse`
- `auth.py` — `LoginRequest`, `RegisterRequest`, `TokenResponse`

**Pattern:** Each resource defines three shapes:
- `*Create` — Required fields for POST requests
- `*Update` — Optional fields for PATCH requests (use `model_dump(exclude_unset=True)`)
- `*Response` — All fields including id, timestamps, relationships

### Backend: `src/app/services/`

**Purpose:** Business logic, all queries, access control

**Contains:** One file per resource plus utilities

**Key files:**
- `base.py` — `BaseService(session)` base class
- `filters.py` — `FilterSpec`, `apply_filters()` utility
- `transactions.py` — `TransactionsService` with filtering, pagination, ownership checks
- `categories.py` — `CategoriesService`
- `users.py` — `UsersService`
- `auth.py` — `AuthService` (login, register)

**Pattern:** Every service method queries via `_query(user_id)` to enforce ownership:

```python
class TransactionsService(BaseService):
    def _query(self, user_id: uuid.UUID):
        return (
            self.session.query(Transaction)
            .options(joinedload(Transaction.category))  # Eager load to avoid N+1
            .filter(Transaction.user_id == user_id, Transaction.deleted_at.is_(None))
        )

    def list_transactions(self, user_id, page, page_size, **filters):
        query = self._query(user_id)
        query = apply_filters(query, TRANSACTION_FILTERS, filters)
        # ... pagination and sorting
```

### Backend: `src/app/db/`

**Purpose:** Data layer — models, sessions, migrations

**Contains:**
- `schema.py` — All SQLAlchemy ORM models
- `session.py` — Engine, SessionLocal, get_db dependency
- `seed.py` — Default data (categories, test users)

**Key files:**
- `schema.py` — `User`, `Category`, `Transaction` models with relationships and soft deletes
- `session.py` — FastAPI dependency for database sessions

### Backend: `alembic/`

**Purpose:** Database schema versioning

**Contains:** Auto-generated migration files (never edited manually)

**Workflow:**
```bash
# After changing db/schema.py:
make db-generate msg="add field to transaction"  # Creates versions/xxxxx_add_field.py
make db-upgrade                                   # Applies all pending migrations
```

### Backend: `tests/`

**Purpose:** Test organization

**Contains:**
- `conftest.py` — `client_with_test_db` fixture (creates SQLite test DB)
- `integration/` — Full HTTP tests via TestClient
- `unit/` — Pure logic tests (filters, validators)

**Structure:**
```
tests/
├── integration/
│   ├── test_transactions_integration.py
│   ├── test_categories_integration.py
│   └── ...
└── unit/
    └── test_filters.py
```

### Frontend: `src/routes/`

**Purpose:** URL structure via file-based routing

**Contains:** TanStack Router route definitions

**File naming:**
- `__root.tsx` — Global layout and providers
- `index.tsx` → `/`
- `_authenticated.tsx` → Layout group (auth guard)
- `_authenticated/index.tsx` → `/_authenticated` (dashboard)
- `_authenticated/transactions.tsx` → `/_authenticated/transactions`
- `auth/login.tsx` → `/auth/login`
- `auth/register.tsx` → `/auth/register`

**Pattern:** Routes are thin; they read params and render feature components:

```typescript
export const Route = createFileRoute("/_authenticated/transactions")({
  validateSearch: (search) => ({
    page: Number(search.page) || 1,
    sort_by: (search.sort_by as string) || "date",
  }),
  component: TransactionsPage,
})

function TransactionsPage() {
  const params = Route.useSearch()
  return <TransactionList params={params} onParamsChange={...} />
}
```

### Frontend: `src/features/`

**Purpose:** Feature-scoped modules with API, queries, and components

**Contains:** One directory per backend resource

**Key directories:**
- `features/transactions/` — All transaction UI logic
- `features/categories/` — Category management
- `features/auth/` — Authentication flows
- `features/navigation/` — App navigation
- `features/dashboard/` — Dashboard analytics

**Structure per feature:**
```
features/transactions/
├── api.ts                 # Raw fetch functions
├── queries.ts             # React Query hooks + query key factory
└── components/
    ├── TransactionList.tsx
    ├── TransactionTable.tsx
    ├── TransactionModal.tsx
    ├── TransactionForm.tsx
    ├── TransactionFilterBar.tsx
    └── TransactionPagination.tsx
```

### Frontend: `src/features/{resource}/api.ts`

**Purpose:** HTTP layer — raw fetch wrappers

**Contains:** Plain JS functions (no React/hooks)

**Pattern:**

```typescript
export const transactionsApi = {
  list(params: ListTransactionsParams = {}) {
    return apiClient
      .get<PaginatedResponse<Transaction>>("/transactions/", { params })
      .then((r) => r.data)
  },

  create(body: CreateTransactionBody) {
    return apiClient
      .post<Transaction>("/transactions/", body)
      .then((r) => r.data)
  },
}
```

### Frontend: `src/features/{resource}/queries.ts`

**Purpose:** React Query integration — cache management and hooks

**Contains:**
- Query key factory
- `useQuery` hooks (data fetching)
- `useMutation` hooks (mutations with cache invalidation)

**Pattern:**

```typescript
export const transactionKeys = {
  all: ["transactions"] as const,
  lists: () => [...transactionKeys.all, "list"] as const,
  list: (params) => [...transactionKeys.lists(), params] as const,
  detail: (id: string) => [...transactionKeys.all, "detail", id] as const,
}

export function useTransactions(params: ListTransactionsParams = {}) {
  return useQuery({
    queryKey: transactionKeys.list(params),
    queryFn: () => transactionsApi.list(params),
  })
}

export function useCreateTransaction() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (body: CreateTransactionBody) => transactionsApi.create(body),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: transactionKeys.lists() })
    },
  })
}
```

### Frontend: `src/features/{resource}/components/`

**Purpose:** Feature-specific React components

**Contains:** Forms, lists, modals, tables for the resource

**Pattern:** Components use hooks from `queries.ts` and ShadCN primitives:

```typescript
export function TransactionList({ params, onParamsChange }) {
  const { data, isPending } = useTransactions(params)
  const createMutation = useCreateTransaction()

  if (isPending) return <Skeleton />
  return <TransactionTable items={data.items} onRowClick={...} />
}
```

### Frontend: `src/components/ui/`

**Purpose:** ShadCN-generated Radix UI wrappers

**Contains:** Buttons, inputs, tables, dialogs, forms, etc.

**Rule:** Never hand-edit; regenerate with CLI:
```bash
pnpm dlx shadcn@latest add button  # Updates or adds button component
```

### Frontend: `src/lib/api-client.ts`

**Purpose:** HTTP client with interceptors

**Contains:** Axios instance with:
- Base URL configuration
- JWT Bearer token injection (request interceptor)
- 401 redirect to login (response interceptor)

**Code:**

```typescript
export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? "http://localhost:8000/api",
})

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("token")
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token")
      window.location.href = "/auth/login"
    }
    return Promise.reject(error)
  }
)
```

### Frontend: `src/types/api.ts`

**Purpose:** TypeScript interfaces mirroring backend schemas

**Contains:** `Transaction`, `Category`, `User`, `PaginatedResponse<T>`, etc.

**Pattern:** Keep in sync with backend Pydantic models:

```typescript
export interface Transaction {
  id: string
  user_id: string
  type: "income" | "expense"
  description: string
  amount: number
  date: string
  category: Category | null
  // ...
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}
```

## Key File Locations

### Backend Entry Points

- `backend/src/app/main.py` — FastAPI app instance
- `backend/alembic/env.py` — Migration runner
- `Makefile` — Development commands (run, test, db-generate)

### Frontend Entry Points

- `frontend/src/main.tsx` — React 19 app mount
- `frontend/src/routes/__root.tsx` — Root layout and providers
- `frontend/vite.config.ts` — Build configuration

### Configuration Files

- `backend/src/app/core/config.py` — Settings (env vars)
- `frontend/.env` — Frontend environment variables (e.g., VITE_API_URL)
- `docker-compose.yml` — PostgreSQL, pgAdmin
- `pyproject.toml` — Backend dependencies

### Core Logic

- `backend/src/app/services/transactions.py` — Transaction business logic
- `backend/src/app/db/schema.py` — All ORM models
- `frontend/src/features/transactions/queries.ts` — Transaction state management
- `frontend/src/features/transactions/components/TransactionList.tsx` — Main transaction UI

### Testing

- `backend/tests/conftest.py` — Test database fixture
- `backend/tests/integration/test_transactions_integration.py` — Full HTTP tests
- `backend/tests/unit/test_filters.py` — Pure logic tests

## Naming Conventions

### Files

**Backend:**
- Modules: `snake_case.py` (e.g., `transactions.py`, `auth.py`)
- Classes: `PascalCase` (e.g., `TransactionsService`, `TransactionCreate`)
- Functions: `snake_case` (e.g., `list_transactions`, `get_transaction`)

**Frontend:**
- Components: `PascalCase.tsx` (e.g., `TransactionList.tsx`, `TransactionModal.tsx`)
- Hooks/utilities: `camelCase.ts` (e.g., `api.ts`, `queries.ts`, `useTransactions()`)
- Types: `PascalCase` (e.g., `Transaction`, `ListTransactionsParams`)

### Directories

**Backend:**
- Feature modules: `plural snake_case` (e.g., `transactions/`, `categories/`)
- Organizational: `lowercase` (e.g., `api/`, `services/`, `models/`, `db/`, `core/`)

**Frontend:**
- Feature modules: `singular lowercase` (e.g., `transactions/`, `categories/`, `auth/`)
- Routes: `snake_case` with prefixes (`_authenticated/`, `auth/`)
- Special files: `__root.tsx`, `_authenticated.tsx` (TanStack Router conventions)

## Where to Add New Code

### Adding a New Backend Resource (e.g., `accounts`)

1. **Create ORM model** → `backend/src/app/db/schema.py`
   - Add `Account` class extending `Base`
   - Include relationships, enums, validation logic

2. **Create request/response schemas** → `backend/src/app/models/account.py`
   - `AccountCreate`, `AccountUpdate`, `AccountResponse`, `PaginatedAccountResponse`
   - Add field validators and model validators

3. **Create service** → `backend/src/app/services/accounts.py`
   - Extend `BaseService`
   - Implement `_query(user_id)`, `list_accounts()`, `create_account()`, `get_account()`, etc.
   - Use `apply_filters()` if needed

4. **Create router** → `backend/src/app/api/accounts.py`
   - Define `get_accounts_service()` dependency
   - Create `AccountsServiceDep` alias
   - Implement endpoints (GET /, POST /, GET /{id}, PATCH /{id}, DELETE /{id})

5. **Register router** → `backend/src/app/main.py`
   - Add `app.include_router(accounts.router, prefix=PREFIX)`

6. **Create migrations** → `backend/alembic/versions/`
   - Run `make db-generate msg="add accounts table"`
   - Run `make db-upgrade`

7. **Add tests** → `backend/tests/integration/test_accounts_integration.py`

### Adding a New Frontend Resource (e.g., `budgets`)

1. **Add types** → `frontend/src/types/api.ts`
   - Add `Budget`, `CreateBudgetBody`, `UpdateBudgetBody` interfaces

2. **Create feature module** → `frontend/src/features/budgets/`
   - `api.ts` — `budgetsApi.list()`, `.create()`, `.update()`, `.delete()`
   - `queries.ts` — `budgetKeys` factory, `useBudgets()`, `useCreateBudget()`, `useUpdateBudget()`
   - `components/` — `BudgetList.tsx`, `BudgetForm.tsx`, etc.

3. **Create route** → `frontend/src/routes/_authenticated/budgets.tsx` (if needed)
   - Define search params validator
   - Render feature component with params

4. **Update navigation** → `frontend/src/features/navigation/components/AppNavbar.tsx`
   - Add link to `/budgets` route

### Adding Shared Components

**Location:** `frontend/src/components/` (not feature-specific)

**Naming:** `PascalCase.tsx` (e.g., `PageHeader.tsx`, `DataTable.tsx`)

**Pattern:** Build on ShadCN primitives; no business logic:

```typescript
export function PageHeader({ title, subtitle }) {
  return (
    <div className="mb-6">
      <h1 className="text-2xl font-bold">{title}</h1>
      {subtitle && <p className="text-gray-500">{subtitle}</p>}
    </div>
  )
}
```

### Adding Utilities

**Backend:** `backend/src/app/services/filters.py` (shared query utilities)

**Frontend:** `frontend/src/lib/utils.ts` (shared functions, `cn()` helper)

## Special Directories

### Backend: `.venv/`

**Purpose:** Virtual environment (Python dependencies)

**Generated:** Yes (created by `poetry install`)

**Committed:** No (excluded via .gitignore)

### Backend: `alembic/versions/`

**Purpose:** Database migration files

**Generated:** Auto-generated by Alembic (do not edit)

**Committed:** Yes (part of schema version control)

### Frontend: `src/components/ui/`

**Purpose:** ShadCN-generated Radix UI components

**Generated:** Yes (created by `pnpm dlx shadcn@latest add`)

**Committed:** Yes (part of source tree)

**Important:** Never hand-edit; re-run CLI to update

### Frontend: `dist/`

**Purpose:** Production build output (Vite)

**Generated:** Yes (created by `pnpm build`)

**Committed:** No (excluded via .gitignore)

### Frontend: `routeTree.gen.ts`

**Purpose:** Auto-generated by TanStack Router from file-based routes

**Generated:** Yes (created on `pnpm dev` or `pnpm build`)

**Committed:** Yes (needs to be in sync with routes/)

**Important:** Never hand-edit; let TanStack Router regenerate

---

*Structure analysis: 2026-03-02*
