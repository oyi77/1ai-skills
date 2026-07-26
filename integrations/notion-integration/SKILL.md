---
name: notion-integration
description: Use when notion Automation Hub — API, Database, and Page management for knowledge bases, project trackers, and content systems. Monetize through workspace automation-as-a-service.
domain: integrations
tags:
- api
- automation
- integrations
- notion
- third-party
- workflow
- notion-api
- notion-db
- notion-pages
- knowledge-management
---

# Notion Automation Hub

## Money-Making Overview

Notion is the go-to workspace for thousands of companies running on the "build it yourself" model. They hit scaling pain and pay for automation:

| Service | ROI Estimate | Market |
|---------|-------------|--------|
| Workspace migration & setup | $2K-$8K/project | SaaS teams, startups migrating from Google Drive/Confluence |
| CRM automation (sync Stripe/HubSpot → Notion DB) | $1K-$4K/mo retainer | Sales teams doing pipeline tracking |
| Automated report generation | $500-$2K/mo | Agencies, VCs, e-commerce tracking |
| Content publishing pipeline | $1K-$3K/setup | Blogs, newsletters, documentation sites |
| Custom Notion API integration | $3K-$15K/project | Mid-market needing Jira/GitHub ↔ Notion sync |
| Database schema design & migration | $500-$3K/hour consult | Growing teams outgrowing their initial Notion setup |

**Combined monthly recurring potential: $3K-$10K/client** (as workspace automation retainer).

### Who Pays
- **Startups ($15-50 employees)** — need structured CRM/PM but no engineering time ($800-2K/mo)
- **VC/PE firms** — portfolio tracking dashboards ($2-5K/setup)
- **Content creators** — editorial calendar + publishing automation ($300-1K/mo)
- **Agencies** — white-label Notion setup for client onboarding ($1-3K markup)
- **B2B SaaS** — customer-facing Notion portals (pricing, changelog, docs) ($3-8K)

## Combined Capabilities

| Capability | Scope | Output |
|-----------|-------|--------|
| **Notion API** | Full CRUD via REST API, database queries, filtering, sorting, OAuth integration, webhook listeners | Python/curl scripts, automation workflows |
| **Notion Database** | Schema management, query/filter/sort, relation & rollup, formula validation, bulk import/export, views | Python scripts, migration tools, schema blueprints |
| **Notion Pages** | Create, read, update, append blocks, embed content, manage hierarchy, templates, archive/restore | Content generators, publishing pipelines |

## Authentication & Setup

```bash
# Notion Integration Token — create at https://www.notion.so/my-integrations
export NOTION_TOKEN="secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Share target database/page with your integration
# → Open the page → Share → Invite your integration by name
```

```python
import os, requests

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}
API = "https://api.notion.com/v1"
```

Rate limits: 3 requests/second per integration. Requests beyond are queued (not dropped) up to a burst of 30. Batch operations by sleeping ~350ms between calls.

## Concrete Action Flows

### Flow 1: Database Query with Filters

Query a Notion database with complex filters — the core building block for any automation:

```python
#!/usr/bin/env python3
"""Query a Notion database with multi-filter support."""
import os, json, requests, time

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def query_db(db_id, filter_obj=None, sorts=None, page_size=100):
    """Query a database with optional filter and sort. Handles pagination."""
    url = f"https://api.notion.com/v1/databases/{db_id}/query"
    payload = {"page_size": min(page_size, 100)}
    if filter_obj:
        payload["filter"] = filter_obj
    if sorts:
        payload["sorts"] = sorts

    results = []
    has_more = True
    cursor = None

    while has_more:
        if cursor:
            payload["start_cursor"] = cursor
        resp = requests.post(url, headers=HEADERS, json=payload)
        resp.raise_for_status()
        data = resp.json()
        results.extend(data["results"])
        has_more = data["has_more"]
        cursor = data.get("next_cursor")
        time.sleep(0.35)  # rate limit

    return results

def extract_properties(page):
    """Extract page properties into a flat dict."""
    props = {}
    for name, value in page.get("properties", {}).items():
        ptype = value.get("type", "unknown")
        content = value.get(ptype, {})
        if ptype == "title":
            props[name] = "".join(t.get("plain_text", "") for t in content)
        elif ptype == "rich_text":
            props[name] = "".join(t.get("plain_text", "") for t in content)
        elif ptype == "select":
            props[name] = content.get("name") if content else None
        elif ptype == "multi_select":
            props[name] = [opt.get("name") for opt in content] if content else []
        elif ptype == "date":
            props[name] = content.get("start") if content else None
        elif ptype == "number":
            props[name] = content
        elif ptype == "checkbox":
            props[name] = content
        elif ptype == "status":
            props[name] = content.get("name") if content else None
        elif ptype == "email":
            props[name] = content
        elif ptype == "url":
            props[name] = content
        else:
            props[name] = str(content)
    return props

# Example: Find all tasks with status "In Progress" assigned to "Alice"
results = query_db(
    "YOUR_DATABASE_ID",
    filter_obj={
        "and": [
            {"property": "Status", "status": {"equals": "In Progress"}},
            {"property": "Assignee", "rich_text": {"contains": "Alice"}},
        ]
    },
    sorts=[{"property": "Priority", "direction": "descending"}],
)

for page in results:
    props = extract_properties(page)
    print(f"  Task: {props.get('Task Name', '?')}")
    print(f"  Priority: {props.get('Priority', '?')}")
    print(f"---")
```

### Flow 2: Create Pages from External Data (CRM Sync)

Sync Stripe customers into a Notion CRM database:

```python
#!/usr/bin/env python3
"""Sync Stripe customer data into a Notion CRM database."""
import os, requests, time

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def create_database_page(db_id, properties, children=None):
    url = f"https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": db_id},
        "properties": properties,
    }
    if children:
        payload["children"] = children
    resp = requests.post(url, headers=HEADERS, json=payload)
    resp.raise_for_status()
    return resp.json()

def update_page(page_id, properties):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    resp = requests.patch(url, headers=HEADERS, json={"properties": properties})
    resp.raise_for_status()
    return resp.json()

# Example: Create a CRM entry from external data
def sync_customer_to_notion(db_id, customer):
    """Sync a customer object into Notion CRM database."""
    properties = {
        "Name": {"title": [{"text": {"content": customer["name"]}}]},
        "Email": {"email": customer["email"]},
        "Plan": {"select": {"name": customer["plan_name"]}},
        "MRR": {"number": customer["mrr_cents"] / 100},
        "Status": {"status": {"name": customer["status"]}},
        "Created": {"date": {"start": customer["created_at"]}},
    }
    page = create_database_page(db_id, properties, children=[
        {"object": "block", "type": "heading_2", "heading_2": {
            "rich_text": [{"text": {"content": "Notes"}}]
        }},
        {"object": "block", "type": "paragraph", "paragraph": {
            "rich_text": [{"text": {"content": customer.get("notes", "")}}]
        }},
    ])
    print(f"Created page: {page['url']}")
    return page

# Example batch sync
customers = [
    {"name": "Acme Inc", "email": "billing@acme.com", "plan_name": "Pro",
     "mrr_cents": 29900, "status": "Active", "created_at": "2025-01-15"},
    {"name": "Beta Corp", "email": "finance@beta.co", "plan_name": "Enterprise",
     "mrr_cents": 99900, "status": "Active", "created_at": "2025-03-01"},
]
for c in customers:
    sync_customer_to_notion("YOUR_DB_ID", c)
    time.sleep(0.35)
```

### Flow 3: Database Schema Management

Create a new database with typed columns — useful for migrations:

```python
#!/usr/bin/env python3
"""Create and configure Notion databases programmatically."""
import os, requests, json

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def create_database(parent_page_id, title, properties):
    """Create a database inside a parent page."""
    url = "https://api.notion.com/v1/databases"
    payload = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": title}}],
        "properties": properties,
    }
    resp = requests.post(url, headers=HEADERS, json=payload)
    resp.raise_for_status()
    return resp.json()

def update_database(db_id, properties):
    """Update database schema properties."""
    url = f"https://api.notion.com/v1/databases/{db_id}"
    resp = requests.patch(url, headers=HEADERS, json={"properties": properties})
    resp.raise_for_status()
    return resp.json()

# Example: Create a Project Tracker database
project_db = create_database(
    parent_page_id="YOUR_PAGE_ID",
    title="Project Tracker",
    properties={
        "Project Name": {"title": {}},
        "Status": {"status": {}},
        "Priority": {
            "select": {
                "options": [
                    {"name": "Urgent", "color": "red"},
                    {"name": "High", "color": "orange"},
                    {"name": "Medium", "color": "yellow"},
                    {"name": "Low", "color": "green"},
                ]
            }
        },
        "Deadline": {"date": {}},
        "Owner": {"rich_text": {}},
        "Budget": {"number": {"format": "dollar"}},
        "Tags": {"multi_select": {}},
        "Client": {"rich_text": {}},
        "Progress": {"number": {"format": "percent"}},
    }
)

print(f"Created database: {project_db['url']}")
```

### Flow 4: Automated Report Generator

Generate a weekly report by aggregating database data:

```bash
#!/usr/bin/env bash
# weekly-report.sh — Generate Notion-based weekly report
set -euo pipefail

NOTION_TOKEN="${1?Usage: $0 <token> <db_id>}"
DB_ID="${2}"

# Query for tasks completed this week
RESP=$(curl -s -X POST "https://api.notion.com/v1/databases/$DB_ID/query" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "property": "Completed",
      "date": {
        "this_week": {}
      }
    }
  }')

echo "$RESP" | jq -r '
  "=== Weekly Report ===",
  ("Total completed: " + (.results | length | tostring)),
  "",
  "Tasks:",
  (.results[] | "- " + (.properties["Task Name"].title[0].text.content // "?"))
'
```

### Flow 5: Content Publishing Pipeline

Schedule blog posts by setting a "Publish Date" field and running a checker:

```python
#!/usr/bin/env python3
"""content-pipeline.py — Auto-publish content when publish date arrives."""
import os, requests, datetime, time

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
}

DB_ID = "YOUR_CONTENT_CALENDAR_DB_ID"

# Query pages where Publish = today and Status = "Ready"
today = datetime.date.today().isoformat()
results = query_db(DB_ID, filter_obj={
    "and": [
        {"property": "Publish Date", "date": {"equals": today}},
        {"property": "Status", "status": {"equals": "Ready"}},
    ]
})

for page in results:
    props = extract_properties(page)
    title = props.get("Title", "Untitled")
    content = props.get("Content", "")

    # Publish to your platform (e.g., write to local markdown)
    slug = title.lower().replace(" ", "-").replace("?", "").replace("/", "-")
    with open(f"_posts/{today}-{slug}.md", "w") as f:
        f.write(f"---\ntitle: {title}\ndate: {today}\n---\n\n{content}\n")

    # Mark as published in Notion
    update_page(page["id"], {
        "Status": {"status": {"name": "Published"}},
        "Published URL": {"url": f"https://yoursite.com/{slug}"},
    })
    print(f"Published: {title}")

# Also: find overdue items
overdue = query_db(DB_ID, filter_obj={
    "and": [
        {"property": "Publish Date", "date": {"before": today}},
        {"property": "Status", "status": {"does_not_equal": "Published"}},
    ]
})
for p in overdue:
    props = extract_properties(p)
    print(f"OVERDUE: {props.get('Title', '?')} (due: {props.get('Publish Date', '?')})")
```

### Flow 6: Bulk Archive/Delete

Clean up stale pages:

```python
#!/usr/bin/env python3
"""Archive pages matching a filter (Notion = move to trash)."""
import os, requests, time

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
}

def archive_page(page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    resp = requests.patch(url, headers=HEADERS, json={"archived": True})
    resp.raise_for_status()
    return resp.json()

# Archive completed tasks older than 90 days
old_tasks = query_db("YOUR_DB_ID", filter_obj={
    "and": [
        {"property": "Status", "status": {"equals": "Done"}},
        {"property": "Completed Date", "date": {"before": "2025-04-16"}},
    ]
})
for t in old_tasks:
    archive_page(t["id"])
    print(f"Archived: {extract_properties(t).get('Task Name', '?')}")
    time.sleep(0.35)
```

## First Action in 60 Minutes

```
00:00-05:00 — Go to https://www.notion.so/my-integrations and create an integration
05:00-08:00 — Copy the integration token and store as NOTION_TOKEN
08:00-12:00 — Create a test database in Notion with 3+ columns (Name, Status, Priority)
12:00-15:00 — Share the database with your integration (Share → Invite)
15:00-25:00 — Run query_db.py to fetch all rows — verify it works
25:00-35:00 — Create a new row via the API — verify it appears in Notion
35:00-45:00 — Set up a Stripe → Notion CRM sync script
45:00-55:00 — Run the pipeline and push a test customer
55:00-60:00 — Add a weekly report cron (crontab -e) and set up content pipeline
```

**By the end of 60 minutes:**
- Notion integration authenticated and functional
- Database query/filter/create/update working
- CRM sync script ready for client onboarding
- Weekly report automation scheduled
- Content publishing pipeline validated
- Reusable deliverables to sell as workspace automation

## Anti-Rationalization Table

| Rationalization | Reality |
|---------------|---------|
| "I can just manually update Notion" | Manual entry doesn't scale past 20 records. Automate creation and updates from day one. |
| "Database schema can be fixed later" | Notion has no migration tools. Changing property types after data is entered requires rebuilding. Design upfront. |
| "Rate limits are high enough" | At 3 req/s, bulk imports of 5000+ records take 25+ minutes. Build batching into every sync. |
| "Relations are optional" | Without relations, you get duplicated data and sync hell. Normalize early. |
| "The API is just read-only" | Full CRUD + block manipulation + comments + search. You can build a mini-app entirely in Notion. |
| "No one pays for Notion setup" | Companies with 50+ employees pay $500-2K/mo for workspace optimization. It's a recurring need. |

## Output Format

```
notion-automation/
├── auth.py                 # Shared auth helpers
├── query_db.py             # Database query with filter/sort/pagination
├── create_page.py          # Page creation with rich content
├── sync_crm.py             # External data → Notion CRM sync
├── content-pipeline.py     # Scheduled publishing automation
├── archive.py              # Bulk archive/cleanup
└── weekly-report.sh        # Shell-based report generator
```

## Verification Checklist

- [ ] Integration token works for database query (scope validated)
- [ ] Database CRUD: query, create, update, archive all functional
- [ ] Multi-filter queries return correct subset (and, or, compound)
- [ ] Pagination works for databases with >100 records
- [ ] Rate limiting respected — sleep between sequential calls
- [ ] Property extraction handles all types (title, rich_text, select, date, number, etc.)
- [ ] External sync: data flows correctly from source → Notion
- [ ] Content pipeline: pages with today's publish date get processed
- [ ] Archive: pages move to trash without exceptions
- [ ] Schema creation: database is created with correct property types and options
- [ ] Error handling: clear messages on bad tokens, invalid DB IDs, rate limit hits
- [ ] Money protocol: deliverable is packaged and billable


## When to Use
Use this skill when working with notion.


## Workflow
See the parent skill for authoritative workflow documentation.
