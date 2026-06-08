---
name: kalodata-integrations
description: Multi-platform integrations for Kalodata research. Connect Shopify for
  product listings, Notion for research reports, and Slack for alerts + daily digests.
  CLI-friendly with config-based API key management.
metadata:
  model: sonnet
domain: integrations
---

# Kalodata Integrations Skill

Multi-platform connections for Kalodata research automation.

## Overview

Enables multi-platform integrations for Kalodata research automation, connecting Shopify for product listings, Notion for research reports, and Slack for alerts and daily digests. Provides CLI-friendly configuration management with secure API key handling.

## When to Use

- User wants to create Shopify product listings from TikTok Shop research
- User needs to save research reports to Notion databases
- User wants Slack alerts for new products and daily digests
- User prefers CLI-based integration management
- User needs secure API key configuration (not hardcoded)

## The Process

1. **Set up configuration** – Create `.kalodata-integrations` config directory with credentials
2. **Choose platform to integrate** – Select from Shopify, Notion, or Slack
3. **Implement integration** – Use the core integration patterns
4. **Test and deploy** – Verify connection and automate workflows

## How to Use

1. Obtain Kalodata API credentials from the dashboard
2. Configure authentication headers for API requests
3. Use the product research endpoints to fetch trending data
4. Export findings to your analytics pipeline

## API Integration

```python
import requests

KALODATA_API = "https://api.kalodata.com/v1"
headers = {"Authorization": f"Bearer {KALODATA_TOKEN}"}

resp = requests.get(f"{KALODATA_API}/products/trending", headers=headers)
products = resp.json()["data"]

import csv
with open("trending.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "category", "revenue"])
    writer.writeheader()
    writer.writerows(products)
```

## Common Patterns

- Cache API responses to reduce rate limit pressure
- Use pagination for large result sets
- Filter by category and date range for relevant results
- Schedule regular data pulls for trend analysis

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- Hardcoding API keys in source code (always use config files or environment variables)
- Integrating unrelated platforms (stick to Shopify, Notion, Slack as designed)
- Expecting real-time synchronization (this is batch-oriented, not streaming)
- Using this skill for basic research without integration needs

## Verification

- Config file loads successfully without errors
- Platform connections establish (test Shopify, Notion, Slack separately)
- Product listings create successfully in Shopify admin
- Research reports appear in Notion database as expected
- Slack alerts appear in configured channel without failures
