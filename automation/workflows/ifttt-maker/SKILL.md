---
name: ifttt-maker
description: Use when iFTTT-style trigger-action automations for connecting apps and services. See parent skill for full docs.
domain: automation
tags:
- automation
- ifttt
- triggers
- workflows
version: 1.0.0
---
# IFTTT Maker

## Quick Reference

IFTTT (If This Then That) connects 800+ apps with simple trigger-action applets — no code required. This skill covers the **Maker Webhooks** integration (programmatic triggers from your own code) and rapid prototyping patterns. Unlike the parent workflows skill (which covers n8n and cron), IFTTT is for zero-code, single-condition automations where speed beats depth.

## Overview

IFTTT is the fastest way to prototype an automation: pick a trigger (Gmail email received), pick an action (Slack notification), go live in 60 seconds. The Maker Webhooks channel lets your own scripts fire triggers — a server-side event becomes an IFTTT applet. Use IFTTT for personal automations and rapid validation, then graduate to n8n when you need branching logic, retries, or multi-step pipelines. The money is in rapid prototyping for clients ($50-200/setup) where the automation is simple enough that an applet suffices.

## Quick Start

**Prerequisites:** Free IFTTT account, IFTTT app installed, Maker Webhooks service connected.

1. **Create an applet** — IFTTT.com → Create → "If This" → choose a trigger service (Gmail, RSS, Weather, Webhooks). Then "Then That" → choose an action service (Slack, Google Sheets, Email).

2. **Get your Maker key** — Go to Webhooks service → Settings → Documentation. Your API key is in the URL: `https://maker.ifttt.com/use/{YOUR_KEY}`. Copy it; you'll use it to fire events programmatically.

3. **Fire a webhook event** — From any script, curl the Maker endpoint. IFTTT runs the linked action within seconds.

```bash
# Fire an IFTTT event from your server
EVENT="new_lead"
KEY="your-maker-key-here"

curl -X POST "https://maker.ifttt.com/trigger/${EVENT}/with/key/${KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "value1": "John Doe",
    "value2": "john@example.com",
    "value3": "Premium Plan"
  }'
```

Then in IFTTT, set up an applet: Webhook trigger (`new_lead`) → Google Sheets action (append row). Every time your script fires the webhook, a new row appears in your sheet. For Slack alerts, change the action to Slack → Send Message using `{{Value1}}`, `{{Value2}}`, `{{Value3}}` as template variables.

## Checklist

- [ ] Maker Webhook tested end-to-end: curl the event, verify the action executed within 60 seconds
- [ ] Applet uses the free tier — each applet is limited to ~100 runs/month; for production volume, migrate to n8n
- [ ] IFTTT failure notifications enabled — ifttt sends email when an applet fails; forward to Telegram/Slack
- [ ] Value fields templated correctly in the action — `{{Value1}}`, `{{Value2}}`, `{{Value3}}` correspond to the three JSON fields
- [ ] Applet validated with real data before handing to a client — IFTTT has no test mode, so use a test spreadsheet/channel first

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "IFTTT is too limited for real automation" | 90% of personal automations are single-trigger, single-action; IFTTT solves those in 2 minutes vs 30 minutes in n8n |
| "I'll build it myself in Python" | You'll spend 3 hours wiring API auth, error handling, and scheduling for what an IFTTT applet does in 60 seconds |
| "Clients want custom solutions" | Client onboarding often needs simple lead alerts (Typeform→Sheets→Slack); IFTTT delivers that today, n8n replaces it next month |

## When to Use
Use this skill when working with ifttt maker.

## Workflow
See the parent skill for authoritative workflow documentation.
