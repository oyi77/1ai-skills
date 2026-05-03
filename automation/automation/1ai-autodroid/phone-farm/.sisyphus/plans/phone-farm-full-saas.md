# Phone Farm Full SaaS — Build Plan

## TL;DR

> **Goal**: Transform Phone Farm from an internal admin tool into a complete user-facing SaaS product with public landing page, email/password authentication, role-based dashboards (device owner vs. admin), an Android client program for device rental, and comprehensive documentation.
>
> **Deliverables**:
> - Public landing page at `/` (marketing, how it works, pricing, CTA)
> - User registration + login system with email/password
> - **User Dashboard**: device earnings, rental status, task history, earnings history
> - **Admin Dashboard**: all users, all devices, platform revenue, user management
> - Android client APK for device owners to connect/rent their devices
> - User Manual + OpenAPI docs + Developer Guide
>
> **Estimated Effort**: XL (50+ tasks across 5 waves)
> **Parallel Execution**: YES — up to 8 tasks per wave
> **Critical Path**: DB users table → Auth system → Registration/Login → User Dashboard → Admin Dashboard → Client APK → Docs

---

## Context

### Original Request
User asked "What did we do so far?" and then demanded answers to 8 questions:
1. Where is the landing page?
2. Where is the registration form?
3. Where is the login form?
4. Where is the user dashboard?
5. Where is the admin dashboard?
6. How do users earn by connecting their devices? (client program needed?)
7. "This app is too simple to even be used by myself, let alone being sold to user!"
8. Where is the documentation?

### Current State Assessment

**What EXISTS:**
- FastAPI server on port 8889 with 50+ endpoints
- SQLite database with multi-tenant isolation (devices, tasks, alerts, groups, tags, screenshots, audit_log, usage)
- JWT + API key authentication (admin/operator/viewer roles)
- ADB-based device control (screenshot, tap, swipe, type, app install/uninstall, etc.)
- Task runner with 10 built-in automation tasks
- Single-file Alpine.js dashboard SPA (dashboard/index.html, 1051 lines) with login card, devices, live monitor, apps, tasks, alerts, settings, billing, API keys, audit log
- Stripe billing integration (usage-based)
- PM2 + systemd process persistence
- Comprehensive README with API reference

**What is MISSING (all 8 items):**
1. **Landing page** — `/` currently redirects to `/dashboard/`. No marketing content exists.
2. **Registration form** — No user table, no email/password auth, no self-service registration.
3. **Login page** — Only an inline API-key login card inside the dashboard SPA.
4. **User dashboard** — No role-based views. All users see the same admin-style dashboard.
5. **Admin dashboard** — No user management UI, no platform-wide analytics view.
6. **Client program** — No Android app for device owners to connect their phones.
7. **Documentation** — Only README.md exists. No user manual, no OpenAPI spec, no developer guide.
8. **Feature completeness** — Missing: email notifications, password reset, billing improvements, user settings, etc.

### Key Architectural Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **User table** | Add `users` table to SQLite alongside `tenants` | Email/password auth for end users; tenants remain for API-key multi-tenancy |
| **Password hashing** | bcrypt via `passlib` | Industry standard, pure Python, no C dependencies |
| **Dashboard routing** | Hash-based routing in existing Alpine SPA | Avoids full SPA rewrite; add `#/login`, `#/user-dashboard`, `#/admin` routes |
| **Client connectivity** | Reverse SSH tunnel (like ngrok) | Simplest for NAT traversal; device initiates outbound tunnel to platform |
| **Client protocol** | WebSocket over reverse tunnel | Screen streaming + command execution + earnings heartbeat |
| **Earnings model** | Per-task credit system, tracked in DB | Device owners earn credits; platform deducts from consumer tenants |
| **Frontend stack** | Keep Alpine.js SPA + Tailwind | Already in use; adding pages faster than rewriting to React |
| **API docs** | OpenAPI/Swagger via FastAPI + `fastapi-openapi` | Auto-generated from route decorators, minimal effort |

---

## Work Objectives

### Core Objective
Ship a demonstrable SaaS product that:
1. Has a professional public landing page explaining the service
2. Allows self-service registration with email/password
3. Gives device owners a dashboard to see their devices and earnings
4. Gives admins a dashboard to manage all users and platform stats
5. Provides an installable Android APK for device owners to connect phones
6. Ships with a user manual, API documentation, and developer guide

### Concrete Deliverables

| # | File/Endpoint | Description |
|---|---------------|-------------|
| 1 | `dashboard/landing.html` | Landing page: hero, features, how it works, pricing, CTA |
| 2 | `dashboard/login.html` | Dedicated login page with email/password form |
| 3 | `dashboard/register.html` | Registration page with name, email, password, role selection |
| 4 | `db.py` + `auth.py` | New `users` table, bcrypt password hashing, login/register endpoints |
| 5 | `farm_daemon.py` | New routes: `POST /auth/register`, `POST /auth/login`, `POST /auth/logout`, `GET /me`, `POST /auth/password-reset` |
| 6 | `dashboard/index.html` | Added `#/user-dashboard` and `#/admin` views with role-based rendering |
| 7 | `client-android/` | Android Studio project for client APK (Kotlin, WebSocket, ADB over network) |
| 8 | `docs/` | User Manual (Markdown), API Reference (OpenAPI JSON/YAML), Developer Guide |
| 9 | `db.py` | New `earnings` table, `devices` table additions for rental status |
| 10 | `farm_daemon.py` | New endpoints: `GET /user/earnings`, `POST /device/register-client`, `GET /admin/users` |

### Definition of Done

- [ ] Landing page accessible at `/` (not redirected) with marketing content
- [ ] New user can register via `/register` and login via `/login`
- [ ] Device owner (user role) sees user dashboard: their devices, earnings, rental status
- [ ] Admin sees admin dashboard: all users, all devices, platform stats
- [ ] Android APK compiles and connects to platform via WebSocket over reverse tunnel
- [ ] User manual covers sign-up, connecting a device, viewing earnings
- [ ] OpenAPI docs at `/docs` with all endpoints documented
- [ ] Developer guide covers client protocol and API integration

### Must Have

- Functional email/password registration and login
- Role-based dashboard access (user vs. admin)
- Device owner can see their connected devices and earnings
- Admin can see platform-wide data
- Android client APK that registers with the platform
- Basic OpenAPI documentation

### Must NOT Have (Guardrails)

- Do NOT replace the existing API key auth — it must continue working alongside email/password
- Do NOT modify existing database table schemas in breaking ways
- Do NOT remove or break existing dashboard sections (devices, tasks, alerts, etc.)
- Do NOT change the port from 8889
- Do NOT add dependencies that require a full Python rebuild without documenting them
- AI slop pattern to avoid: Generic names like `user_data`, `device_info` — use specific domain names
- Over-engineering: Do NOT build a billing subscription system; use simple credit-based earnings for MVP
- Client APK: Do NOT require root or bootloader unlock — use standard Android Debug Bridge (ADB) over network

---

## Verification Strategy

### Test Decision
- **Infrastructure exists**: NO (no test framework in project)
- **Automated tests**: NO
- **Agent-Executed QA**: YES — every task includes QA scenarios executed by the agent

### QA Policy
Every task MUST include agent-executed QA scenarios. Evidence saved to `.sisyphus/evidence/task-{N}-{scenario}.{ext}`.

- **Frontend/UI**: Use `playwright` skill — navigate pages, fill forms, assert DOM state, screenshots
- **API/Backend**: Use `Bash` (curl) — send HTTP requests, assert JSON response fields + status codes
- **Android APK**: Use `Bash` (adb) — install APK, check logcat, verify WebSocket connection attempt
- **Documentation**: Use `Bash` — verify files exist, validate OpenAPI JSON, check links in markdown

---

## Execution Strategy

### Wave Overview

```
Wave 1 (Foundation — Auth + DB + Landing):
├── T1:  Add users table + earnings table to db.py
├── T2:  Add password hashing + user auth helpers to auth.py
├── T3:  Create registration endpoint POST /auth/register
├── T4:  Create login/logout/reset endpoints
├── T5:  Create landing page HTML (hero, features, pricing, CTA)
├── T6:  Create dedicated login.html page
└── T7:  Create register.html page

Wave 2 (Dashboards — Split user vs admin views):
├── T8:  Add role field to users table + user management endpoints
├── T9:  Add user dashboard API endpoints (earnings, my devices)
├── T10: Add admin dashboard API endpoints (all users, platform stats)
├── T11: Update dashboard/index.html — add #/user-dashboard route
├── T12: Build user dashboard UI (my devices, earnings, rental status)
├── T13: Build admin dashboard UI (all users, platform stats, user mgmt)
└── T14: Add hash-based navigation to dashboard SPA

Wave 3 (Client Program — Android APK):
├── T15: Design client protocol (WebSocket messages, device registration flow)
├── T16: Create Android project scaffold (Kotlin, Gradle, dependencies)
├── T17: Implement device registration + authentication (client → platform)
├── T18: Implement reverse tunnel manager (SSH reverse tunnel or ngrok-style)
├── T19: Implement screen streaming client (screencap → WebSocket → platform)
├── T20: Implement task execution engine (receive task → execute via ADB → report result)
├── T21: Implement earnings heartbeat (periodic credits update to platform)
└── T22: Build debug APK, test basic connect/register flow

Wave 4 (Documentation + Polish):
├── T23: Create User Manual (Markdown) — sign-up, connect device, earn money, FAQ
├── T24: Generate OpenAPI spec (auto via FastAPI + redoclya)
├── T25: Create Developer Guide — API reference, client protocol, WebSocket messages
├── T26: Add password reset email flow (token-based, SMTP)
├── T27: Add email notifications (new device connected, earnings milestone)
└── T28: Dashboard polish — dark/light mode, export to CSV, UI improvements

Wave 5 (Integration + Verification):
├── T29: End-to-end test — register → login → connect device → earn credits
├── T30: Security audit — password hashing, session tokens, API rate limits
├── T31: Admin user management UI — ban user, delete user, impersonate
└── T32: Stripe billing improvements — credit purchase, withdrawal for device owners
```

### Dependency Matrix

- **T1** (users table) → T2, T3, T4
- **T2** (auth helpers) → T3, T4
- **T3** (register endpoint) → T7 (register.html)
- **T4** (login/logout endpoints) → T6 (login.html)
- **T5** (landing page) — Independent
- **T7** (register.html) → T3 (register endpoint)
- **T6** (login.html) → T4 (login endpoint)
- **T8** (user mgmt endpoints) → T13 (admin UI)
- **T9** (user API) → T12 (user dashboard)
- **T10** (admin API) → T13 (admin dashboard)
- **T11** (SPA routing) → T12, T13
- **T12** (user dashboard UI) → T9, T11
- **T13** (admin dashboard UI) → T10, T11
- **T15** (protocol design) → T16-22
- **T16** (Android scaffold) → T17-22
- **T17-22** (client features) → T22 (debug APK)
- **T23** (user manual) → Independent
- **T24** (OpenAPI) → Independent
- **T25** (dev guide) → T15
- **T26** (password reset) → T2
- **T27** (email notifications) → T2
- **T28** (dashboard polish) → T12, T13
- **T29** (e2e test) → T12, T13, T22
- **T30** (security audit) → T2, T3, T4
- **T31** (admin user mgmt) → T8, T13
- **T32** (Stripe credits) → T1, T9

### Agent Dispatch Summary

- **Wave 1**: 7 agents (T1, T2, T3, T4, T5, T6, T7) — 7 parallel
- **Wave 2**: 6 agents (T8, T9, T10, T11, T12, T13) — 6 parallel
- **Wave 3**: 8 agents (T15, T16, T17, T18, T19, T20, T21, T22) — 8 parallel (Android = largest wave)
- **Wave 4**: 6 agents (T23, T24, T25, T26, T27, T28) — 6 parallel
- **Wave 5**: 4 agents (T29, T30, T31, T32) — 4 parallel

---

## TODOs

- [x] 1. **Add users table + earnings table to db.py**

  **What to do**:
  - Add `users` table: `id` (TEXT PK), `email` (UNIQUE), `password_hash`, `name`, `role` (TEXT: "user" | "admin"), `tenant_id` (FK → tenants), `credits` (REAL DEFAULT 0), `created_at`, `updated_at`, `last_login`
  - Add `earnings` table: `id` (INTEGER PK), `user_id` (FK → users), `device_serial`, `amount` (credits), `task_type`, `ts`, `ts_str`
  - Add `sessions` table: `id` (TEXT PK), `user_id` (FK → users), `token_hash`, `expires_at`, `created_at`
  - Add `password_reset_tokens` table: `token_hash` (PK), `user_id` (FK), `expires_at`
  - Add DB helper functions: `create_user()`, `get_user_by_email()`, `verify_password()`, `update_user()`, `get_user_earnings()`, `add_earning()`, `create_session()`, `get_session()`, `delete_session()`, `create_password_reset_token()`, `get_password_reset_token()`
  - Migration: ensure `role` column defaults to "user" for existing tenants
  - **Test cases to cover**: create user, duplicate email, password hash verification, earning aggregation, session creation/expiry

  **Must NOT do**:
  - Do NOT drop or rename existing tables
  - Do NOT modify the `tenants` or `devices` table schemas in breaking ways
  - Do NOT store plain-text passwords

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Database schema design, password hashing, session management — requires careful security consideration
  - **Skills**: []
    - `passlib`: For bcrypt password hashing integration
  - **Skills Evaluated but Omitted**:
    - `test-driven-development`: No test infrastructure exists yet

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with T2-T7)
  - **Blocks**: T2 (auth helpers need users table), T3 (register endpoint), T4 (login endpoint)
  - **Blocked By**: None

  **References**:

  **Pattern References** (existing code to follow):
  - `db.py:125-271` — Existing `init_db()` pattern with `CREATE TABLE IF NOT EXISTS` and indexes
  - `db.py:299-311` — `upsert_device()` pattern with `INSERT ... ON CONFLICT` for upserts
  - `db.py:517-531` — `get_groups()` with QueryParams pagination pattern to follow for `get_users()`
  - `auth.py:24-123` — JWT class pattern for session token handling
  - `tenant.py:15-31` — `create_tenant()` pattern for `create_user()`

  **API/Type References** (contracts to implement against):
  - `auth.py:JWT` — Use similar patterns for session token creation/validation
  - `db.py:QueryParams` — `get_users()` should accept QueryParams like `get_groups()`

  **Test References** (testing patterns to follow):
  - None available — test infrastructure doesn't exist yet

  **External References** (libraries and frameworks):
  - `passlib` bcrypt: `https://passlib.readthedocs.io/en/stable/` — `CryptContext` with bcrypt backend
  - SQLite WAL mode: Already in use at `db.py:117` — continue using it

  **WHY Each Reference Matters**:
  - `db.py:init_db()` — Shows the exact CREATE TABLE syntax and migration pattern to follow
  - `auth.py:JWT` — The session token pattern (hash, expiry, lookup) mirrors JWT approach
  - `tenant.py:create_tenant()` — `create_user()` should follow the same insert + return pattern

  **Acceptance Criteria**:

  \`\`\`
  Scenario: Create new user
    Tool: Bash (python inline)
    Preconditions: Fresh database, no users exist
    Steps:
      1. python3 -c "
          import sys; sys.path.insert(0, '.')
          import db; db.init_db()
          from auth_user import create_user, get_user_by_email
          uid = create_user('test@example.com', 'Test User', 'password123')
          user = get_user_by_email('test@example.com')
          print('OK', uid, user['name'])
      "
    Expected Result: Creates user, returns valid user dict with hashed password
    Failure Indicators: Plain-text password stored, duplicate email allowed, FK constraint fails
    Evidence: .sisyphus/evidence/task-1-create-user.txt

  Scenario: Password verification
    Tool: Bash (python inline)
    Preconditions: User from previous scenario exists
    Steps:
      1. python3 -c "
          import sys; sys.path.insert(0, '.')
          from auth_user import verify_password
          ok = verify_password('test@example.com', 'password123')
          bad = verify_password('test@example.com', 'wrongpass')
          print('OK' if ok and not bad else 'FAIL')
      "
    Expected Result: Correct password returns True, wrong returns False
    Failure Indicators: Plain-text comparison, timing attacks, hash mismatch
    Evidence: .sisyphus/evidence/task-1-password-verify.txt

  Scenario: Duplicate email registration rejected
    Tool: Bash (python inline)
    Preconditions: User from scenario 1 exists
    Steps:
      1. python3 -c "
          import sys; sys.path.insert(0, '.')
          from auth_user import create_user
          try:
              create_user('test@example.com', 'Another User', 'pass456')
              print('FAIL - should have raised')
          except Exception as e:
              print('OK - rejected duplicate')
      "
    Expected Result: Raises exception or returns None for duplicate email
    Failure Indicators: Two users with same email created
    Evidence: .sisyphus/evidence/task-1-duplicate-email.txt
  \`\`\`

  **Evidence to Capture:**
  - [ ] User creation output showing hashed password (not plain text)
  - [ ] Password verification success/failure output
  - [ ] Duplicate email rejection output

  **Commit**: YES
  - Message: `feat(db): add users, earnings, sessions, password_reset_tokens tables`
  - Files: `db.py`
  - Pre-commit: `python3 -c "import db; db.init_db(); print('OK')"`

---

- [x] 2. **Add password hashing + user auth helpers to auth.py**

  **What to do**:
  - Create `auth_user.py` (new file to avoid polluting existing auth.py):
    - `hash_password(password: str) -> str` — bcrypt hash using passlib
    - `verify_password(email: str, password: str) -> bool` — lookup user, verify hash
    - `create_session(user_id: str) -> tuple[str, dict]` — create secure token + store hash in sessions table
    - `get_session(token: str) -> Optional[dict]` — lookup valid session
    - `delete_session(token: str) -> bool`
    - `delete_expired_sessions()` — cleanup job
    - `create_password_reset_token(user_id: str) -> str` — generate token, store hash
    - `get_password_reset_token(token: str) -> Optional[str]` — validate and return user_id
    - `consume_password_reset_token(token: str) -> bool` — invalidate after use
    - `update_password(user_id: str, new_password_hash: str) -> bool`
  - Keep existing `auth.py` unchanged (API key + JWT auth continues to work)
  - `PHONEFARM_SESSION_SECRET` env var for session token signing
  - Session tokens: 64-char hex (from `secrets.token_hex(32)`), stored as SHA-256 hash in DB
  - **Test cases**: correct password, wrong password, expired session, password reset token flow

  **Must NOT do**:
  - Do NOT modify existing `auth.py` — existing API key auth must keep working
  - Do NOT use MD5 or SHA-1 for password hashing — must use bcrypt
  - Do NOT store session tokens in plain text in DB

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Security-critical code (password hashing, session management) requires careful implementation
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - `code-reviewer`: Will be used in final verification wave

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with T1, T3, T4, T5, T6, T7)
  - **Blocks**: T3 (register endpoint), T4 (login endpoint), T26 (password reset)
  - **Blocked By**: T1 (users table must exist first)

  **References**:

  **Pattern References** (existing code to follow):
  - `auth.py:24-123` — JWT class implementation as pattern for session token handling
  - `auth.py:204-206` — `APIKeyManager._hash_key()` for hashing approach reference
  - `db.py:684-689` — `insert_audit()` for logging auth events
  - `auth.py:343-347` — `create_token()` pattern for `create_session()`

  **API/Type References** (contracts to implement against):
  - `auth.py:JWT` — Session token structure similar to JWT but simpler (no claims, just user_id + expiry)
  - `db.py:QueryParams` — Not needed for session lookups (single-record lookups)

  **External References** (libraries and frameworks):
  - `passlib bcrypt`: `https://passlib.readthedocs.io/en/stable/` — CryptContext with bcrypt_sha256
  - Python `secrets`: Built-in, `secrets.token_hex(32)` for session token generation

  **WHY Each Reference Matters**:
  - `auth.py:JWT` — Shows how to structure token creation, hashing, and validation
  - `auth.py:_hash_key()` — Shows how to securely hash tokens for storage

  **Acceptance Criteria**:

  \`\`\`
  Scenario: Session creation and lookup
    Tool: Bash (python inline)
    Preconditions: User from T1 scenario 1 exists
    Steps:
      1. python3 -c "
          import sys; sys.path.insert(0, '.')
          from auth_user import create_session, get_session, delete_session
          token, sess = create_session('test@example.com')
          looked = get_session(token)
          deleted = delete_session(token)
          after = get_session(token)
          print('OK' if looked and deleted and not after else 'FAIL')
      "
    Expected Result: Session created, looked up successfully, deleted, then invalid
    Failure Indicators: Token stored in plain text, session not found, delete doesn't work
    Evidence: .sisyphus/evidence/task-2-session.txt

  Scenario: Password reset token lifecycle
    Tool: Bash (python inline)
    Preconditions: User from T1 scenario 1 exists
    Steps:
      1. python3 -c "
          import sys; sys.path.insert(0, '.')
          from auth_user import create_password_reset_token, get_password_reset_token, consume_password_reset_token, update_password, get_session
          token = create_password_reset_token('test@example.com')
          uid = get_password_reset_token(token)
          consumed = consume_password_reset_token(token)
          after = get_password_reset_token(token)
          print('OK' if uid and consumed and not after else 'FAIL')
      "
    Expected Result: Token created, validated, consumed, then invalid
    Failure Indicators: Token reusable, token invalid after consumption fails
    Evidence: .sisyphus/evidence/task-2-reset-token.txt
  \`\`\`

  **Evidence to Capture:**
  - [ ] Session creation and lookup evidence
  - [ ] Password reset token lifecycle evidence

  **Commit**: YES
  - Message: `feat(auth): add session-based user auth with bcrypt passwords`
  - Files: `auth_user.py` (new file)
  - Pre-commit: `python3 -c "from auth_user import hash_password; print(hash_password('test'))"`

---

- [ ] 3. **Create registration endpoint POST /auth/register**

  **What to do**:
  - Add `POST /auth/register` route to `farm_daemon.py`:
    - Request body: `{"email": str, "password": str, "name": str, "role": str}` (role optional, default "user")
    - Validations: email format, password min 8 chars, name non-empty
    - Creates user in DB, creates associated tenant, returns session token + user info
    - On duplicate email: return 409 Conflict
    - On validation failure: return 422 with field-level errors
  - Add `POST /auth/verify-email` endpoint (sends verification email, marks email as verified)
  - Add `GET /me` endpoint to return current user info
  - Add `require_user_auth()` dependency that checks session token (similar to `require_auth()`)
  - Rate limit registration: 5 per IP per hour
  - **Test cases**: happy path, duplicate email, weak password, invalid email, missing fields

  **Must NOT do**:
  - Do NOT auto-login after registration — return token explicitly
  - Do NOT allow role="admin" registration by default — only "user"
  - Do NOT store password in plain text

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: FastAPI endpoint implementation, moderate complexity with validation
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - None

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with T1, T2, T4, T5, T6, T7)
  - **Blocks**: T7 (register.html needs this endpoint)
  - **Blocked By**: T1 (users table), T2 (auth helpers)

  **References**:

  **Pattern References** (existing code to follow):
  - `farm_daemon.py:793-827` — Existing `/auth/token` and `/auth/keys` endpoints as route pattern
  - `farm_daemon.py:796-802` — `create_token_endpoint()` as response format pattern
  - `farm_daemon.py:368-385` — `require_auth()` usage in endpoints
  - `farm_daemon.py:534-578` — Audit middleware as logging pattern for auth events

  **API/Type References** (contracts to implement against):
  - `farm_daemon.py:create_token_endpoint` — Response format: `{token, type, expires_in}`
  - New response: `{ok: true, user: {id, email, name, role}, token: str}`

  **External References** (libraries and frameworks):
  - FastAPI `Body`, `HTTPException`, `status`: `https://fastapi.tiangolo.com/tutorial/body/`
  - Email validation regex: Simple RFC-compliant pattern

  **WHY Each Reference Matters**:
  - `farm_daemon.py:793-827` — Shows exact FastAPI route pattern, response format, and import structure

  **Acceptance Criteria**:

  \`\`\`
  Scenario: Successful registration
    Tool: Bash (curl)
    Preconditions: No existing user with test email
    Steps:
      1. curl -s -X POST http://localhost:8889/auth/register \
           -H "Content-Type: application/json" \
           -d '{"email":"newuser@example.com","password":"TestPass123","name":"New User"}' | \
           python3 -c "import sys,json; d=json.load(sys.stdin); print('OK' if d.get('token') and d['user']['email']=='newuser@example.com' else 'FAIL')"
    Expected Result: 200, token + user info returned
    Failure Indicators: 500 error, missing token, wrong email in response
    Evidence: .sisyphus/evidence/task-3-register-ok.json

  Scenario: Duplicate email rejected
    Tool: Bash (curl)
    Preconditions: User from previous scenario exists
    Steps:
      1. curl -s -X POST http://localhost:8889/auth/register \
           -H "Content-Type: application/json" \
           -d '{"email":"newuser@example.com","password":"TestPass123","name":"Dup User"}' | \
           python3 -c "import sys,json; d=json.load(sys.stdin); print('OK' if d.get('detail','').startswith('Email') else 'FAIL')"
    Expected Result: 409 with "Email already registered"
    Failure Indicators: 200 (created duplicate), wrong error message
    Evidence: .sisyphus/evidence/task-3-register-dup.json

  Scenario: Weak password rejected
    Tool: Bash (curl)
    Preconditions: None
    Steps:
      1. curl -s -X POST http://localhost:8889/auth/register \
           -H "Content-Type: application/json" \
           -d '{"email":"weak@example.com","password":"short","name":"W"}' | \
           python3 -c "import sys,json; d=json.load(sys.stdin); print('OK' if d.get('detail') else 'FAIL')"
    Expected Result: 422 with password validation error
    Failure Indicators: 200 on weak password, no error detail
    Evidence: .sisyphus/evidence/task-3-register-weak.json
  \`\`\`

  **Evidence to Capture:**
  - [ ] Successful registration JSON response
  - [ ] Duplicate email rejection JSON
  - [ ] Weak password rejection JSON

  **Commit**: YES
  - Message: `feat(api): add POST /auth/register endpoint with validation`
  - Files: `farm_daemon.py`
  - Pre-commit: `python3 -m py_compile farm_daemon.py`

---

- [ ] 4. **Create login/logout/reset/password-change endpoints**

  **What to do**:
  - `POST /auth/login` — email + password, returns session token + user info
    - On success: create session record, return token + user
    - On failure: return 401 Unauthorized (don't reveal whether email or password was wrong)
    - Rate limit: 10 per IP per 5 minutes
  - `POST /auth/logout` — invalidate session token
    - Requires valid session token in `Authorization: Bearer <token>` header
  - `POST /auth/password-reset/request` — generate reset token, send email (logs token to console if SMTP not configured)
    - Input: `{"email": str}`
    - Output: always 200 (don't reveal whether email exists)
  - `POST /auth/password-reset/confirm` — consume token, set new password
    - Input: `{"token": str, "new_password": str}`
  - `POST /auth/me` (GET) — return current user info from session token
    - Returns: `{id, email, name, role, credits, tenant_id}`
  - `PUT /auth/me` — update name or password
  - Update audit middleware to log user_id from session tokens
  - **Test cases**: happy path login, wrong password, invalid token on /me, logout invalidates, reset flow

  **Must NOT do**:
  - Do NOT reveal in error messages whether an email is registered (prevent enumeration)
  - Do NOT allow password reset without valid token
  - Do NOT keep sessions valid after logout

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: FastAPI endpoints with session management, moderate complexity
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - None

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with T1, T2, T3, T5, T6, T7)
  - **Blocks**: T6 (login.html needs these endpoints)
  - **Blocked By**: T1 (users/sessions tables), T2 (auth helpers)

  **References**:

  **Pattern References** (existing code to follow):
  - `farm_daemon.py:796-802` — Token response format pattern
  - `farm_daemon.py:534-578` — Audit middleware for logging user_id from tokens
  - `farm_daemon.py:368-385` — `require_auth()` as `require_user_auth()` template

  **WHY Each Reference Matters**:
  - Shows how to structure responses and integrate with existing middleware

  **Acceptance Criteria**:

  \`\`\`
  Scenario: Successful login
    Tool: Bash (curl)
    Preconditions: User from T1 scenario 1 exists
    Steps:
      1. curl -s -X POST http://localhost:8889/auth/login \
           -H "Content-Type: application/json" \
           -d '{"email":"test@example.com","password":"password123"}' | \
           python3 -c "import sys,json; d=json.load(sys.stdin); print('OK' if d.get('token') and d['user']['email']=='test@example.com' else 'FAIL: '+str(d))"
    Expected Result: 200, token + user returned
    Failure Indicators: 401 on correct credentials, missing token
    Evidence: .sisyphus/evidence/task-4-login-ok.json

  Scenario: Wrong password does not reveal which field
    Tool: Bash (curl)
    Preconditions: User from T1 scenario 1 exists
    Steps:
      1. curl -s -X POST http://localhost:8889/auth/login \
           -H "Content-Type: application/json" \
           -d '{"email":"test@example.com","password":"wrongpassword"}' | \
           python3 -c "import sys,json; d=json.load(sys.stdin); r=__import__('requests',fromlist=['codes']).codes; print('OK' if d.get('detail')=='Invalid credentials' else 'FAIL')"
    Expected Result: 401 with generic "Invalid credentials" message (not "wrong password")
    Failure Indicators: Message reveals email exists vs password wrong
    Evidence: .sisyphus/evidence/task-4-login-wrongpass.json

  Scenario: /me returns user info with valid token
    Tool: Bash (curl)
    Preconditions: Valid token from login scenario
    Steps:
      1. TOKEN=$(curl -s -X POST http://localhost:8889/auth/login \
           -H "Content-Type: application/json" \
           -d '{"email":"test@example.com","password":"password123"}' | \
           python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")
           curl -s http://localhost:8889/auth/me -H "Authorization: Bearer $TOKEN" | \
           python3 -c "import sys,json; d=json.load(sys.stdin); print('OK' if d.get('email')=='test@example.com' else 'FAIL')"
    Expected Result: 200 with user email, name, role
    Failure Indicators: 401 on valid token, wrong user data
    Evidence: .sisyphus/evidence/task-4-me-ok.json

  Scenario: Logout invalidates token
    Tool: Bash (curl)
    Preconditions: Valid token from login scenario
    Steps:
      1. TOKEN=$(curl -s -X POST http://localhost:8889/auth/login \
           -H "Content-Type: application/json" \
           -d '{"email":"test@example.com","password":"password123"}' | \
           python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")
           curl -s -X POST http://localhost:8889/auth/logout -H "Authorization: Bearer $TOKEN" | python3 -c "import sys,json; print(json.load(sys.stdin))"
           curl -s http://localhost:8889/auth/me -H "Authorization: Bearer $TOKEN" | python3 -c "import sys,json; d=json.load(sys.stdin); print('FAIL' if d.get('email') else 'OK')"
    Expected Result: Logout returns OK, subsequent /me returns 401
    Failure Indicators: Token still valid after logout
    Evidence: .sisyphus/evidence/task-4-logout.json
  \`\`\`

  **Evidence to Capture:**
  - [ ] Login success JSON
  - [ ] Wrong password error JSON
  - [ ] /me response JSON
  - [ ] Logout + post-logout /me JSON

  **Commit**: YES
  - Message: `feat(auth): add login, logout, password-reset, /me endpoints`
  - Files: `farm_daemon.py`, `auth_user.py`
  - Pre-commit: `python3 -m py_compile farm_daemon.py && python3 -m py_compile auth_user.py`

---

- [ ] 5. **Create landing page HTML (hero, features, pricing, CTA)**

  **What to do**:
  - Create `dashboard/landing.html` — new file
  - Design: Professional SaaS landing page matching the dark theme of the dashboard
  - Sections:
    1. **Hero**: "Rent Your Phone. Earn Passive Income." / subheadline about device farming / CTA button "Get Started Free"
    2. **How It Works**: 3-step visual (1. Install app → 2. Connect device → 3. Earn credits)
    3. **Features**: Remote device access, screen sharing, task automation, 24/7 availability
    4. **Pricing**: Free (earn 50% of task value) / Pro (earn 70%, $9.99/mo) — simple credit-based
    5. **For Businesses**: "Need devices? Rent from our network" CTA
    6. **FAQ**: How do I earn? How much can I make? Is my device safe? What tasks are run?
    7. **Footer**: Links (Login, Register, Docs, Privacy, Terms)
  - All CTA buttons link to `/register` or `/login`
  - Mobile responsive, fast loading
  - **Test cases**: Page loads at `/`, hero text visible, CTA links work, FAQ accordion

  **Must NOT do**:
  - Do NOT create a separate login/register page inside landing.html — those are separate files
  - Do NOT add complex JavaScript frameworks — vanilla JS or minimal Alpine.js for FAQ accordion
  - Do NOT use bright/loud colors — keep dark theme consistent

  **Recommended Agent Profile**:
  - **Category**: `writing`
    - Reason: Marketing copy and page structure — content-focused
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - `frontend-ui-ux`: Could enhance but landing page is mostly content

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with T1, T2, T3, T4, T6, T7)
  - **Blocks**: None (independent)
  - **Blocked By**: None

  **References**:

  **Pattern References** (existing code to follow):
  - `dashboard/index.html:1-148` — CSS custom properties (`:root{--bg:...`) for dark theme consistency
  - `dashboard/index.html:45-53` — Login card styling as color/font reference
  - `dashboard/index.html:40-148` — General page styling (cards, buttons, typography)

  **External References** (libraries and frameworks):
  - Tailwind CSS via CDN: `https://tailwindcss.com/docs` — utility classes for rapid layout
  - Alpine.js via CDN (already loaded in dashboard): `https://alpinejs.start.com` — FAQ accordion

  **WHY Each Reference Matters**:
  - `dashboard/index.html` CSS vars ensure visual consistency with the existing dashboard

  **Acceptance Criteria**:

  \`\`\`
  Scenario: Landing page loads at root URL
    Tool: Bash (curl)
    Preconditions: Farm daemon running
    Steps:
      1. curl -s -o /tmp/landing.html http://localhost:8889/ && \
           python3 -c "
              content = open('/tmp/landing.html').read()
              checks = ['Phone Farm', 'Earn', 'Get Started', 'How It Works', 'Pricing']
              ok = all(c in content for c in checks)
              print('OK' if ok else 'FAIL - missing content')
              print('Size:', len(content), 'bytes')
           "
    Expected Result: 200, HTML with all 5 key sections present, >5KB
    Failure Indicators: 301 redirect to dashboard, missing sections, <1KB
    Evidence: .sisyphus/evidence/task-5-landing-load.html

  Scenario: CTA buttons link to register/login
    Tool: Bash (curl)
    Preconditions: Landing page loaded
    Steps:
      1. curl -s http://localhost:8889/ | grep -o 'href="[^"]*register[^"]*"' | head -3
           curl -s http://localhost:8889/ | grep -o 'href="[^"]*login[^"]*"' | head -3
    Expected Result: At least 1 href to /register and 1 href to /login
    Failure Indicators: No register/login links found
    Evidence: .sisyphus/evidence/task-5-cta-links.txt
  \`\`\`

  **Evidence to Capture:**
  - [ ] Landing page HTML saved to evidence
  - [ ] CTA links verification output

  **Commit**: YES
  - Message: `feat(ui): add public landing page with marketing content`
  - Files: `dashboard/landing.html`
  - Pre-commit: None (static HTML)

---

- [ ] 6. **Create dedicated login.html page**

  **What to do**:
  - Create `dashboard/login.html` — new file
  - Standalone login page (not part of the SPA)
  - Design: Centered card, dark theme matching existing dashboard
  - Fields: Email input, Password input, "Login" button
  - Links: "Forgot password?" → `/forgot-password.html`, "Don't have an account? Register" → `/register.html`
  - On success: Store session token in `localStorage`, redirect to `/dashboard/`
  - On failure: Show error message below form (generic: "Invalid email or password")
  - Form submission via `fetch()` to `POST /auth/login`
  - Session token stored as `localStorage.setItem('session_token', data.token)`
  - **Test cases**: happy path login, wrong password, empty fields, redirect after login

  **Must NOT do**:
  - Do NOT copy the existing API-key login from dashboard/index.html — build a proper email/password form
  - Do NOT store password in localStorage — only the session token
  - Do NOT redirect to the old dashboard SPA without the session token

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Simple standalone HTML page, straightforward implementation
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - None

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with T1, T2, T3, T4, T5, T7)
  - **Blocks**: None
  - **Blocked By**: T4 (login endpoint must exist)

  **References**:

  **Pattern References** (existing code to follow):
  - `dashboard/index.html:45-53` — Login card styling (`.login-card`, `.login-wrap`) to reuse
  - `dashboard/index.html:153-162` — Existing inline login HTML as reference for structure

  **WHY Each Reference Matters**:
  - Shows the exact dark theme CSS classes to reuse

  **Acceptance Criteria**:

  \`\`\`
  Scenario: Login page loads
    Tool: Bash (curl)
    Preconditions: Farm daemon running
    Steps:
      1. curl -s -o /tmp/login.html http://localhost:8889/login.html && \
           python3 -c "
              c = open('/tmp/login.html').read()
              checks = ['email', 'password', 'login', 'POST', '/auth/login']
              print('OK' if all(x in c.lower() for x in checks) else 'FAIL')
           "
    Expected Result: 200, form with email/password fields, POST to /auth/login
    Failure Indicators: Wrong path, missing fields
    Evidence: .sisyphus/evidence/task-6-login-page.html

  Scenario: Successful login redirects to dashboard
    Tool: playwright (playwright skill)
    Preconditions: User exists, browser with clean localStorage
    Steps:
      1. Navigate to http://localhost:8889/login.html
      2. Fill email: test@example.com
      3. Fill password: password123
      4. Click Login button
      5. Wait for redirect
      6. Assert current URL contains /dashboard/
      7. Assert localStorage has session_token
    Expected Result: Redirected to dashboard, token stored
    Failure Indicators: Stays on login page, no token stored
    Evidence: .sisyphus/evidence/task-6-login-success.png (screenshot)
  \`\`\`

  **Evidence to Capture:**
  - [ ] Login page HTML saved
  - [ ] Successful login screenshot showing dashboard redirect

  **Commit**: YES
  - Message: `feat(ui): add dedicated login page with email/password form`
  - Files: `dashboard/login.html`
  - Pre-commit: None (static HTML)

---

- [ ] 7. **Create register.html page**

  **What to do**:
  - Create `dashboard/register.html` — new file
  - Standalone registration page, matching dark theme
  - Fields: Name, Email, Password, Confirm Password, Role selector (radio: "I want to rent my devices" / "I want to use devices")
  - Validation: Email format, password min 8 chars with number, passwords match, name non-empty
  - Form submits to `POST /auth/register`
  - On success: auto-login + redirect to dashboard
  - Links: "Already have an account? Login" → `/login.html`
  - **Test cases**: happy path, duplicate email, weak password, password mismatch, empty fields

  **Must NOT do**:
  - Do NOT allow selecting "admin" role — only "user" (device owner) or "consumer"
  - Do NOT auto-create an API key — user gets session token only
  - Do NOT skip client-side validation before submitting

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Simple standalone HTML page, similar to login page
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - None

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with T1, T2, T3, T4, T5, T6)
  - **Blocks**: None
  - **Blocked By**: T3 (register endpoint must exist)

  **References**:

  **Pattern References** (existing code to follow):
  - `dashboard/login.html` (T6) — Same structure and styling to reuse
  - `dashboard/index.html:45-53` — Login card CSS

  **WHY Each Reference Matters**:
  - Same pattern as login.html, just with additional fields

  **Acceptance Criteria**:

  \`\`\`
  Scenario: Registration page loads
    Tool: Bash (curl)
    Preconditions: Farm daemon running
    Steps:
      1. curl -s -o /tmp/register.html http://localhost:8889/register.html && \
           python3 -c "
              c = open('/tmp/register.html').read()
              checks = ['name', 'email', 'password', 'role', '/auth/register']
              print('OK' if all(x in c.lower() for x in checks) else 'FAIL: missing '+str([x for x in checks if x not in c.lower()]))
           "
    Expected Result: 200, all required fields present
    Failure Indicators: Missing fields
    Evidence: .sisyphus/evidence/task-7-register-page.html

  Scenario: Successful registration
    Tool: playwright (playwright skill)
    Preconditions: Browser with clean state
    Steps:
      1. Navigate to http://localhost:8889/register.html
      2. Fill name: Test User
      3. Fill email: regtest@example.com
      4. Fill password: TestPass123
      5. Fill confirm password: TestPass123
      6. Select role: "I want to rent my devices"
      7. Click Register
      8. Wait for redirect
      9. Assert URL contains /dashboard/
    Expected Result: Redirected to dashboard after registration
    Failure Indicators: Error shown, or redirected to login page instead of dashboard
    Evidence: .sisyphus/evidence/task-7-register-success.png

  Scenario: Duplicate email shows error
    Tool: playwright (playwright skill)
    Preconditions: regtest@example.com exists from scenario 2
    Steps:
      1. Navigate to http://localhost:8889/register.html
      2. Fill name: Dup User
      3. Fill email: regtest@example.com
      4. Fill password: TestPass123
      5. Fill confirm password: TestPass123
      6. Click Register
      7. Assert error message visible
    Expected Result: Error below form (not a popup/alert)
    Failure Indicators: Page crash, no error shown, misleading error
    Evidence: .sisyphus/evidence/task-7-register-dup-error.png
  \`\`\`

  **Evidence to Capture:**
  - [ ] Registration page HTML saved
  - [ ] Successful registration screenshot
  - [ ] Duplicate email error screenshot

  **Commit**: YES
  - Message: `feat(ui): add user registration page with role selection`
  - Files: `dashboard/register.html`
  - Pre-commit: None (static HTML)

---

- [ ] 8. **Add role field + user management endpoints**

  **What to do**:
  - Add `role` column to `users` table: TEXT DEFAULT 'user' CHECK(role IN ('user', 'admin', 'consumer'))
  - Add migration to set existing users to 'admin' if they have API key activity
  - Add endpoints:
    - `GET /admin/users` — paginated list of all users (admin only)
    - `GET /admin/users/{user_id}` — user detail
    - `PUT /admin/users/{user_id}` — update role, ban status, credits
    - `DELETE /admin/users/{user_id}` — soft delete (mark inactive)
    - `POST /admin/users/{user_id}/impersonate` — get session token for any user (audit logged)
  - Add `require_admin()` dependency for admin-only routes
  - Add `banned` column to users table: INTEGER DEFAULT 0
  - Add banned users can't login (check in session creation)
  - **Test cases**: admin can list users, non-admin gets 403, banned user can't login

  **Must NOT do**:
  - Do NOT allow regular users to access admin endpoints
  - Do NOT allow self-promotion to admin
  - Do NOT hard delete users — soft delete only

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Admin API endpoints with authorization checks
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - None

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with T9, T10, T11, T12, T13)
  - **Blocks**: T13 (admin dashboard UI)
  - **Blocked By**: T1 (users table)

  **References**:

  **Pattern References** (existing code to follow):
  - `farm_daemon.py:804-826` — Existing `/auth/keys` CRUD as endpoint pattern
  - `farm_daemon.py:368-385` — `require_auth()` as template for `require_admin()`

  **Acceptance Criteria**:

  \`\`\`
  Scenario: Admin can list all users
    Tool: Bash (curl)
    Preconditions: Admin token
    Steps:
      1. curl -s http://localhost:8889/admin/users \
           -H "Authorization: Bearer $ADMIN_TOKEN" | \
           python3 -c "import sys,json; d=json.load(sys.stdin); print('OK' if isinstance(d.get('items',[]), list) else 'FAIL')"
    Expected Result: 200, paginated list of users
    Failure Indicators: 403 on admin token, wrong format
    Evidence: .sisyphus/evidence/task-8-admin-list.json

  Scenario: Non-admin cannot access admin endpoints
    Tool: Bash (curl)
    Preconditions: User (non-admin) token
    Steps:
      1. curl -s -o /dev/null -w "%{http_code}" http://localhost:8889/admin/users \
           -H "Authorization: Bearer $USER_TOKEN"
    Expected Result: 403 Forbidden
    Failure Indicators: 200 (leak), 500 (error)
    Evidence: .sisyphus/evidence/task-8-user-403.txt
  \`\`\`

  **Commit**: YES
  - Message: `feat(api): add admin user management endpoints`
  - Files: `db.py`, `farm_daemon.py`
  - Pre-commit: `python3 -m py_compile farm_daemon.py`

---

- [ ] 9. **Add user dashboard API endpoints**

  **What to do**:
  - `GET /user/devices` — list of devices owned by current user (via tenant_id or explicit ownership table)
    - Add `device_ownership` table: `user_id` (FK), `device_serial` (FK), `earned_credits`, `joined_at`
    - OR use `tenant_id` — each user has one tenant, devices have tenant_id
  - `GET /user/earnings` — earnings history, paginated, with date filters
    - Returns: list of earning events, total earned, pending payout
  - `GET /user/stats` — total devices, total earned, this month's earnings, pending credits
  - `POST /user/devices/claim` — claim a device serial for the current user (device must not already be claimed)
  - `GET /user/notifications` — recent notifications for the user
  - `require_user_auth()` dependency ensures session-only auth
  - **Test cases**: user sees only their devices, non-owned device not shown, earnings aggregation

  **Must NOT do**:
  - Do NOT let user see another user's devices or earnings
  - Do NOT allow claiming an already-claimed device without admin override

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Standard REST endpoints with authorization
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - None

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with T8, T10, T11, T12, T13)
  - **Blocks**: T12 (user dashboard UI)
  - **Blocked By**: T8 (device ownership model)

  **References**:

  **Pattern References** (existing code to follow):
  - `farm_daemon.py:661-676` — `/devices` endpoint as pattern for `/user/devices`
  - `db.py:517-531` — `get_groups()` with QueryParams as pagination pattern

  **Acceptance Criteria**:

  \`\`\`
  Scenario: User sees only their devices
    Tool: Bash (curl)
    Preconditions: User has claimed devices, other users have devices
    Steps:
      1. curl -s http://localhost:8889/user/devices \
           -H "Authorization: Bearer $USER_TOKEN" | \
           python3 -c "import sys,json; d=json.load(sys.stdin); serials=[x['serial'] for x in d.get('items',[])]; print('OK - devices:', serials)"
    Expected Result: Only devices owned by the requesting user
    Failure Indicators: Devices from other users visible
    Evidence: .sisyphus/evidence/task-9-user-devices.json
  \`\`\`

  **Commit**: YES
  - Message: `feat(api): add user dashboard endpoints (my devices, earnings, stats)`
  - Files: `db.py`, `farm_daemon.py`
  - Pre-commit: `python3 -m py_compile farm_daemon.py`

---

- [ ] 10. **Add admin dashboard API endpoints**

  **What to do**:
  - `GET /admin/stats` — platform-wide stats: total users, total devices, total earnings paid out, total tasks, revenue
  - `GET /admin/devices` — all devices across all users (paginated, filterable by owner, status)
  - `GET /admin/earnings` — all earnings events across platform (for payout management)
  - `GET /admin/tasks` — all tasks across platform with device/owner info
  - `POST /admin/devices/{serial}/reassign` — reassign device from one user to another
  - `GET /admin/notifications` — platform-wide notifications
  - All require `require_admin()` role check
  - **Test cases**: admin sees all data, user gets 403, pagination works

  **Must NOT do**:
  - Do NOT allow non-admin access
  - Do NOT expose raw password hashes in any response

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Admin-only endpoints with authorization
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - None

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with T8, T9, T11, T12, T13)
  - **Blocks**: T13 (admin dashboard UI)
  - **Blocked By**: T8 (admin auth)

  **References**:

  **Pattern References** (existing code to follow):
  - `farm_daemon.py:661-676` — `/devices` as pattern for `/admin/devices`
  - `db.py:440-483` — `get_stats()` as pattern for `/admin/stats`

  **Acceptance Criteria**:

  \`\`\`
  Scenario: Admin can access platform stats
    Tool: Bash (curl)
    Preconditions: Admin token
    Steps:
      1. curl -s http://localhost:8889/admin/stats \
           -H "Authorization: Bearer $ADMIN_TOKEN" | \
           python3 -c "import sys,json; d=json.load(sys.stdin); keys=['total_users','total_devices','total_earnings']; print('OK' if all(k in d for k in keys) else 'FAIL: '+str(d))"
    Expected Result: Stats with total_users, total_devices, total_earnings
    Failure Indicators: Missing keys, 403
    Evidence: .sisyphus/evidence/task-10-admin-stats.json
  \`\`\`

  **Commit**: YES
  - Message: `feat(api): add admin dashboard endpoints for platform-wide management`
  - Files: `db.py`, `farm_daemon.py`
  - Pre-commit: `python3 -m py_compile farm_daemon.py`

---

- [ ] 11. **Update dashboard SPA — add hash-based navigation + user/admin views**

  **What to do**:
  - Modify `dashboard/index.html` Alpine.js `app()` function:
    - Add hash-based routing: `window.location.hash` determines which view shows
    - Routes: `#/devices` (default for logged-in user), `#/user-dashboard`, `#/admin`
    - On load: check `localStorage.session_token`, if valid → show appropriate view, else → redirect to `/login.html`
    - Add `userRole` state variable: 'admin' | 'user' | 'consumer'
    - Add `isAdmin()` and `isUser()` helper functions that check role
    - Conditionally show nav items based on role (admin sees "Admin", user sees "My Dashboard")
    - Add `logout()` that clears session_token from localStorage and redirects to `/login.html`
  - Add `require_user_auth()` to all existing API calls (add Bearer token to fetch headers)
  - Update existing API calls to include `Authorization: Bearer <token>` header
  - Update `stats` loading to use role-appropriate endpoint
  - **Test cases**: hash routes work, admin sees admin nav, user redirected without token

  **Must NOT do**:
  - Do NOT break existing API key auth flow in the dashboard
  - Do NOT remove any existing dashboard sections
  - Do NOT change the URLs of existing dashboard sections

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Alpine.js SPA modification with routing logic
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - `frontend-ui-ux`: Could review but routing is straightforward

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with T8, T9, T10, T12, T13)
  - **Blocks**: T12 (user dashboard UI), T13 (admin dashboard UI)
  - **Blocked By**: T4 (login endpoint so we know the token format)

  **References**:

  **Pattern References** (existing code to follow):
  - `dashboard/index.html:151` — `x-data="app()"` entry point
  - `dashboard/index.html:169-176` — `navItems` array structure to extend
  - `dashboard/index.html:153-162` — Login check logic to replace with session check

  **WHY Each Reference Matters**:
  - All current dashboard logic is in the `app()` function and `x-init="init()"`

  **Acceptance Criteria**:

  \`\`\`
  Scenario: Dashboard redirects to login if no token
    Tool: playwright (playwright skill)
    Preconditions: Browser with no localStorage.session_token
    Steps:
      1. Clear localStorage
      2. Navigate to http://localhost:8889/dashboard/
      3. Assert redirected to /login.html
    Expected Result: Automatic redirect to login page
    Failure Indicators: Dashboard page visible without login
    Evidence: .sisyphus/evidence/task-11-redirect-no-token.png

  Scenario: Admin sees admin nav item
    Tool: playwright (playwright skill)
    Preconditions: Browser logged in as admin
    Steps:
      1. Login as admin
      2. Check sidebar nav items
      3. Assert "Admin" nav item visible
    Expected Result: Admin nav item visible in sidebar
    Failure Indicators: Admin nav item missing
    Evidence: .sisyphus/evidence/task-11-admin-nav.png
  \`\`\`

  **Commit**: YES
  - Message: `feat(ui): add hash-based SPA routing with role-based access control`
  - Files: `dashboard/index.html`
  - Pre-commit: None (HTML/JS)

---

- [ ] 12. **Build user dashboard UI (my devices, earnings, rental status)**

  **What to do**:
  - In `dashboard/index.html`, add new section `<!-- USER DASHBOARD -->` with `x-show="page === 'user-dashboard'"`
  - Subsections:
    1. **Earnings Overview**: Cards showing total earned, this month, pending payout, lifetime credits
    2. **My Devices**: List of user's connected devices (from `/user/devices`), status badge, battery, last seen
    3. **Earnings History**: Paginated table with date, device, task type, amount earned
    4. **How to Connect a Device**: Instructions panel with download link (for the client APK)
    5. **Referral/Earnings Calculator**: "If you connect 3 devices, earn ~$X/month"
  - Each device row has: device name, status (online/offline), earnings contributed, "View Screen" button → `/control/{serial}`
  - Earnings history table: columns (Date, Device, Task, Credits Earned), sortable, paginated (server-side)
  - Add to `navItems`: `{id: 'user-dashboard', label: 'My Dashboard', icon: '💰'}`
  - **Test cases**: earnings displayed, device list loads, history pagination works

  **Must NOT do**:
  - Do NOT show data from other users
  - Do NOT hardcode earnings values — always fetch from API

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
    - Reason: UI development with data fetching and conditional rendering
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - None

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with T8, T9, T10, T11, T13)
  - **Blocks**: T28 (dashboard polish)
  - **Blocked By**: T9 (user API endpoints), T11 (SPA routing)

  **References**:

  **Pattern References** (existing code to follow):
  - `dashboard/index.html:188-244` — Devices page as data fetching + display pattern
  - `dashboard/index.html:74-78` — `stat-card` grid for earnings overview cards
  - `dashboard/index.html:97-100` — `table` styling for earnings history
  - `dashboard/index.html:137-148` — Pagination + search styling

  **WHY Each Reference Matters**:
  - Reuse existing component patterns for consistency

  **Acceptance Criteria**:

  \`\`\`
  Scenario: User dashboard loads and shows earnings
    Tool: playwright (playwright skill)
    Preconditions: User logged in with earnings history
    Steps:
      1. Login as user
      2. Navigate to user dashboard
      3. Assert earnings cards visible (total, this month, pending)
      4. Assert device list loaded
      5. Assert earnings history table has rows
    Expected Result: All 4 subsections render with data
    Failure Indicators: Empty sections, 401 errors in console
    Evidence: .sisyphus/evidence/task-12-user-dashboard.png

  Scenario: Pagination on earnings history
    Tool: playwright (playwright skill)
    Preconditions: User has >10 earning records
    Steps:
      1. Navigate to user dashboard
      2. Assert pagination controls visible
      3. Click "Next" 
      4. Assert different data shown (page 2)
    Expected Result: Page 2 shows different earnings records
    Failure Indicators: Same data on all pages, pagination controls missing
    Evidence: .sisyphus/evidence/task-12-earnings-pagination.png
  \`\`\`

  **Commit**: YES
  - Message: `feat(ui): add user dashboard with earnings and device management views`
  - Files: `dashboard/index.html`
  - Pre-commit: None

---

- [ ] 13. **Build admin dashboard UI (all users, platform stats, user management)**

  **What to do**:
  - In `dashboard/index.html`, add new section `<!-- ADMIN DASHBOARD -->` with `x-show="page === 'admin'"`
  - Subsections:
    1. **Platform Overview**: Total users, total devices, total earnings paid out, active sessions, platform revenue
    2. **All Users**: Paginated table (Email, Name, Role, Devices, Total Earned, Status, Joined)
       - Click row → user detail modal
       - Actions: Ban/Unban, Adjust Credits, Delete, Impersonate
    3. **All Devices**: Paginated table across all users (Serial, Owner, Model, Status, Earnings, Connected)
    4. **Pending Payouts**: Users awaiting payout, amount, payment method
    5. **Platform Earnings**: Chart showing earnings over time (simple text-based bar chart if no chart lib)
  - Add to `navItems`: `{id: 'admin', label: 'Admin', icon: '⚙️'}` (only visible if `isAdmin()`)
  - **Test cases**: admin sees all users, user gets 403 trying to access admin page, ban/unban works

  **Must NOT do**:
  - Do NOT allow non-admin to access this page (must check server-side AND client-side)
  - Do NOT show raw user IDs in the UI — use email/name

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
    - Reason: UI with tables, modals, admin actions
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - None

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with T8, T9, T10, T11, T12)
  - **Blocks**: T31 (admin user management)
  - **Blocked By**: T10 (admin API endpoints), T11 (SPA routing)

  **References**:

  **Pattern References** (existing code to follow):
  - `dashboard/index.html:97-100` — Table styling for user/device tables
  - `dashboard/index.html:97-100` — Modal pattern (confirm dialogs use `x-show` with buttons)

  **Acceptance Criteria**:

  \`\`\`
  Scenario: Admin sees all users table
    Tool: playwright (playwright skill)
    Preconditions: Admin logged in
    Steps:
      1. Login as admin
      2. Navigate to Admin dashboard
      3. Assert table with all users visible
      4. Assert at least email and name columns
    Expected Result: Full user table with multiple users
    Failure Indicators: Empty table, missing columns, 403
    Evidence: .sisyphus/evidence/task-13-admin-users.png
  \`\`\`

  **Commit**: YES
  - Message: `feat(ui): add admin dashboard with platform management and user administration`
  - Files: `dashboard/index.html`
  - Pre-commit: None

---

- [ ] 14. **Design client protocol (WebSocket messages, device registration flow)**

  **What to do**:
  - Create `docs/client-protocol.md` — protocol specification for Android client ↔ platform communication
  - Document:
    1. **Registration Flow**: Client → Platform: `{"type":"register","device_serial","model","android_ver","owner_token"}`; Platform → Client: `{"type":"registered","client_id","api_token"}`
    2. **Heartbeat**: Client → Platform: `{"type":"heartbeat","client_id","status","battery","screen_on"}` every 30s; Platform → Client: `{"type":"ack"}`
    3. **Task Assignment**: Platform → Client: `{"type":"task","task_id","task_type","params":{}}`; Client → Platform: `{"type":"task_result","task_id","success","data","error"}`
    4. **Screen Streaming**: Client streams JPEG frames over WebSocket; Platform sends `{type:"screencap_request"}`; Client sends binary frames
    5. **Earnings Update**: Platform → Client: `{"type":"earning","amount","total"}` after task completion
    6. **Disconnect**: Client sends `{"type":"disconnect"}` on app close
  - Authentication: Bearer token (from registration) in WebSocket URL: `wss://platform/ws/client?token=<api_token>`
  - Error codes: `AUTH_FAILED`, `DEVICE_LIMIT_REACHED`, `TASK_TIMEOUT`, `DEVICE_OFFLINE`
  - **Test cases**: Document all message types, verify no ambiguity in state transitions

  **Must NOT do**:
  - Do NOT use plaintext device_serial as identity — must use server-assigned client_id
  - Do NOT allow tasks to run without explicit user consent (for sensitive operations)

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Protocol design requiring security and architecture thinking
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - None

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with T15, T17, T18, T19, T20, T21, T22)
  - **Blocks**: T17-22 (all Android client features depend on this spec)
  - **Blocked By**: None (design work, can start anytime)

  **References**:

  **Pattern References** (existing code to follow):
  - `farm_daemon.py:586-632` — Existing WebSocket endpoint (`/ws/{serial}`) as message handling pattern
  - `farm_daemon.py:131-285` — `DeviceStreamer` class for screen frame format (JPEG) reference

  **External References** (libraries and frameworks):
  - WebSocket RFC 6455: `https://tools.ietf.org/html/rfc6455` — for message framing
  - ngrok reverse tunnel: `https://ngrok.com/docs/` — for NAT traversal approach

  **WHY Each Reference Matters**:
  - Existing WS endpoint shows the platform's WS handling patterns to stay consistent

  **Acceptance Criteria**:

  \`\`\`
  Scenario: Protocol document covers all message types
    Tool: Bash
    Preconditions: docs/client-protocol.md exists
    Steps:
      1. python3 -c "
          import re
          content = open('docs/client-protocol.md').read()
          msg_types = re.findall(r'type.*?register|heartbeat|task|screencap|earning|disconnect', content, re.IGNORECASE)
          print('Found', len(msg_types), 'message type references')
          print('OK' if len(msg_types) >= 12 else 'FAIL - missing message types')
      "
    Expected Result: All 6 message types documented with fields and flow
    Failure Indicators: Missing message types, unclear field definitions
    Evidence: .sisyphus/evidence/task-14-protocol-check.txt
  \`\`\`

  **Commit**: YES
  - Message: `docs: add client protocol specification for device rental`
  - Files: `docs/client-protocol.md`
  - Pre-commit: None

---

- [ ] 15. **Create Android project scaffold (Kotlin, Gradle, dependencies)**

  **What to do**:
  - Create `client-android/` directory with Android Studio project structure
  - Key files:
    - `build.gradle.kts` (root): Android Gradle plugin 8.x, Kotlin 1.9.x
    - `app/build.gradle.kts`: minSdk 26 (Android 8), targetSdk 34, permissions (INTERNET, ACCESS_NETWORK_STATE, FOREGROUND_SERVICE)
    - `app/src/main/AndroidManifest.xml`: INTERNET permission, foreground service permission, no special privacy-invasive permissions
    - `app/src/main/kotlin/com/phonefarm/client/`:
      - `MainActivity.kt` — Entry point, shows login/register + device list
      - `ClientApp.kt` — Application class for global state
      - `WebSocketManager.kt` — WebSocket connection management with auto-reconnect
      - `DeviceInfo.kt` — Data class with serial, model, Android version
      - `TaskExecutor.kt` — Receives and executes tasks via ADB
  - Dependencies: OkHttp WebSocket, Kotlin Coroutines, AndroidX Core KTX, Material Design Components
  - `local.properties`: SDK path reference
  - `gradle.properties`: AndroidX configuration
  - Build script uses Gradle wrapper (no system Gradle required for rebuild)
  - **Test cases**: Project compiles to debug APK, basic activity launches

  **Must NOT do**:
  - Do NOT require root permissions
  - Do NOT add permissions without explaining why in comments
  - Do NOT use deprecated APIs

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Android project setup with Gradle, multiple files, first-time for this codebase
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - None

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with T14, T16, T17, T18, T19, T20, T21, T22)
  - **Blocks**: T17-22 (all features need the scaffold)
  - **Blocked By**: T14 (protocol spec needed for WebSocketManager)

  **References**:

  **Pattern References** (existing code to follow):
  - `device_manager.py:42-47` — Shows how device serial and model are detected

  **External References** (libraries and frameworks):
  - Android Gradle plugin: `https://developer.android.com/build/gradle-plugin-8-7-0` — AGP 8.x configuration
  - OkHttp WebSocket: `https://square.github.io/okhttp/4.x/okhttp/okhttp3/-web-socket/` — WebSocket client
  - Kotlin Coroutines: `https://kotlinlang.org/docs/coroutines-overview.html`

  **Acceptance Criteria**:

  \`\`\`
  Scenario: Android project compiles to debug APK
    Tool: Bash (gradle)
    Preconditions: Java 17+, Android SDK installed
    Steps:
      1. cd client-android && ./gradlew assembleDebug 2>&1 | tail -20
    Expected Result: BUILD SUCCESSFUL, .apk generated at app/build/outputs/apk/debug/
    Failure Indicators: Compilation errors, missing dependencies
    Evidence: .sisyphus/evidence/task-15-apk-build.txt

  Scenario: Basic activity launches in emulator
    Tool: Bash (adb)
    Preconditions: APK installed on emulator or device
    Steps:
      1. adb install -r client-android/app/build/outputs/apk/debug/app-debug.apk
         adb shell am start -n com.phonefarm.client/.MainActivity
         adb shell dumpsys activity activities | grep mResumedActivity
    Expected Result: MainActivity is resumed/lunched
    Failure Indicators: Activity not found, crash on launch
    Evidence: .sisyphus/evidence/task-15-activity-launch.txt
  \`\`\`

  **Commit**: YES
  - Message: `feat(client-android): add Android project scaffold for device rental client`
  - Files: `client-android/` (entire directory)
  - Pre-commit: `./gradlew assembleDebug`

---

- [ ] 16. **Implement device registration + authentication (client → platform)**

  **What to do**:
  - In `client-android/`, implement `AuthService.kt` and integrate into `MainActivity`:
    - Login screen: email/password fields, POST to `https://platform/auth/login`
    - Registration screen: email/password/name, POST to `https://platform/auth/register`
    - After login: store `api_token` and `user_id` in `SharedPreferences` (encrypted)
    - Device registration: on first launch, POST to `/auth/client/register` with device serial, model, Android version, user's api_token
    - Response: `client_id` (server-assigned UUID) + `device_api_token` (JWT for WS auth)
    - On app reopen: if `client_id` exists and `device_api_token` valid → go straight to main screen
    - On logout: clear SharedPreferences, return to login
  - Show onboarding: "Connect your first device" flow
  - **Test cases**: Registration flow works, stored credentials persist, logout clears state

  **Must NOT do**:
  - Do NOT store raw passwords — only store tokens from registration response
  - Do NOT hardcode platform URL — read from `local.properties` or `BuildConfig`

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Android Kotlin code with network calls
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - None

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with T14, T15, T17, T18, T19, T20, T21, T22)
  - **Blocks**: T22 (depends on all client features)
  - **Blocked By**: T15 (scaffold)

  **References**:

  **External References** (libraries and frameworks):
  - OkHttp: `https://square.github.io/okhttp/4.x/okhttp/okhttp3/` — HTTP client for registration API

  **Acceptance Criteria**:

  \`\`\`
  Scenario: User can register a device
    Tool: Bash (adb + curl simulation)
    Preconditions: APK installed, platform running
    Steps:
      1. adb shell am start -n com.phonefarm.client/.MainActivity
         # Simulate: register device via HTTP
         curl -s -X POST http://localhost:8889/auth/client/register \
           -H "Content-Type: application/json" \
           -d '{"user_token":"<user_token>","serial":"TEST123","model":"TestPhone","android_ver":"14"}' | \
           python3 -c "import sys,json; d=json.load(sys.stdin); print('OK' if d.get('client_id') else 'FAIL')"
    Expected Result: Device registered, client_id returned
    Failure Indicators: No client_id, error
    Evidence: .sisyphus/evidence/task-16-register-device.json
  \`\`\`

  **Commit**: YES
  - Message: `feat(client-android): add device registration and user authentication`
  - Files: `client-android/app/src/main/kotlin/.../AuthService.kt`, `MainActivity.kt`
  - Pre-commit: `./gradlew assembleDebug`

---

- [ ] 17. **Implement reverse tunnel manager (SSH reverse tunnel or ngrok-style)**

  **What to do**:
  - In `client-android/`, implement `TunnelManager.kt`:
    - Device needs to be reachable from platform (platform can't reach devices behind NAT)
    - Use **SSH reverse tunnel**: client opens outbound SSH connection to platform's public IP
      - `ssh -R 0:localhost:8888 platform@your-server.com -p 2222 -N -T`
      - This creates a port forward from platform's public port → device's local ADB
    - Alternative: Use **WebSocket tunnel** (simpler, no SSH server needed):
      - Client connects WebSocket to `wss://platform/ws/client`
      - All ADB commands go over this WebSocket
      - Platform's `DeviceStreamer` already handles WS → ADB conversion
    - Choose WebSocket tunnel approach (no server-side SSH required)
    - `TunnelManager` opens WebSocket connection, maintains it, auto-reconnects on dropout
    - Heartbeat ping every 30s to keep connection alive
    - Background foreground service keeps tunnel alive when app is backgrounded
  - **Test cases**: Tunnel connects, survives network switch, reconnects after kill

  **Must NOT do**:
  - Do NOT require port forwarding on user's router
  - Do NOT require a third-party tunnel service (ngrok) — must be self-hosted compatible

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Network architecture, WebSocket server changes needed
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - None

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with T14, T15, T16, T18, T19, T20, T21, T22)
  - **Blocks**: T19 (screen streaming needs tunnel), T20 (task execution needs tunnel)
  - **Blocked By**: T15 (scaffold)

  **References**:

  **Pattern References** (existing code to follow):
  - `farm_daemon.py:586-632` — Existing WS `/ws/{serial}` as WebSocket server pattern
  - `farm_daemon.py:131-285` — `DeviceStreamer` for frame capture and WS broadcast

  **WHY Each Reference Matters**:
  - Shows existing WS handling to design compatible client-side tunnel

  **Acceptance Criteria**:

  \`\`\`
  Scenario: WebSocket client tunnel connects to platform
    Tool: Bash (Python WS client)
    Preconditions: Farm daemon running with WS endpoint
    Steps:
      1. python3 -c "
          import asyncio, json, websockets
          async def test():
              token = '<device_api_token>'
              async with websockets.connect(f'ws://localhost:8889/ws/client?token={token}') as ws:
                  msg = await ws.recv()
                  print('OK - received:', json.loads(msg).get('type') if isinstance(msg, str) else 'binary')
          asyncio.run(test())
      "
    Expected Result: Connection established, platform sends registration prompt or ack
    Failure Indicators: Connection refused, auth failure
    Evidence: .sisyphus/evidence/task-17-tunnel-connect.txt
  \`\`\`

  **Commit**: YES
  - Message: `feat(client-android): add WebSocket tunnel manager for NAT traversal`
  - Files: `client-android/app/src/main/kotlin/.../TunnelManager.kt`
  - Pre-commit: `./gradlew assembleDebug`

---

- [ ] 18. **Implement screen streaming client (screencap → WebSocket → platform)**

  **What to do**:
  - In `client-android/`, implement `ScreenStreamer.kt`:
    - Uses `MediaProjection` API (requires user permission, shown once) to capture screen
    - Encodes frames as JPEG (quality 60-80) for bandwidth efficiency
    - Sends frames over WebSocket (from TunnelManager) every ~200ms (5 fps)
    - Handles orientation changes, stops streaming when app backgrounded
    - On platform request `{type:"screencap_request"}`: immediately send current frame
    - Permission request: explain "Screen sharing is only active when you're using the app"
  - Integrate with `DeviceStreamer` server-side (modify `farm_daemon.py`):
    - Add new WS endpoint `/ws/client` for incoming client connections
    - Client streams binary JPEG frames; server broadcasts to admin viewing that device
  - **Test cases**: Stream starts on demand, frames arrive at server, permission dialog shown

  **Must NOT do**:
  - Do NOT stream without explicit user consent (MediaProjection permission required)
  - Do NOT stream at full resolution — must scale down for bandwidth

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Android media APIs + WebSocket streaming
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - None

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with T14, T15, T16, T17, T19, T20, T21, T22)
  - **Blocks**: T22 (depends on all features)
  - **Blocked By**: T17 (tunnel must work first)

  **References**:

  **Pattern References** (existing code to follow):
  - `farm_daemon.py:161-186` — Existing screencap approach using `adb exec-out screencap`
  - `farm_daemon.py:161-186` — JPEG encoding as frame format
  - `farm_daemon.py:187-203` — Streaming loop as pattern

  **Acceptance Criteria**:

  \`\`\`
  Scenario: Server receives screen frames from client
    Tool: Bash (Python WS client sending JPEG)
    Preconditions: WebSocket endpoint ready
    Steps:
      1. python3 -c "
          import asyncio, websockets, struct
          async def send_frame():
              async with websockets.connect('ws://localhost:8889/ws/client?token=test') as ws:
                  # Send binary JPEG frame (mock)
                  await ws.send(b'\\xff\\xd8\\xff\\xe0MOCK_JPEG')
                  print('OK - frame sent')
          asyncio.run(send_frame())
      "
    Expected Result: Frame accepted without error
    Failure Indicators: Connection rejected, server error
    Evidence: .sisyphus/evidence/task-18-frame-received.txt
  \`\`\`

  **Commit**: YES
  - Message: `feat(client-android): add screen streaming via WebSocket tunnel`
  - Files: `client-android/app/src/main/kotlin/.../ScreenStreamer.kt`, `farm_daemon.py`
  - Pre-commit: `./gradlew assembleDebug && python3 -m py_compile farm_daemon.py`

---

- [ ] 19. **Implement task execution engine (receive task → execute via ADB → report result)**

  **What to do**:
  - In `client-android/`, implement `TaskExecutor.kt`:
    - Receives task assignment from platform over WebSocket: `{"type":"task","task_id":"...","task_type":"health_check","params":{}}`
    - Maps `task_type` → local shell command(s) via ADB:
      - `health_check`: `dumpsys battery`, `dumpsys power`
      - `screenshot`: `screencap -p /sdcard/tmp.png && base64 /sdcard/tmp.png`
      - `app_check`: `pm list packages -3`
      - Custom tasks: execute whatever shell commands are provided in `params`
    - Captures output, reports result to platform: `{"type":"task_result","task_id":"...","success":true,"data":"output"}`
    - Timeout: default 60s, configurable per task
    - Error handling: if command fails, report with error message
  - Built-in task registry in `TaskExecutor`: maps task_type → shell command + timeout
  - **Test cases**: health_check runs, result sent back, timeout works, unknown task rejected

  **Must NOT do**:
  - Do NOT allow arbitrary shell execution from platform (security: only predefined task types)
  - Do NOT run tasks without user being aware (show notification before/during)
  - Do NOT allow file system access beyond /sdcard/

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Android ADB execution + WebSocket communication
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - None

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with T14, T15, T16, T17, T18, T20, T21, T22)
  - **Blocks**: T22 (depends on all features)
  - **Blocked By**: T17 (tunnel must work first)

  **References**:

  **Pattern References** (existing code to follow):
  - `device_manager.py` — Existing ADB command patterns to replicate on client
  - `task_runner.py` — Task registry and execution pattern as reference

  **Acceptance Criteria**:

  \`\`\`
  Scenario: Task execution returns result
    Tool: Bash (Python WS test)
    Preconditions: WS client connected, TaskExecutor running
    Steps:
      1. python3 -c "
          import asyncio, websockets, json
          async def test():
              async with websockets.connect('ws://localhost:8889/ws/client?token=test') as ws:
                  # Receive task
                  task = await ws.recv()
                  print('Received:', json.loads(task).get('type'))
                  # Send result
                  result = {'type':'task_result','task_id':'123','success':True,'data':'ok'}
                  await ws.send(json.dumps(result))
                  print('OK - result sent')
          asyncio.run(test())
      "
    Expected Result: Task received, result acknowledged
    Failure Indicators: No task received, result not sent
    Evidence: .sisyphus/evidence/task-19-task-execution.txt
  \`\`\`

  **Commit**: YES
  - Message: `feat(client-android): add task execution engine via ADB`
  - Files: `client-android/app/src/main/kotlin/.../TaskExecutor.kt`
  - Pre-commit: `./gradlew assembleDebug`

---

- [ ] 20. **Implement earnings heartbeat (periodic credits update to platform)**

  **What to do**:
  - In `client-android/`, implement `EarningsTracker.kt`:
    - Each completed task earns credits: configured per task_type (e.g., health_check = 0.01, screenshot = 0.02)
    - Tracks local earnings counter in SharedPreferences
    - Every 5 minutes OR after each task completion, sends earnings update to platform via HTTP POST:
      - `POST /user/earnings/report` with `{"client_id","earned":[{"task_type","count","credits"}]}`
    - Platform aggregates and credits the user's account
    - Show notification: "You earned 0.05 credits today! Total: 2.35 credits"
  - UI: Earnings counter on main screen, tap for history
  - **Test cases**: Earnings accumulate correctly, update sent to platform, notification shown

  **Must NOT do**:
  - Do NOT trust client-reported earnings directly — platform must validate and adjust
  - Do NOT show misleading earnings estimates

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Business logic + notifications
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - None

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with T14, T15, T16, T17, T18, T19, T21, T22)
  - **Blocks**: T22 (depends on all features)
  - **Blocked By**: T16 (needs user token for earnings endpoint)

  **References**:

  **Pattern References** (existing code to follow):
  - `dashboard/index.html:137-148` — Notification/toast styling for earnings notifications

  **Acceptance Criteria**:

  \`\`\`
  Scenario: Earnings update sent to platform
    Tool: Bash (curl)
    Preconditions: Valid user token, client_id
    Steps:
      1. curl -s -X POST http://localhost:8889/user/earnings/report \
           -H "Content-Type: application/json" \
           -H "Authorization: Bearer $USER_TOKEN" \
           -d '{"client_id":"test-client","earned":[{"task_type":"health_check","count":5,"credits":"0.05"}]}' | \
           python3 -c "import sys,json; d=json.load(sys.stdin); print('OK' if d.get('ok') else 'FAIL')"
    Expected Result: Earnings credited to user account
    Failure Indicators: 401, 500, or rejected
    Evidence: .sisyphus/evidence/task-20-earnings-report.json
  \`\`\`

  **Commit**: YES
  - Message: `feat(client-android): add earnings tracker with platform reporting`
  - Files: `client-android/app/src/main/kotlin/.../EarningsTracker.kt`
  - Pre-commit: `./gradlew assembleDebug`

---

- [ ] 21. **Build debug APK, test basic connect/register flow**

  **What to do**:
  - Final assembly and smoke test of Android client:
    - `./gradlew assembleDebug` → produces `app-debug.apk`
    - Verify APK size is reasonable (<20MB)
    - Verify APK is signed (debug keystore)
    - Verify main activity is launchable
  - Manual test flow on emulator:
    1. Launch app → Login/Register screen
    2. Register new user → auto-login
    3. See "Connect your first device" onboarding
    4. (Simulate) Device registered → main screen with device list
    5. Verify tunnel WebSocket attempts connection to platform
  - Package the APK at `client-android/app/build/outputs/apk/debug/app-debug.apk`
  - Create `client-android/README.md` with: how to build, how to configure platform URL, how to install
  - **Test cases**: APK builds, installs, launches, connects, registers

  **Must NOT do**:
  - Do NOT release to Play Store yet — debug APK only for testing
  - Do NOT hardcode production URLs

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Final assembly + smoke testing of Android app
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - None

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with T14, T15, T16, T17, T18, T19, T20, T22)
  - **Blocks**: None (final task of Wave 3)
  - **Blocked By**: T15-T20 (all client features must be done)

  **References**:

  **Pattern References** (existing code to follow):
  - `README.md` — As format template for client-android/README.md

  **Acceptance Criteria**:

  \`\`\`
  Scenario: APK builds successfully
    Tool: Bash (gradle)
    Preconditions: Java + Android SDK
    Steps:
      1. cd client-android && ./gradlew assembleDebug 2>&1 | grep -E "BUILD|apk|Error"
    Expected Result: BUILD SUCCESSFUL, app-debug.apk exists
    Failure Indicators: Build errors, missing outputs
    Evidence: .sisyphus/evidence/task-21-apk-build.txt

  Scenario: APK is installable and launches
    Tool: Bash (adb)
    Preconditions: APK from scenario 1, Android device/emulator
    Steps:
      1. adb install -r client-android/app/build/outputs/apk/debug/app-debug.apk
         adb shell am start -n com.phonefarm.client/.MainActivity
         sleep 2
         adb shell dumpsys activity activities | grep mResumedActivity | grep MainActivity
    Expected Result: MainActivity launched
    Failure Indicators: Install failed, activity not found
    Evidence: .sisyphus/evidence/task-21-install-launch.txt
  \`\`\`

  **Commit**: YES
  - Message: `feat(client-android): build debug APK and test registration flow`
  - Files: `client-android/app/build/outputs/apk/debug/app-debug.apk`, `client-android/README.md`
  - Pre-commit: `./gradlew assembleDebug`

---

- [ ] 22. **Create User Manual (Markdown) — sign-up, connect device, earn money, FAQ**

  **What to do**:
  - Create `docs/user-manual.md`:
    1. **Getting Started**: Create account, download client app, system requirements
    2. **Connecting Your First Device**: Step-by-step with screenshots (or descriptions)
    3. **Understanding Earnings**: How credits work, payout schedule, fee structure
    4. **Managing Devices**: Add/remove devices, check status, troubleshoot connectivity
    5. **Device Client App**: Settings (pause earning, data saver mode), notifications
    6. **FAQ**: Is my device safe? What tasks are run? How much can I earn? When do I get paid?
    7. **Privacy & Security**: What data is accessed, how tasks are sandboxed, data retention
    8. **Support**: How to report issues, contact info
  - Keep it user-friendly, not overly technical
  - Use simple language for non-technical users
  - **Test cases**: All sections populated, links work, FAQ covers major concerns

  **Must NOT do**:
  - Do NOT include API keys or technical details (that's for the developer guide)
  - Do NOT make assumptions about user technical knowledge

  **Recommended Agent Profile**:
  - **Category**: `writing`
    - Reason: Content writing, user-facing documentation
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - None

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with T23, T25, T26, T27, T28)
  - **Blocks**: None (documentation only)
  - **Blocked By**: None

  **References**:

  **Pattern References** (existing code to follow):
  - `README.md` — As writing quality reference and Markdown format reference

  **Acceptance Criteria**:

  \`\`\`
  Scenario: User manual covers all major sections
    Tool: Bash
    Preconditions: docs/user-manual.md exists
    Steps:
      1. python3 -c "
          content = open('docs/user-manual.md').read().lower()
          sections = ['getting started', 'connecting', 'earnings', 'faq', 'privacy', 'support']
          missing = [s for s in sections if s not in content]
          print('OK' if not missing else 'MISSING: '+str(missing))
          print('Size:', len(content), 'chars')
      "
    Expected Result: All 6 sections present, >2000 chars
    Failure Indicators: Missing sections, too short (<1000 chars)
    Evidence: .sisyphus/evidence/task-22-manual-check.txt
  \`\`\`

  **Commit**: YES
  - Message: `docs: add user manual with setup, earning, and FAQ sections`
  - Files: `docs/user-manual.md`
  - Pre-commit: None

---

- [ ] 23. **Generate OpenAPI spec (auto via FastAPI + redocly)**

  **What to do**:
  - FastAPI auto-generates OpenAPI at `/openapi.json`
  - Enhance with proper docstrings on all endpoints in `farm_daemon.py`:
    - Add `summary=`, `description=`, `response_model=` to all route decorators
    - Add example request/response for complex endpoints
  - Install `redocly` or use FastAPI's built-in `/docs` (Swagger UI)
  - Document the new auth endpoints: register, login, logout, password-reset, /me
  - Document the new user endpoints: /user/devices, /user/earnings, /user/stats
  - Document the new admin endpoints: /admin/users, /admin/stats, /admin/devices
  - Document WebSocket endpoint: `/ws/client` for device client connections
  - Serve OpenAPI JSON at `/openapi.json` (already FastAPI default)
  - Serve Swagger UI at `/docs`
  - Serve ReDoc at `/redoc` (install redocly and add route)
  - **Test cases**: `/docs` loads, `/openapi.json` valid, all new endpoints documented

  **Must NOT do**:
  - Do NOT expose internal error details in OpenAPI responses
  - Do NOT document deprecated endpoints inconsistently

  **Recommended Agent Profile**:
  - **Category**: `unspecified-low`
    - Reason: Documentation + FastAPI decorator enhancement
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - None

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with T22, T25, T26, T27, T28)
  - **Blocks**: None (documentation)
  - **Blocked By**: T3, T4 (auth endpoints must exist first)

  **References**:

  **Pattern References** (existing code to follow):
  - `farm_daemon.py:507` — FastAPI `app = FastAPI(title=...)` as setup reference

  **External References** (libraries and frameworks):
  - FastAPI docs: `https://fastapi.tiangolo.com/features/` — OpenAPI auto-generation
  - ReDoc: `https://redocly.com/docs/redoc/` — Alternative API documentation UI

  **Acceptance Criteria**:

  \`\`\`
  Scenario: OpenAPI JSON is valid and complete
    Tool: Bash (curl)
    Preconditions: Farm daemon running
    Steps:
      1. curl -s http://localhost:8889/openapi.json | python3 -c "
          import sys, json
          d = json.load(sys.stdin)
          paths = list(d.get('paths', {}).keys())
          print('Endpoints:', len(paths))
          new_endpoints = ['/auth/register', '/auth/login', '/user/devices', '/admin/users']
          missing = [e for e in new_endpoints if e not in paths]
          print('OK - all new endpoints' if not missing else 'MISSING: '+str(missing))
      "
    Expected Result: All new endpoints present in OpenAPI spec
    Failure Indicators: Missing endpoints, invalid JSON
    Evidence: .sisyphus/evidence/task-23-openapi.json

  Scenario: Swagger UI accessible
    Tool: Bash (curl)
    Preconditions: Farm daemon running
    Steps:
      1. curl -s -o /dev/null -w "%{http_code}" http://localhost:8889/docs
    Expected Result: 200 (Swagger UI loads)
    Failure Indicators: 404, 500
    Evidence: .sisyphus/evidence/task-23-swagger-ui.txt
  \`\`\`

  **Commit**: YES
  - Message: `docs: enhance OpenAPI spec with docstrings and serve Swagger UI`
  - Files: `farm_daemon.py`
  - Pre-commit: `python3 -m py_compile farm_daemon.py`

---

- [ ] 24. **Create Developer Guide — API reference, client protocol, WebSocket messages**

  **What to do**:
  - Create `docs/developer-guide.md`:
    1. **Overview**: Phone Farm architecture, platform components
    2. **Quick Start**: Clone, configure, run locally
    3. **API Reference**: All REST endpoints with request/response examples
       - Auth: `/auth/register`, `/auth/login`, `/auth/logout`, `/auth/me`
       - Devices: `/devices`, `/device/{serial}/screenshot`, `/device/{serial}/task/{task_type}`
       - Users: `/user/devices`, `/user/earnings`, `/admin/users`
    4. **WebSocket Protocol**: Full message reference for `/ws/client`
       - Message types: `register`, `heartbeat`, `task`, `task_result`, `screencap_request`, `earning`
       - Authentication: token in query param
    5. **Database Schema**: All tables, columns, relationships (from db.py)
    6. **Authentication**: JWT vs session tokens vs API keys (existing vs new)
    7. **Adding New Task Types**: How to add a new built-in task
    8. **Testing**: How to run tests, test device farm locally
    9. **Deployment**: Docker, systemd, environment variables
  - **Test cases**: All API endpoints documented, WebSocket protocol documented, code examples compile

  **Must NOT do**:
  - Do NOT include credentials or secrets
  - Do NOT duplicate content from user-manual.md

  **Recommended Agent Profile**:
  - **Category**: `writing`
    - Reason: Technical documentation with code examples
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - None

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with T22, T23, T26, T27, T28)
  - **Blocks**: None (documentation)
  - **Blocked By**: T14 (client protocol must be designed first)

  **References**:

  **Pattern References** (existing code to follow):
  - `README.md` — For structure and writing quality
  - `docs/client-protocol.md` (T14) — Reference for WebSocket section

  **Acceptance Criteria**:

  \`\`\`
  Scenario: Developer guide covers all major sections
    Tool: Bash
    Preconditions: docs/developer-guide.md exists
    Steps:
      1. python3 -c "
          content = open('docs/developer-guide.md').read().lower()
          sections = ['api reference', 'websocket', 'database schema', 'authentication', 'deployment']
          missing = [s for s in sections if s not in content]
          print('OK' if not missing else 'MISSING: '+str(missing))
          print('Size:', len(content), 'chars')
      "
    Expected Result: All 5 sections present, >3000 chars
    Failure Indicators: Missing sections, too short
    Evidence: .sisyphus/evidence/task-24-dev-guide-check.txt
  \`\`\`

  **Commit**: YES
  - Message: `docs: add developer guide with API reference and protocol documentation`
  - Files: `docs/developer-guide.md`
  - Pre-commit: None

---

- [ ] 25. **Add password reset email flow (token-based, SMTP)**

  **What to do**:
  - In `farm_daemon.py`:
    - `POST /auth/password-reset/request`: generate token, send email via SMTP
      - If SMTP not configured: log token to console as fallback
      - Email template: "Reset your Phone Farm password: {reset_link}"
      - Reset link: `https://platform/reset-password.html?token={token}`
    - `POST /auth/password-reset/confirm`: validate token, update password, consume token
  - Add `smtp_config` to `.env.example`: `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `SMTP_FROM`, `SMTP_TLS`
  - In `auth_user.py`: `send_password_reset_email(email, token)` function
  - **Test cases**: Request generates token, email sent (or logged), valid token resets password, expired token rejected

  **Must NOT do**:
  - Do NOT send email without HTTPS (token in URL is security risk — use POST form)
  - Do NOT store reset tokens in plain text

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Email sending, token lifecycle, security considerations
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - None

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with T22, T23, T24, T27, T28)
  - **Blocks**: None
  - **Blocked By**: T2 (password reset token functions)

  **References**:

  **Pattern References** (existing code to follow):
  - `auth_user.py` — Token creation pattern from T2

  **Acceptance Criteria**:

  \`\`\`
  Scenario: Password reset token generated and logged
    Tool: Bash (curl)
    Preconditions: User exists, farm daemon running
    Steps:
      1. curl -s -X POST http://localhost:8889/auth/password-reset/request \
           -H "Content-Type: application/json" \
           -d '{"email":"test@example.com"}' | \
           python3 -c "import sys,json; print(json.load(sys.stdin))"
    Expected Result: Always 200 (no email enumeration), token logged to server console
    Failure Indicators: Error response to client, no token logged
    Evidence: .sisyphus/evidence/task-25-reset-request.json
  \`\`\`

  **Commit**: YES
  - Message: `feat(auth): add password reset email flow with SMTP support`
  - Files: `farm_daemon.py`, `auth_user.py`, `.env.example`
  - Pre-commit: `python3 -m py_compile farm_daemon.py`

---

- [ ] 26. **Add email notifications (new device connected, earnings milestone)**

  **What to do**:
  - In `farm_daemon.py`, add email notification endpoints/services:
    - `POST /notifications/email/send` (internal, called by other services)
    - Trigger on: device connected, device disconnected, earnings milestone ($1, $10, $100), payout processed
    - Email templates: plain text, simple HTML, configurable via DB
  - Add `notifications` table: `id`, `user_id`, `type`, `channel` (email/in_app), `sent_at`, `payload`
  - `GET /user/notifications` — list user's notifications (in-app + email)
  - `PUT /user/notifications/preferences` — set which notifications to receive via email
  - **Test cases**: Notification created on device connect, user can fetch notifications, preferences work

  **Must NOT do**:
  - Do NOT send notification emails without user opt-in for marketing
  - Do NOT store full email content in logs

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Notification system with multiple channels
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - None

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with T22, T23, T24, T25, T28)
  - **Blocks**: None
  - **Blocked By**: T25 (SMTP config needed)

  **Acceptance Criteria**:

  \`\`\`
  Scenario: Notification created on device connect
    Tool: Bash (curl)
    Preconditions: User logged in, device registered
    Steps:
      1. curl -s http://localhost:8889/user/notifications \
           -H "Authorization: Bearer $USER_TOKEN" | \
           python3 -c "import sys,json; d=json.load(sys.stdin); print('OK' if isinstance(d.get('items',[]), list) else 'FAIL')"
    Expected Result: List of notifications returned
    Failure Indicators: 401, empty without notifications
    Evidence: .sisyphus/evidence/task-26-notifications.json
  \`\`\`

  **Commit**: YES
  - Message: `feat(notifications): add email and in-app notification system`
  - Files: `db.py`, `farm_daemon.py`
  - Pre-commit: `python3 -m py_compile farm_daemon.py`

---

- [ ] 27. **Dashboard polish — dark/light mode, export to CSV, UI improvements**

  **What to do**:
  - Dark/light mode toggle in dashboard:
    - Add `theme` state variable ('dark' | 'light')
    - Add CSS variable overrides for light mode
    - Persist theme preference in `localStorage`
    - Toggle button in sidebar footer
  - Export to CSV on tables:
    - Devices: export device list as CSV
    - Tasks: export task history as CSV
    - Earnings: export earnings history as CSV
    - Button on each table: "Export CSV" → downloads file
  - UI improvements:
    - Loading skeletons/spinners on async operations
    - Toast notifications for actions (device added, task run, etc.)
    - Improved empty states with helpful messages
    - Better error messages on API failures
    - Responsive improvements for mobile
  - **Test cases**: Theme toggle works, CSV export produces valid file, spinners show during load

  **Must NOT do**:
  - Do NOT break existing functionality while adding theme toggle
  - Do NOT add charting libraries (keep it simple text/bar based)

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
    - Reason: UI enhancements, CSS, interactivity
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - None

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with T22, T23, T24, T25, T26)
  - **Blocks**: None
  - **Blocked By**: T12, T13 (dashboards must exist first)

  **References**:

  **Pattern References** (existing code to follow):
  - `dashboard/index.html:40-148` — Existing CSS as theme base
  - `dashboard/index.html:115-116` — Toast notification styling

  **Acceptance Criteria**:

  \`\`\`
  Scenario: Theme toggle switches between dark and light
    Tool: playwright (playwright skill)
    Preconditions: Dashboard loaded
    Steps:
      1. Login to dashboard
      2. Toggle theme to light
      3. Assert background color changes to light
      4. Toggle back to dark
      5. Assert background returns to dark
    Expected Result: Theme toggles smoothly, persists on reload
    Evidence: .sisyphus/evidence/task-27-theme-toggle.png

  Scenario: CSV export produces valid file
    Tool: playwright (playwright skill)
    Preconditions: Dashboard loaded with data
    Steps:
      1. Login to dashboard
      2. Navigate to Devices page
      3. Click "Export CSV"
      4. Assert downloaded file is CSV with header row and data
    Expected Result: Valid CSV with device data
    Failure Indicators: Empty file, wrong format, missing columns
    Evidence: .sisyphus/evidence/task-27-csv-export.csv
  \`\`\`

  **Commit**: YES
  - Message: `feat(ui): add dark/light theme toggle, CSV export, and polish improvements`
  - Files: `dashboard/index.html`
  - Pre-commit: None

---

## Final Verification Wave

> 4 review agents run in PARALLEL. ALL must APPROVE. Rejection → fix → re-run.

- [ ] **F1. Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists (read file, curl endpoint, run command). For each "Must NOT Have": search codebase for forbidden patterns — reject with file:line if found. Check evidence files exist in .sisyphus/evidence/. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [ ] **F2. Code Quality Review** — `unspecified-high`
  Run `python3 -m py_compile` on all modified Python files + `python3 -m pyflakes` or basic lint. For Android: `./gradlew assembleDebug` passes. Review all changed files for: `as any`/`@ts-ignore`, empty catches, `console.log` in prod, commented-out code, unused imports. Check AI slop: excessive comments, over-abstraction, generic names (data/result/item/temp).
  Output: `Build [PASS/FAIL] | Files [N clean/N issues] | VERDICT`

- [ ] **F3. Real Manual QA** — `unspecified-high` (+ `playwright` skill if UI)
  Start from clean state. Execute EVERY QA scenario from EVERY task — follow exact steps, capture evidence. Test cross-task integration (features working together, not isolation). Test edge cases: empty state, invalid input, rapid actions. Save to `.sisyphus/evidence/final-qa/`.
  Output: `Scenarios [N/N pass] | Integration [N/N] | Edge Cases [N tested] | VERDICT`

- [ ] **F4. Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual diff (git log/diff). Verify 1:1 — everything in spec was built (no missing), nothing beyond spec was built (no creep). Check "Must NOT do" compliance. Detect cross-task contamination: Task N touching Task M's files without justification. Flag unaccounted changes.
  Output: `Tasks [N/N compliant] | Contamination [CLEAN/N issues] | Unaccounted [CLEAN/N files] | VERDICT`

---

## Commit Strategy

- Wave 1: `feat(auth): add user registration, login, password hashing`
- Wave 2: `feat(dashboard): add user and admin dashboard views`
- Wave 3: `feat(client): add Android device rental client APK`
- Wave 4: `docs: add user manual, API docs, developer guide`
- Wave 5: `test: add e2e tests and security audit`

---

## Success Criteria

- Landing page accessible at `/` with marketing content (200 response, non-empty body)
- User can register at `POST /auth/register` and login at `POST /auth/login`
- Protected routes return 401 without valid session token
- User dashboard (`#/user-dashboard`) shows device owner's devices and earnings
- Admin dashboard (`#/admin`) shows all users and platform stats
- Android APK compiles to `.apk` file
- APK connects to platform WebSocket and sends device registration
- OpenAPI docs available at `/docs`
- User manual at `docs/user-manual.md` covers all major flows

- [ ] **F1: Plan Compliance Audit** — `oracle`
- [ ] **F2: Code Quality Review** — `unspecified-high`
- [ ] **F3: Real Manual QA** — `unspecified-high`
- [ ] **F4: Scope Fidelity Check** — `deep`

---

## Commit Strategy

- Wave 1: `feat(auth): add user registration, login, password hashing`
- Wave 2: `feat(dashboard): add user and admin dashboard views`
- Wave 3: `feat(client): add Android device rental client APK`
- Wave 4: `docs: add user manual, API docs, developer guide`
- Wave 5: `test: add e2e tests and security audit`

---

## Success Criteria

- Landing page loads at `/` with marketing content (200 response, non-empty body)
- User can register at `POST /auth/register` and login at `POST /auth/login`
- Protected routes return 401 without valid session token
- User dashboard (`#/user-dashboard`) shows device owner's devices and earnings
- Admin dashboard (`#/admin`) shows all users and platform stats
- Android APK compiles to `.apk` file
- APK connects to platform WebSocket and sends device registration
- OpenAPI docs available at `/docs`
- User manual at `docs/user-manual.md` covers all major flows
