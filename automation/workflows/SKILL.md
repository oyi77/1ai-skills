---
name: workflows
description: Use when workflow automation hub — cron scheduling, IFTTT triggers, n8n visual builder, webhook routing, and self-hosted Zapier alternatives for zero-vendor-lock-in automation.
domain: automation
author: oyi77
license: Apache-2.0
subdomain: workflow-automation
tags:
- automation
- workflows
- cron
- ifttt
- n8n
- webhook
- zapier
- productivity
- pipelines
version: 1.0.0
---
# Workflows — Automation Workflow Hub

## Money-Making Overview

| Tool | Service You Sell | Monthly Revenue Potential | Setup Complexity |
|---|---|---|---|
| **n8n Builder** | Build custom automation workflows for clients ($200-$2,000/project) | $2,000-$8,000/mo | Medium |
| **Cron Designer** | Scheduled data jobs, report generation, batch processing | $500-$3,000/mo | Low |
| **Webhook Router** | Integration middleware for SaaS apps, payment gateways | $1,000-$5,000/mo | Medium |
| **IFTTT Maker** | Simple applet-based automations for non-technical clients | $300-$2,000/mo | Very Low |
| **Zapier Alt** | Self-hosted Zapier replacement — sell as managed service | $1,000-$6,000/mo | High |
| **Build-in-Public Pipeline** | Document and sell your automation setup as a productized service | $1,000-$4,000/mo | Low |

**Combined Revenue Potential: $5,000-$25,000/mo** when you build once, deploy for many clients.

---

## Combined Capabilities Table

| Feature | Cron | IFTTT | n8n | Webhook Router | Zapier Alt |
|---|---|---|---|---|---|
| Visual drag-and-drop builder | No | Yes (applets) | Yes | No | Yes (Zaps) |
| Trigger type | Time-based only | App event + time | App + webhook + time | HTTP/webhook | App + webhook + time |
| Custom code | Shell/Python | No | JS/Python nodes | Your server | No (native) |
| 400+ integrations | No | Yes | Yes | No (custom) | Yes |
| Self-hosted | System cron | No | Docker/K8s | Your server | n8n (alt) |
| Free tier | Yes | Limited | Yes (self-host) | Yes | $20/mo (Zapier) |
| Error handling | Bash retry | Applet limits | Full nodes | Express/Caddy | Built-in |
| Money potential | Reports/data | Simple triggers | Complex pipelines | API middleware | Managed hosting |

---

## 1. Cron Designer

### Overview

Cron is the UNIX standard for time-based job scheduling. A cron expression (`min hour day month weekday`) triggers commands at precise intervals. Combined with bash/Python, cron drives the entire automation pipeline.

### Quick Reference — Cron Expressions

```
# ┌───────────── minute (0-59)
# │ ┌───────────── hour (0-23)
# │ │ ┌───────────── day of month (1-31)
# │ │ │ ┌───────────── month (1-12)
# │ │ │ │ ┌───────────── day of week (0-7, 0=Sun)
# │ │ │ │ │
  * * * * *  command-to-execute
```

### Common Patterns

```bash
# ─── Daily reports ───
0 8 * * * /home/user/scripts/generate-daily-report.sh

# ─── Hourly price check ───
0 * * * * /usr/bin/python3 /home/user/bots/check-prices.py

# ─── Every 30 min content publish ───
*/30 * * * * /usr/bin/node /home/user/content-queue/dispatch.js

# ─── Weekly full backup (Sunday 3am) ───
0 3 * * 0 /home/user/scripts/backup-full.sh

# ─── Monthly invoice generation ───
0 9 1 * * /usr/bin/python3 /home/user/billing/generate-invoices.py

# ─── Every 5 min check webhook queue ───
*/5 * * * * /home/user/webhooks/process-queue.sh
```

### Advanced — Self-Healing Cron

```bash
#!/bin/bash
# healer.sh — wrap cron jobs with logging and retry
JOB_NAME="$1"
shift
LOG_FILE="/var/log/cron/${JOB_NAME}.log"
MAX_RETRIES=3
RETRY_DELAY=60

for i in $(seq 1 $MAX_RETRIES); do
    echo "[$(date)] Attempt $i/$MAX_RETRIES: $*" >> "$LOG_FILE"
    if "$@" >> "$LOG_FILE" 2>&1; then
        echo "[$(date)] SUCCESS" >> "$LOG_FILE"
        exit 0
    fi
    echo "[$(date)] FAILED (attempt $i)" >> "$LOG_FILE"
    [ $i -lt $MAX_RETRIES ] && sleep $RETRY_DELAY
done
exit 1

# Usage in crontab:
# 0 * * * * /home/user/scripts/healer.sh price-check /usr/bin/python3 /home/user/check-prices.py
```

### Money-Making Workflows

1. **Scheduled Data Reports** — Client subscribes for hourly/daily market data (crypto, stocks, weather) emailed or posted
2. **Batch Invoice Processing** — Generate and email 100s of invoices via cron + API
3. **Uptime Monitoring** — Ping client sites every 5 min, alert on failure; white-label as service
4. **Content Queue Dispatch** — Cron triggers content posting across platforms at optimal times
5. **Database Maintenance** — Schedule vacuum, backup, archive jobs for client databases

---

## 2. IFTTT Maker (If-This-Then-That)

### Overview

IFTTT connects 800+ apps with simple trigger-action applets. No code needed. Use for lightweight personal automation or as a rapid prototyping layer while building the real pipeline in n8n.

### Trigger-Action Patterns

| Trigger | Action | Use Case |
|---|---|---|
| New email (Gmail) | Send Slack notification | Instant team alerts |
| Instagram post | Save to Google Drive | Automatic backup |
| Google Sheets row added | Send email | Form submission → alert |
| Weather forecast rain | Push notification | Umbrella reminder |
| RSS feed new item | Post to Twitter/X | Auto-curation |
| Webhook received (Maker) | Append to spreadsheet | Data collection |

### Money-Making with IFTTT

1. **Rapid Prototyping** — Build an automation for a client in 15 min; charge $50-$200 for setup
2. **Lead Capture Bridge** — IFTTT connects Typeform → Google Sheets → Slack; sell as "instant lead alert"
3. **Social Media Cross-Post** — One post to Instagram/Facebook → auto-crosspost to Twitter/LinkedIn
4. **SaaS Onboarding** — New Stripe subscription → add to Mailchimp → add to Slack channel; charge $100-$500
5. **Limitation** — IFTTT is brittle for production; use it to validate demand, then replace with n8n

```bash
# IFTTT Webhook trigger — curl from your server
curl -X POST "https://maker.ifttt.com/trigger/{event}/with/key/$IFTTT_KEY" \
  -H "Content-Type: application/json" \
  -d '{"value1": "New subscriber", "value2": "user@example.com", "value3": "premium-plan"}'
```

---

## 3. n8n Builder

### Overview

n8n is the leading open-source workflow automation tool (self-hosted). It provides 400+ nodes (integrations), visual drag-and-drop editor, and supports custom JS/Python code nodes. This is the **primary revenue generator** in this group.

### Quick Start — Docker Deployment

```bash
# Deploy n8n with PostgreSQL backend
docker run -d \
  --name n8n \
  --restart always \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  -e N8N_SECURE_COOKIE=false \
  -e DB_TYPE=postgresdb \
  -e DB_POSTGRESDB_DATABASE=n8n \
  -e DB_POSTGRESDB_HOST=localhost \
  n8nio/n8n

# Open http://localhost:5678
```

### Workflow-as-Code (JSON Export)

```json
{
  "name": "Lead Capture → Email → Slack → CRM",
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": { "path": "lead-capture" },
      "position": [250, 300]
    },
    {
      "name": "Format Email",
      "type": "n8n-nodes-base.code",
      "position": [450, 300],
      "parameters": {
        "language": "python",
        "code": "items[0].json.formatted = f\"New lead: {items[0].json.name} ({items[0].json.email})\""
      }
    },
    {
      "name": "Send Email",
      "type": "n8n-nodes-base.emailSend",
      "position": [650, 300]
    },
    {
      "name": "Slack Notification",
      "type": "n8n-nodes-base.slack",
      "position": [650, 500]
    }
  ],
  "connections": {
    "Webhook": { "main": [[ { "node": "Format Email" } ]] },
    "Format Email": { "main": [[ { "node": "Send Email" }, { "node": "Slack Notification" } ]] }
  }
}
```

### Money-Making Workflows

1. **Client Automation Packages** — $500-$2,000 to build and deploy a custom n8n workflow:
   - E-commerce: Shopify → Email → Inventory → Accounting
   - SaaS: Stripe → Mailchimp → Slack → CRM → Google Sheets
   - Content: RSS → AI Summarize → Social Posts → Analytics
2. **n8n Hosting Service** — Host n8n on your server + manage workflows: $100-$500/mo/client
3. **Templates Marketplace** — Sell pre-built workflow templates (Lead capture, Invoice bot, Review monitor): $20-$100 each
4. **Integration Middleware** — Connect two SaaS platforms that have no native integration ($300-$800)

```python
# n8n Code node — Python for complex logic
def process_order(order):
    import json

    # Calculate discount
    if order['total'] > 100:
        discount = order['total'] * 0.1
    elif order['total'] > 50:
        discount = order['total'] * 0.05
    else:
        discount = 0

    return {
        'order_id': order['id'],
        'customer': order['customer_email'],
        'original_total': order['total'],
        'discount': discount,
        'final_total': order['total'] - discount,
        'items': len(order['line_items'])
    }

# n8n passes `items` array — process each
results = [process_order(item.json) for item in items]
return results
```

---

## 4. Webhook Router

### Overview

A webhook router is a lightweight HTTP server that receives webhook payloads, validates signatures, routes to the correct handler, and returns acknowledgment. Essential middleware for any multi-SaaS integration.

### Quick Start — Express.js Webhook Router

```javascript
const express = require('express');
const crypto = require('crypto');
const app = express();

app.use(express.json());

// Webhook handler registry
const handlers = {
    stripe: async (event) => {
        if (event.type === 'checkout.session.completed') {
            await grantAccess(event.data.object.customer_email);
            await slackNotify(`New payment: ${event.data.object.amount_total}`);
        }
    },
    github: async (event) => {
        if (event.action === 'opened' && event.pull_request) {
            await autoAssignReviewer(event.pull_request.number);
        }
    },
    shopify: async (event) => {
        if (event.topic === 'orders/create') {
            await processOrder(event);
        }
    }
};

// Universal webhook endpoint
app.post('/webhook/:source', async (req, res) => {
    const { source } = req.params;
    const handler = handlers[source];

    if (!handler) {
        return res.status(404).json({ error: 'Unknown webhook source' });
    }

    // Signature verification
    const sig = req.headers['x-webhook-signature'];
    if (sig && !verifySignature(req.body, sig, process.env[`${source.toUpperCase()}_SECRET`])) {
        return res.status(401).json({ error: 'Invalid signature' });
    }

    try {
        await handler(req.body);
        res.status(200).json({ received: true });
    } catch (err) {
        console.error(`Webhook error [${source}]:`, err);
        // Store for retry
        await queueForRetry(source, req.body);
        res.status(202).json({ queued: true });
    }
});

app.listen(3000, () => console.log('Webhook router on :3000'));

// Signature verification — HMAC-SHA256
function verifySignature(payload, signature, secret) {
    const expected = crypto
        .createHmac('sha256', secret)
        .update(JSON.stringify(payload))
        .digest('hex');
    return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expected));
}
```

### Webhook Security Checklist

- [ ] Verify signature on every incoming webhook (HMAC-SHA256 or similar)
- [ ] Respond with 200/202 quickly; never block on downstream processing
- [ ] Queue payloads to Redis/SQS for async processing
- [ ] Log all webhooks with ID for debugging
- [ ] Rate-limit per source IP
- [ ] Rotate secrets quarterly
- [ ] Test with each provider's webhook tester tools

### Money-Making Workflows

1. **Integration Middleware Service** — $200-$500/mo to maintain webhook integrations for client
2. **One-Time Connectors** — $100-$300 to connect two systems that don't talk to each other
3. **Webhook Debugger/Logger** — Charge for webhook inspection dashboard
4. **Webhook Firewall** — Filter/monitor webhooks for security; $50-$200/mo

---

## 5. Zapier Alt (Self-Hosted)

### Overview

Zapier Alt = running **n8n** as a full Zapier replacement. Self-host means no per-task billing, no vendor lock-in, full data control. Most cost-effective for high-volume automation.

### Cost Comparison (Monthly)

| Volume (tasks/mo) | Zapier Pro | n8n Self-Hosted | Savings |
|---|---|---|---|
| 2,000 | $29 | ~$5 (server) | 83% |
| 10,000 | $99 | ~$10 (server) | 90% |
| 50,000 | $599 | ~$20 (server) | 97% |
| 200,000 | Custom ($2,000+) | ~$50 (server) | 97.5%+ |

### Deployment Architecture

```yaml
# docker-compose.yml — full-stack n8n deployment
version: '3.8'
services:
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_SECURE_COOKIE=false
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD=${DB_PASSWORD}
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      - postgres
    restart: always

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=n8n
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

  redis:
    image: redis:7-alpine
    restart: always

volumes:
  n8n_data:
  postgres_data:
```

### Money-Making Workflows

1. **Zapier Migration Service** — Migrate client from Zapier to self-hosted n8n: $500-$2,000/project
2. **n8n Managed Hosting** — Host + maintain + monitor client workflows: $100-$500/mo/client
3. **Template Library** — Sell recurring workflow templates (invoicing, CRM sync, email marketing)
4. **Enterprise On-Prem** — Deploy and customize for enterprise clients with compliance requirements ($2,000-$10,000)

---

## Build-in-Public Pipeline (The Real Money)

This is the meta-workflow: build ONE automation infrastructure, then productize it.

```python
# build_in_public.py — track every automation you ship
automations = []

def ship_automation(name, tools, hours, revenue):
    """Register a completed automation for showcase."""
    automations.append({
        "name": name,
        "tools": tools,  # ["cron", "n8n", "webhook"]
        "hours": hours,
        "revenue": revenue,
        "status": "active"
    })
    tweet_thread(name, hours, revenue)  # auto-build-in-public

# Example
ship_automation("Shopify→Sheets→Slack", ["n8n", "webhook"], 3, 200)
ship_automation("Daily Price Monitor", ["cron", "python"], 2, 150)
```

### Content Pipeline that Sells Itself

```
1. Build automation for yourself          (saves you $500/mo)
2. Tweet/blog about what you built        (attracts 5 leads)
3. First client pays you $500 to copy it  (you adapt in 1 hour)
4. Client testimonials → sell template    ($50 x 100 = $5,000)
5. Productize as managed service          ($200/mo x 50 = $10,000/mo)
```

---

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I can just use Zapier" | $600/mo vs $10/mo self-hosted; vendor lock-in at scale |
| "I'll build it when I need it" | The first automation saves 10+ hours/week; build it before you need it |
| "Clients don't know what n8n is" | They don't need to; they want results (auto-invoicing, lead alerts) |
| "I'll host it locally" | $10/mo VPS runs everything; scale is elastic |
| "Cron is good enough" | Cron is the foundation; n8n adds error handling, retry, notifications, and UI |
| "Webhooks are scary" | One Express endpoint handles all providers; signature verification is 5 lines |

---

## First Action in 60 Minutes

1. **Deploy n8n** — `docker run -d --name n8n -p 5678:5678 n8nio/n8n` (2 min)
2. **Create first workflow** — Webhook → Slack → Email (5 min)
3. **Set up cron for one daily job** — Price check or report generation (5 min)
4. **Build webhook router** — Express.js, 30 lines, handles Stripe + GitHub (15 min)
5. **Connect to Zapier alt** — Migrate one Zapier task to n8n (10 min)
6. **Document build** — Screenshot + tweet = first build-in-public post (5 min)
7. **Day 2** — Productize the workflow as a $200 package
8. **Week 2** — Client #1: deploy + adapt = $500
9. **Month 1** — 5 clients on managed n8n hosting = $1,000/mo MRR

---

## Verification

- [ ] n8n instance is accessible and workflows run end-to-end
- [ ] Cron jobs execute on schedule with logging and retry
- [ ] Webhook router accepts POSTs, verifies signatures, returns 200
- [ ] Zapier alt migration test: same task runs cheaper on n8n
- [ ] Error handling tested: retry on failure, Slack alert on fatal
- [ ] At least one build-in-public post drafted/scheduled
- [ ] Cost comparison (Zapier vs self-hosted) documented
- [ ] Template workflow exported as JSON and stored


## When to Use
Use this skill when working with workflows.
