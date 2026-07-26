---
name: content-monitor
description: Use when monitor websites, blogs, and RSS feeds for content changes and updates. See parent skill for full docs.
domain: automation
tags:
- automation
- content
- monitor
- alerts
version: 1.0.0
---
# Content Monitor

## Quick Reference

Content monitoring watches websites, blogs, docs, and RSS feeds for changes, extracts the diff, and alerts via Telegram/Slack/email. Unlike the parent scrapers skill (which covers all four scrape types), this skill focuses purely on **change detection** — hash comparisons, multi-site polling, and diff-based alerting without scraping whole pages on every cycle.

## Overview

A content monitor polls URLs at a fixed interval, hashes the response body (or a CSS selector's content), and fires an alert when the hash changes. The magic is reliable change detection: diff generation with context, deduplication across poll cycles, and alerting that doesn't spam you on every CSS version bump. The `requests` + SQLite pattern below handles 50+ sites on a single VPS without breaking a sweat.

## Quick Start

**Prerequisites:** Python 3.8+, `requests`, and a Telegram bot token or Slack webhook for alerts.

1. **Set up hash cache** — SQLite for persistence across restarts. Without it, every script restart fires alerts for all unchanged pages.

2. **Configure target sites** — Pick 3-5 competitor blogs, changelogs, or regulatory pages. Each needs a URL and optional CSS selector for the content region.

3. **Run** — The loop stores a SHA-256 baseline on first run; subsequent runs alert on any mismatch with a unified diff.

```python
import requests, hashlib, sqlite3
from difflib import unified_diff
from datetime import datetime

def init_db():
    conn = sqlite3.connect("monitor.db")
    conn.execute("CREATE TABLE IF NOT EXISTS pages (url TEXT PRIMARY KEY, name TEXT, last_hash TEXT, last_content TEXT, last_checked TEXT)")
    return conn

def check(conn, url, name, selector=None):
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    content = resp.text
    if selector:
        from bs4 import BeautifulSoup
        content = BeautifulSoup(content, "html.parser").select_one(selector).get_text()
    new_hash = hashlib.sha256(content.encode()).hexdigest()
    row = conn.execute("SELECT last_hash, last_content FROM pages WHERE url=?", (url,)).fetchone()
    if row and row[0] != new_hash:
        diff = "\n".join(unified_diff((row[1] or "").splitlines(), content.splitlines(), lineterm=""))[:1500]
        print(f"[CHANGE] {name}\n{diff[:500]}...")
    elif not row:
        print(f"[BASELINE] {name}")
    conn.execute("INSERT OR REPLACE INTO pages VALUES (?,?,?,?,?)",
                 (url, name, new_hash, content[:2000], datetime.now().isoformat()))
    conn.commit()

def poll_all():
    conn = init_db()
    for url, name in [("https://competitor.com/blog", "Competitor Blog"),
                      ("https://docs.example.com/changelog", "Changelog"),
                      ("https://regulator.gov/updates", "Regulatory")]:
        try:
            check(conn, url, name)
        except Exception as e:
            print(f"[ERROR] {name}: {e}")

if __name__ == "__main__":
    poll_all()
```

## Checklist

- [ ] Hash cache uses persistent storage (SQLite/Redis) — in-memory dict re-alerts on every restart
- [ ] CSS selector scoped to content area, not full page — avoids nav/ads/footer noise
- [ ] Rate limits honored: max 1 req/5s per domain; stagger timestamps to avoid IP blocks
- [ ] RSS feeds preferred over HTML scraping when available — structured data with published timestamps
- [ ] Alert channel tested end-to-end: force a hash mismatch, confirm delivery to Telegram/Slack

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll just check manually once a day" | By the time you see a competitor announcement, their customers have already seen it; 15-min polling catches it in the same hour |
| "Google Alerts is good enough" | Google Alerts has 6-24 hour delay, no diffs, and misses 80% of sub-page changes (pricing, new features) |
| "Full-page hash works fine" | Every ad refresh or footer change triggers a false alert; always scope to the relevant content selector |

## When to Use
Use this skill when working with content monitor.

## Workflow
See the parent skill for authoritative workflow documentation.
