# PhoneFarm Improvements Work Plan

## TL;DR

> Add production-ready features to phonefarm: JWT/API key auth, structured logging, device groups, Docker, health endpoints, and webhooks.

> **Deliverables**: auth.py, enhanced farm_daemon.py, Dockerfile, docker-compose.yml, updated README
> **Estimated Effort**: Short (3-5 hours)
> **Parallel Execution**: YES - 2 waves

---

## Context

### Original Request
Improve phonefarm (1ai-phonefarm) with minimum effort, maximum result.

### Current State
- Basic FastAPI server on port 8889
- No authentication
- Basic logging
- Single device config (devices.json)
- PM2 deployment only

### Improvement Goals
- Production-ready security
- Easier debugging
- Better organization (device groups)
- Docker deployment
- Ops visibility (health checks)
- Automation (webhooks)

---

## Work Objectives

### Core Objective
Make phonefarm production-ready with essential security and operational features.

### Concrete Deliverables
- `auth.py` - JWT + API key authentication module
- Enhanced `farm_daemon.py` - Auth-protected endpoints, structured logging
- `Dockerfile` - Container deployment
- `docker-compose.yml` - Local development
- Updated `README.md` - New features documentation
- Device groups support in `db.py`

### Definition of Done
- [ ] API endpoints require auth (JWT or API key)
- [ ] Structured JSON logging to file
- [ ] Device groups/tags functional via API
- [ ] Dockerfile builds and runs
- [ ] Health endpoint returns status
- [ ] Webhook endpoint for task events

### Must Have
- JWT authentication for API
- API key management (create/revoke/list)
- Structured JSON logging
- Device grouping (groups, tags)

### Must NOT Have
- No external auth services (keep simple)
- No Redis queue (overkill)
- No Kubernetes (use Docker only)
- No test suite (skip for now)

---

## Verification Strategy

**QA Policy**: Every task includes agent-executed QA scenarios.

- **API Testing**: Use curl to test authenticated endpoints
- **Docker**: Build image, run container, test endpoints
- **Logging**: Check JSON log output

---

## Execution Strategy

### Wave 1 (Foundation - can parallelize)
- Task 1: Create auth.py module (JWT + API keys)
- Task 2: Add structured JSON logging
- Task 3: Update db.py for device groups/tags

### Wave 2 (Integration + Deployment)
- Task 4: Update farm_daemon.py with auth + logging
- Task 5: Add health endpoints + webhooks
- Task 6: Create Dockerfile + docker-compose.yml
- Task 7: Update README with new features
- Task 8: Commit + push to GitHub

---

## TODOs

- [ ] 1. Create auth.py — JWT + API Key authentication module

  **What to do**:
  - Create `auth.py` with JWT class (encode/decode, no external deps)
  - Create APIKeyManager class (create/validate/revoke/list keys)
  - Implement `require_auth(role)` decorator for FastAPI
  - Support both `Authorization: Bearer <token>` and `X-API-Key` headers
  - JWT secret from env var `PHONEFARM_JWT_SECRET`

  **Must NOT do**:
  - No external JWT libraries (keep zero-dep)
  - No OAuth integration

  **References**:
  - Based on current `farm_daemon.py` API structure

  **QA Scenarios**:
  - Create JWT token and validate it
  - Create API key, validate, then revoke
  - Test decorated endpoint without auth → 401

- [ ] 2. Add structured JSON logging

  **What to do**:
  - Replace basic logging with JSONFormatter
  - Log format: `{"timestamp": "...", "level": "INFO", "logger": "...", "message": "...", "context": {...}}`
  - Keep console output human-readable
  - Log file: `logs/phone-farm/app.log` (JSON lines)

  **Must NOT do**:
  - Don't break existing log output

  **References**:
  - Python `logging` module

  **QA Scenarios**:
  - Check log file contains JSON lines
  - Verify console still readable

- [ ] 3. Update db.py for device groups/tags

  **What to do**:
  - Add `groups` table (id, name, description)
  - Add `device_groups` table (device_serial, group_id)
  - Add `tags` table (id, name, color)
  - Add `device_tags` table (device_serial, tag_id)
  - Add migration/creation in `init_db()`
  - Add CRUD methods: create_group, add_device_to_group, get_devices_by_group, etc.

  **Must NOT do**:
  - Don't break existing device queries

  **References**:
  - Current `db.py` schema

  **QA Scenarios**:
  - Create group, add device, list devices in group
  - Add tag to device, filter by tag

- [ ] 4. Update farm_daemon.py with auth + logging

  **What to do**:
  - Import and use auth.py for protected endpoints
  - Add `/auth/token` endpoint (create JWT)
  - Add `/auth/keys` endpoints (CRUD API keys)
  - Add auth decorator to all API endpoints except `/health` and `/docs`
  - Replace logging with structured JSON logger
  - Add `/api/groups` endpoints (CRUD)
  - Add `/api/tags` endpoints (CRUD)

  **Must NOT do**:
  - Don't break WebSocket endpoints
  - Keep backward compatibility

  **References**:
  - Current `farm_daemon.py` endpoints at lines 361-452

  **QA Scenarios**:
  - Test `/health` without auth → 200
  - Test `/devices` without auth → 401
  - Test `/devices` with valid JWT → 200

- [ ] 5. Add health endpoints + webhooks

  **What to do**:
  - Add `/health/ready` - detailed health (DB, ADB, devices)
  - Add `/health/live` - simple liveness check
  - Add `/webhook` POST endpoint for external events
  - Add webhook notification on: task_complete, device_connected, device_disconnected, alert
  - Webhook config in `config/webhooks.json`

  **Must NOT do**:
  - Don't make webhooks blocking (use async)

  **References**:
  - Current `/health` endpoint at line 376

  **QA Scenarios**:
  - `/health/ready` returns detailed status
  - POST to `/webhook` triggers callback

- [ ] 6. Create Dockerfile + docker-compose.yml

  **What to do**:
  - Create `Dockerfile`:
    - Python 3.11 slim base
    - Install ADB (android-tools)
    - Copy app files
    - Expose port 8889
    - Non-root user
  - Create `docker-compose.yml`:
    - phonefarm service
    - Volume for ADB devices
    - Environment variables
    - Restart policy

  **Must NOT do**:
  - Don't include device hardware access in Docker

  **References**:
  - PM2 ecosystem.config.js for runtime settings

  **QA Scenarios**:
  - `docker build .` succeeds
  - `docker run -p 8889:8889` starts
  - `curl localhost:8889/health` returns 200

- [ ] 7. Update README.md

  **What to do**:
  - Add Authentication section (JWT, API keys)
  - Add Device Groups section
  - Add Webhooks section
  - Add Docker deployment section
  - Add Environment variables section

  **References**:
  - Current README.md

  **QA Scenarios**:
  - README contains all new sections

- [ ] 8. Commit + push to GitHub

  **What to do**:
  - Git add all new/modified files
  - Commit with descriptive message
  - Push to origin master

  **QA Scenarios**:
  - GitHub repo shows new commits

---

## Commit Strategy

- **1**: `feat(auth): add JWT and API key authentication` — auth.py
- **2**: `feat(logging): add structured JSON logging` — farm_daemon.py
- **3**: `feat(db): add device groups and tags` — db.py
- **4**: `feat(api): add auth-protected endpoints, health, webhooks` — farm_daemon.py
- **5**: `feat(deploy): add Dockerfile and docker-compose` — Dockerfile, docker-compose.yml
- **6**: `docs: update README with new features` — README.md
- **7**: `chore: commit all changes` — all files

---

## Success Criteria

### Verification Commands
```bash
# Test without auth
curl http://localhost:8889/health  # Should return 200
curl http://localhost:8889/devices  # Should return 401

# Test with JWT
TOKEN=$(curl -s -X POST http://localhost:8889/auth/token \
  -H "Content-Type: application/json" \
  -d '{"user_id": "admin", "role": "admin"}' | jq -r .token)
curl -H "Authorization: Bearer $TOKEN" http://localhost:8889/devices

# Test API key
curl -H "X-API-Key: pk_xxx" http://localhost:8889/devices

# Docker
docker build -t phonefarm .
docker run -p 8889:8889 phonefarm
```

### Final Checklist
- [ ] All endpoints (except health/docs) require auth
- [ ] JWT token creation and validation works
- [ ] API key CRUD works
- [ ] JSON logs in logs/phone-farm/app.log
- [ ] Device groups can be created and devices added
- [ ] Dockerfile builds successfully
- [ ] Health endpoints return proper status
- [ ] Webhook endpoint exists and can be configured
