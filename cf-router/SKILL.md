---
name: cf-router
description: Manage Cloudflare Tunnel routing, nginx reverse proxy, DNS records, and service ports via CF-Router. Use when adding/removing subdomains, checking routing status, listing mappings, deploying DNS to Cloudflare, registering portless services, managing nginx configs, health checks, backups, or scanning local ports. Domain routing is wildcard-based — all subdomains point to local nginx which routes by hostname.
---

# CF-Router Skill

CF-Router simplifies wildcard Cloudflare Tunnel management. One config file → auto-generate nginx + tunnel + DNS records.

**Source:** https://github.com/oyi77/cloudflare-router  
**Local install:** `~/.cloudflare-router/`  
**CLI binary:** `cloudflare-router` at `/home/openclaw/.local/bin/cloudflare-router`  
**Dashboard:** `http://localhost:7070` (also exposed via CF Tunnel)  
**PM2 process name:** `cloudflare-router`

> ⚠️ **Credentials are NOT stored in this skill.** Read them from `~/.cloudflare-router/config.yml` at runtime.

---

## Architecture

```
*.domain.com
     ↓
Cloudflare CDN
     ↓
Cloudflare Tunnel  ←── cloudflared daemon
     ↓
Nginx :6969  (per-subdomain server blocks in ~/.cloudflare-router/nginx/sites/)
     ↓
localhost:PORT
```

**Config files:**
| File | Purpose |
|------|---------|
| `~/.cloudflare-router/config.yml` | Accounts, zones, nginx settings, auth |
| `~/.cloudflare-router/mappings.yml` | Subdomain → port mappings (legacy format) |
| `~/.cloudflare-router/apps.yaml` | Apps with full hostname (preferred format) |
| `~/.cloudflare-router/portless.yml` | Portless service registry (auto port allocation 4000-4999) |

---

## CLI — Quick Reference

All commands use the global binary `cloudflare-router` (or alias `cfr`).

### Status & Listing
```bash
cloudflare-router status          # overview: accounts, zones, mappings count, nginx state
cloudflare-router list            # all subdomain → port mappings with labels
cloudflare-router account:list    # all configured Cloudflare accounts
cloudflare-router port:list       # portless service registry
```

### Add / Remove Mappings
```bash
# Add subdomain mapping (explicitly specify port)
cloudflare-router add \
  --subdomain myapp \
  --port 5000 \
  -d "My App Description"

# Add with specific account/zone (needed if multi-account)
cloudflare-router add \
  --account <account-id-from-config> \
  --zone <zone-id-from-config> \
  --subdomain myapp \
  --port 5000 \
  -d "My App"

# Remove mapping
cloudflare-router remove --subdomain myapp
```

### Generate & Deploy
```bash
# ALWAYS run these after any add/remove
cloudflare-router generate    # regenerate nginx server blocks
cloudflare-router deploy      # push DNS records to Cloudflare API
```

### Portless Mode (auto port allocation, range 4000-4999)
```bash
# Register service (allocates next free port automatically)
cloudflare-router port:register \
  --service my-backend \
  --subdomain my-backend \
  -d "My Backend Service"

# Get allocated port for a service
cloudflare-router port:get my-backend

# Export all ports as shell vars
eval $(cloudflare-router port:env)
# e.g. MY_BACKEND_PORT=4003

# One-shot: register → nginx → DNS
cloudflare-router port:sync

# Release port when service decommissioned
cloudflare-router port:release my-backend
```

### Accounts & Zones
```bash
cloudflare-router account:add                   # interactive: add new CF account
cloudflare-router account:remove --account <id>
cloudflare-router zone:discover --account <id>  # discover zones from CF API
cloudflare-router zone:add --account <id> --zone <zone-id> --domain <domain>
cloudflare-router zone:remove --account <id> --zone <zone-id>
```

---

## API — Full Reference

**Base URL:** `http://localhost:7070`  
**Auth:** `Authorization: Bearer <password>` — password stored in `~/.cloudflare-router/config.yml`  
  (if no password configured, omit auth header)

Read the password at runtime:
```bash
CF_PASS=$(python3 -c "import yaml; c=yaml.safe_load(open(\"$HOME/.cloudflare-router/config.yml\")); print(c.get('server',{}).get('password',''))")
```

### Auth
```bash
# Login (returns token = password)
curl -s -X POST http://localhost:7070/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"password\":\"$CF_PASS\"}"

# Check auth status
curl -s http://localhost:7070/api/auth/check
```

### System Status
```bash
curl -s http://localhost:7070/api/status -H "Authorization: Bearer $CF_PASS"
# Returns: { nginx: {running, processes}, accounts, zones, mappings, enabled }
```

### Mappings (CRUD)
```bash
# List (supports ?page=1&limit=50&filter=sub&sort=subdomain:asc)
curl -s "http://localhost:7070/api/mappings" \
  -H "Authorization: Bearer $CF_PASS"

# Create
curl -s -X POST http://localhost:7070/api/mappings \
  -H "Authorization: Bearer $CF_PASS" \
  -H "Content-Type: application/json" \
  -d '{"account_id":"<from-config>","zone_id":"<from-config>","subdomain":"myapp","port":5000,"description":"My App"}'

# Toggle enable/disable
curl -s -X PATCH "http://localhost:7070/api/mappings/<account>/<zone>/myapp" \
  -H "Authorization: Bearer $CF_PASS"

# Update
curl -s -X PUT "http://localhost:7070/api/mappings/<account>/<zone>/myapp" \
  -H "Authorization: Bearer $CF_PASS" \
  -H "Content-Type: application/json" \
  -d '{"enabled": false}'

# Delete
curl -s -X DELETE "http://localhost:7070/api/mappings/<account>/<zone>/myapp" \
  -H "Authorization: Bearer $CF_PASS"
```

### Generate & Deploy
```bash
# Regenerate nginx configs from current mappings
curl -s -X POST http://localhost:7070/api/generate \
  -H "Authorization: Bearer $CF_PASS"

# Deploy DNS records to Cloudflare
curl -s -X POST http://localhost:7070/api/deploy \
  -H "Authorization: Bearer $CF_PASS"
```

### DNS & Tunnels
```bash
# List all DNS records (all zones)
curl -s http://localhost:7070/api/dns/all -H "Authorization: Bearer $CF_PASS"

# List all tunnels
curl -s http://localhost:7070/api/tunnels/all -H "Authorization: Bearer $CF_PASS"

# Tunnels for specific account
curl -s "http://localhost:7070/api/accounts/<id>/tunnels" \
  -H "Authorization: Bearer $CF_PASS"

# Restart tunnel
curl -s -X POST http://localhost:7070/api/tunnel/restart \
  -H "Authorization: Bearer $CF_PASS"

# Restart all tunnels
curl -s -X POST http://localhost:7070/api/tunnel/restart-all \
  -H "Authorization: Bearer $CF_PASS"

# Sync from Cloudflare (pull live DNS into local config)
curl -s -X POST http://localhost:7070/api/cloudflare/sync \
  -H "Authorization: Bearer $CF_PASS"
```

### Nginx Management
```bash
# List all generated nginx config files
curl -s http://localhost:7070/api/nginx/configs -H "Authorization: Bearer $CF_PASS"

# Update a specific nginx config file
curl -s -X PUT "http://localhost:7070/api/nginx/configs/<filename>" \
  -H "Authorization: Bearer $CF_PASS" \
  -H "Content-Type: application/json" \
  -d '{"content":"server { ... }"}'

# Reload nginx (after manual config changes)
curl -s -X POST http://localhost:7070/api/nginx/reload \
  -H "Authorization: Bearer $CF_PASS"
```

### Apps (apps.yaml management)
```bash
# List all apps
curl -s http://localhost:7070/api/apps -H "Authorization: Bearer $CF_PASS"

# Bulk update apps.yaml
curl -s -X PUT http://localhost:7070/api/apps \
  -H "Authorization: Bearer $CF_PASS" \
  -H "Content-Type: application/json" \
  -d '{"apps": {...}}'

# Update single app
curl -s -X PUT "http://localhost:7070/api/apps/myapp" \
  -H "Authorization: Bearer $CF_PASS" \
  -H "Content-Type: application/json" \
  -d '{"port":5001,"enabled":true,"description":"Updated"}'

# Delete app
curl -s -X DELETE "http://localhost:7070/api/apps/myapp" \
  -H "Authorization: Bearer $CF_PASS"

# Start app process (if managed)
curl -s -X POST "http://localhost:7070/api/apps/myapp/start" \
  -H "Authorization: Bearer $CF_PASS"

# View app logs
curl -s "http://localhost:7070/api/apps/myapp/logs?lines=50" \
  -H "Authorization: Bearer $CF_PASS"
```

### Portless API
```bash
# List portless services
curl -s http://localhost:7070/api/portless -H "Authorization: Bearer $CF_PASS"

# Register service
curl -s -X POST http://localhost:7070/api/portless \
  -H "Authorization: Bearer $CF_PASS" \
  -H "Content-Type: application/json" \
  -d '{"name":"my-service","subdomain":"my-service","description":"My Service"}'

# Release service
curl -s -X DELETE "http://localhost:7070/api/portless/my-service" \
  -H "Authorization: Bearer $CF_PASS"
```

### Health Checks
```bash
# Run all health checks now
curl -s -X POST http://localhost:7070/api/health-check/run \
  -H "Authorization: Bearer $CF_PASS"

# Get health check history
curl -s http://localhost:7070/api/health-check/history \
  -H "Authorization: Bearer $CF_PASS"

# List configured health checks
curl -s http://localhost:7070/api/health-checks \
  -H "Authorization: Bearer $CF_PASS"

# Add health check
curl -s -X POST http://localhost:7070/api/health-check/add \
  -H "Authorization: Bearer $CF_PASS" \
  -H "Content-Type: application/json" \
  -d '{"url":"http://localhost:5000/health","name":"My App","interval":60}'

# Remove health check
curl -s -X DELETE "http://localhost:7070/api/health-check/<id>" \
  -H "Authorization: Bearer $CF_PASS"
```

### SSL Monitoring
```bash
# All SSL cert statuses
curl -s http://localhost:7070/api/ssl/all -H "Authorization: Bearer $CF_PASS"

# Specific domain cert details
curl -s "http://localhost:7070/api/ssl/myapp.example.com" \
  -H "Authorization: Bearer $CF_PASS"
```

### Logs
```bash
# Access logs (last N lines)
curl -s "http://localhost:7070/api/logs/access?lines=100" \
  -H "Authorization: Bearer $CF_PASS"

# Error logs
curl -s "http://localhost:7070/api/logs/errors?lines=50" \
  -H "Authorization: Bearer $CF_PASS"

# Log statistics
curl -s http://localhost:7070/api/logs/stats \
  -H "Authorization: Bearer $CF_PASS"

# Clear logs
curl -s -X DELETE http://localhost:7070/api/logs \
  -H "Authorization: Bearer $CF_PASS"
```

### Traffic Stats
```bash
curl -s http://localhost:7070/api/stats -H "Authorization: Bearer $CF_PASS"
```

### Security — IP Whitelist/Blacklist
```bash
# View lists
curl -s http://localhost:7070/api/ip/lists -H "Authorization: Bearer $CF_PASS"

# Add to whitelist
curl -s -X POST http://localhost:7070/api/ip/whitelist \
  -H "Authorization: Bearer $CF_PASS" \
  -H "Content-Type: application/json" \
  -d '{"ip":"1.2.3.4"}'

# Add to blacklist
curl -s -X POST http://localhost:7070/api/ip/blacklist \
  -H "Authorization: Bearer $CF_PASS" \
  -H "Content-Type: application/json" \
  -d '{"ip":"5.6.7.8"}'

# Remove from list
curl -s -X DELETE "http://localhost:7070/api/ip/whitelist/1.2.3.4" \
  -H "Authorization: Bearer $CF_PASS"
curl -s -X DELETE "http://localhost:7070/api/ip/blacklist/5.6.7.8" \
  -H "Authorization: Bearer $CF_PASS"

# Rate limit stats
curl -s http://localhost:7070/api/rate-limit/stats -H "Authorization: Bearer $CF_PASS"
```

### Backup & Restore
```bash
# Create backup
curl -s -X POST http://localhost:7070/api/backup/create \
  -H "Authorization: Bearer $CF_PASS"

# List backups
curl -s http://localhost:7070/api/backup/list -H "Authorization: Bearer $CF_PASS"

# Restore backup
curl -s -X POST http://localhost:7070/api/backup/restore \
  -H "Authorization: Bearer $CF_PASS" \
  -H "Content-Type: application/json" \
  -d '{"file":"backup-2026-03-28.yml"}'

# Get/update backup config
curl -s http://localhost:7070/api/backup/config -H "Authorization: Bearer $CF_PASS"
```

### Config Export/Import
```bash
# Export full config
curl -s http://localhost:7070/api/config/export -H "Authorization: Bearer $CF_PASS"

# Import config
curl -s -X POST http://localhost:7070/api/config/import \
  -H "Authorization: Bearer $CF_PASS" \
  -H "Content-Type: application/json" \
  -d '{"config": {...}}'
```

### Port Scanner
```bash
# Scan for listening local ports
curl -s -X POST http://localhost:7070/api/scan-ports \
  -H "Authorization: Bearer $CF_PASS"
```

### Webhooks
```bash
# List webhooks
curl -s http://localhost:7070/api/webhooks -H "Authorization: Bearer $CF_PASS"

# Add webhook
curl -s -X POST http://localhost:7070/api/webhooks \
  -H "Authorization: Bearer $CF_PASS" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://hooks.example.com/notify","events":["deploy","error"]}'

# Remove webhook
curl -s -X DELETE "http://localhost:7070/api/webhooks/<id>" \
  -H "Authorization: Bearer $CF_PASS"
```

### Settings
```bash
# Get settings
curl -s http://localhost:7070/api/settings -H "Authorization: Bearer $CF_PASS"

# Update settings
curl -s -X PUT http://localhost:7070/api/settings \
  -H "Authorization: Bearer $CF_PASS" \
  -H "Content-Type: application/json" \
  -d '{"auto_sync": true, "health_check_interval": 60}'
```

### Error Pages
```bash
# List all custom error pages
curl -s http://localhost:7070/api/error-pages -H "Authorization: Bearer $CF_PASS"

# Get specific error page
curl -s "http://localhost:7070/api/error-pages/404" -H "Authorization: Bearer $CF_PASS"

# Update error page
curl -s -X PUT "http://localhost:7070/api/error-pages/404" \
  -H "Authorization: Bearer $CF_PASS" \
  -H "Content-Type: application/json" \
  -d '{"content":"<html>Custom 404</html>"}'
```

---

## Common Workflows

### Add a New Service (Standard)
```bash
# 1. Add mapping
cloudflare-router add --subdomain myapp --port 5000 -d "My App"

# 2. Generate nginx config
cloudflare-router generate

# 3. Deploy DNS
cloudflare-router deploy

# Result: myapp.<domain> → localhost:5000
```

### Add a New Service (Portless — no hardcoded port)
```bash
# 1. Register service (auto-allocates port 4000-4999)
cloudflare-router port:register --service myapp --subdomain myapp -d "My App" --auto-map

# 2. Sync (generate + deploy in one step)
cloudflare-router port:sync

# 3. In your app, read port at startup:
PORT=$(cloudflare-router port:get myapp)
node server.js --port $PORT
```

### Debug Routing Issues
```bash
# 1. Check overall status
cloudflare-router status

# 2. Verify mapping exists
cloudflare-router list | grep myapp

# 3. Check nginx errors
curl -s "http://localhost:7070/api/logs/errors?lines=30" -H "Authorization: Bearer $CF_PASS"

# 4. Check health
curl -s -X POST http://localhost:7070/api/health-check/run -H "Authorization: Bearer $CF_PASS"

# 5. Reload nginx if config changed manually
curl -s -X POST http://localhost:7070/api/nginx/reload -H "Authorization: Bearer $CF_PASS"
```

### Disable/Enable a Service Temporarily
```bash
# Toggle via CLI (PATCH)
CF_PASS=$(python3 -c "import yaml; c=yaml.safe_load(open(\"$HOME/.cloudflare-router/config.yml\")); print(c.get('server',{}).get('password',''))")
ACCOUNT=$(python3 -c "import yaml; c=yaml.safe_load(open(\"$HOME/.cloudflare-router/config.yml\")); print(c['accounts'][0]['id'])")
ZONE=$(python3 -c "import yaml; c=yaml.safe_load(open(\"$HOME/.cloudflare-router/config.yml\")); print(c['accounts'][0]['zones'][0]['zone_id'])")
curl -s -X PATCH "http://localhost:7070/api/mappings/$ACCOUNT/$ZONE/myapp" \
  -H "Authorization: Bearer $CF_PASS"
```

### Bulk Add Multiple Services
```python
import subprocess
import requests

# Read credentials from config
import yaml, os
config = yaml.safe_load(open(os.path.expanduser("~/.cloudflare-router/config.yml")))
password = config.get("server", {}).get("password", "")
account_id = config["accounts"][0]["id"]
zone_id = config["accounts"][0]["zones"][0]["zone_id"]

base = "http://localhost:7070"
headers = {"Authorization": f"Bearer {password}", "Content-Type": "application/json"}

services = [
    {"subdomain": "app1", "port": 5001, "description": "App 1"},
    {"subdomain": "app2", "port": 5002, "description": "App 2"},
    {"subdomain": "app3", "port": 5003, "description": "App 3"},
]

for svc in services:
    svc["account_id"] = account_id
    svc["zone_id"] = zone_id
    r = requests.post(f"{base}/api/mappings", json=svc, headers=headers)
    print(f"{svc['subdomain']}: {r.status_code}")

# Generate + deploy
requests.post(f"{base}/api/generate", headers=headers)
requests.post(f"{base}/api/deploy", headers=headers)
print("Done!")
```

---

## PM2 Management
```bash
pm2 status cloudflare-router       # check running state
pm2 restart cloudflare-router      # restart server
pm2 reload cloudflare-router       # zero-downtime reload
pm2 stop cloudflare-router         # stop
pm2 start cloudflare-router        # start
pm2 logs cloudflare-router         # tail live logs
pm2 logs cloudflare-router --lines 100   # last 100 lines

# Log files
~/.cloudflare-router/logs/pm2-out.log
~/.cloudflare-router/logs/pm2-error.log
```

---

## API Validation Rules

| Field | Rule |
|-------|------|
| `subdomain` | Alphanumeric + hyphens, 1-63 chars |
| `port` | Integer 1-65535 |
| `domain` | Valid FQDN |
| `ip` | Valid IPv4 or IPv6 |
| `api_key` / `api_token` | Min 10 chars |

Validation errors return `400`:
```json
{
  "error": "Validation failed",
  "code": "validation_error",
  "details": [{"field": "subdomain", "message": "Valid subdomain required"}]
}
```

---

## Security Headers & Rate Limits

- Auth endpoints: **5 req / 15 min** per IP
- API endpoints: **100 req / min** per IP
- Helmet.js headers: CSP, HSTS, X-Frame-Options, etc.
- Request tracing: `X-Request-ID` header in all responses

---

## Notes & Gotchas

- **Always generate + deploy after mapping changes** — nginx and DNS are NOT auto-updated
- `apps.yaml` is preferred over `mappings.yml` for new services (richer options: health_check, no_tls_verify, host override)
- Portless range is **4000-4999** — don't assign services outside this range if using portless mode
- Dashboard password is stored in `config.yml` under `server.password` — never hardcode in scripts
- If nginx fails to reload: check `api/logs/errors` then `api/nginx/configs` to inspect generated files
- Tunnel credentials file path is in `config.yml` under `accounts[].zones[].tunnel_credentials`
