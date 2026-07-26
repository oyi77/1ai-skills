---
name: zapier-alt
description: Use when self-hosted Zapier alternative using n8n for zero-vendor-lock-in automation. See parent skill for full docs.
domain: automation
tags:
- automation
- zapier
- alternative
- self-hosted
version: 1.0.0
---
# Zapier Alt

## Quick Reference

Zapier Alt means running **n8n** (the open-source workflow automation tool) on your own server as a full Zapier replacement. Self-hosting eliminates per-task billing, gives full data control, and supports unlimited workflows. Unlike the parent workflows skill (which covers the full automation toolbox), this skill focuses specifically on **the Zapier replacement use case** — migrating existing Zaps, the cost math, and delivering it as a managed service.

## Overview

The fundamental pitch: Zapier charges $30/mo for 2K tasks, $600/mo for 50K tasks. A $10/mo VPS running n8n handles 200K+ tasks with no per-task fee. The switch requires upfront investment (Docker setup, workflow re-creation) but pays for itself in month 1 if you run any serious automation volume. Beyond cost savings, self-hosting means sensitive data (customer PII, financial records) never passes through a third-party processor — a compliance win for finance, healthcare, and legal clients.

## Quick Start

**Prerequisites:** A Linux VPS ($5-10/mo from Hetzner/DigitalOcean), Docker + Compose installed, a domain or Cloudflare Tunnel for HTTPS.

1. **Deploy n8n stack** — Use the Docker Compose from the parent skill (n8n + PostgreSQL + Redis). `docker compose up -d` gives you a running instance on port 5678.

2. **Re-create your first Zap** — In Zapier, export your workflow as a JSON blueprint (free Zapier export tool). Create a new n8n workflow → add a Webhook trigger node → replicate each Zap step as an n8n node. The visual editor is similar.

3. **Set up HTTPS** — n8n uses cookies for auth; it requires HTTPS. Use Caddy (`caddy reverse-proxy --from your.domain --to localhost:5678`) for automatic TLS.

```bash
# Production n8n deployment — one-liner
docker run -d \
  --name n8n \
  --restart always \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  -e N8N_SECURE_COOKIE=true \
  -e N8N_HOST=n8n.yourdomain.com \
  -e WEBHOOK_URL=https://n8n.yourdomain.com/ \
  -e EXECUTIONS_DATA_PRUNE=true \
  -e EXECUTIONS_DATA_MAX_AGE=168 \
  n8nio/n8n

# Behind Caddy reverse proxy
# Caddyfile
n8n.yourdomain.com {
    reverse_proxy localhost:5678
}

# Test: open https://n8n.yourdomain.com, create a Webhook → Slack workflow
```

The critical env vars: `N8N_SECURE_COOKIE=true` (requires HTTPS), `EXECUTIONS_DATA_PRUNE=true` (auto-deletes old execution logs to prevent disk bloat), `WEBHOOK_URL` (must match your public domain for webhooks to work).

## Checklist

- [ ] HTTPS configured with valid TLS cert — n8n owner auth AND webhook endpoints both require HTTPS
- [ ] Execution data pruning enabled (`EXECUTIONS_DATA_MAX_AGE=168`) — n8n stores every run forever by default, which fills a 20GB disk in weeks
- [ ] PostgreSQL backend used instead of SQLite — SQLite locks on concurrent workflow execution, causing 5s delays
- [ ] Backup strategy tested: `pg_dump n8n > backup.sql` + `docker cp n8n_data:/home/node/.n8n .` → restore on fresh VPS in 10 min
- [ ] At least one Zapier Zap migrated and running equally in n8n — run both in parallel for 24h, verify identical outputs

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Zapier's $30/mo is fine for my volume" | At 10K tasks/mo that's $99/mo on Zapier vs $10/mo on a VPS; at 50K tasks it's $599/mo vs $10/mo — the gap widens linearly |
| "Self-hosting is too complex for clients" | Wrap it in a managed service: $100-500/mo for setup + maintenance; clients don't touch the server, you handle updates |
| "Migrating Zaps is too much work" | Most Zaps use 2-5 steps (trigger → filter → action); recreating them in n8n takes 10-15 min per Zap after the first one |

## When to Use
Use this skill when working with zapier alt.

## Workflow
See the parent skill for authoritative workflow documentation.
