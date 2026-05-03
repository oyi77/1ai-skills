# PhoneFarm SaaS Improvement Plan

## TL;DR

> Transform phonefarm from a self-managed device farm into a usage-based SaaS platform.
> Users pay per API call/task executed. Self-hosted for zero cloud costs.

> **Deliverables**: Multi-tenant backend, HTML+Alpine.js dashboard, Stripe billing, rate limiting, API documentation
> **Estimated Effort**: XL (10-15 days)
> **Parallel Execution**: YES - 5 waves
> **Critical Path**: Auth → Multi-tenancy → Billing → Dashboard → Launch

---

## Context

### Current State
- Single FastAPI server on port 8889
- SQLite database with no tenant isolation
- In-memory groups/tags (no persistence)
- Basic JWT auth (single-tenant only)
- Static HTML dashboard
- No billing, no rate limiting, no usage tracking
- No API documentation

### Target State
- Multi-tenant SaaS with per-user data isolation
- Usage-based pricing via Stripe metered billing
- Modern HTML+Alpine.js dashboard with real-time updates
- API rate limiting and usage tracking
- Comprehensive API documentation
- Self-hosted deployment (zero cloud costs)

### Business Model
- **Pricing**: Usage-based (per API call / task executed)
- **Free tier**: 100 API calls/month
- **Pay-as-you-go**: $0.001 per API call, $0.01 per task
- **Stripe**: Metered billing for automated invoicing
- **Self-hosted**: User runs on their own server with Docker

---

## Work Objectives

### Core Objective
Make phonefarm a production-ready SaaS platform with multi-tenancy, usage-based billing, and a modern dashboard.

### Concrete Deliverables
- `tenant.py` — Multi-tenant isolation (tenant_id on all tables)
- `billing.py` — Stripe integration for metered billing
- `rate_limiter.py` — API rate limiting (token bucket)
- `usage_tracker.py` — Usage tracking and metering
- `api_docs.py` — OpenAPI documentation
- `dashboard/` — HTML+Alpine.js dashboard (replace static/)
- Updated `farm_daemon.py` — Tenant-aware endpoints
- Updated `db.py` — Tenant_id columns
- Updated `auth.py` — Multi-tenant JWT
- `docker-compose.yml` — SaaS-ready configuration

### Definition of Done
- [ ] All endpoints require tenant_id context
- [ ] Usage tracked per tenant per endpoint
- [ ] Stripe metered billing working
- [ ] Dashboard shows tenant-specific data
- [ ] API rate limiting enforced
- [ ] OpenAPI docs at /docs

---

## Verification Strategy

**QA Policy**: Every task includes agent-executed QA scenarios.

- **Multi-tenancy**: Create 2 tenants, verify data isolation
- **Billing**: Test Stripe webhook, verify metered billing
- **Rate limiting**: Test rate limit exceeded, verify 429 response
- **Dashboard**: Playwright tests for dashboard UI
- **API**: curl tests for all endpoints

---

## Execution Strategy

### Wave 1: Foundation (Multi-tenancy + Rate Limiting)
- Task 1: Add tenant_id to all DB tables
- Task 2: Create tenant.py for tenant management
- Task 3: Create rate_limiter.py (token bucket)
- Task 4: Update auth.py for multi-tenant JWT

### Wave 2: Billing + Usage Tracking
- Task 5: Create usage_tracker.py for metering
- Task 6: Create billing.py for Stripe integration
- Task 7: Add /billing endpoints (subscription, invoices)

### Wave 3: API + Documentation
- Task 8: Update farm_daemon.py with tenant-aware endpoints
- Task 9: Add API documentation (OpenAPI)
- Task 10: Add API versioning (/v1/, /v2/)

### Wave 4: Dashboard
- Task 11: Create dashboard/ with HTML+Alpine.js
- Task 12: Dashboard: Device management page
- Task 13: Dashboard: Usage & billing page
- Task 14: Dashboard: Settings & API keys page
- Task 15: Dashboard: Real-time WebSocket integration

### Wave 5: Deployment + Launch
- Task 16: Update Dockerfile for SaaS
- Task 17: Create .env.example with all config
- Task 18: Update README with SaaS documentation
- Task 19: Integration testing
- Task 20: GitHub commit + push

---

## TODOs

---

- [ ] 1. Add tenant_id to all DB tables

  **What to do**:
  - Add `tenants` table (id TEXT PRIMARY KEY, name, email, stripe_customer_id, api_key, created_at)
  - Add `tenant_id` column to devices, tasks, alerts, groups, tags
  - Add foreign key constraint: tenant_id REFERENCES tenants(id)
  - Update init_db() to create new tables
  - Add migration function for existing data

  **Must NOT do**:
  - Don't break existing single-tenant usage
  - Don't remove existing tables

  **QA Scenarios**:
  - Create tenant, verify devices table accepts tenant_id
  - Query devices by tenant_id, verify isolation

- [ ] 2. Create tenant.py for tenant management

  **What to do**:
  - Create TenantManager class
  - CRUD: create_tenant, get_tenant, update_tenant, delete_tenant
  - API key generation (pk_xxx format)
  - Tenant lookup by API key
  - Tenant stats (devices, tasks, usage)

  **Must NOT do**:
  - Don't use external auth services

  **QA Scenarios**:
  - Create tenant, verify API key works
  - Query tenant stats, verify counts

- [ ] 3. Create rate_limiter.py (token bucket)

  **What to do**:
  - Token bucket algorithm (in-memory, no Redis)
  - Per-tenant rate limits
  - Configurable: requests_per_second, burst_size
  - Returns 429 Too Many Requests when exceeded
  - Headers: X-RateLimit-Remaining, X-RateLimit-Reset

  **Must NOT do**:
  - Don't use Redis (keep cheap)

  **QA Scenarios**:
  - Send 100 requests rapidly, verify rate limit kicks in
  - Check rate limit headers in response

- [ ] 4. Update auth.py for multi-tenant JWT

  **What to do**:
  - JWT includes tenant_id in payload
  - API key lookup returns tenant_id
  - require_auth decorator extracts tenant_id from token
  - All authenticated endpoints get tenant_id automatically

  **Must NOT do**:
  - Don't break existing API key format

  **QA Scenarios**:
  - Create JWT with tenant_id, verify payload
  - Use API key, verify tenant_id extracted

- [ ] 5. Create usage_tracker.py for metering

  **What to do**:
  - Track API calls per tenant (in-memory counters)
  - Track tasks executed per tenant
  - Periodic flush to SQLite (every 60 seconds)
  - Query: get_usage(tenant_id, period)
  - Export: usage_report(tenant_id, start_date, end_date)

  **Must NOT do**:
  - Don't use external analytics services

  **QA Scenarios**:
  - Make 10 API calls, verify usage tracked
  - Query usage report, verify data

- [ ] 6. Create billing.py for Stripe integration

  **What to do**:
  - Stripe metered billing for usage-based pricing
  - Create Stripe customer on tenant creation
  - Report usage to Stripe (daily)
  - Webhook handler for invoice.payment_succeeded
  - Price configuration: $0.001/API call, $0.01/task

  **Must NOT do**:
  - Don't hardcode Stripe keys (use env vars)
  - Don't break if Stripe is unavailable

  **QA Scenarios**:
  - Create tenant, verify Stripe customer created
  - Simulate webhook, verify payment recorded

- [ ] 7. Add /billing endpoints

  **What to do**:
  - GET /billing/subscription — current plan and usage
  - GET /billing/invoices — list past invoices
  - POST /billing/portal — Stripe customer portal link
  - GET /billing/usage — current period usage

  **Must NOT do**:
  - Don't expose Stripe internal IDs

  **QA Scenarios**:
  - GET /billing/subscription, verify plan data
  - GET /billing/usage, verify usage counts

- [ ] 8. Update farm_daemon.py with tenant-aware endpoints

  **What to do**:
  - All device endpoints filter by tenant_id
  - All task endpoints filter by tenant_id
  - All alert endpoints filter by tenant_id
  - Add tenant_id to all DB queries
  - Rate limit decorator on all endpoints
  - Usage tracking on all endpoints

  **Must NOT do**:
  - Don't break WebSocket endpoints
  - Don't expose other tenants' data

  **QA Scenarios**:
  - Create 2 tenants, verify data isolation
  - Make API call, verify usage tracked

- [ ] 9. Add API documentation (OpenAPI)

  **What to do**:
  - Auto-generate OpenAPI spec from FastAPI
  - Add /docs endpoint with Swagger UI
  - Add /redoc endpoint with ReDoc
  - Document all endpoints with examples
  - Add authentication section

  **Must NOT do**:
  - Don't expose internal implementation details

  **QA Scenarios**:
  - GET /docs, verify Swagger UI loads
  - GET /redoc, verify ReDoc loads

- [ ] 10. Add API versioning (/v1/, /v2/)

  **What to do**:
  - Move current endpoints to /v1/ prefix
  - Add version header support
  - Deprecation warnings for old versions
  - Version discovery endpoint

  **Must NOT do**:
  - Don't break existing /v1/ endpoints

  **QA Scenarios**:
  - GET /v1/devices, verify works
  - GET /api/versions, verify list

- [ ] 11. Create dashboard/ with HTML+Alpine.js

  **What to do**:
  - Replace static/ with dashboard/
  - Login page (API key or email/password)
  - Layout with sidebar navigation
  - Alpine.js for reactivity (no build step)
  - Tailwind CSS via CDN for styling
  - WebSocket for real-time updates

  **Must NOT do**:
  - Don't use build tools (no npm, no webpack)

  **QA Scenarios**:
  - Playwright: load dashboard, verify login page
  - Playwright: enter API key, verify redirect to dashboard

- [ ] 12. Dashboard: Device management page

  **What to do**:
  - List all devices with status, battery, model
  - Device groups and tags
  - Device actions (screenshot, wake, launch app)
  - Real-time status updates via WebSocket
  - Device filtering and search

  **Must NOT do**:
  - Don't expose other tenants' devices

  **QA Scenarios**:
  - Playwright: load devices page, verify list
  - Playwright: click device, verify details panel

- [ ] 13. Dashboard: Usage & billing page

  **What to do**:
  - Current period usage chart
  - Usage by endpoint breakdown
  - Cost calculator
  - Invoice history
  - Stripe customer portal link

  **Must NOT do**:
  - Don't expose raw Stripe data

  **QA Scenarios**:
  - Playwright: load billing page, verify chart
  - Playwright: click portal link, verify redirect

- [ ] 14. Dashboard: Settings & API keys page

  **What to do**:
  - Profile settings (name, email)
  - API key management (create, revoke, list)
  - Webhook configuration
  - Notification preferences
  - Plan selection

  **Must NOT do**:
  - Don't expose full API keys (show prefix only)

  **QA Scenarios**:
  - Playwright: create API key, verify displayed
  - Playwright: revoke key, verify removed

- [ ] 15. Dashboard: Real-time WebSocket integration

  **What to do**:
  - WebSocket connection for live updates
  - Device status changes in real-time
  - Task completion notifications
  - Alert notifications
  - Usage counter updates

  **Must NOT do**:
  - Don't send data to wrong tenant

  **QA Scenarios**:
  - Playwright: connect WebSocket, verify updates
  - Playwright: device disconnect, verify notification

- [ ] 16. Update Dockerfile for SaaS

  **What to do**:
  - Multi-stage build for smaller image
  - Health check endpoint
  - Environment variable configuration
  - Non-root user for security
  - Log rotation

  **Must NOT do**:
  - Don't hardcode any secrets

  **QA Scenarios**:
  - Docker build, verify image size < 500MB
  - Docker run, verify health endpoint

- [ ] 17. Create .env.example with all config

  **What to do**:
  - Document all environment variables
  - Required vs optional variables
  - Default values
  - Stripe configuration
  - Database configuration

  **Must NOT do**:
  - Don't include real secrets

  **QA Scenarios**:
  - Copy .env.example to .env, verify app starts

- [ ] 18. Update README with SaaS documentation

  **What to do**:
  - Quick start guide
  - API documentation
  - Billing configuration
  - Dashboard setup
  - Docker deployment
  - Self-hosting guide

  **Must NOT do**:
  - Don't include internal implementation details

  **QA Scenarios**:
  - Follow README, verify app runs

- [ ] 19. Integration testing

  **What to do**:
  - Test full flow: signup → API key → device → task → billing
  - Test multi-tenancy: 2 tenants, verify isolation
  - Test rate limiting: exceed limits, verify 429
  - Test billing: webhook, verify payment
  - Test dashboard: all pages load, all actions work

  **Must NOT do**:
  - Don't test with real Stripe keys

  **QA Scenarios**:
  - Full integration test via curl + Playwright

- [ ] 20. GitHub commit + push

  **What to do**:
  - Git add all new/modified files
  - Commit with descriptive message
  - Push to both repos (1ai-skills + 1ai-phonefarm)

  **Must NOT do**:
  - Don't include .env files

  **QA Scenarios**:
  - GitHub repo shows new commits

---

## Final Verification Wave

- [ ] F1. **Multi-tenancy Audit** — Verify all endpoints filter by tenant_id
- [ ] F2. **Billing Audit** — Verify Stripe integration works
- [ ] F3. **Rate Limiting Audit** — Verify rate limits enforced
- [ ] F4. **Dashboard Audit** — Verify all pages work with Playwright

---

## Commit Strategy

- **Wave 1**: `feat(tenant): add multi-tenancy + rate limiting`
- **Wave 2**: `feat(billing): add Stripe metered billing`
- **Wave 3**: `feat(api): add versioning + documentation`
- **Wave 4**: `feat(dashboard): add HTML+Alpine.js dashboard`
- **Wave 5**: `feat(deploy): update Docker + README`

---

## Success Criteria

### Verification Commands
```bash
# Multi-tenancy
curl -H "X-API-Key: pk_tenant1" http://localhost:8889/v1/devices
curl -H "X-API-Key: pk_tenant2" http://localhost:8889/v1/devices  # Should show different data

# Rate limiting
for i in {1..200}; do curl -s -o /dev/null -w "%{http_code}\n" -H "X-API-Key: pk_test" http://localhost:8889/v1/devices; done | grep 429

# Billing
curl -H "X-API-Key: pk_test" http://localhost:8889/billing/usage

# Dashboard
curl http://localhost:8889/dashboard/
```

### Final Checklist
- [ ] All endpoints require tenant_id context
- [ ] Usage tracked per tenant
- [ ] Stripe metered billing working
- [ ] Dashboard shows tenant-specific data
- [ ] Rate limiting enforced
- [ ] API documentation at /docs
- [ ] Docker deployment works
- [ ] README updated

---

## Cost Analysis (Cheapest SaaS)

| Component | Cost | Notes |
|-----------|------|-------|
| Server | $0 | Self-hosted on existing hardware |
| Database | $0 | SQLite (no separate DB server) |
| Auth | $0 | Built-in JWT + API keys |
| Billing | $0 | Stripe takes % per transaction (no monthly fee) |
| Frontend | $0 | HTML+Alpine.js via CDN (no build tools) |
| DNS | $0 | Cloudflare free tier |
| SSL | $0 | Let's Encrypt |
| **Total** | **$0/month** | Pay only on successful transactions |

**Stripe fees**: 2.9% + $0.30 per successful charge. No monthly fees.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    PhoneFarm SaaS                        │
├─────────────────────────────────────────────────────────┤
│  Dashboard (HTML+Alpine.js)                              │
│  ├── Login / API Key                                     │
│  ├── Devices (list, groups, tags)                        │
│  ├── Tasks (history, execute)                            │
│  ├── Usage & Billing (charts, invoices)                  │
│  └── Settings (API keys, webhooks)                       │
├─────────────────────────────────────────────────────────┤
│  API (FastAPI)                                           │
│  ├── /v1/devices/* (tenant-aware)                        │
│  ├── /v1/tasks/* (tenant-aware)                          │
│  ├── /auth/* (JWT + API keys)                            │
│  ├── /billing/* (Stripe integration)                     │
│  └── /health/* (health checks)                           │
├─────────────────────────────────────────────────────────┤
│  Middleware                                              │
│  ├── Tenant Isolation (filter by tenant_id)              │
│  ├── Rate Limiting (token bucket per tenant)             │
│  ├── Usage Tracking (meter per endpoint)                 │
│  └── Auth (JWT validation + API key lookup)              │
├─────────────────────────────────────────────────────────┤
│  Services                                                │
│  ├── DeviceManager (ADB operations)                      │
│  ├── TaskRunner (priority queue)                         │
│  ├── BillingService (Stripe metered)                     │
│  └── UsageTracker (in-memory + SQLite flush)             │
├─────────────────────────────────────────────────────────┤
│  Storage                                                 │
│  ├── SQLite (devices, tasks, alerts, tenants, usage)     │
│  ├── JSON (webhook config, device config)                │
│  └── Files (screenshots, logs)                           │
├─────────────────────────────────────────────────────────┤
│  External                                                │
│  ├── ADB (device communication)                          │
│  ├── Stripe (billing)                                    │
│  └── Webhooks (notifications)                            │
└─────────────────────────────────────────────────────────┘
```
