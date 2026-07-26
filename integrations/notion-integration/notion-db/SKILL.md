---
name: notion-db
description: Use when notion Database — Schema management, query/filter/sort, relations, rollups, formula validation, bulk import/export. See parent skill for all Notion automation capabilities.
domain: integrations
tags:
- api
- database
- integrations
- notion
version: 1.0.0
---

# Notion Database

## Quick Reference

The Notion Database sub-skill covers schema-first interactions — creating and modifying database schemas, defining property types (select, multi-select, date, number, formula, relation, rollup), building compound filters, managing relations between databases, validating formula syntax, and bulk import/export. This layers on the parent [Notion Automation Hub](../SKILL.md) which covers the full API+Database+Page ecosystem and money-making protocols.

**Use this when** you need to design, migrate, or manipulate Notion database structures — not just individual pages.

## Overview

Notion databases are the backbone of structured workspaces. Unlike flat APIs, they have rich property types, relation chains, rollup aggregations, and formula evaluations that behave like a lightweight spreadsheet-database hybrid. Key concepts:
- **Property types** — title, rich_text, number, select, multi_select, status, date, email, phone, url, checkbox, files, formula, relation, rollup, people, created_time, last_edited_time, created_by, last_edited_by
- **Relations** — link databases together (one-to-one, one-to-many, many-to-many via junction)
- **Rollups** — aggregate values from related database rows (sum, count, average, etc.)
- **Formulas** — spreadsheet-like expressions referencing other properties
- **Views** — filtered/sorted/grouped presentations of the same data (table, board, gallery, list, calendar)

The parent skill's `create_database()` flow, CRM sync, and content pipeline scripts are the canonical templates.

## Quick Start

### 1. Create a Database with a Schema
```python
import os, requests
resp = requests.post("https://api.notion.com/v1/databases",
    headers={"Authorization": f"Bearer {os.environ['NOTION_TOKEN']}",
             "Notion-Version": "2022-06-28"},
    json={
        "parent": {"type": "page_id", "page_id": "PARENT_PAGE_ID"},
        "title": [{"type": "text", "text": {"content": "Project Tracker"}}],
        "properties": {
            "Project Name": {"title": {}},
            "Status": {"status": {}},
            "Priority": {"select": {"options": [
                {"name": "Urgent", "color": "red"},
                {"name": "High", "color": "orange"},
                {"name": "Medium", "color": "yellow"},
                {"name": "Low", "color": "green"},
            ]}},
            "Deadline": {"date": {}},
            "Budget": {"number": {"format": "dollar"}},
        },
    })
print(f"Created: {resp.json()['url']}")
```

### 2. Query with Compound Filters
```python
# AND filter: Status=In Progress AND Priority≥High
filter_obj = {
    "and": [
        {"property": "Status", "status": {"equals": "In Progress"}},
        {"property": "Priority", "select": {"in": ["Urgent", "High"]}},
    ]
}
# See parent skill for the full query_db() function with pagination
```

### 3. Add a Relation and Rollup
```python
update_schema = {
    "Related Tasks": {
        "relation": {
            "database_id": "TARGET_DB_ID",
            "type": "single_property",
            "single_property": {}
        }
    },
    "Task Count": {
        "rollup": {
            "relation_property_name": "Related Tasks",
            "rollup_property_name": "Status",
            "function": "count"
        }
    }
}
```

## Code Snippet: Export Database Schema

```python
#!/usr/bin/env python3
"""Dump a database's schema as a portable blueprint."""
import os, requests, json

TOKEN = os.environ["NOTION_TOKEN"]
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Notion-Version": "2022-06-28"}

def export_schema(db_id):
    resp = requests.get(f"https://api.notion.com/v1/databases/{db_id}", headers=HEADERS)
    resp.raise_for_status()
    db = resp.json()
    blueprint = {
        "title": "".join(t["plain_text"] for t in db.get("title", [])),
        "properties": {},
    }
    for name, prop in db.get("properties", {}).items():
        ptype = prop["type"]
        entry = {"type": ptype}
        if ptype == "select":
            entry["options"] = [o["name"] for o in prop.get("select", {}).get("options", [])]
        elif ptype == "relation":
            entry["database_id"] = prop["relation"]["database_id"]
        elif ptype == "rollup":
            entry["function"] = prop["rollup"]["function"]
        blueprint["properties"][name] = entry
    return blueprint

blueprint = export_schema("YOUR_DB_ID")
print(json.dumps(blueprint, indent=2))
# Use this to migrate schemas or document for clients
```

## Verification Checklist

- [ ] All property types render correctly (no silent fallback to `rich_text`)
- [ ] Select/multi-select options are predefined with correct colors and order
- [ ] Relation points to an existing database shared with the integration
- [ ] Rollup function matches the target property type (count for status, sum for number)
- [ ] Formula syntax is valid (Notion rejects malformed formulas silently — test with a single page first)

## When to Use

Use when notion Database — Schema management, query/filter/sort, relations, rollups, formula validation, bulk import/export. See parent skill for all Notion automation capabilities.

## Workflow

Execute these steps sequentially:

### 1. Create a Database with a Schema
```python
import os, requests
resp = requests.post("https://api.notion.com/v1/databases",
    headers={"Authorization": f"Bearer {os.environ['NOTION_TOKEN']}",
             "Notion-Version": "2022-06-28"},
    json={
        "parent": {"type": "page_id", "page_id": "PARENT_PAGE_ID"},
        "title": [{"type": "text", "text": {"content": "Project Tracker"}}],
        "properties": {
            "Project Name": {"title": {}},
            "Status": {"status": {}},
            "Priority": {"select": {"options": [
                {"name": "Urgent", "color": "red"},
                {"name": "High", "color": "orange"},
                {"name": "Medium", "color": "yellow"},
                {"name": "Low", "color": "green"},
            ]}},
            "Deadline": {"date": {}},
            "Budget": {"number": {"format": "dollar"}},
        },
    })
print(f"Created: {resp.json()['url']}")
```

### 2. Query with Compound Filters
```python
# AND filter: Status=In Progress AND Priority≥High
filter_obj = {
    "and": [
        {"property": "Status", "status": {"equals": "In Progress"}},
        {"property": "Priority", "select": {"in": ["Urgent", "High"]}},
    ]
}
# See parent skill for the full query_db() function with pagination
```

### 3. Add a Relation and Rollup
```python
update_schema = {
    "Related Tasks": {
        "relation": {
            "database_id": "TARGET_DB_ID",
            "type": "single_property",
            "single_property": {}
        }
    },
    "Task Count": {
        "rollup": {
            "relation_property_name": "Related Tasks",
            "rollup_property_name": "Status",
            "function": "count"
        }
    }
}
```

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll just use text fields instead of select" | Select/multi-select enables filtering, grouping, and rollups. Text fields make data non-queryable — always use typed properties. |
| "Relations are overkill for small setups" | Without relations, every project duplicates client/team/status data across rows. A relation + rollup eliminates data drift entirely. |
| "Schema changes are easy to make later" | Notion has NO in-place migration. Changing a property type requires rebuilding the database and re-importing data. Design the schema as if it's permanent. |
