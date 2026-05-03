# Learnings - PhoneFarm SaaS Consolidated

## Codebase Conventions
- Pure Python, zero external deps for core modules (auth.py uses no PyJWT)
- FastAPI + uvicorn for HTTP server
- SQLite with WAL mode, thread-local connections via `db.py`
- JSON config files for device state
- `phonefarm_logging.py` provides structured JSON logging
- All API keys use `pf_` prefix
- Auth: `require_auth(role)` decorator, roles: viewer < operator < admin
- Groups/tags already in db.py but farm_daemon.py uses in-memory dicts (not db.py functions)

## Gotchas
- farm_daemon.py has duplicate `/health` endpoint definition (line 569 and line 710)
- Groups/tags API in farm_daemon.py uses in-memory dicts `_device_groups` and `_device_tags` instead of db.py functions
- No tenant_id concept exists anywhere yet
- No rate limiting, no usage tracking, no billing
- Static dashboard is vanilla HTML/CSS/JS (no framework)
- WebSocket streaming works for device control
