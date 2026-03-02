# Architecture

**Analysis Date:** 2026-03-02

## Pattern Overview

**Overall:** Layered full-stack architecture with clear separation of concerns. The backend follows a service-oriented pattern with dedicated layers for routing, business logic, and data access. The frontend uses a feature-first modular architecture with React Query for server state and TanStack Router for client-side navigation.

**Key Characteristics:**
- **Backend:** One file per layer per resource; thin routes, heavy services, single schema file
- **Frontend:** Feature-scoped modules co-locating API, queries, and components
- **State Management:** Server state in React Query cache; URL state in router search params; local state in components
- **Authentication:** JWT-based with Bearer tokens; decentralized enforcement at route level

## Layers

### Backend Layers

**`db/schema.py` — ORM Models:**
- Purpose: Single source of truth for all database entities
- Location: `backend/src/app/db/schema.py`
- Contains: SQLAlchemy declarative models with UUID PKs, timestamps, soft deletes, and relationships
- Depends on: sqlalchemy
- Used by: Services query this; migrations generated from changes here

**`models/` — Pydantic Request/Response Schemas:**
- Purpose: Validation and serialization contracts between HTTP clients and handlers
- Location: `backend/src/app/models/{resource}.py` (one per resource: `auth.py`, `user.py`, `transaction.py`, `category.py`)
- Contains: `*Create`, `*Update`, `*Response`, and `*Filters` Pydantic models with field validators
- Depends on: `app.db.schema` for enums and relationships
- Used by: Route handlers receive and return these; services accept them

**`services/` — Business Logic:**
- Purpose: All query construction, access control, and domain logic
- Location: `backend/src/app/services/{resource}.py` (one per resource: `auth.py`, `users.py`, `transactions.py`, `categories.py`)
- Contains: Service classes extending `BaseService`, owning all SQLAlchemy queries
- Depends on: `BaseService`, `db.schema`, filter specs
- Used by: Route handlers call service methods; services raise HTTPException for errors

**`api/` — Route Handlers:**
- Purpose: HTTP endpoint definitions and request routing
- Location: `backend/src/app/api/{resource}.py` (one per resource)
- Contains: FastAPI routers with endpoints; thin handlers that call services
- Depends on: services, models, security
- Used by: FastAPI includes these in `main.py` under `/api` prefix

**`core/` — Infrastructure:**
- Purpose: Cross-cutting configuration and authentication
- Location: `backend/src/app/core/` → `config.py`, `security.py`
- Contains: Settings (env vars), JWT creation/validation, password hashing, `CurrentUser` dependency
- Depends on: app-specific schemas and session
- Used by: All layers reference these

**`db/session.py` — Database Session:**
- Purpose: Engine and session lifecycle
- Location: `backend/src/app/db/session.py`
- Contains: SQLAlchemy engine creation, `SessionLocal` factory, `get_db()` FastAPI dependency
- Depends on: settings
- Used by: Services receive session via dependency injection; Alembic reads settings for migrations

### Frontend Layers

**`routes/` — Pages and Layouts:**
- Purpose: URL structure and page-level layout composition
- Location: `frontend/src/routes/*.tsx` (file-based routing with TanStack Router)
- Contains: `__root.tsx` (global providers), `_authenticated.tsx` (layout guard), resource pages like `_authenticated/transactions.tsx`
- Depends on: Feature components, TanStack Router hooks
- Used by: User navigation triggers route changes; routes render feature components
- Auth Flow: `_authenticated` routes check `localStorage.token` in `beforeLoad` hook; redirect to `/auth/login` if missing

**`features/<resource>/api.ts` — HTTP Functions:**
- Purpose: Raw fetch wrapper around backend endpoints
- Location: `frontend/src/features/{resource}/api.ts` (one per resource: `auth/api.ts`, `transactions/api.ts`, `categories/api.ts`)
- Contains: Plain JS functions returning Promises; no React or hooks
- Depends on: `lib/api-client.ts`
- Used by: `queries.ts` wraps these in React Query hooks

**`features/<resource>/queries.ts` — TanStack Query Hooks:**
- Purpose: Server state management and cache synchronization
- Location: `frontend/src/features/{resource}/queries.ts`
- Contains: Query key factories, `useQuery` hooks, `useMutation` hooks
- Depends on: `api.ts`, `@tanstack/react-query`
- Used by: Components call these hooks to fetch and mutate data

**`features/<resource>/components/*.tsx` — Feature UI:**
- Purpose: Resource-specific React components
- Location: `frontend/src/features/{resource}/components/*.tsx`
- Contains: Forms, lists, modals, tables specific to the resource
- Depends on: queries, `components/ui/`, types
- Used by: Routes render these; components orchestrate mutations and queries

**`components/ui/` — ShadCN Primitives:**
- Purpose: Auto-generated Radix UI component wrappers
- Location: `frontend/src/components/ui/*.tsx`
- Contains: Button, Input, Dialog, Table, Form, etc. (auto-generated, never hand-edit)
- Depends on: @radix-ui, tailwindcss
- Used by: Feature components and composite components build on these

**`lib/api-client.ts` — HTTP Client:**
- Purpose: Axios wrapper with auth and error handling
- Location: `frontend/src/lib/api-client.ts`
- Contains: Axios instance with base URL, request interceptor (adds JWT Bearer token), response interceptor (handles 401 redirects)
- Depends on: axios
- Used by: All `api.ts` files call `apiClient.get()`, `apiClient.post()`, etc.

**`types/api.ts` — Shared Types:**
- Purpose: TypeScript interfaces mirroring backend Pydantic schemas
- Location: `frontend/src/types/api.ts`
- Contains: `Transaction`, `Category`, `User`, `PaginatedResponse<T>`, etc.
- Depends on: None
- Used by: All feature modules import these for type safety

## Data Flow

### Create Transaction Flow

```
User clicks "Add Transaction" in TransactionsPage
  ↓
TransactionList opens TransactionModal
  ↓
TransactionModal renders TransactionForm (inputs, validation)
  ↓
User submits form
  ↓
useCreateTransaction() mutation is triggered
  ↓
transactionsApi.create(body) → apiClient.post("/transactions/", body)
  ↓
Backend receives at POST /api/transactions/
  → FastAPI router (api/transactions.py) calls service
  → TransactionsService.create_transaction(body, user_id) validates ownership
  → Inserts ORM model, returns TransactionResponse
  ↓
Frontend mutation succeeds
  → onSuccess callback: queryClient.invalidateQueries({queryKey: transactionKeys.lists()})
  → React Query refetches list automatically
  → useTransactions() hook re-renders with new data
  ↓
TransactionList re-renders with updated list
  → Toast notification shown
  → Modal closes
```

### List Transactions Flow with Filters

```
TransactionsPage route loads
  ↓
validateSearch extracts query params (page, sort_by, type, date_from, etc.)
  ↓
TransactionList receives params props
  ↓
useTransactions(params) query runs
  → transactionsApi.list(params) builds query string and calls GET /api/transactions/?...
  ↓
Backend receives at GET /api/transactions/?
  → FastAPI extracts filters via Depends(TransactionFilters)
  → Router calls TransactionsService.list_transactions(user_id, filters, pagination)
  → Service builds SQLAlchemy query with apply_filters(query, TRANSACTION_FILTERS, filters)
  → apply_filters maps filter specs to WHERE clauses
  → Joins Category eagerly via joinedload to avoid N+1
  → Returns paginated result: {items, total, page, page_size, total_pages}
  ↓
Frontend renders TransactionTable with items
  ↓
User changes filter (e.g., date range)
  ↓
TransactionFilterBar calls onParamsChange()
  ↓
TransactionsPage calls navigate({search: newParams})
  ↓
Route search params update
  ↓
useTransactions(params) detects new query key
  ↓
Automatic refetch with new filters
```

### Authentication Flow

```
User navigates to /auth/login
  ↓
Login route (routes/auth/login.tsx) renders LoginForm
  ↓
User submits credentials
  ↓
useLoginMutation() calls authApi.login(email, password)
  ↓
apiClient.post("/auth/login", {email, password})
  ↓
Backend receives at POST /api/auth/login
  → Router calls AuthService.login(email, password)
  → Service queries User by email
  → verify_password(password, hashed) checks credentials
  → create_access_token(user_id) generates JWT
  → Returns {access_token, token_type}
  ↓
Frontend stores token in localStorage
  ↓
useLoginMutation() onSuccess redirects to /
  ↓
User navigates to protected route
  ↓
_authenticated beforeLoad hook checks localStorage.token
  ↓
If token exists, allow; else redirect to /auth/login?redirect=...
  ↓
Subsequent requests: apiClient request interceptor adds Authorization: Bearer {token}
  ↓
If backend responds 401: response interceptor clears token and redirects to login
```

## State Management

| State Type | Where It Lives | How It Works |
|---|---|---|
| Server state (transactions, categories, users) | TanStack Query cache (`queryClient`) | Queries keyed by resource; mutations invalidate related keys |
| Navigation/pagination state | TanStack Router search params (`useSearch()`) | User updates params → navigate({search}) → route re-renders → query re-runs |
| Ephemeral UI state (modal open, form focus) | Component `useState` | Local to component; not synced to URL or server |
| Auth token | localStorage | Read on app start and per request; cleared on 401 |
| User session | JWT claims (decoded from token) | Stateless; re-validated per request on backend |

## Key Abstractions

### Backend: `BaseService` Pattern

**Purpose:** Enforce consistent service structure and session management

**Location:** `backend/src/app/services/base.py`

**Example Usage:**

```python
class TransactionsService(BaseService):
    def _query(self, user_id: uuid.UUID):
        return (
            self.session.query(Transaction)
            .options(joinedload(Transaction.category))
            .filter(Transaction.user_id == user_id, Transaction.deleted_at.is_(None))
        )

    def list_transactions(self, user_id, page, page_size, **filters):
        query = self._query(user_id)
        query = apply_filters(query, TRANSACTION_FILTERS, filters)
        ...
```

**Pattern:** Every service defines `_query(user_id)` as the base query with ownership filter and eager loads; all other methods start from `_query()` to ensure consistent filtering.

### Backend: `FilterSpec` Utility

**Purpose:** Declarative, reusable query filters

**Location:** `backend/src/app/services/filters.py`

**Example:**

```python
TRANSACTION_FILTERS = [
    FilterSpec("type", lambda v: Transaction.type == v),
    FilterSpec("category_id", lambda v: Transaction.category_id == v),
    FilterSpec("date_from", lambda v: Transaction.date >= datetime.combine(...)),
]

query = apply_filters(query, TRANSACTION_FILTERS, filters)
```

**Pattern:** Filters are applied via SQLAlchemy ORM; `apply_filters()` only adds WHERE clauses if the filter value is provided.

### Frontend: Query Key Factory Pattern

**Purpose:** Centralized cache key management and safe invalidation

**Location:** `frontend/src/features/{resource}/queries.ts`

**Example:**

```typescript
export const transactionKeys = {
  all: ["transactions"] as const,
  lists: () => [...transactionKeys.all, "list"] as const,
  list: (params) => [...transactionKeys.lists(), params] as const,
  detail: (id: string) => [...transactionKeys.all, "detail", id] as const,
}

// Usage in component:
queryClient.invalidateQueries({ queryKey: transactionKeys.lists() })
```

**Pattern:** Hierarchical keys enable precise cache invalidation (e.g., invalidate all transaction lists without touching individual detail queries).

### Frontend: Route Search Params for Pagination/Filtering

**Purpose:** Keep filter state in URL for bookmarkability and back-button support

**Location:** `frontend/src/routes/_authenticated/transactions.tsx`

**Example:**

```typescript
type TransactionSearch = {
  page?: number
  sort_by?: string
  type?: "income" | "expense"
  date_from?: string
}

export const Route = createFileRoute("/_authenticated/transactions")({
  validateSearch: (search) => ({ ... }),
  component: TransactionsPage,
})

// In component:
const searchParams = Route.useSearch()
const navigate = useNavigate({ from: Route.fullPath })

navigate({ search: { ...searchParams, page: 2 } })
```

**Pattern:** TanStack Router's type-safe search params replace Redux for pagination and filtering; URL reflects current state.

## Entry Points

### Backend Entry Point

**Location:** `backend/src/app/main.py`

**Responsibilities:**
- Create FastAPI app instance
- Register CORS middleware (allow all origins for dev)
- Include routers with `/api` prefix
- Health check endpoint

**Code:**
```python
app = FastAPI(title="Financial Tracker API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], ...)
app.include_router(auth.router, prefix=PREFIX)
app.include_router(users.router, prefix=PREFIX)
```

### Frontend Entry Point

**Location:** `frontend/src/routes/__root.tsx`

**Responsibilities:**
- Create and configure `QueryClient` (staleTime: 60s, retry: 1)
- Wrap app in `QueryClientProvider`
- Provide theme, tooltips, toasts
- Mount devtools

**Code:**
```typescript
const queryClient = new QueryClient({
  defaultOptions: { queries: { staleTime: 60_000, retry: 1 } }
})

export const Route = createRootRoute({
  component: () => (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <TooltipProvider>
          <Outlet />
          <Toaster />
        </TooltipProvider>
      </ThemeProvider>
    </QueryClientProvider>
  )
})
```

## Error Handling

### Backend Strategy

**Exceptions raised directly from services:** Services raise `HTTPException` with appropriate status codes:
- `404` — Resource not found (e.g., no transaction with ID)
- `403` — Ownership violation (e.g., user tries to access another user's transaction)
- `409` — Conflict (e.g., category already exists)

**Patterns:**

```python
def get_transaction(self, transaction_id: uuid.UUID, user_id: uuid.UUID) -> Transaction:
    transaction = self._query(user_id).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction
```

### Frontend Strategy

**Error states from React Query:** Each hook returns `{ data, isPending, isError }`:

```typescript
const { data, isPending, isError } = useTransactions(params)

if (isPending) return <Skeleton />
if (isError) return <ErrorAlert message="Failed to load transactions" />
return <TransactionTable items={data.items} />
```

**Global 401 handling:** API client interceptor on 401 clears token and redirects to login:

```typescript
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

## Cross-Cutting Concerns

**Logging:** Not currently implemented at the application level; FastAPI access logs via uvicorn, browser console logs as needed.

**Validation:**
- Backend: Pydantic `@field_validator` and `@model_validator(mode="after")` on request schemas
- Frontend: React Hook Form with client-side validation in TransactionForm components

**Authentication:**
- Backend: JWT Bearer token; `CurrentUser` dependency decodes and verifies token
- Frontend: Token stored in localStorage; request interceptor adds Bearer header; 401 redirects to login

**Authorization:**
- Backend: Services scope queries to `current_user.id` in `_query()` method; soft deletes via `deleted_at` filter
- Frontend: Route guards check token existence; component-level checks not needed (backend enforces)

---

*Architecture analysis: 2026-03-02*
