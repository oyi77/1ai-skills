# PhoneFarm SaaS — Consolidated Work Plan

## TL;DR

> Transform phonefarm from a self-managed device farm into a usage-based SaaS platform.
> Users pay per API call/task executed. Self-hosted for zero cloud costs.

> **Already Built**: auth.py (JWT+API keys), phonefarm_logging.py (JSON logging), db.py (groups/tags), farm_daemon.py (auth endpoints, health, webhooks), Dockerfile, docker-compose.yml, static dashboard
> **Remaining**: Multi-tenancy, billing, rate limiting, usage tracking, API versioning, modern Alpine.js dashboard, .env.example, integration testing
> **Estimated Effort**: XL (10-15 days)
> **Parallel Execution**: YES - 5 waves
> **Critical Path**: Auth → Multi-tenancy → Billing → Dashboard → Launch

---

## Context

### Current State (After Plan 1 Completion)
- JWT + API key auth (`auth.py`, 515 lines)
- Structured JSON logging (`phonefarm_logging.py`, 211 lines)
- SQLite with groups/tags (`db.py`, 406 lines)
- FastAPI server with auth, health, webhooks, groups/tags API (`farm_daemon.py`, 1018 lines)
- Docker deployment (`Dockerfile` + `docker-compose.yml`)
- Static HTML dashboard (`static/index.html`, 350 lines)
- Device manager + task runner fully operational

### What's Missing (This Plan)
- Multi-tenant data isolation
- Usage tracking and metering
- Rate limiting (token bucket)
- Stripe billing integration
- API versioning
- Modern Alpine.js dashboard with real-time updates
- .env.example configuration

---

## Work Objectives

### Core Objective
Make phonefarm a production-ready SaaS platform with multi-tenancy, usage-based billing, and a modern dashboard.

### Concrete Deliverables
- `tenant.py` — Multi-tenant isolation
- `rate_limiter.py` — Token bucket rate limiting
- `usage_tracker.py` — Usage tracking and metering
- `billing.py` — Stripe integration
- `dashboard/` — HTML+Alpine.js dashboard (replace static/)
- Updated `db.py` — tenant_id columns
- Updated `auth.py` — Multi-tenant JWT
- Updated `farm_daemon.py` — Tenant-aware endpoints
- Updated `Dockerfile` — SaaS-ready
- `.env.example` — All config variables

### Definition of Done
- [ ] All endpoints require tenant_id context
- [ ] Usage tracked per tenant per endpoint
- [ ] Stripe metered billing working
- [ ] Dashboard shows tenant-specific data
- [ ] API rate limiting enforced
- [ ] API versioning working
- [ ] .env.example documented

---

## Verification Strategy

- **Multi-tenancy**: Create 2 tenants, verify data isolation
- **Billing**: Test Stripe webhook, verify metered billing
- **Rate limiting**: Test rate limit exceeded, verify 429 response
- **Dashboard**: curl tests for dashboard pages
- **API**: curl tests for all endpoints

---

## Execution Strategy

### Wave 1: Foundation (Multi-tenancy + Rate Limiting)
- Task 1: Add tenant_id to all DB tables + update db.py
- Task 2: Create tenant.py for tenant management
- Task 3: Create rate_limiter.py (token bucket)
- Task 4: Update auth.py for multi-tenant JWT

### Wave 2: Billing + Usage Tracking
- Task 5: Create usage_tracker.py for metering
- Task 6: Create billing.py for Stripe integration
- Task 7: Add /billing endpoints to farm_daemon.py

### Wave 3: API + Integration
- Task 8: Update farm_daemon.py with tenant-aware endpoints
- Task 9: Add API versioning (/v1/)
- Task 10: Fix groups/tags to use db.py instead of in-memory dicts

### Wave 4: Dashboard
- Task 11: Create dashboard/ with HTML+Alpine.js layout
- Task 12: Dashboard: Device management page
- Task 13: Dashboard: Usage & billing page
- Task 14: Dashboard: Settings & API keys page
- Task 15: Dashboard: Real-time WebSocket integration

### Wave 5: Deployment + Polish
- Task 16: Update Dockerfile for SaaS
- Task 17: Create .env.example with all config
- Task 18: Update README with SaaS documentation
- Task 19: Integration testing (all endpoints)
- Task 20: Commit + push to GitHub

---

## TODOs

- [ ] 1. Add tenant_id to all DB tables + update db.py

  **What to do**:
  - Add `tenants` table (id TEXT PRIMARY KEY, name, email, stripe_customer_id, api_key_hash, created_at)
  - Add `tenant_id` column to devices, tasks, alerts, groups
  - Add foreign key constraint: tenant_id REFERENCES tenants(id)
  - Update init_db() to create new tables
  - Add migration function for existing data (set existing rows to 'default' tenant)
  - Update all existing db.py functions to accept optional tenant_id parameter for filtering
  - DO NOT break existing single-tenant usage (tenant_id defaults to 'default')

  **Must NOT do**:
  - Don't remove existing tables or columns
  - Don't break existing queries

  **References**:
  - Current `db.py` at /mnt/data/berkahkarya/skills/1ai-skills/automation/1ai-autodroid/phone-farm/db.py (406 lines)
  - Tables: devices, tasks, alerts, groups, device_groups, tags, device_tags

  **QA Scenarios**:
  - Create tenant, verify devices table accepts tenant_id
  - Query devices by tenant_id, verify isolation
  - Existing data still accessible with 'default' tenant_id

- [ ] 2. Create tenant.py for tenant management

  **What to do**:
  - Create `tenant.py` with TenantManager class
  - CRUD: create_tenant, get_tenant, update_tenant, list_tenants
  - API key generation (pf_tenant_xxx format, store hash in tenants table)
  - Tenant lookup by API key
  - Tenant stats (devices count, tasks count, usage)
  - Default tenant auto-created on init

  **Must NOT do**:
  - Don't use external auth services
  - Don't duplicate auth.py JWT logic

  **References**:
  - auth.py at /mnt/data/berkahkarya/skills/1ai-skills/automation/1ai-autodroid/phone-farm/auth.py
  - db.py for database access patterns

  **QA Scenarios**:
  - Create tenant, verify API key works
  - Query tenant stats, verify counts
  - Lookup tenant by API key hash

- [ ] 3. Create rate_limiter.py (token bucket)

  **What to do**:
  - Token bucket algorithm (in-memory, no Redis)
  - Per-tenant rate limits configurable per tenant
  - Default: 100 req/min, burst 20
  - Returns 429 Too Many Requests when exceeded
  - Headers: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset
  - FastAPI middleware integration

  **Must NOT do**:
  - Don't use Redis (keep zero-dep)
  - Don't use external rate limiting libraries

  **References**:
  - farm_daemon.py for middleware pattern

  **QA Scenarios**:
  - Send 100 requests rapidly, verify rate limit kicks in
  - Check rate limit headers in response
  - Different tenants have independent limits

- [ ] 4. Update auth.py for multi-tenant JWT

  **What to do**:
  - JWT includes tenant_id in payload
  - API key lookup returns tenant_id (from tenant.py)
  - require_auth decorator extracts tenant_id from token/key
  - All authenticated endpoints get tenant_id automatically
  - Backward compatible: existing tokens without tenant_id default to 'default'

  **Must NOT do**:
  - Don't break existing API key format (pf_ prefix)
  - Don't remove existing functionality

  **References**:
  - auth.py at /mnt/data/berkahkarya/skills/1ai-skills/automation/1ai-autodroid/phone-farm/auth.py (515 lines)
  - tenant.py for tenant lookup

  **QA Scenarios**:
  - Create JWT with tenant_id, verify payload
  - Use API key, verify tenant_id extracted
  - Old tokens without tenant_id still work (default)

- [ ] 5. Create usage_tracker.py for metering

  **What to do**:
  - Track API calls per tenant (in-memory counters)
  - Track tasks executed per tenant
  - Track by endpoint and method
  - Periodic flush to SQLite (every 60 seconds)
  - `usage` table in db.py (tenant_id, endpoint, method, count, period_start, period_end)
  - Query: get_usage(tenant_id, period)
  - Export: usage_report(tenant_id, start_date, end_date)

  **Must NOT do**:
  - Don't use external analytics services
  - Don't store raw per-request data (aggregate only)

  **References**:
  - db.py for SQLite patterns

  **QA Scenarios**:
  - Make 10 API calls, verify usage tracked
  - Query usage report, verify data
  - Flush to DB, verify persistence

- [ ] 6. Create billing.py for Stripe integration

  **What to do**:
  - Stripe metered billing for usage-based pricing
  - Create Stripe customer on tenant creation
  - Report usage to Stripe (daily batch)
  - Webhook handler for invoice.payment_succeeded/failed
  - Price config: $0.001/API call, $0.01/task
  - Graceful degradation if Stripe is unavailable
  - All Stripe keys from env vars (STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET)

  **Must NOT do**:
  - Don't hardcode Stripe keys
  - Don't break the app if Stripe is unavailable
  - Don't require Stripe for basic operation

  **References**:
  - tenant.py for tenant data
  - usage_tracker.py for usage data

  **QA Scenarios**:
  - Create tenant, verify Stripe customer created (or gracefully skipped if no key)
  - Simulate webhook, verify payment recorded
  - App works normally without Stripe keys set

- [ ] 7. Add /billing endpoints to farm_daemon.py

  **What to do**:
  - GET /billing/subscription — current plan and usage
  - GET /billing/invoices — list past invoices
  - POST /billing/portal — Stripe customer portal link
  - GET /billing/usage — current period usage
  - All endpoints require auth + tenant_id

  **Must NOT do**:
  - Don't expose Stripe internal IDs
  - Don't break existing endpoints

  **References**:
  - farm_daemon.py at /mnt/data/berkahkarya/skills/1ai-skills/automation/1ai-autodroid/phone-farm/farm_daemon.py (1018 lines)
  - billing.py for billing logic

  **QA Scenarios**:
  - GET /billing/subscription, verify plan data
  - GET /billing/usage, verify usage counts
  - Unauthenticated → 401

- [ ] 8. Update farm_daemon.py with tenant-aware endpoints

  **What to do**:
  - All device endpoints filter by tenant_id
  - All task endpoints filter by tenant_id
  - All alert endpoints filter by tenant_id
  - Add rate limit middleware to all endpoints
  - Add usage tracking to all endpoints
  - Health endpoints remain public (no tenant_id)
  - Auth endpoints remain public (no tenant_id for /auth/token)

  **Must NOT do**:
  - Don't break WebSocket endpoints
  - Don't expose other tenants' data
  - Don't break health/auth endpoints

  **References**:
  - farm_daemon.py (1018 lines)
  - rate_limiter.py for middleware
  - usage_tracker.py for tracking

  **QA Scenarios**:
  - Create 2 tenants, verify data isolation
  - Make API call, verify usage tracked
  - Rate limit kicks in after threshold

- [ ] 9. Add API versioning (/v1/)

  **What to do**:
  - Move current endpoints to /v1/ prefix (while keeping backward compat at root)
  - Add /v1/ prefix routes that mirror existing endpoints
  - Add version discovery endpoint /api/versions
  - Keep existing root-level endpoints working (backward compat)

  **Must NOT do**:
  - Don't break existing /devices, /tasks, etc. endpoints
  - Don't add version negotiation complexity

  **References**:
  - farm_daemon.py for current endpoint structure

  **QA Scenarios**:
  - GET /v1/devices, verify works
  - GET /devices, verify still works (backward compat)
  - GET /api/versions, verify list

- [ ] 10. Fix groups/tags to use db.py instead of in-memory dicts

  **What to do**:
  - Replace in-memory `_device_groups` dict in farm_daemon.py with db.py functions
  - Replace in-memory `_device_tags` dict in farm_daemon.py with db.py functions
  - Groups/tags API already exists in db.py (create_group, delete_group, add_device_to_group, etc.)
  - Also add tenant_id filtering to groups/tags

  **Must NOT do**:
  - Don't change db.py group/tag functions (they already work)
  - Don't break the API contract

  **References**:
  - farm_daemon.py lines 891-966 (in-memory groups/tags)
  - db.py lines 262-401 (groups/tags CRUD functions)

  **QA Scenarios**:
  - Create group via API, verify persisted to SQLite
  - Restart daemon, verify groups still exist
  - Add device to group, verify persisted

- [ ] 11. Create dashboard/ with HTML+Alpine.js layout

  **What to do**:
  - Create `dashboard/` directory
  - Create login page (API key input)
  - Layout with sidebar navigation (Devices, Tasks, Alerts, Usage, Billing, Settings)
  - Alpine.js via CDN for reactivity
  - Tailwind CSS via CDN for styling
  - Dark theme consistent with existing static/index.html
  - API integration with /v1/ endpoints
  - Replace static/index.html mount to serve from dashboard/

  **Must NOT do**:
  - Don't use build tools (no npm, no webpack)
  - Don't use React/Vue/Svelte

  **References**:
  - static/index.html for existing design patterns (dark theme, card layout)
  - farm_daemon.py for API endpoints

  **QA Scenarios**:
  - Load dashboard, verify login page
  - Enter API key, verify redirect to dashboard
  - All navigation links work

- [ ] 12. Dashboard: Device management page

  **What to do**:
  - List all devices with status, battery, model, connection type
  - Device groups and tags display
  - Device actions (screenshot, wake, launch app)
  - Device filtering and search
  - Real-time status indicator (connected/disconnected)
  - Link to device control page (/control/{serial})

  **Must NOT do**:
  - Don't expose other tenants' devices (use tenant API key)

  **References**:
  - /v1/devices API endpoint
  - static/index.html for existing device card design

  **QA Scenarios**:
  - Load devices page, verify list
  - Click device, verify details/actions
  - Filter devices, verify results

- [ ] 13. Dashboard: Usage & billing page

  **What to do**:
  - Current period usage summary (API calls, tasks)
  - Usage by endpoint breakdown
  - Cost calculator (calls × $0.001 + tasks × $0.01)
  - Invoice history list
  - Stripe customer portal link (if configured)
  - Simple chart (can use inline SVG or canvas)

  **Must NOT do**:
  - Don't expose raw Stripe data
  - Don't add heavy chart libraries

  **References**:
  - /v1/billing/* API endpoints

  **QA Scenarios**:
  - Load billing page, verify usage display
  - Verify cost calculation
  - Portal link present (if Stripe configured)

- [ ] 14. Dashboard: Settings & API keys page

  **What to do**:
  - Profile settings (tenant name, email)
  - API key management (create new, list, revoke)
  - Webhook configuration (URL, events)
  - Display API key prefix only (pf_xxx...)
  - Copy-to-clipboard for API keys

  **Must NOT do**:
  - Don't expose full API keys after creation

  **References**:
  - /v1/auth/keys API endpoints
  - /v1/webhook/config API endpoint

  **QA Scenarios**:
  - Create API key, verify displayed (prefix only)
  - Revoke key, verify removed
  - Configure webhook, verify saved

- [ ] 15. Dashboard: Real-time WebSocket integration

  **What to do**:
  - WebSocket connection for live updates
  - Device status changes (connected/disconnected)
  - Task completion notifications
  - Alert notifications (toast/popup)
  - Usage counter updates in header
  - Auto-reconnect on disconnect

  **Must NOT do**:
  - Don't send data to wrong tenant
  - Don't flood with updates (throttle)

  **References**:
  - Existing WebSocket at /ws/{serial} in farm_daemon.py
  - Need new /ws/notifications endpoint for dashboard events

  **QA Scenarios**:
  - Connect WebSocket, verify updates received
  - Device disconnect, verify notification
  - Auto-reconnect after disconnect

- [ ] 16. Update Dockerfile for SaaS

  **What to do**:
  - Multi-stage build for smaller image
  - Copy dashboard/ directory
  - Environment variable documentation in comments
  - Non-root user for security
  - Log rotation config

  **Must NOT do**:
  - Don't hardcode any secrets
  - Don't increase image size significantly

  **References**:
  - Current Dockerfile at /mnt/data/berkahkarya/skills/1ai-skills/automation/1ai-autodroid/phone-farm/Dockerfile (38 lines)

  **QA Scenarios**:
  - Docker build, verify image builds
  - Docker run, verify health endpoint
  - Dashboard accessible

- [ ] 17. Create .env.example with all config

  **What to do**:
  - Document ALL environment variables used across all modules
  - Required vs optional clearly marked
  - Default values shown
  - Categories: Auth, Database, Stripe, Server, Logging
  - Comments explaining each variable

  **Must NOT do**:
  - Don't include real secrets
  - Don't include .env in git

  **References**:
  - auth.py: PHONEFARM_JWT_SECRET, PHONEFARM_API_KEYS_PATH
  - billing.py: STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET
  - farm_daemon.py: port, mode
  - phonefarm_logging.py: log levels

  **QA Scenarios**:
  - Copy .env.example to .env, verify app starts
  - All variables documented

- [ ] 18. Update README with SaaS documentation

  **What to do**:
  - Multi-tenancy section
  - API versioning section
  - Billing configuration section
  - Dashboard screenshots/description
  - Self-hosting guide
  - Environment variables reference
  - Update existing sections to reflect SaaS changes

  **Must NOT do**:
  - Don't include internal implementation details
  - Don't remove existing documentation

  **References**:
  - Current README at /mnt/data/berkahkarya/skills/1ai-skills/automation/1ai-autodroid/phone-farm/README.md

  **QA Scenarios**:
  - Follow README, verify app runs
  - All new features documented

- [ ] 19. Integration testing (all endpoints)

  **What to do**:
  - Test full flow: create tenant → API key → add device → run task → check usage → check billing
  - Test multi-tenancy: 2 tenants, verify data isolation
  - Test rate limiting: exceed limits, verify 429
  - Test auth: no auth → 401, valid JWT → 200, valid API key → 200
  - Test backward compat: old /devices endpoint still works
  - Test dashboard: all pages load
  - Create test script `tests/integration_test.sh`

  **Must NOT do**:
  - Don't test with real Stripe keys
  - Don't modify production data

  **References**:
  - All API endpoints in farm_daemon.py

  **QA Scenarios**:
  - Run integration test script, all pass
  - Multi-tenancy verified
  - Rate limiting verified

- [ ] 20. Commit + push to GitHub

  **What to do**:
  - Git add all new/modified files
  - Commit with descriptive message per wave
  - Push to origin

  **Must NOT do**:
  - Don't include .env files
  - Don't include __pycache__

  **QA Scenarios**:
  - Git status clean after push
  - All new files committed

---

## Commit Strategy

- **Wave 1**: `feat(saas): add multi-tenancy + rate limiting foundation`
- **Wave 2**: `feat(billing): add Stripe metered billing + usage tracking`
- **Wave 3**: `feat(api): add tenant-aware endpoints + versioning`
- **Wave 4**: `feat(dashboard): add HTML+Alpine.js dashboard`
- **Wave 5**: `feat(deploy): update Docker + README + env config`

---

## Success Criteria

### Verification Commands
```bash
# Multi-tenancy
curl -H "X-API-Key: pf_tenant1_xxx" http://localhost:8889/v1/devices
curl -H "X-API-Key: pf_tenant2_xxx" http://localhost:8889/v1/devices

# Rate limiting
for i in {1..200}; do curl -s -o /dev/null -w "%{http_code}\n" -H "X-API-Key: pf_test" http://localhost:8889/v1/devices; done | grep 429

# Billing
curl -H "X-API-Key: pf_test" http://localhost:8889/v1/billing/usage

# Dashboard
curl http://localhost:8889/dashboard/
```

### Final Checklist
- [ ] All endpoints require tenant_id context
- [ ] Usage tracked per tenant
- [ ] Rate limiting enforced
- [ ] API versioning at /v1/
- [ ] Dashboard shows tenant-specific data
- [ ] Docker deployment works
- [ ] .env.example documented
- [ ] README updated
