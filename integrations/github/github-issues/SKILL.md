---
name: github-issues
description: Use when gitHub Issues — CRUD operations, labels, milestones, comments, templates, webhooks, and automation. See parent skill for all GitHub automation capabilities.
domain: integrations
tags:
- api
- github
- integrations
- issues
version: 1.0.0
---

# GitHub Issues

## Quick Reference

The GitHub Issues sub-skill covers issue lifecycle automation — CRUD via REST and GraphQL APIs, label and milestone management, comments, issue templates, webhook-driven triage, and bulk operations. This layers on the parent [GitHub Automation Hub](../SKILL.md) which covers the full Actions+Issues+PR ecosystem and money-making protocols.

**Use this when** you need to programmatically create, read, update, close, label, triage, or migrate issues at any scale.

## Overview

GitHub Issues is the project tracking layer of every repository. Automation prevents maintainer burnout and enables structured workflows:
- **Issue templates** — standardize bug reports, feature requests, and questions
- **Auto-labeling** — classify issues by content patterns on creation
- **Bulk operations** — close stale issues, migrate between repos, update labels in batch
- **Webhook-driven flows** — trigger external systems on issue creation, update, or close
- **Cross-repo synchronization** — mirror issues between upstream and fork

The parent skill's `triage.yml` workflow, `bulk-issues.py`, and issue template files are the canonical templates.

## Quick Start

### 1. Create an Issue via API
```bash
gh issue create --repo owner/repo \
  --title "Login form crashes on mobile" \
  --body "## Steps to reproduce\n1. Open /login on iPhone\n2. Tap email field\n3. App crashes" \
  --label bug --assignee @me
```

### 2. Query and Filter Issues
```python
import os, requests
TOKEN = os.environ["GITHUB_TOKEN"]
resp = requests.get(
    "https://api.github.com/repos/owner/repo/issues",
    headers={"Authorization": f"Bearer {TOKEN}"},
    params={"labels": "bug,priority:high", "state": "open", "per_page": 100},
)
for issue in resp.json():
    print(f"#{issue['number']}: {issue['title']} ({issue['html_url']})")
```

### 3. Add Label-Based Triage Automation
Create `.github/workflows/triage.yml` (see parent skill for the complete script) that:
- Auto-adds `bug` label when title/body contains "crash", "error", "fail"
- Auto-adds `enhancement` for "feature request" or "would like"
- Greets first-time contributors with a welcome comment
- Sets `priority:high` for "urgent", "critical", "p0" mentions

## Code Snippet: Close Stale Issues

```python
#!/usr/bin/env python3
"""Close issues with no activity in 90 days."""
import os, requests
from datetime import datetime, timezone

TOKEN = os.environ["GITHUB_TOKEN"]
API = "https://api.github.com"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

for issue in requests.get(f"{API}/repos/owner/repo/issues",
    headers=HEADERS, params={"state": "open", "per_page": 100}).json():

    updated = datetime.fromisoformat(issue["updated_at"].replace("Z", "+00:00"))
    days_since = (datetime.now(timezone.utc) - updated).days
    if days_since > 90 and not issue.get("pull_request"):
        requests.patch(issue["url"], headers=HEADERS,
            json={"state": "closed", "state_reason": "not_planned"})
        print(f"Closed stale #{issue['number']}: {issue['title']}")
```

## Verification Checklist

- [ ] Issue CRUD works via both REST API and `gh` CLI
- [ ] Auto-labeling regex triggers correctly on test issues
- [ ] Issue templates render in the UI with correct YAML frontmatter
- [ ] Webhook endpoint receives and processes issue events
- [ ] Rate limits managed: 5,000 req/hr authenticated, pagination handled for bulk ops

## When to Use

Use when gitHub Issues — CRUD operations, labels, milestones, comments, templates, webhooks, and automation. See parent skill for all GitHub automation capabilities.

## Workflow

Execute these steps sequentially:

### 1. Create an Issue via API
```bash
gh issue create --repo owner/repo \
  --title "Login form crashes on mobile" \
  --body "## Steps to reproduce\n1. Open /login on iPhone\n2. Tap email field\n3. App crashes" \
  --label bug --assignee @me
```

### 2. Query and Filter Issues
```python
import os, requests
TOKEN = os.environ["GITHUB_TOKEN"]
resp = requests.get(
    "https://api.github.com/repos/owner/repo/issues",
    headers={"Authorization": f"Bearer {TOKEN}"},
    params={"labels": "bug,priority:high", "state": "open", "per_page": 100},
)
for issue in resp.json():
    print(f"#{issue['number']}: {issue['title']} ({issue['html_url']})")
```

### 3. Add Label-Based Triage Automation
Create `.github/workflows/triage.yml` (see parent skill for the complete script) that:
- Auto-adds `bug` label when title/body contains "crash", "error", "fail"
- Auto-adds `enhancement` for "feature request" or "would like"
- Greets first-time contributors with a welcome comment
- Sets `priority:high` for "urgent", "critical", "p0" mentions

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Labels are cosmetic — they don't affect workflow" | Label-driven automation is the backbone of triage. Without labels, you cannot auto-assign, prioritize, or route issues programmatically. |
| "Manual triage is fine for small projects" | A triage bot costs 15 minutes to set up and saves 2+ hours/week per maintainer. Automate on day one. |
| "I'll just use the web UI for issue management" | The API enables cross-repo sync, bulk migrations, and automated SLA tracking — none possible through the UI. |
