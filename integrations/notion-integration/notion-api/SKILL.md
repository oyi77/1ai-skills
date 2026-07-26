---
name: notion-api
description: Use when notion API — Full CRUD via REST, database queries, filtering, sorting, OAuth integration. See parent skill for all Notion automation capabilities.
domain: integrations
tags:
- api
- integrations
- notion
version: 1.0.0
---

# Notion API

## Quick Reference

The Notion API sub-skill covers direct REST API interactions — authentication, CRUD on pages and databases, query filters and sorts, search, block manipulation, and OAuth integration for multi-user apps. This layers on the parent [Notion Automation Hub](../SKILL.md) which covers the full API+Database+Page ecosystem and money-making protocols.

**Use this when** you need to read or write Notion data programmatically — syncing external data, building integrations, or automating workflows.

## Overview

The Notion REST API (`https://api.notion.com/v1/`) provides full programmatic access to pages, databases, blocks, users, and search. Unlike the database sub-skill (schema-focused) and pages sub-skill (content-focused), the API sub-skill covers the raw HTTP layer: authentication, error handling, pagination, rate limiting, and endpoint reference.

Key patterns:
- **Integration token** (Internal) — single-workspace, simplest, use for automation scripts
- **OAuth 2.0** (Public) — multi-user, needed for apps installed by multiple workspaces
- **Pagination** — cursor-based via `start_cursor` / `has_more` / `next_cursor`
- **Rate limiting** — 3 requests/second per integration (burst up to 30, then queued)

The parent skill's `query_db.py`, `create_page.py`, `sync_crm.py`, and `content-pipeline.py` are the canonical templates.

## Quick Start

### 1. Get an Integration Token
```bash
# Go to https://www.notion.so/my-integrations → New Integration
export NOTION_TOKEN="secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# Share target page/database: Open in Notion → Share → Invite your integration
```

### 2. Query a Database
```bash
curl -X POST "https://api.notion.com/v1/databases/DB_ID/query" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {"property": "Status", "status": {"equals": "In Progress"}},
    "sorts": [{"property": "Priority", "direction": "descending"}]
  }'
```

### 3. Create a Page
```python
import os, requests

resp = requests.post("https://api.notion.com/v1/pages",
    headers={
        "Authorization": f"Bearer {os.environ['NOTION_TOKEN']}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    },
    json={
        "parent": {"database_id": "YOUR_DB_ID"},
        "properties": {
            "Name": {"title": [{"text": {"content": "New Task"}}]},
            "Status": {"status": {"name": "To Do"}},
            "Priority": {"select": {"name": "High"}},
        },
    })
resp.raise_for_status()
print(f"Created: {resp.json()['url']}")
```

## Code Snippet: Search All Accessible Content

```python
import os, requests, time

TOKEN, HEADERS = os.environ["NOTION_TOKEN"], {
    "Authorization": f"Bearer {os.environ['NOTION_TOKEN']}",
    "Notion-Version": "2022-06-28",
}

def search_notion(query, page_size=50):
    """Search pages, databases, and blocks across the workspace."""
    results, cursor = [], None
    while True:
        payload = {"query": query, "page_size": page_size}
        if cursor:
            payload["start_cursor"] = cursor
        resp = requests.post("https://api.notion.com/v1/search",
            headers=HEADERS, json=payload)
        resp.raise_for_status()
        data = resp.json()
        results.extend(data["results"])
        if not data["has_more"]:
            break
        cursor = data["next_cursor"]
        time.sleep(0.35)
    return results

# Find everything referencing "Q4 Planning"
hits = search_notion("Q4 Planning")
for h in hits:
    obj_type = h["object"]  # "page" or "database"
    title = h.get("title", [{}])[0].get("plain_text",
            h.get("properties", {}).get("title", {}).get("title", [{}])[0].get("plain_text", "?"))
    print(f"[{obj_type}] {title} → {h['url']}")
```

## Verification Checklist

- [ ] Integration token scoped to correct workspace (cannot cross workspaces)
- [ ] Target page/database shared with the integration (Share menu → Invite)
- [ ] Pagination handled with cursor loop, not fixed limit
- [ ] Rate limit respected: 350ms+ sleep between sequential requests
- [ ] Error handling for 400 (bad request), 404 (not shared), 429 (rate limit), 401 (bad token)

## When to Use

Use when notion API — Full CRUD via REST, database queries, filtering, sorting, OAuth integration. See parent skill for all Notion automation capabilities.

## Workflow

Execute these steps sequentially:

### 1. Get an Integration Token
```bash
# Go to https://www.notion.so/my-integrations → New Integration
export NOTION_TOKEN="secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# Share target page/database: Open in Notion → Share → Invite your integration
```

### 2. Query a Database
```bash
curl -X POST "https://api.notion.com/v1/databases/DB_ID/query" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {"property": "Status", "status": {"equals": "In Progress"}},
    "sorts": [{"property": "Priority", "direction": "descending"}]
  }'
```

### 3. Create a Page
```python
import os, requests

resp = requests.post("https://api.notion.com/v1/pages",
    headers={
        "Authorization": f"Bearer {os.environ['NOTION_TOKEN']}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    },
    json={
        "parent": {"database_id": "YOUR_DB_ID"},
        "properties": {
            "Name": {"title": [{"text": {"content": "New Task"}}]},
            "Status": {"status": {"name": "To Do"}},
            "Priority": {"select": {"name": "High"}},
        },
    })
resp.raise_for_status()
print(f"Created: {resp.json()['url']}")
```

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll use the official SDK instead of raw HTTP" | The SDK is convenient but can mask rate limits and pagination. Understanding the raw API is essential for debugging production integrations. |
| "Notion tokens never expire" | Integration tokens are permanent, but OAuth tokens expire. If building for multiple workspaces, implement OAuth refresh token rotation. |
| "I can query without sharing the database" | The API will return 404 for any database/page not explicitly shared with the integration. Always share after creating the token. |
