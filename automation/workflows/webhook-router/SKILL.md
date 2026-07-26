---
name: webhook-router
description: Use when lightweight HTTP server for receiving, validating, and routing webhooks. See parent skill for full docs.
domain: automation
tags:
- automation
- webhook
- router
- api
version: 1.0.0
---
# Webhook Router

## Quick Reference

A webhook router is a lightweight HTTP server that receives incoming webhooks from SaaS platforms (Stripe, GitHub, Shopify), validates their signatures, routes to platform-specific handlers, and returns a quick 200. Unlike the parent workflows skill (which covers cron scheduling and n8n), this skill focuses on the **HTTP middleware layer** — connecting external event sources to your automation pipeline with signature verification as the non-negotiable first step.

## Overview

Every platform sends webhooks differently — different headers, different signature algorithms (HMAC-SHA256 for Stripe, `X-Hub-Signature-256` for GitHub, RSA for Shopify). A webhook router normalizes them all behind `POST /webhook/:source`. The critical job is signature verification: without it, anyone can POST fake events to your server. After verification, the handler queues the event for async processing (via cron or n8n from the parent skill) and returns 200 immediately — the router never blocks on downstream logic.

## Quick Start

**Prerequisites:** Node.js 18+ or Python 3.9+, a public URL (ngrok for testing, Cloudflare Tunnel for production).

1. **Create the router** — One endpoint dispatches to platform handlers via `req.params.source`.

2. **Add verification** — Implement HMAC-SHA256 verification per platform; reject unverifiable payloads with 401.

3. **Deploy** — `ngrok http 3000` for dev, then set webhook URLs to `https://you.ngrok.io/webhook/stripe`.

```python
# webhook_router.py — FastAPI
from fastapi import FastAPI, Request, HTTPException
import hmac, hashlib, json

app = FastAPI()
SECRETS = {"stripe": "whsec_...", "github": "gh_secret..."}
HANDLERS = {}

def handler(src):
    def wrap(fn): HANDLERS[src] = fn; return fn
    return wrap

@handler("stripe")
async def on_stripe(event):
    if event["type"] == "checkout.session.completed":
        print(f"New customer: {event['data']['object']['customer_email']}")

@handler("github")
async def on_github(event):
    if event.get("action") == "opened":
        print(f"PR #{event['pull_request']['number']}")

@app.post("/webhook/{source}")
async def webhook(request: Request, source: str):
    body = await request.body()
    sig = request.headers.get("X-Hub-Signature-256") or request.headers.get("Stripe-Signature") or ""
    expected = "sha256=" + hmac.new(SECRETS.get(source, "").encode(), body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(sig, expected):
        raise HTTPException(401, "Invalid signature")
    await HANDLERS[source](json.loads(body))
    return {"ok": True}
```

## Checklist

- [ ] Signature verification implemented and tested with each platform's webhook tester before going live
- [ ] Idempotency checked via `Idempotency-Key` header or `event.id` to prevent double-processing on retries
- [ ] Response sent within 3 seconds (most platforms timeout at 5-10s); use a queue for slow handlers
- [ ] Webhooks logged with timestamp, source, event type, and outcome for debugging
- [ ] Rate limiter per source IP to prevent replay/DOS attacks (e.g., 100 req/min per source)

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll handle webhooks inline in my app" | Coupling webhook handling to your app's routes ties event uptime to app uptime; a separate router keeps both resilient |
| "Signature verification is optional" | Without it, anyone can forge events; a single forged `invoice.payment_failed` can trigger false billing |
| "Express is fine for production webhooks" | Express blocks on large JSON payloads; pin `body-parser` limits or switch to streaming for platforms with multi-MB payloads |

## When to Use
Use this skill when working with webhook router.

## Workflow
See the parent skill for authoritative workflow documentation.
