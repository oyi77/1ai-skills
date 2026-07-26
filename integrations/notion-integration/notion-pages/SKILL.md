---
name: notion-pages
description: Use when notion Pages — Create, read, update, append blocks, embed content, manage hierarchy, templates, archive/restore. See parent skill for all Notion automation capabilities.
domain: integrations
tags:
- api
- integrations
- notion
- pages
version: 1.0.0
---

# Notion Pages — Quick Reference

**Role:** Notion Pages are the content unit of Notion — database rows, stand-alone documents, or nested sub-pages. This sub-skill covers page-specific CRUD: creating pages with rich block content, appending blocks, managing page hierarchy (parent/child), working with templates, and archive/restore lifecycle. For database schema and query operations, see the parent skill.

## Quick Start

### 1. Create a Page with Content
Create a page inside a database with properties and block children:

```python
import os, requests
TOKEN = os.environ["NOTION_TOKEN"]
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json", "Notion-Version": "2022-06-28"}

def create_page(parent_db_id, properties, children=None):
    payload = {"parent": {"database_id": parent_db_id}, "properties": properties}
    if children:
        payload["children"] = children
    resp = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload)
    resp.raise_for_status()
    return resp.json()

# Add a page to a CRM database with rich body content
page = create_page("DB_ID", {
    "Name": {"title": [{"text": {"content": "Acme Corp"}}]},
    "Status": {"status": {"name": "Active"}},
}, children=[
    {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "Notes"}}]}},
    {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "First meeting scheduled for next week."}}]}},
])
```

### 2. Append Blocks to an Existing Page
Add new content blocks to an already-created page without replacing existing content:

```python
def append_blocks(page_id, blocks):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    resp = requests.patch(url, headers=HEADERS, json={"children": blocks})
    resp.raise_for_status()
    return resp.json()

append_blocks(page["id"], [
    {"object": "block", "type": "to_do", "to_do": {"rich_text": [{"text": {"content": "Send proposal"}}], "checked": False}},
    {"object": "block", "type": "toggle", "toggle": {"rich_text": [{"text": {"content": "Details"}}]}},
])
```

### 3. Archive (Soft-Delete) and Restore
Move pages to trash and restore them:

```python
def archive_page(page_id):
    requests.patch(f"https://api.notion.com/v1/pages/{page_id}", headers=HEADERS, json={"archived": True}).raise_for_status()

def restore_page(page_id):
    requests.patch(f"https://api.notion.com/v1/pages/{page_id}", headers=HEADERS, json={"archived": False}).raise_for_status()
```

## One Focused Code Snippet — Page Template Engine

Create pages from a template by substituting variables:

```python
def create_from_template(db_id, template_text, variables, properties_override=None):
    """Create a page with rendered template content."""
    for k, v in variables.items():
        template_text = template_text.replace(f"{{{{{k}}}}}", v)
    blocks = [{"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": line}}]}}
              for line in template_text.split("\n") if line.strip()]
    return create_page(db_id, properties_override or {"Name": {"title": [{"text": {"content": variables.get("title", "Untitled")}}]}}, children=blocks)
```

## Checklist

- [ ] Page creation handles all property types: title, rich_text, select, date, number, checkbox, status
- [ ] Block hierarchy preserved: heading → bullet_list → child blocks nested correctly
- [ ] Append blocks does NOT replace existing children — uses PATCH to children endpoint
- [ ] Archive vs delete: Notion has no hard delete via API. Archived pages can be restored.
- [ ] Rate limit: 3 req/s. Sleep ~350ms between sequential calls. Batch with exponential backoff on 429.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I can just copy-paste the page content manually" | Automated page creation with block children eliminates 15 min of manual formatting per page. At 50+ pages/month, that's 12+ hours saved. |
| "All pages go in databases" | Stand-alone pages exist too. Use `parent: {"page_id": id}` for sub-pages, not `database_id`. Different endpoint behavior for block children. |
| "Archive is permanent" | Archived pages retain all content and can be unarchived via PATCH `archived: false`. Hard deletion requires manual workspace trash emptying. |
|---|---|
| "I'll figure it out as I go" | A structured approach saves time and reduces errors. Follow the workflow in this skill rather than improvising. |
| "I already know this topic" | Familiarity breeds shortcuts. Use the checklist to verify you haven't missed critical steps. |
| "This doesn't apply to my situation" | The patterns here generalize across contexts. Adapt, don't skip — the underlying principles hold. |
| "One more tool will fix it" | Adding complexity rarely solves process gaps. Master the core workflow first. |

## When to Use
Use this skill when working with notion pages.


## Workflow
See the parent skill for authoritative workflow documentation.
