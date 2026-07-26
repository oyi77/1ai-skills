---
name: price-tracker
description: Automated e-commerce price tracking with threshold alerts and history logging. See parent skill for full docs.
domain: automation
tags:
- automation
- price
- tracker
- ecommerce
version: 1.0.0
---
# Price Tracker

## Quick Reference

A price tracker polls product pages at regular intervals, logs prices to SQLite, and alerts when a price drops below a configured threshold. Unlike the parent scrapers skill (which covers content monitoring and social listening), this skill focuses purely on **price intelligence** — selector maintenance, affiliate arbitrage, and multi-site comparison for the most directly monetizable scraper use case.

## Overview

Each price drop alert carries an affiliate link: 30% of alerted users click, 1-3% buy, you earn 5-30% commission per sale. The challenge is selector fragility — e-commerce sites change HTML structure frequently during sales events. Durable selectors like `[data-testid="product-price"]` or `[itemprop="price"]` survive redesigns that break fragile class-name selectors. Price tracking works best on high-ticket items (commission >$10) in under-monitored markets (SE Asia, India, Brazil).

## Quick Start

**Prerequisites:** Python 3.8+, `requests`, `beautifulsoup4`.

1. **Find a durable selector** — DevTools → right-click the price element → Copy selector. Prefer `[data-testid]` or `[itemprop="price"]`.

2. **Set targets** — For each product: URL, name, target price, and affiliate link. Start with 3-5 products on one platform.

3. **Run** — Logs every check to SQLite. Alerts when price ≤ target.

```python
import requests, sqlite3, time
from bs4 import BeautifulSoup
from datetime import datetime

PRODUCTS = [
    {"url": "https://shopee.co.id/product/12345", "name": "Gadget X",
     "target": 500000, "affiliate": "https://lynk.id/x-deal",
     "selector": "[data-testid='product-price']"}
]

def init_db():
    conn = sqlite3.connect("prices.db")
    conn.execute("CREATE TABLE IF NOT EXISTS price_log (product TEXT, price INT, currency TEXT DEFAULT 'IDR', ts TEXT, url TEXT, alerted INT DEFAULT 0)")
    return conn

def check(p):
    resp = requests.get(p["url"], headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    price = int(''.join(c for c in BeautifulSoup(resp.text, "html.parser").select_one(p["selector"]).get_text(strip=True) if c.isdigit()))
    return price

conn = init_db()
while True:
    for p in PRODUCTS:
        try:
            price = check(p)
            if price <= p["target"]:
                print(f"ALERT: {p['name']} now {price:,}! {p['affiliate']}")
            conn.execute("INSERT INTO price_log VALUES (?,?,?,?,?,?)",
                         (p["name"], price, "IDR", datetime.now().isoformat(), p["url"], int(price <= p["target"])))
            conn.commit()
        except Exception as e:
            print(f"ERROR {p['name']}: {e}")
    time.sleep(3600)
```

## Checklist

- [ ] Selector tested independently — run once and verify the parsed price matches what the page shows
- [ ] Affiliate links include your tracking ID and redirect through to the real product page
- [ ] History database has at least 10 data points before relying on trend analysis
- [ ] Alert channel tested with a manual threshold (set target artificially high to trigger immediately)
- [ ] Retry logic for transient failures: 3 retries with 30s backoff on timeout/503

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll scrape 100 products for max revenue" | 5 well-chosen high-ticket products with reliable selectors outperform 100 broken trackers |
| "The selector will work forever" | E-commerce sites change HTML weekly; budget 15 min/week for maintenance or use attribute-based selectors |
| "Price tracking is saturated" | Most trackers cover US/UK markets; SE Asian and Latin American markets are wide open |

## When to Use
Use this skill when working with price tracker.

## Workflow
See the parent skill for authoritative workflow documentation.
