---
name: data-pipeline-engine
description: ETL pipelines that pull data from multiple sources (APIs, databases, web scraping), transform it, and produce actionable dashboards and reports
---

## Overview

Build automated data pipelines that extract from multiple sources, transform into unified formats, and deliver actionable reports/dashboards. Turns raw data scattered across APIs, databases, and websites into strategic intelligence. A force multiplier for research, trading, marketing, and operations.

## Required Tools

- `curl` / `httpie` for API calls
- `jq` for JSON processing
- `pandas` / `polars` for data transformation (Python)
- `sqlite3` / `psql` for database operations
- `beautifulsoup4` / `playwright` for web scraping
- `cron` / `systemd timers` for scheduling
- `markdown` / `html` for report generation

## Capabilities

- Connect to REST APIs, GraphQL, SQL databases, CSV/JSON files
- Scrape websites with anti-bot bypass (Playwright, rotating proxies)
- Transform data: dedup, normalize, enrich, aggregate, join across sources
- Output to markdown reports, HTML dashboards, CSV/JSON exports, Slack/Telegram alerts
- Schedule pipelines hourly/daily/weekly with monitoring and retry
- Incremental extraction (only new/changed data since last run)
- Data quality checks and anomaly detection

## When to Use

- "Pull competitor pricing from 50 sources daily and generate a weekly brief"
- "Monitor product rankings across platforms and alert on changes"
- "Aggregate financial data from multiple APIs into a single dashboard"
- "Scrape job postings and track hiring trends over time"
- "Build a daily digest of industry news from RSS feeds and APIs"

## When NOT to Use

- Task is about implementation, not research (use implementation skills)
- Task is about analysis of existing data (use analysis skills)
- You need to build research tools (use development skills)
- Task is about testing hypotheses (use test skills)
- You don't have access to research sources
- Task requires domain expertise (consult experts)


## Pseudo Code

Implementation patterns for common use cases with this skill.


### Pipeline Configuration

```yaml
# pipeline.yaml
name: data-pipeline-engine
schedule: "0 8 * * *"  # daily at 8am
sources:
  - type: api
    url: https://api.competitor1.com/prices
    auth: ${COMPETITOR1_API_KEY}
    extract:
      path: ".data.products[]"
      fields: [id, name, price, updated_at]
  - type: scraper
    url: https://competitor2.com/pricing
    selectors:
      price: ".price-value"
      product: ".product-name"
  - type: database
    connection: ${DATABASE_URL}
    query: "SELECT * FROM prices WHERE updated_at > {{last_run}}"
transform:
  - deduplicate: [product_name, source]
  - normalize:
      price: "float"
      currency: "USD"
  - enrich:
      - field: price_change
        calc: "price - previous_price"
      - field: price_change_pct
        calc: "(price - previous_price) / previous_price * 100"
output:
  - type: markdown
    path: reports/competitor-pricing-{{date}}.md
  - type: alert
    condition: "price_change_pct > 10 OR price_change_pct < -10"
    channel: slack
    webhook: ${SLACK_WEBHOOK_URL}
```

### Extract Phase

```python
import httpx
from bs4 import BeautifulSoup
import sqlite3

def extract_api(source, last_run):
    """Extract from REST API with pagination and retry."""
    headers = {"Authorization": f"Bearer {source['auth']}"}
    data = []
    page = 1
    while True:
        resp = httpx.get(
            source['url'],
            headers=headers,
            params={"page": page, "since": last_run},
            timeout=30
        )
        resp.raise_for_status()
        batch = jmespath.search(source['extract']['path'], resp.json())
        if not batch:
            break
        data.extend(batch)
        page += 1
    return data

def extract_scraper(source):
    """Extract from website with Playwright for JS-rendered pages."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(source['url'], wait_until='networkidle')
        items = []
        for row in page.query_selector_all('.product-row'):
            items.append({
                'name': row.query_selector(source['selectors']['product']).inner_text(),
                'price': row.query_selector(source['selectors']['price']).inner_text(),
            })
        browser.close()
    return items

def extract_database(source, last_run):
    """Extract from SQL database with incremental loading."""
    conn = sqlite3.connect(source['connection'])
    query = source['query'].replace('{{last_run}}', last_run)
    cursor = conn.execute(query)
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
```

### Transform Phase

```python
import pandas as pd

def transform(raw_data, config):
    """Apply transformation pipeline to raw data."""
    df = pd.DataFrame(raw_data)

    # Deduplicate
    if 'deduplicate' in config:
        df = df.drop_duplicates(subset=config['deduplicate'])

    # Normalize types
    if 'normalize' in config:
        for field, dtype in config['normalize'].items():
            if dtype == 'float':
                df[field] = pd.to_numeric(df[field], errors='coerce')

    # Enrich with calculations
    if 'enrich' in config:
        for rule in config['enrich']:
            df[rule['field']] = df.eval(rule['calc'])

    return df
```

### Output Phase

```python
def output_markdown(df, config):
    """Generate markdown report from DataFrame."""
    path = config['path'].replace('{{date}}', datetime.now().strftime('%Y-%m-%d'))
    with open(path, 'w') as f:
        f.write(f"# {config.get('title', 'Report')} - {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write(df.to_markdown(index=False))
    return path

def output_alert(df, config):
    """Send alerts when conditions are met."""
    alerts = df.query(config['condition'])
    if not alerts.empty:
        message = f"Alert: {len(alerts)} items triggered\n"
        message += alerts.to_markdown(index=False)
        httpx.post(config['webhook'], json={"text": message})
```

### Full Pipeline Runner

```python
def run_pipeline(config_path):
    """Execute full ETL pipeline."""
    config = load_config(config_path)
    last_run = get_last_run(config['name'])
    all_data = []

    # Extract
    for source in config['sources']:
        if source['type'] == 'api':
            all_data.extend(extract_api(source, last_run))
        elif source['type'] == 'scraper':
            all_data.extend(extract_scraper(source))
        elif source['type'] == 'database':
            all_data.extend(extract_database(source, last_run))

    # Transform
    df = transform(all_data, config['transform'])

    # Output
    for output in config['output']:
        if output['type'] == 'markdown':
            output_markdown(df, output)
        elif output['type'] == 'alert':
            output_alert(df, output)

    save_last_run(config['name'], datetime.now().isoformat())
```

### Scheduling

```bash
# Add to crontab for daily execution
crontab -e
# Add line:
0 8 * * * cd /path/to/pipelines && python runner.py pipeline.yaml >> /var/log/pipeline.log 2>&1

# Or use systemd timer for more control
# /etc/systemd/system/pipeline.service
# /etc/systemd/system/pipeline.timer
```

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| API 429 | Rate limit hit | Exponential backoff, respect Retry-After header |
| API 401 | Auth expired | Refresh token, alert if refresh fails |
| Scraper timeout | Page too slow | Increase timeout, use retry with Playwright |
| DB connection refused | Database down | Retry 3x with 5s delay, alert on failure |
| Data quality check failed | Anomalous values | Quarantine bad rows, alert, continue with clean data |
| Empty extraction | Source changed format | Alert immediately, skip this run |

## Common Patterns

- **Incremental loading**: Track `last_run` timestamp, only fetch new/changed records
- **Multi-source join**: Extract from N sources, join on common key (product_id, date)
- **Fan-out alerts**: One pipeline, multiple output channels (Slack + email + dashboard)
- **Data quality gates**: Validate before output — reject if >10% rows fail checks
- **Pipeline chaining**: Output of one pipeline feeds input of another (daily → weekly aggregation)

## Red Flags

- Claiming completion without running verification
- Skipping the analysis phase and jumping to implementation
- Ignoring existing codebase patterns and conventions

## Verification

- [ ] Output matches the original requirements
- [ ] All code or content runs without errors
- [ ] Edge cases have been considered and handled
- [ ] No placeholder content or TODOs remain