---
name: cicd-deployment
description: "Build production CI/CD pipelines with GitHub Actions, Docker, zero-downtime blue/green deploys, rollback, and Telegram alerts."
domain: development
---

# cicd-deployment

**name:** cicd-deployment  
**description:** Production-ready CI/CD pipeline and deployment skill for BerkahKarya Software House. Covers GitHub Actions workflows, systemd user services, Docker, VPS deployment, zero-downtime blue/green strategy, rollback, health checks, and Telegram notifications. Stack: Python/Node.js on Kali Linux (kali-openclaw). AI GM: Vilona.

---

## Overview

This skill provides opinionated, fast-to-implement CI/CD patterns for BerkahKarya services. The pipeline follows a strict flow:

```
lint → test → build → deploy → health-check → notify
```

Every deployment is automated, auditable, and reversible. Secrets never touch git. Failures auto-notify via Telegram.

---

## Environments

| Env | Branch | Auto-deploy | Approval Required |
|-----|--------|-------------|-------------------|
| dev | `develop` | ✅ Yes | ❌ No |
| staging | `staging` | ✅ Yes | ❌ No |
| production | `main` | ✅ Yes (after staging pass) | ✅ Yes (manual gate) |

---

## Secrets Management — CRITICAL

**Golden Rule: `.env` files NEVER go in git. Ever.**

### Setup Pattern

```bash
# On the server, create env file manually:
nano ~/.config/berkahkarya/<service-name>/.env

# Set strict permissions:
chmod 600 ~/.config/berkahkarya/<service-name>/.env

# Add to .gitignore (non-negotiable):
echo ".env" >> .gitignore
echo ".env.*" >> .gitignore
echo "!.env.example" >> .gitignore
```

### .env.example Template (commit this, not .env)

```env
# .env.example — copy to .env and fill values
APP_NAME=berkahkarya-service
APP_ENV=production
APP_PORT=8000

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# External APIs
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# Service-specific
SECRET_KEY=
API_KEY=
```

### GitHub Actions Secrets

Store in repo Settings → Secrets and variables → Actions:
- `SSH_PRIVATE_KEY` — deploy key for server access
- `SERVER_HOST` — VPS IP/hostname
- `SERVER_USER` — SSH user (openclaw)
- `TELEGRAM_BOT_TOKEN` — for deployment notifications
- `TELEGRAM_CHAT_ID` — target chat/channel

---

## GitHub Actions Template

- Configure cicd, deployment, domain, relevant, this settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### `.github/workflows/deploy.yml`

```yaml
name: CI/CD Deploy Pipeline

on:
  push:
    branches:
      - main        # triggers production deploy
      - staging     # triggers staging deploy
      - develop     # triggers dev deploy
  pull_request:
    branches:
      - main
      - staging

env:
  SERVICE_NAME: berkahkarya-service    # change per repo
  SERVER_USER: openclaw
  DEPLOY_PATH: /home/openclaw/services/${{ env.SERVICE_NAME }}

jobs:
  # ─── STAGE 1: LINT ───────────────────────────────────────────────
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        if: ${{ hashFiles('requirements.txt') != '' }}
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Set up Node.js
        if: ${{ hashFiles('package.json') != '' }}
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install Python deps
        if: ${{ hashFiles('requirements.txt') != '' }}
        run: pip install ruff black isort

      - name: Lint Python (ruff)
        if: ${{ hashFiles('requirements.txt') != '' }}
        run: ruff check .

      - name: Install Node deps
        if: ${{ hashFiles('package.json') != '' }}
        run: npm ci

      - name: Lint Node (eslint)
        if: ${{ hashFiles('package.json') != '' }}
        run: npm run lint --if-present

  # ─── STAGE 2: TEST ───────────────────────────────────────────────
  test:
    name: Test
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        if: ${{ hashFiles('requirements.txt') != '' }}
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        if: ${{ hashFiles('requirements.txt') != '' }}
        run: pip install -r requirements.txt

      - name: Run Python tests
        if: ${{ hashFiles('requirements.txt') != '' }}
        run: pytest tests/ -v --tb=short

      - name: Set up Node.js
        if: ${{ hashFiles('package.json') != '' }}
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install Node deps
        if: ${{ hashFiles('package.json') != '' }}
        run: npm ci

      - name: Run Node tests
        if: ${{ hashFiles('package.json') != '' }}
        run: npm test --if-present

  # ─── STAGE 3: BUILD ──────────────────────────────────────────────
  build:
    name: Build
    runs-on: ubuntu-latest
    needs: test
    if: github.event_name == 'push'
    steps:
      - uses: actions/checkout@v4

      - name: Build Docker image (if Dockerfile exists)
        if: ${{ hashFiles('Dockerfile') != '' }}
        run: |
          docker build -t ${{ env.SERVICE_NAME }}:${{ github.sha }} .
          docker tag ${{ env.SERVICE_NAME }}:${{ github.sha }} ${{ env.SERVICE_NAME }}:latest

      - name: Build Node.js app
        if: ${{ hashFiles('package.json') != '' }}
        run: |
          npm ci
          npm run build --if-present

      - name: Create deployment artifact
        run: |
          tar -czf deploy.tar.gz \
            --exclude='.git' \
            --exclude='node_modules' \
            --exclude='__pycache__' \
            --exclude='.env' \
            --exclude='*.pyc' \
            .

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: deploy-artifact
          path: deploy.tar.gz
          retention-days: 7

  # ─── STAGE 4: DEPLOY ─────────────────────────────────────────────
  deploy:
    name: Deploy
    runs-on: ubuntu-latest
    needs: build
    if: github.event_name == 'push'
    environment:
      name: ${{ github.ref_name == 'main' && 'production' || github.ref_name == 'staging' && 'staging' || 'development' }}
    steps:
      - name: Set environment variables
        run: |
          if [[ "${{ github.ref_name }}" == "main" ]]; then
            echo "ENV=production" >> $GITHUB_ENV
            echo "PORT=8000" >> $GITHUB_ENV
          elif [[ "${{ github.ref_name }}" == "staging" ]]; then
            echo "ENV=staging" >> $GITHUB_ENV
            echo "PORT=8001" >> $GITHUB_ENV
          else
            echo "ENV=development" >> $GITHUB_ENV
            echo "PORT=8002" >> $GITHUB_ENV
          fi

      - name: Download artifact
        uses: actions/download-artifact@v4
        with:
          name: deploy-artifact

      - name: Setup SSH
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/deploy_key
          chmod 600 ~/.ssh/deploy_key
          ssh-keyscan -H ${{ secrets.SERVER_HOST }} >> ~/.ssh/known_hosts

      - name: Deploy to server
        run: |
          # Upload artifact
          scp -i ~/.ssh/deploy_key deploy.tar.gz \
            ${{ env.SERVER_USER }}@${{ secrets.SERVER_HOST }}:/tmp/

          # Execute remote deploy script
          ssh -i ~/.ssh/deploy_key \
            ${{ env.SERVER_USER }}@${{ secrets.SERVER_HOST }} \
            "bash ~/services/${{ env.SERVICE_NAME }}/scripts/deploy.sh \
              ${{ env.SERVICE_NAME }} \
              ${{ github.sha }} \
              ${{ env.ENV }} \
              ${{ env.PORT }}"

  # ─── STAGE 5: HEALTH CHECK ───────────────────────────────────────
  health_check:
    name: Health Check
    runs-on: ubuntu-latest
    needs: deploy
    steps:
      - name: Setup SSH
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/deploy_key
          chmod 600 ~/.ssh/deploy_key
          ssh-keyscan -H ${{ secrets.SERVER_HOST }} >> ~/.ssh/known_hosts

      - name: Run health check
        run: |
          ssh -i ~/.ssh/deploy_key \
            ${{ env.SERVER_USER }}@${{ secrets.SERVER_HOST }} \
            "bash ~/services/${{ env.SERVICE_NAME }}/scripts/health_check.sh ${{ env.SERVICE_NAME }}"

  # ─── STAGE 6: NOTIFY ─────────────────────────────────────────────
  notify_success:
    name: Notify Success
    runs-on: ubuntu-latest
    needs: [health_check]
    if: success()
    steps:
      - name: Telegram — Deploy Success
        run: |
          curl -s -X POST "https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage" \
            -d chat_id="${{ secrets.TELEGRAM_CHAT_ID }}" \
            -d parse_mode="Markdown" \
            -d text="✅ *Deploy SUCCESS*
          Service: \`${{ env.SERVICE_NAME }}\`
          Branch: \`${{ github.ref_name }}\`
          Commit: \`${{ github.sha }}\`
          By: ${{ github.actor }}
          Time: $(date '+%Y-%m-%d %H:%M UTC')"

  notify_failure:
    name: Notify Failure
    runs-on: ubuntu-latest
    needs: [lint, test, build, deploy, health_check]
    if: failure()
    steps:
      - name: Telegram — Deploy FAILED
        run: |
          curl -s -X POST "https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage" \
            -d chat_id="${{ secrets.TELEGRAM_CHAT_ID }}" \
            -d parse_mode="Markdown" \
            -d text="🚨 *Deploy FAILED*
          Service: \`${{ env.SERVICE_NAME }}\`
          Branch: \`${{ github.ref_name }}\`
          Commit: \`${{ github.sha }}\`
          By: ${{ github.actor }}
          Time: $(date '+%Y-%m-%d %H:%M UTC')
          Check: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
```

---

## Deployment Scripts

- Configure cicd, deployment, domain, relevant, this settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### `scripts/deploy.sh`

```bash
#!/bin/bash
# scripts/deploy.sh — Zero-downtime deploy with blue/green swap
# Usage: ./scripts/deploy.sh <service-name> <git-sha> <env> <port>
set -euo pipefail

SERVICE_NAME="${1:-berkahkarya-service}"
GIT_SHA="${2:-unknown}"
ENV="${3:-production}"
PORT="${4:-8000}"

DEPLOY_BASE="$HOME/services/$SERVICE_NAME"
ARTIFACT="/tmp/deploy.tar.gz"
BLUE_DIR="$DEPLOY_BASE/blue"
GREEN_DIR="$DEPLOY_BASE/green"
ACTIVE_LINK="$DEPLOY_BASE/active"
LOG_FILE="$DEPLOY_BASE/logs/deploy.log"

mkdir -p "$DEPLOY_BASE/logs" "$BLUE_DIR" "$GREEN_DIR"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"; }

log "=== DEPLOY START: $SERVICE_NAME @ $GIT_SHA ($ENV) ==="

# ── Determine inactive slot ──────────────────────────────────────
if [[ -L "$ACTIVE_LINK" && "$(readlink "$ACTIVE_LINK")" == "$BLUE_DIR" ]]; then
    INACTIVE_DIR="$GREEN_DIR"
    INACTIVE_SERVICE="${SERVICE_NAME}-green"
    ACTIVE_SERVICE="${SERVICE_NAME}-blue"
else
    INACTIVE_DIR="$BLUE_DIR"
    INACTIVE_SERVICE="${SERVICE_NAME}-blue"
    ACTIVE_SERVICE="${SERVICE_NAME}-green"
fi

log "Active slot: $ACTIVE_SERVICE → Deploying to: $INACTIVE_SERVICE"

# ── Unpack artifact ──────────────────────────────────────────────
log "Unpacking artifact..."
rm -rf "$INACTIVE_DIR"/*
tar -xzf "$ARTIFACT" -C "$INACTIVE_DIR"
rm -f "$ARTIFACT"

# ── Copy .env from secure location ──────────────────────────────
ENV_FILE="$HOME/.config/berkahkarya/$SERVICE_NAME/.env"
if [[ -f "$ENV_FILE" ]]; then
    cp "$ENV_FILE" "$INACTIVE_DIR/.env"
    log ".env copied from secure location"
else
    log "WARNING: .env not found at $ENV_FILE — service may fail"
fi

# ── Install dependencies ─────────────────────────────────────────
cd "$INACTIVE_DIR"

if [[ -f "requirements.txt" ]]; then
    log "Installing Python dependencies..."
    python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt -q
fi

if [[ -f "package.json" ]]; then
    log "Installing Node dependencies..."
    npm ci --production --silent
fi

# ── Start inactive slot ──────────────────────────────────────────
log "Starting $INACTIVE_SERVICE..."
systemctl --user stop "$INACTIVE_SERVICE" 2>/dev/null || true
systemctl --user start "$INACTIVE_SERVICE"

# ── Wait for service to be healthy ──────────────────────────────
log "Waiting for health check..."
MAX_WAIT=30
WAITED=0
until curl -sf "http://localhost:$PORT/health" > /dev/null 2>&1; do
    sleep 2
    WAITED=$((WAITED + 2))
    if [[ $WAITED -ge $MAX_WAIT ]]; then
        log "ERROR: Health check timeout after ${MAX_WAIT}s. Rolling back..."
        systemctl --user stop "$INACTIVE_SERVICE"
        exit 1
    fi
done
log "Health check passed after ${WAITED}s"

# ── Swap active link ─────────────────────────────────────────────
log "Swapping active slot to $INACTIVE_SERVICE..."
ln -sfn "$INACTIVE_DIR" "$ACTIVE_LINK"

# ── Stop old slot ────────────────────────────────────────────────
log "Stopping old slot: $ACTIVE_SERVICE"
systemctl --user stop "$ACTIVE_SERVICE" 2>/dev/null || true

log "=== DEPLOY COMPLETE: $SERVICE_NAME ($INACTIVE_SERVICE) ==="
echo "$GIT_SHA" > "$DEPLOY_BASE/DEPLOYED_SHA"
echo "$INACTIVE_SERVICE" > "$DEPLOY_BASE/ACTIVE_SLOT"
```

---

### `scripts/rollback.sh`

```bash
#!/bin/bash
# scripts/rollback.sh — Instant rollback via git revert + service restart
# Usage: ./scripts/rollback.sh <service-name>
set -euo pipefail

SERVICE_NAME="${1:-berkahkarya-service}"
DEPLOY_BASE="$HOME/services/$SERVICE_NAME"
LOG_FILE="$DEPLOY_BASE/logs/deploy.log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"; }

log "=== ROLLBACK START: $SERVICE_NAME ==="

# ── Read slots ───────────────────────────────────────────────────
ACTIVE_SLOT=$(cat "$DEPLOY_BASE/ACTIVE_SLOT" 2>/dev/null || echo "${SERVICE_NAME}-blue")
ACTIVE_LINK="$DEPLOY_BASE/active"
BLUE_DIR="$DEPLOY_BASE/blue"
GREEN_DIR="$DEPLOY_BASE/green"

if [[ "$ACTIVE_SLOT" == "${SERVICE_NAME}-blue" ]]; then
    FALLBACK_DIR="$GREEN_DIR"
    FALLBACK_SERVICE="${SERVICE_NAME}-green"
else
    FALLBACK_DIR="$BLUE_DIR"
    FALLBACK_SERVICE="${SERVICE_NAME}-blue"
fi

log "Switching from $ACTIVE_SLOT → $FALLBACK_SERVICE"

# ── Start fallback slot ──────────────────────────────────────────
systemctl --user start "$FALLBACK_SERVICE" 2>/dev/null || {
    log "ERROR: Cannot start fallback slot $FALLBACK_SERVICE"
    exit 1
}

sleep 3  # Give it a moment

# ── Verify fallback is alive ─────────────────────────────────────
if systemctl --user is-active --quiet "$FALLBACK_SERVICE"; then
    log "Fallback service active — swapping link..."
    ln -sfn "$FALLBACK_DIR" "$ACTIVE_LINK"
    echo "$FALLBACK_SERVICE" > "$DEPLOY_BASE/ACTIVE_SLOT"

    # Stop current broken slot
    systemctl --user stop "$ACTIVE_SLOT" 2>/dev/null || true
    log "Stopped broken slot: $ACTIVE_SLOT"
else
    log "ERROR: Fallback service failed to start. Manual intervention required."
    exit 2
fi

log "=== ROLLBACK COMPLETE: Now running $FALLBACK_SERVICE ==="

# ── Notify via Telegram ──────────────────────────────────────────
if [[ -f "$DEPLOY_BASE/.env" ]]; then
    source "$DEPLOY_BASE/.env"
fi

if [[ -n "${TELEGRAM_BOT_TOKEN:-}" && -n "${TELEGRAM_CHAT_ID:-}" ]]; then
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d chat_id="${TELEGRAM_CHAT_ID}" \
        -d parse_mode="Markdown" \
        -d text="⚠️ *ROLLBACK EXECUTED*
Service: \`$SERVICE_NAME\`
Now running: \`$FALLBACK_SERVICE\`
Time: $(date '+%Y-%m-%d %H:%M UTC')
Action: Manual rollback completed" > /dev/null
fi
```

---

### `scripts/health_check.sh`

```bash
#!/bin/bash
# scripts/health_check.sh — Multi-stage health verification
# Usage: ./scripts/health_check.sh <service-name> [port]
set -euo pipefail

SERVICE_NAME="${1:-berkahkarya-service}"
PORT="${2:-8000}"
DEPLOY_BASE="$HOME/services/$SERVICE_NAME"
LOG_FILE="$DEPLOY_BASE/logs/health.log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"; }
pass() { log "✅ PASS: $*"; }
fail() { log "❌ FAIL: $*"; exit 1; }

log "=== HEALTH CHECK: $SERVICE_NAME ==="

# ── 1. Process check ─────────────────────────────────────────────
ACTIVE_SLOT=$(cat "$DEPLOY_BASE/ACTIVE_SLOT" 2>/dev/null || echo "$SERVICE_NAME")
if systemctl --user is-active --quiet "$ACTIVE_SLOT"; then
    pass "systemd service $ACTIVE_SLOT is active"
else
    fail "systemd service $ACTIVE_SLOT is NOT active"
fi

# ── 2. Port check ────────────────────────────────────────────────
if ss -tlnp | grep -q ":$PORT "; then
    pass "Port $PORT is listening"
else
    fail "Port $PORT is NOT listening"
fi

# ── 3. HTTP health endpoint ──────────────────────────────────────
HTTP_STATUS=$(curl -o /dev/null -s -w "%{http_code}" --max-time 5 "http://localhost:$PORT/health" || echo "000")
if [[ "$HTTP_STATUS" == "200" ]]; then
    pass "HTTP /health returned 200"
elif [[ "$HTTP_STATUS" == "000" ]]; then
    fail "HTTP /health — connection refused or timeout"
else
    fail "HTTP /health returned $HTTP_STATUS (expected 200)"
fi

# ── 4. Log tail check (last 20 lines for errors) ─────────────────
RECENT_LOGS=$(journalctl --user -u "$ACTIVE_SLOT" -n 20 --no-pager 2>/dev/null || echo "")
ERROR_COUNT=$(echo "$RECENT_LOGS" | grep -c -i "error\|exception\|traceback\|fatal" || true)
if [[ "$ERROR_COUNT" -gt 5 ]]; then
    log "WARNING: $ERROR_COUNT error-like lines in recent logs"
    echo "$RECENT_LOGS" | tail -10
else
    pass "Recent logs look clean ($ERROR_COUNT error-like lines)"
fi

# ── 5. Memory/CPU sanity check ───────────────────────────────────
if command -v ps &>/dev/null; then
    PID=$(systemctl --user show -p MainPID "$ACTIVE_SLOT" --value 2>/dev/null || echo "")
    if [[ -n "$PID" && "$PID" != "0" ]]; then
        MEM_MB=$(ps -o rss= -p "$PID" 2>/dev/null | awk '{printf "%.0f", $1/1024}' || echo "?")
        pass "Process $PID using ~${MEM_MB}MB RAM"
    fi
fi

log "=== HEALTH CHECK PASSED ==="
```

---

## Systemd User Service Templates

Reusable templates for cicd-deployment.

Standard config:
```yaml
name: cicd-deployment_standard
mode: production
output: results/
format: json
```

Test config:
```yaml
name: cicd-deployment_test
mode: development
dry_run: true
verbose: true
```


### FastAPI Service (`~/.config/systemd/user/<service-name>.service`)

```ini
[Unit]
Description=BerkahKarya FastAPI Service — <service-name>
After=network.target
Wants=network.target

[Service]
Type=simple
WorkingDirectory=/home/openclaw/services/<service-name>/active
EnvironmentFile=/home/openclaw/.config/berkahkarya/<service-name>/.env
ExecStart=/home/openclaw/services/<service-name>/active/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```

### Blue/Green Pair (create two: blue + green)

```ini
# <service-name>-blue.service
[Unit]
Description=BerkahKarya <service-name> (Blue Slot)
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/openclaw/services/<service-name>/blue
EnvironmentFile=/home/openclaw/.config/berkahkarya/<service-name>/.env
ExecStart=/home/openclaw/services/<service-name>/blue/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```

### Enable Services

```bash
# Enable lingering so user services survive logout:
loginctl enable-linger openclaw

# Enable both slots:
systemctl --user daemon-reload
systemctl --user enable <service-name>-blue <service-name>-green
```

---

## Docker Templates

Reusable templates for cicd-deployment.

Standard config:
```yaml
name: cicd-deployment_standard
mode: production
output: results/
format: json
```

Test config:
```yaml
name: cicd-deployment_test
mode: development
dry_run: true
verbose: true
```


### `Dockerfile` — Python/FastAPI

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first (layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Non-root user
RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

### `Dockerfile` — Node.js/Express

```dockerfile
FROM node:20-alpine

WORKDIR /app

# Install deps first (layer cache)
COPY package*.json ./
RUN npm ci --production

# Copy app
COPY . .

# Non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -qO- http://localhost:3000/health || exit 1

CMD ["node", "src/index.js"]
```

### `docker-compose.yml`

```yaml
version: '3.8'

services:
  app:
    build: .
    container_name: berkahkarya-${SERVICE_NAME}
    restart: unless-stopped
    ports:
      - "${APP_PORT:-8000}:8000"
    env_file:
      - .env
    volumes:
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
    labels:
      - "com.berkahkarya.service=${SERVICE_NAME}"
      - "com.berkahkarya.env=${APP_ENV}"

  # Optional: nginx reverse proxy
  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - app

networks:
  default:
    name: berkahkarya-network
```

---

## BerkahKarya Service Patterns

- Configure cicd, deployment, domain, relevant, this settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### FastAPI Service — Minimum Viable Structure

```
my-fastapi-service/
├── main.py                  # Entry point (app = FastAPI())
├── requirements.txt
├── .env.example
├── .gitignore               # Must include .env
├── Dockerfile
├── docker-compose.yml
├── scripts/
│   ├── deploy.sh
│   ├── rollback.sh
│   └── health_check.sh
├── .github/
│   └── workflows/
│       └── deploy.yml
└── tests/
    └── test_main.py
```

**Required `/health` endpoint:**

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok", "service": "my-service"}
```

---

### Node.js Express Service — Minimum Viable Structure

```
my-express-service/
├── src/
│   └── index.js             # Entry point
├── package.json
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── scripts/
│   ├── deploy.sh
│   ├── rollback.sh
│   └── health_check.sh
└── .github/
    └── workflows/
        └── deploy.yml
```

**Required `/health` endpoint:**

```javascript
// src/index.js
const express = require('express');
const app = express();

app.get('/health', (req, res) => {
    res.json({ status: 'ok', service: 'my-service' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Listening on :${PORT}`));
```

---

### Python Script / Worker Service

For non-HTTP workers (e.g., automation scripts, cron workers):

```ini
# ~/.config/systemd/user/berkahkarya-worker.service
[Unit]
Description=BerkahKarya Background Worker
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/openclaw/services/my-worker/active
EnvironmentFile=/home/openclaw/.config/berkahkarya/my-worker/.env
ExecStart=/home/openclaw/services/my-worker/active/.venv/bin/python worker.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```

**Health check for workers (process check only):**

```bash
# In health_check.sh, skip HTTP check:
if systemctl --user is-active --quiet "berkahkarya-worker"; then
    pass "Worker process is running"
else
    fail "Worker process is NOT running"
fi

# Check worker heartbeat file (update this in your worker every N minutes):
HEARTBEAT="$HOME/services/my-worker/active/heartbeat"
if [[ -f "$HEARTBEAT" ]]; then
    LAST_BEAT=$(cat "$HEARTBEAT")
    NOW=$(date +%s)
    AGE=$((NOW - LAST_BEAT))
    if [[ $AGE -lt 300 ]]; then   # 5 minute tolerance
        pass "Worker heartbeat fresh (${AGE}s ago)"
    else
        fail "Worker heartbeat stale (${AGE}s ago — possible hang)"
    fi
fi
```

---

## Zero-Downtime Blue/Green Flow

```
Deploy Request
     │
     ▼
[Determine Active Slot]
blue active → deploy to green
green active → deploy to blue
     │
     ▼
[Deploy to INACTIVE slot]
- Unpack artifact
- Copy .env
- Install deps
- Start inactive service
     │
     ▼
[Health Check Inactive]
curl /health → 200?
     │
   Yes │               No
     ▼                 ▼
[Swap Active Link]  [Rollback]
  ln -sfn            Stop inactive
     │               Exit 1
     ▼
[Stop Old Slot]
     │
     ▼
[Notify Telegram]
✅ Deploy SUCCESS
```

---

## Rollback Strategy

- Configure cicd, deployment, domain, relevant, this settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Automatic (on deploy failure)

```bash
# In deploy.sh — if health check fails, auto-rollback:
if ! curl -sf "http://localhost:$PORT/health"; then
    log "Health check failed — rolling back"
    systemctl --user stop "$INACTIVE_SERVICE"
    exit 1
    # Active slot was never swapped, so old service continues
fi
```

### Manual Rollback

```bash
# SSH to server:
ssh openclaw@<server>

# Run rollback:
cd ~/services/<service-name>
bash scripts/rollback.sh <service-name>

# Verify:
systemctl --user status <service-name>-blue
systemctl --user status <service-name>-green
curl http://localhost:8000/health
```

### Git Revert (for code rollback)

```bash
# On local machine:
git log --oneline -10
git revert <bad-commit-sha>
git push origin main
# This triggers a new deploy pipeline with reverted code
```

---

## Quick Setup Checklist

For a new BerkahKarya service:

```bash
# 1. On server — create directory structure:
mkdir -p ~/services/<service-name>/{blue,green,logs}
mkdir -p ~/.config/berkahkarya/<service-name>

# 2. Create and secure .env:
nano ~/.config/berkahkarya/<service-name>/.env
chmod 600 ~/.config/berkahkarya/<service-name>/.env

# 3. Copy systemd service files:
cp *.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable <service-name>-blue <service-name>-green
loginctl enable-linger openclaw

# 4. In GitHub repo — add secrets:
# SSH_PRIVATE_KEY, SERVER_HOST, SERVER_USER
# TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

# 5. Push to trigger first deploy:
git push origin main

# 6. Monitor:
journalctl --user -u <service-name>-blue -f
```

---

## Common Commands Reference

```bash
# View service logs:
journalctl --user -u <service-name>-blue -f
journalctl --user -u <service-name>-green --since "10 min ago"

# Check service status:
systemctl --user status <service-name>-blue
systemctl --user status <service-name>-green

# Manual deploy (skip CI):
bash ~/services/<service-name>/scripts/deploy.sh <name> local production 8000

# Manual rollback:
bash ~/services/<service-name>/scripts/rollback.sh <name>

# Check which slot is active:
cat ~/services/<service-name>/ACTIVE_SLOT
readlink ~/services/<service-name>/active

# Check deployed SHA:
cat ~/services/<service-name>/DEPLOYED_SHA

# Health check:
bash ~/services/<service-name>/scripts/health_check.sh <name>

# Docker quick commands:
docker compose up -d --build
docker compose logs -f
docker compose ps
docker compose down
```

---

## Telegram Notification Patterns

Manual alert (from any script):

```bash
#!/bin/bash
# Reusable notify function
telegram_notify() {
    local message="$1"
    local bot_token="${TELEGRAM_BOT_TOKEN}"
    local chat_id="${TELEGRAM_CHAT_ID}"

    if [[ -z "$bot_token" || -z "$chat_id" ]]; then
        echo "WARNING: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set"
        return 0
    fi

    curl -s -X POST "https://api.telegram.org/bot${bot_token}/sendMessage" \
        -d chat_id="${chat_id}" \
        -d parse_mode="Markdown" \
        -d text="${message}" > /dev/null
}

# Usage:
telegram_notify "✅ *Deploy SUCCESS* — \`my-service\` @ $(date)"
telegram_notify "🚨 *Deploy FAILED* — \`my-service\` — manual action required"
```

---

*Skill maintained by Vilona — BerkahKarya AI GM | Software House Division*  
*Stack: Python/Node.js | Server: kali-openclaw | Updated: 2026-03*

## How to Use

1. Understand the requirement and existing codebase patterns
2. Design the solution with error handling and testability in mind
3. Implement incrementally with tests for each change
4. Verify against expected outcomes (manual and automated)
5. Document usage, edge cases, and integration points
6. Review with team before merging to shared branches

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Red Flags

- **Skipping tests to ship faster**: Untested code breaks in production when you least expect it
- **No error handling in production code**: Unhandled errors crash services and lose user data
- **Hardcoded configuration values**: Hardcoded values prevent environment switching and leak secrets
- **Ignoring security implications**: Missing input validation, auth bypasses, and injection vulnerabilities
- **Over-engineering simple solutions**: Premature abstraction adds complexity without proportional benefit

## Verification

- All tests pass after code changes (unit, integration, e2e as appropriate)
- Error handling covers documented failure modes and edge cases
- Configuration uses environment variables or config files, not hardcoded values
- Security-sensitive code (auth, payments, API) has explicit review
- Code follows project conventions (naming, patterns, structure)
