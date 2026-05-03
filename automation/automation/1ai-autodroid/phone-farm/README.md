# Phone Farm — Android Device Farm Automation

Production-grade Android device farm orchestrator with multi-tenant SaaS support, usage-based billing, and real-time dashboard.

## Architecture

```
phonefarm CLI → device_manager.py (ADB abstraction layer)
                     ↑
farm_daemon.py ──────┘ (autonomous orchestrator + FastAPI)
      │
      ├── Multi-tenant API (tenant isolation, rate limiting)
      ├── Usage tracking (per-tenant metering)
      ├── Stripe billing (usage-based, optional)
      ├── Alpine.js dashboard (real-time WebSocket)
      └── API versioning (/v1/ prefix)
```

## Components

| File | Purpose |
|------|---------|
| `device_manager.py` | ADB abstraction: connect, screenshot, tap, swipe, type, UI dump, health monitor, auto-reconnect |
| `task_runner.py` | 10 built-in tasks: health_check, screenshot, app_check, tiktok_inbox, shopee_orders, whatsapp_unread, instagram_dms, etc. |
| `farm_daemon.py` | FastAPI server: auth, tenant-aware endpoints, billing, rate limiting, WebSocket, dashboard |
| `farm_cli.py` | Unified CLI interface (`phonefarm` command) |
| `auth.py` | JWT + API key authentication with multi-tenant support |
| `db.py` | SQLite state store with tenant isolation |
| `tenant.py` | Multi-tenant management (CRUD, API key generation) |
| `rate_limiter.py` | Token bucket rate limiting (per-tenant, in-memory) |
| `usage_tracker.py` | Usage metering (per-tenant, periodic SQLite flush) |
| `billing.py` | Stripe integration (usage-based billing, graceful degradation) |
| `dashboard/` | Alpine.js + Tailwind CSS dashboard (login, devices, billing, settings, WebSocket) |

## Quick Start

```bash
# Symlink for easy access
ln -sf /path/to/farm_cli.py ~/.local/bin/phonefarm

# Check status
phonefarm status

# Start daemon (monitor mode — health + screenshots only)
phonefarm daemon start --mode monitor

# Start daemon (active mode — full app automation)
phonefarm daemon start --mode active

# Run specific tasks
phonefarm health
phonefarm screenshot
phonefarm task shopee_orders
phonefarm task tiktok_inbox --device SERIAL

# Add new device
phonefarm add SERIAL my-phone-name

# View logs
phonefarm logs --lines 100
```

## Daemon Modes

| Mode | What it does | Safe? |
|------|-------------|-------|
| `monitor` | Health checks + screenshots + reconnect only | ✅ Very safe |
| `active` | All of monitor + opens apps + checks inboxes | ⚠️ Interacts with apps |
| `dashboard` | HTTP API only (port 8889), no autonomous tasks | ✅ Safe |

## Authentication

### JWT Tokens
```bash
# Get access token
curl -X POST http://localhost:8889/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'

# Use token in requests
curl -H "Authorization: Bearer <token>" http://localhost:8889/api/devices
```

### API Keys
```bash
# Create API key
curl -X POST /auth/keys -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-api-key", "expires_in_days": 30}'

# Use API key
curl -H "X-API-Key: <key>" http://localhost:8889/api/devices
```

### Environment Variables
- `PHONEFARM_JWT_SECRET` - Secret key for JWT token signing

## Device Groups

### CRUD Endpoints
```bash
# Create group
curl -X POST /api/groups \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "production", "description": "Production devices"}'

# List groups
curl /api/groups -H "Authorization: Bearer <token>"

# Add device to group
curl -X POST /api/groups/<group_id>/devices \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"device_serial": "SERIAL123"}'

# List devices in group
curl /api/groups/<group_id>/devices -H "Authorization: Bearer <token>"
```

## Tags

```bash
# Create tag
curl -X POST /api/tags \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "offline", "color": "#ff0000"}'

# Add tag to device
curl -X POST /api/devices/<serial>/tags \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"tag_id": "tag_uuid"}'

# List all tags
curl /api/tags -H "Authorization: Bearer <token>"
```

## Health Endpoints

| Endpoint | Description | Auth Required |
|----------|-------------|---------------|
| `/health` | Basic health check (public) | ❌ No |
| `/health/ready` | Detailed readiness (DB, ADB, etc.) | ❌ No |
| `/health/live` | Liveness probe for k8s | ❌ No |

```bash
curl http://localhost:8889/health
curl http://localhost:8889/health/ready
curl http://localhost:8889/health/live
```

## Webhooks

### Configuration
```bash
# Create webhook
curl -X POST /webhook/config \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://your-server.com/webhook", "events": ["task_complete", "device_connected"]}'

# List webhooks
curl /webhook/config -H "Authorization: Bearer <token>"

# Delete webhook
curl -X DELETE /webhook/config/<webhook_id> -H "Authorization: Bearer <token>"
```

### Event Types
- `task_complete` - Task finished execution
- `device_connected` - Device connected to farm
- `device_disconnected` - Device disconnected
- `alert` - System alert (low battery, error, etc.)

## Multi-Tenancy

Phone Farm supports multiple tenants with data isolation. Each tenant gets:
- Separate API key for authentication
- Isolated device, task, and alert data
- Independent rate limits and usage tracking
- Separate billing (if Stripe configured)

```bash
# All endpoints automatically filter by tenant when using tenant API key
curl -H "X-API-Key: pf_tenant_xxx" http://localhost:8889/v1/devices
```

## API Versioning

All API endpoints are available at both root and `/v1/` prefix:

```bash
# Both work (backward compatible)
curl http://localhost:8889/devices
curl http://localhost:8889/v1/devices

# Version discovery
curl http://localhost:8889/api/versions
```

## Usage & Billing

Usage is tracked per-tenant for every API call. When Stripe is configured, usage is reported for metered billing.

```bash
# Check current usage
curl -H "X-API-Key: pf_xxx" http://localhost:8889/v1/billing/usage

# Check subscription/billing info
curl -H "X-API-Key: pf_xxx" http://localhost:8889/v1/billing/subscription

# View invoices
curl -H "X-API-Key: pf_xxx" http://localhost:8889/v1/billing/invoices
```

Pricing: $0.001 per API call, $0.01 per task (configurable in `billing.py`).

Stripe is optional — the app works fully without it.

## Rate Limiting

Token bucket rate limiting is enforced per API key. Default: 100 requests/minute with burst of 20.

```bash
# Rate limit headers are included in every response
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1234567890

# Returns 429 Too Many Requests when exceeded
```

## Dashboard

Access the dashboard at `http://localhost:8889/dashboard/`. Features:
- API key login (no passwords stored in dashboard)
- Device list with status, battery, model
- Task history and alert feed
- Usage and billing overview
- API key management and webhook configuration
- Real-time WebSocket notifications

## Environment Variables

See `.env.example` for all configuration options.

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PHONEFARM_JWT_SECRET` | Yes | — | JWT token signing secret |
| `PHONEFARM_MODE` | No | `dashboard` | Daemon mode (monitor/active/dashboard) |
| `PHONEFARM_PORT` | No | `8889` | HTTP server port |
| `STRIPE_SECRET_KEY` | No | — | Stripe secret key for billing |
| `STRIPE_WEBHOOK_SECRET` | No | — | Stripe webhook signature secret |
| `PYTHONUNBUFFERED` | No | `1` | Python output buffering |

## Docker Deployment

```bash
# Copy env config
cp .env.example .env
# Edit .env with your values

# Build and run
docker compose up -d

# Or build manually
docker build -t phonefarm .
docker run -d -p 8889:8889 --env-file .env -v /dev/bus/usb:/dev/bus/usb phonefarm
```

## Systemd Service

```bash
# Enable auto-start on boot
systemctl --user enable phone-farm.service
systemctl --user start phone-farm.service

# Check status
systemctl --user status phone-farm.service
```

## Device Config

Edit `config/devices.json` to register devices and assign skills:

```json
{
  "devices": {
    "SERIAL_NUMBER": {
      "name": "farm-hp1",
      "assigned_skills": ["tiktok", "shopee", "whatsapp"],
      "installed_apps": {
        "shopee": "com.shopee.id",
        "whatsapp": "com.whatsapp"
      },
      "enabled": true
    }
  }
}
```

## Auto-Recovery

- **Disconnect**: Auto-reconnect attempts every 60s
- **Battery critical** (<10%): Alert sent
- **Crash**: Systemd auto-restarts within 30s
- **ADB server death**: Kills and restarts ADB server

## Support

If this saves you time, consider tipping: 👉 https://www.tip.md/oyi77
