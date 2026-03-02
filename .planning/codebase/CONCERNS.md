# Codebase Concerns

**Analysis Date:** 2026-03-02

## Security Considerations

### JWT Secret Not Rotated in Development

**Risk:** Default hardcoded JWT secret in `core/config.py`
- Files: `backend/src/app/core/config.py` (line 13)
- Current mitigation: `.env` file can override with production key
- Recommendations:
  - Document that `secret_key` must be changed in production
  - Consider adding a startup validation that warns if using default secret
  - Add pre-commit hook to prevent committing with default secret to production branch

### CORS Wildcard Allows All Origins

**Risk:** `allow_origins=["*"]` accepts requests from any domain
- Files: `backend/src/app/main.py` (line 10)
- Current state: All origins allowed (intentional for development)
- Recommendations:
  - Before production deployment, replace with explicit allowed origins from environment variable
  - Add CORS_ALLOWED_ORIGINS env var (comma-separated list)
  - Document CORS requirement in IMPLEMENTATION_CHECKLIST.md

### Token Storage in localStorage

**Risk:** JWT tokens stored in browser localStorage are vulnerable to XSS attacks
- Files: `frontend/src/features/auth/hooks.ts` (lines 11, 22, 33), `frontend/src/lib/api-client.ts` (line 10)
- Files: `frontend/src/routes/auth/login.tsx`, `frontend/src/routes/auth/register.tsx`, `frontend/src/routes/_authenticated.tsx`
- Current state: No HttpOnly flag; vulnerable to JavaScript XSS
- Recommendations:
  - Consider moving token to secure, HttpOnly cookie (requires backend support)
  - Implement Content Security Policy (CSP) headers
  - Add XSS protection headers via backend middleware
  - Document token security trade-offs

### Potential SQL Injection in sort_by Parameter

**Risk:** `sort_by` parameter passed directly to getattr() without validation
- Files: `backend/src/app/services/transactions.py` (line 59)
- Files: `backend/src/app/api/transactions.py` (line 32)
- Current mitigation: `getattr(Transaction, sort_by, Transaction.date)` defaults to `date` if column doesn't exist
- Issue: Untrusted user input determines column name; no explicit allowlist
- Recommendations:
  - Add explicit allowlist of sortable columns in TransactionsService
  - Update transaction API to validate sort_by against allowed values
  - Pattern: `SORTABLE_FIELDS = {"date", "amount", "created_at"}`; check before calling getattr

## Performance Bottlenecks

### N+1 Query Risk in Categories

**Risk:** Category relationships may not be consistently eager-loaded
- Files: `backend/src/app/services/categories.py`
- Current state: Some endpoints load categories without joinedload
- Impact: Paginated transaction lists with categories could trigger N+1 if not careful
- Safe modification: Always use `joinedload(Transaction.category)` when fetching transactions

### Pagination Default is Small

**Risk:** Page size defaults to 10, may not be ideal for mobile or desktop UX
- Files: `backend/src/app/api/transactions.py` (line 31)
- Current state: `page_size: int = Query(10, ge=1, le=50)` defaults to 10
- Impact: Users must request multiple pages for reasonable data volume
- Improvement path: Adjust default based on UX testing; frontend should remember user preference

### Missing Database Indexes

**Risk:** No explicit indexes on frequently queried columns
- Files: `backend/src/app/db/schema.py`
- Current state: Only email has `index=True`; no indexes on user_id, category_id, created_at
- Impact: Slow queries on large transaction volumes
- Improvement path: Add indexes to schema for `user_id` (FK lookups), `date` (filtering), `created_at` (sorting)

## Tech Debt

### Transactions Service is Largest File

**Risk:** Complex business logic concentrated in one file
- Files: `backend/src/app/services/transactions.py` (138 lines)
- Contains: Query building, filtering, pagination, soft delete, restore logic
- Fragile areas: Filter application, sort column validation, soft delete logic
- Safe modification: Extract filter logic or pagination into separate service mixin
- Test coverage: Good - 452 lines of integration tests

### Recurrence Logic Incomplete

**Risk:** Recurring transactions are modeled but not executed
- Files: `backend/src/app/db/schema.py` (lines 92-95)
- Files: `backend/src/app/models/transaction.py` (lines 26, 40-48, 61-62)
- Current state: Schema supports `is_recurring` and `recurrence_frequency` but no job to create recurrence instances
- Impact: Recurrence feature is incomplete; UI allows setting but backend doesn't generate recurring entries
- Fix approach: Implement background job (Celery or APScheduler) to generate transaction recurrences

### Print Statements in Production Code

**Risk:** Debugging print statements may appear in logs or output
- Files: `backend/src/app/db/seed.py` (lines 34, 47)
- Current state: Used in seed function (non-critical)
- Recommendations: Replace with structured logging using `logging` module
- Setup logging module in `core/logging.py` and use throughout

### Large Frontend Components

**Risk:** TransactionModal component is 400+ lines (hard to test/maintain)
- Files: `frontend/src/features/transactions/components/TransactionModal.tsx` (400 lines)
- Other large files: Styleguide files are intentionally large (reference docs)
- Fragile areas: Form state management, category creation inline, validation
- Safe modification: Extract category selection into separate sub-component; extract form helpers
- Current approach: Single-file; considered acceptable for modal complexity

## Missing Critical Features

### No Logout Endpoint

**Risk:** No server-side token invalidation or logout
- Files: `backend/src/app/api/auth.py` - No /logout route
- Current state: Logout is client-only (remove localStorage token)
- Impact: Token can be used indefinitely if leaked; no session management
- Fix approach: Implement token blacklist or short-lived tokens with refresh tokens
- Timing: Should be added before production release

### No Input Rate Limiting

**Risk:** API endpoints not protected from brute force or DOS
- Files: All API routes in `backend/src/app/api/`
- Current state: FastAPI app has no rate limiting middleware
- Impact: Auth endpoints (login, register) vulnerable to brute force
- Fix approach: Add `slowapi` middleware with per-user/IP rate limits
- Priority: High - affects auth security

### No Error Logging Infrastructure

**Risk:** Unhandled exceptions may not be logged or tracked
- Files: All services raise HTTPException directly
- Current state: No centralized error tracking (Sentry, etc.)
- Impact: Production bugs may go unnoticed
- Fix approach: Add exception handlers to main.py that log to centralized service

### No Async Recurrence Job System

**Risk:** Recurring transactions must be manually created or have no job scheduler
- Files: `backend/src/app/db/schema.py` (recurrence columns defined but unused)
- Current state: Schema supports recurrence; no execution pipeline
- Impact: Feature is incomplete; users cannot rely on automatic recurrence
- Fix approach: Implement scheduled job (Celery with Redis or APScheduler)

## Test Coverage Gaps

### Missing Unit Tests for Core Security Functions

**Risk:** `hash_password()` and `verify_password()` not directly tested
- Files: `backend/src/app/core/security.py` (lines 17-22)
- What's not tested: Edge cases in bcrypt operations, password encoding issues
- Files: `backend/tests/unit/` - Only has `test_filters.py`
- Risk: Silent failures in password hashing could compromise authentication
- Priority: High - add unit tests for security functions

### Missing Integration Tests for Sort/Filter Edge Cases

**Risk:** SQL injection in sort_by not tested with malicious input
- Files: `backend/tests/integration/test_transactions_integration.py` (452 lines)
- What's not tested: Invalid sort_by values, SQL injection attempts, boundary conditions
- Files: `backend/tests/unit/test_filters.py` (96 lines) - Tests FilterSpec but not sorting
- Priority: Medium - add negative test cases

### Frontend Auth Tests Missing

**Risk:** No tests for token persistence, localStorage edge cases
- Files: `frontend/src/features/auth/hooks.ts` - No corresponding .test file
- What's not tested: localStorage errors, network failures during login, race conditions
- Current state: No frontend test files visible in codebase
- Fix approach: Add Vitest with @testing-library/react for auth flows

### Missing Integration Tests for User Data Isolation

**Risk:** User ownership checks may fail silently
- Files: `backend/tests/integration/test_users_integration.py` (66 lines) - Minimal tests
- What's not tested: Cross-user data access attempts, transaction leakage between users
- Files: `backend/src/app/services/transactions.py` (line 41) - Filters by user_id but need edge case tests
- Priority: High - add tests for multi-user scenarios

## Fragile Areas

### User Ownership Not Enforced Consistently

**Risk:** Some endpoints may not enforce user_id checks properly
- Files: `backend/src/app/api/users.py` (lines 21-23, 37-39) - list_users and get_user have no auth requirement
- Issue: `/users/` lists all users without authentication; `/users/{user_id}` allows reading any user
- Safe modification: Add CurrentUser auth requirement; scope to current user
- Test coverage: test_users_integration.py needs security tests

### Soft Delete Inconsistencies

**Risk:** Some queries may forget to filter deleted_at
- Files: `backend/src/app/services/transactions.py` (line 41) - Filters correctly
- Files: `backend/src/app/services/categories.py` - Verify all queries filter deleted_at
- Pattern to follow: Always use `Model.deleted_at.is_(None)` in WHERE clause
- Priority: Audit all services for soft delete filtering

### Frontend Auth State Not Persisted

**Risk:** User logged out on page refresh (token only in localStorage)
- Files: `frontend/src/lib/api-client.ts` (line 10) - Reads token on each request (OK)
- Files: `frontend/src/routes/_authenticated.tsx` (lines 5-13) - Checks localStorage on route load
- Issue: No React Context or Query cache persistence; token must always be in localStorage
- Impact: Works but not resilient to localStorage corruption
- Improvement path: Add React Query persistence plugin or React Context for auth state

### Category Default Values Not Enforced

**Risk:** Default categories may not be created on first user signup
- Files: `backend/src/app/db/seed.py` (lines 25-49) - Seed function exists but seed not called automatically
- Files: No seed call visible in startup or migration sequence
- Impact: New users may not have default categories available
- Fix approach: Call seed_default_categories() in migration or app startup

## Dependencies at Risk

### OpenAI Integration Defined but Not Used

**Risk:** OpenAI API key required in config but no usage visible
- Files: `backend/src/app/core/config.py` (line 9) - `openai_api_key: str = ""`
- Files: No imports of openai module in codebase
- Current state: Unused dependency; may have been planned feature
- Migration plan: Remove if not needed; document planned AI features if intentional

### Anthropic Integration Defined but Not Used

**Risk:** Anthropic API key required in config but no usage visible
- Files: `backend/src/app/core/config.py` (line 8) - `anthropic_api_key: str = ""`
- Files: No imports of anthropic module in codebase
- Current state: Unused dependency; may have been planned feature
- Migration plan: Remove if not needed; document planned AI features if intentional

### SMTP Configuration Optional but Incomplete

**Risk:** Password reset emails cannot be sent; SMTP disabled but not documented
- Files: `backend/src/app/core/config.py` (lines 21-25) - SMTP fields empty
- Files: No password reset endpoint visible in `backend/src/app/api/auth.py`
- Current state: Feature not implemented
- Impact: Users cannot recover forgotten passwords
- Priority: Medium - add password reset or document limitation

---

*Concerns audit: 2026-03-02*
