---
name: affiliate-manager
description: Automated discovery of affiliate programs, partnership opportunities, and cross-promotion deals with outreach, commission tracking, and placement optimization
---



## Overview

End-to-end affiliate and partnership management system for a one-person company. Discovers relevant affiliate programs, automates outreach, tracks commissions across multiple programs, optimizes placements through A/B testing, and generates revenue reports. Turns content properties into passive income streams by systematically connecting them with the right affiliate offers.

## Required Tools

- **Web scraping**: `curl`, `puppeteer`/`playwright` for program discovery
- **Email automation**: Gmail API, SendGrid, or Mailgun for outreach
- **Link management**: Custom redirect service or tools like Pretty Links, ThirstyAffiliates
- **Analytics**: Google Analytics API, custom UTM tracking
- **Storage**: SQLite or JSON for program database and commission tracking
- **Reporting**: Python/Node.js scripts for revenue aggregation
- **Notification**: Slack webhook for commission alerts

## Capabilities

- Discover affiliate programs in any niche by scraping affiliate networks and direct programs
- Generate personalized outreach emails with partnership proposals
- Track commissions across multiple affiliate networks in a single dashboard
- A/B test affiliate placements (position, CTA text, link format) for conversion optimization
- Monitor cookie windows, commission rates, and payout terms across programs
- Detect commission anomalies (missing conversions, delayed payments)
- Generate revenue reports by program, content piece, and time period
- Identify cross-promotion and co-marketing opportunities with complementary products

## When to Use

- Monetizing a content site, newsletter, or YouTube channel with affiliate offers
- Switching from ad-based revenue to higher-value affiliate partnerships
- Running multiple content properties and need centralized affiliate tracking
- Wanting to optimize existing affiliate placements for higher conversion
- Looking for new high-paying affiliate programs in a specific niche
- Preparing revenue reports for tax purposes or investor updates

## Pseudo Code

The affiliate-manager workflow follows a standard pipeline pattern.

Core flow:
```
# affiliate-manager primary flow
input = prepare(raw_data)
result = process(input, config={affiliate, automated, commission, cross, deals})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Core Workflow
```
# affiliate-manager primary flow
input = prepare(raw_data)
result = process(input, config={affiliate, automated, commission, cross, deals})
validate(result)
deliver(result)
```

### Error Handling
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### 1. Program Discovery

```bash
# Discover affiliate programs in a niche
python3 << 'PYEOF'
import requests
from bs4 import BeautifulSoup
import json

niche = "productivity tools"
programs = []

# Source 1: Scrape affiliate networks
networks = {
    "shareasale": "https://www.shareasale.com/affsearch/searchByKeyword.cfm",
    "cj": "https://www.cj.com/advertiser-search",
    "impact": "https://impact.com/advertiser-search"
}

# Source 2: Direct program searches
search_queries = [
    f"{niche} affiliate program",
    f"{niche} partner program",
    f"{niche} referral program signup",
]

for query in search_queries:
    # Use Google search or SerpAPI
    resp = requests.get("https://serpapi.com/search", params={
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": 10
    })
    results = resp.json().get("organic_results", [])
    for r in results:
        programs.append({
            "name": r["title"],
            "url": r["link"],
            "source": "search",
            "query": query
        })

# Source 3: Competitor affiliate links analysis
# Scrape competitor sites for affiliate link patterns
affiliate_patterns = [
    "go.redirectingat.com",  # Skimlinks
    "amzn.to",               # Amazon
    "shareasale.com",
    "impact.com",
    "refersion.com",
    "tapfiliate.com"
]

# Save discovered programs
with open(".affiliates/discovered.json", "w") as f:
    json.dump(programs, f, indent=2)
print(f"Discovered {len(programs)} potential programs")
PYEOF
```

### 2. Program Evaluation & Scoring

```python
# Evaluate and score discovered programs
def score_program(program):
    score = 0
    
    # Commission rate (higher = better)
    if program["commission_rate"] >= 30: score += 30
    elif program["commission_rate"] >= 20: score += 20
    elif program["commission_rate"] >= 10: score += 10
    
    # Cookie duration (longer = better)
    if program["cookie_days"] >= 90: score += 20
    elif program["cookie_days"] >= 30: score += 15
    elif program["cookie_days"] >= 7: score += 5
    
    # Recurring commission
    if program.get("recurring"): score += 15
    
    # Brand trust (reviews, known brand)
    if program.get("brand_trust") == "high": score += 10
    
    # Payment reliability
    if program.get("payment_terms") == "net30": score += 5
    
    # EPC (earnings per click) if available
    if program.get("epc") and program["epc"] > 1.0: score += 10
    
    program["score"] = score
    return program

# Rank programs
programs = [score_program(p) for p in programs]
programs.sort(key=lambda x: x["score"], reverse=True)
```

### 3. Automated Outreach

```python
# Generate and send personalized outreach emails
import smtplib
from email.mime.text import MIMEText
from string import Template

template = Template("""
Hi $contact_name,

I run $site_name ($site_url), a $niche content platform with $monthly_traffic monthly visitors.

I'd love to explore a partnership with $program_name. My audience aligns well with your product because $alignment_reason.

Here's what I can offer:
- Dedicated review/comparison content
- Email newsletter placement ($list_size subscribers)
- Social media promotion ($social_followers followers)

Would you be open to discussing a custom affiliate arrangement or higher commission tier?

Best,
$my_name
""")

for program in top_programs:
    email_body = template.substitute(
        contact_name=program.get("contact", "Partner Team"),
        site_name="ProductivityHQ",
        site_url="https://productivityhq.com",
        niche="productivity and automation",
        program_name=program["name"],
        alignment_reason="our readers actively seek tools to automate their workflows",
        monthly_traffic="50K",
        list_size="12K",
        social_followers="25K",
        my_name="Your Name"
    )
    
    msg = MIMEText(email_body)
    msg["Subject"] = f"Partnership inquiry — {program['name']} x ProductivityHQ"
    msg["To"] = program["contact_email"]
    msg["From"] = "you@productivityhq.com"
    
    # Send via SMTP or SendGrid API
    # smtp.send_message(msg)
```

### 4. Commission Tracking Database

```sql
-- SQLite schema for affiliate tracking
CREATE TABLE programs (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    network TEXT,          -- shareasale, cj, impact, direct
    commission_rate REAL,
    commission_type TEXT,  -- percentage, flat, recurring
    cookie_days INTEGER,
    payout_minimum REAL,
    payment_method TEXT,
    status TEXT DEFAULT 'active',
    signup_date TEXT,
    notes TEXT
);

CREATE TABLE clicks (
    id INTEGER PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id),
    content_id TEXT,        -- which page/post generated the click
    placement_id TEXT,      -- which CTA/placement
    timestamp TEXT,
    ip_hash TEXT,           -- anonymized
    user_agent TEXT,
    referrer TEXT
);

CREATE TABLE conversions (
    id INTEGER PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id),
    click_id INTEGER REFERENCES clicks(id),
    order_id TEXT,
    revenue REAL,
    commission REAL,
    status TEXT DEFAULT 'pending',  -- pending, approved, paid, rejected
    conversion_date TEXT,
    approval_date TEXT,
    payout_date TEXT
);

-- Revenue by program
SELECT p.name, 
       COUNT(c.id) as conversions,
       SUM(c.commission) as total_commission,
       AVG(c.commission) as avg_commission
FROM conversions c
JOIN programs p ON c.program_id = p.id
WHERE c.status IN ('approved', 'paid')
GROUP BY p.name
ORDER BY total_commission DESC;
```

### 5. A/B Testing Placements

```python
# A/B test affiliate placements for conversion optimization
import random
import json

placements = {
    "test_id": "pricing-table-cta-2024",
    "variants": [
        {"id": "A", "text": "Get Started", "position": "above-fold", "color": "blue"},
        {"id": "B", "text": "Try Free", "position": "above-fold", "color": "green"},
        {"id": "C", "text": "Get Started", "position": "below-fold", "color": "blue"},
    ],
    "traffic_split": [0.33, 0.33, 0.34],
    "min_sample_size": 100,
    "metric": "conversion_rate"
}

def assign_variant(user_id, test):
    """Deterministic variant assignment based on user hash"""
    hash_val = hash(f"{user_id}:{test['test_id']}") % 100
    cumulative = 0
    for i, split in enumerate(test["traffic_split"]):
        cumulative += split * 100
        if hash_val < cumulative:
            return test["variants"][i]
    return test["variants"][-1]

# Track results per variant
def record_impression(test_id, variant_id, user_id):
    # Log to analytics
    pass

def record_conversion(test_id, variant_id, user_id, commission):
    # Log conversion with variant info
    pass

# Analyze results after sufficient data
def analyze_test(test_id):
    results = {}
    for variant in placements["variants"]:
        vid = variant["id"]
        impressions = count_impressions(test_id, vid)
        conversions = count_conversions(test_id, vid)
        rate = conversions / impressions if impressions > 0 else 0
        results[vid] = {
            "impressions": impressions,
            "conversions": conversions,
            "rate": rate,
            "revenue": sum_revenue(test_id, vid)
        }
    
    # Statistical significance check
    winner = max(results.items(), key=lambda x: x[1]["rate"])
    print(f"Winner: Variant {winner[0]} with {winner[1]['rate']:.2%} conversion rate")
    return results
```

### 6. Revenue Reporting

```bash
# Generate monthly affiliate revenue report
python3 << 'PYEOF'
import sqlite3
from datetime import datetime, timedelta

db = sqlite3.connect("affiliates.db")
month_start = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

# Total revenue
total = db.execute("""
    SELECT SUM(commission) FROM conversions 
    WHERE status IN ('approved', 'paid') AND conversion_date >= ?
""", (month_start,)).fetchone()[0] or 0

# By program
by_program = db.execute("""
    SELECT p.name, COUNT(*) as sales, SUM(c.commission) as revenue
    FROM conversions c JOIN programs p ON c.program_id = p.id
    WHERE c.status IN ('approved', 'paid') AND c.conversion_date >= ?
    GROUP BY p.name ORDER BY revenue DESC
""", (month_start,)).fetchall()

# By content
by_content = db.execute("""
    SELECT c.content_id, COUNT(*) as sales, SUM(c2.commission) as revenue
    FROM clicks c JOIN conversions c2 ON c.id = c2.click_id
    WHERE c2.status IN ('approved', 'paid') AND c2.conversion_date >= ?
    GROUP BY c.content_id ORDER BY revenue DESC LIMIT 10
""", (month_start,)).fetchall()

report = f"""# Affiliate Revenue Report — {month_start} to {datetime.now().strftime('%Y-%m-%d')}

## Total Revenue: ${total:,.2f}

- Configure affiliate, automated, commission, cross, deals settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


## By Program
| Program | Sales | Revenue |
|---------|-------|---------|
"""
for name, sales, rev in by_program:
    report += f"| {name} | {sales} | ${rev:,.2f} |\n"

report += "\n## Top Performing Content\n| Content | Sales | Revenue |\n|---------|-------|---------|\n"
for content, sales, rev in by_content:
    report += f"| {content} | {sales} | ${rev:,.2f} |\n"

print(report)
PYEOF
```

### 7. Anomaly Detection

```python
# Detect missing commissions and payment anomalies
def check_anomalies(program_id, days=7):
    conn = sqlite3.connect("affiliates.db")
    
    # Check: clicks without conversions (expected ratio)
    clicks = conn.execute("""
        SELECT COUNT(*) FROM clicks 
        WHERE program_id = ? AND timestamp >= date('now', ?)
    """, (program_id, f"-{days} days")).fetchone()[0]
    
    conversions = conn.execute("""
        SELECT COUNT(*) FROM conversions 
        WHERE program_id = ? AND conversion_date >= date('now', ?)
    """, (program_id, f"-{days} days")).fetchone()[0]
    
    expected_rate = conn.execute("""
        SELECT AVG(1.0 * conversions / clicks) FROM (
            SELECT program_id, COUNT(*) as clicks FROM clicks GROUP BY program_id
        ) t JOIN (
            SELECT program_id, COUNT(*) as conversions FROM conversions GROUP BY program_id
        ) c ON t.program_id = c.program_id
    """).fetchone()[0] or 0.01
    
    if clicks > 50 and conversions == 0:
        return f"🚨 ALERT: {clicks} clicks but 0 conversions — possible tracking issue"
    
    actual_rate = conversions / clicks if clicks > 0 else 0
    if actual_rate < expected_rate * 0.3:
        return f"⚠️  WARNING: Conversion rate ({actual_rate:.2%}) is <30% of expected ({expected_rate:.2%})"
    
    # Check: pending approvals older than 30 days
    stale = conn.execute("""
        SELECT COUNT(*) FROM conversions 
        WHERE program_id = ? AND status = 'pending' 
        AND conversion_date < date('now', '-30 days')
    """, (program_id,)).fetchone()[0]
    
    if stale > 0:
        return f"⚠️  WARNING: {stale} conversions pending approval for >30 days"
    
    return "✅ No anomalies detected"
```

## Error Handling

| Error | Cause | Recovery |
|-------|-------|---------|
| Outreach email bounces | Invalid contact email | Scrape updated contact from program page, try generic partner@ address |
| Commission not tracked | Click ID lost, cookie expired | Implement server-side postback tracking as backup to cookie-based |
| API rate limit (network) | Too many program lookups | Cache program data, refresh weekly not daily |
| Stale program data | Program terms changed | Re-scrape program pages monthly, compare with stored terms |
| Low conversion rate | Poor placement or audience mismatch | Run A/B test, try different content types, switch programs |
| Delayed payments | Program has long payment cycle | Track expected payment dates, send follow-up at 2x normal cycle |

## Common Patterns

**Pattern 1: Multi-Network Aggregation** — Don't rely on a single affiliate network. Run programs from ShareASale, CJ, Impact, and direct partnerships simultaneously. Different networks serve different niches and commission structures.

**Pattern 2: Content-Program Matching** — Maintain a mapping of content topics to best-fit affiliate programs. A "best project management tools" article should link to the highest-converting PM tool affiliate, not a generic one.

**Pattern 3: Cloaked Redirects** — Use your own domain for affiliate links (e.g., `yourdomain.com/go/toolname`). This lets you swap affiliate programs without updating every content page, and provides clean click analytics.

**Pattern 4: Commission Tiers** — After hitting initial volume, negotiate higher commission rates. Most programs have unpublished tiers. Track your volume per program and trigger renegotiation emails at milestones (100 sales, 500 sales, etc.).

**Pattern 5: Seasonal Optimization** — Affiliate conversion rates spike during Black Friday, product launches, and tax season. Pre-schedule content updates and email placements to capitalize on these windows.

## How to Use

1. Define campaign objective and target KPIs
2. Set up tracking and attribution (UTMs, pixels, events)
3. Create campaign assets (copy, creatives, landing pages)
4. Launch with small budget for testing
5. Monitor metrics daily, optimize underperformers
6. Scale winners, pause losers, document learnings

## Red Flags

- **Metrics declining 3+ days**: Investigate funnel leaks or audience fatigue
- **Ad spend with zero conversions**: Pause and review targeting/creative
- **Email open rates below 15%**: Subject lines or sender reputation issue
- **Bounce rate above 70%**: Landing page mismatch or slow load times
- **Attribution gaps**: Missing UTM parameters or broken tracking pixels
