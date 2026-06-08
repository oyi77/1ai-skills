---
name: lead-generation-engine
description: AI-powered lead generation that scrapes intent signals, scores leads,
  generates personalized multi-channel outreach, and manages the full CRM pipeline
domain: sales
---



## Overview

Automated lead generation pipeline that detects buying intent signals from multiple sources, scores leads using AI, generates personalized outreach sequences across email/LinkedIn/Twitter, and manages the full sales pipeline. Replaces manual prospecting with a continuous, data-driven engine.

## Required Tools

- **Web Scraping**: curl, jq, BeautifulSoup (Python), Puppeteer (JS)
- **APIs**: LinkedIn Sales Navigator API, Twitter/X API, Hunter.io, Apollo.io, Clearbit
- **CRM**: HubSpot API, Pipedrive API, or Airtable as lightweight CRM
- **Email**: SendGrid API, Mailgun, or AWS SES for outreach delivery
- **AI/LLM**: Claude API for personalization, GPT for batch processing
- **Data**: SQLite or PostgreSQL for lead storage, pandas for analysis

## Capabilities

- Detect intent signals: job postings, funding announcements, tech stack changes, social media activity, hiring patterns
- Score leads with AI based on fit (ICP match) and intent (signal strength)
- Generate personalized outreach sequences per lead across email, LinkedIn, Twitter
- Track pipeline stages: cold → contacted → engaged → qualified → proposal → closed
- A/B test subject lines, messaging, and timing
- Generate weekly pipeline reports with conversion metrics

## When to Use

- Building a consistent pipeline of qualified prospects
- Scaling outreach beyond manual capacity
- Targeting companies showing buying signals (hiring, funding, expanding)
- Replacing expensive tools like ZoomInfo + Outreach with an automated stack
- Running multi-channel outreach campaigns at scale

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The lead-generation-engine workflow follows a standard pipeline pattern.

Core flow:
```
# lead-generation-engine primary flow
input = prepare(raw_data)
result = process(input, config={channel, engine, full, generates, generation})
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
# lead-generation-engine primary flow
input = prepare(raw_data)
result = process(input, config={channel, engine, full, generates, generation})
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


### Intent Signal Detection

```bash
# Monitor job postings for target companies
curl -s "https://api.linkedin.com/v2/jobPostings?q=company&keywords=machine+learning" \
  -H "Authorization: Bearer $LINKEDIN_TOKEN" | jq '.elements[] | {title, company, location}'

# Track funding announcements via Crunchbase API
curl -s "https://api.crunchbase.com/api/v4/searches/organizations" \
  -H "X-cb-user-key: $CB_KEY" \
  -d '{"field_ids":["identifier","short_description","last_funding_type"],"query":[{"type":"predicate","field_id":"last_funding_at","operator":"gte","values":["2026-01-01"]}]}' \
  | jq '.entities[] | .identifier.value'

# Check tech stack changes via BuiltWith/Wappalyzer
curl -s "https://api.builtwith.com/free1/api.json?KEY=$BW_KEY&LOOKUP=example.com" \
  | jq '.Results[] | .Technologies[] | .Name'
```

### Lead Scoring

```python
import sqlite3
from anthropic import Anthropic

def score_lead(lead, icp_criteria):
    """Score lead 0-100 based on fit + intent signals."""
    client = Anthropic()

    # Fit score: how well does lead match ideal customer profile?
    fit_prompt = f"""
    Rate this lead's fit (0-50) against our ICP:
    ICP: {icp_criteria}
    Lead: {lead['company']}, {lead['industry']}, {lead['size']}, {lead['role']}

    Return only the numeric score with brief justification.
    """

    # Intent score: how strong are the buying signals?
    intent_prompt = f"""
    Rate buying intent (0-50) based on these signals:
    Signals: {lead['signals']}

    Strong signals: hiring for relevant roles, recent funding, tech migration, expansion.
    Return only the numeric score with brief justification.
    """

    fit_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=200,
        messages=[{"role": "user", "content": fit_prompt}]
    )

    intent_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=200,
        messages=[{"role": "user", "content": intent_prompt}]
    )

    fit_score = extract_number(fit_response.content[0].text)
    intent_score = extract_number(intent_response.content[0].text)

    return {
        "total": fit_score + intent_score,
        "fit": fit_score,
        "intent": intent_score,
        "grade": "A" if (fit_score + intent_score) >= 80 else "B" if (fit_score + intent_score) >= 60 else "C"
    }

# Update lead scores in database
db = sqlite3.connect("leads.db")
for lead in db.execute("SELECT * FROM leads WHERE scored = 0"):
    result = score_lead(lead, ICP_CRITERIA)
    db.execute("UPDATE leads SET score=?, fit=?, intent=?, grade=?, scored=1 WHERE id=?",
               (result["total"], result["fit"], result["intent"], result["grade"], lead["id"]))
db.commit()
```

### Personalized Outreach Generation

```python
def generate_outreach_sequence(lead, sequence_type="cold"):
    """Generate 3-touch outreach sequence personalized to the lead."""
    client = Anthropic()

    prompt = f"""
    Generate a 3-touch outreach sequence for this lead:
    - Name: {lead['name']}, Title: {lead['title']}
    - Company: {lead['company']}, Industry: {lead['industry']}
    - Intent signals: {lead['signals']}
    - Our solution: {OUR_SOLUTION_DESCRIPTION}

    For each touch, provide:
    1. Channel (email/linkedin/twitter)
    2. Subject line (for email) or hook (for social)
    3. Body (under 150 words, personalized to their signals)
    4. Timing (days after previous touch)

    Style: conversational, not salesy. Lead with value, not pitch.
    Return as JSON array.
    """

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(response.content[0].text)
```

### Pipeline Tracking & Reporting

```bash
# Weekly pipeline report
sqlite3 leads.db <<'SQL'
SELECT
  grade,
  COUNT(*) as total,
  SUM(CASE WHEN stage='contacted' THEN 1 ELSE 0 END) as contacted,
  SUM(CASE WHEN stage='engaged' THEN 1 ELSE 0 END) as engaged,
  SUM(CASE WHEN stage='qualified' THEN 1 ELSE 0 END) as qualified,
  SUM(CASE WHEN stage='proposal' THEN 1 ELSE 0 END) as proposal,
  ROUND(AVG(score), 1) as avg_score
FROM leads
WHERE created_at > datetime('now', '-7 days')
GROUP BY grade
ORDER BY grade;
SQL
```

### A/B Testing Outreach

```python
def ab_test_subject_lines(lead_group_a, lead_group_b, subject_a, subject_b):
    """Send variant subject lines to equal groups, track open rates."""
    import random

    for lead in get_leads_by_criteria(lead_group_a):
        send_email(lead, subject=subject_a, variant="A")

    for lead in get_leads_by_criteria(lead_group_b):
        send_email(lead, subject=subject_b, variant="B")

    # After 48 hours, check results
    results = db.execute("""
        SELECT variant, COUNT(*) as sent,
               SUM(CASE WHEN opened_at IS NOT NULL THEN 1 ELSE 0 END) as opened
        FROM outreach_log
        WHERE campaign_id = ?
        GROUP BY variant
    """, [campaign_id]).fetchall()

    for r in results:
        print(f"Variant {r[0]}: {r[2]}/{r[1]} opened ({r[2]/r[1]*100:.1f}%)")
```

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| API rate limit (429) | Too many requests to LinkedIn/Twitter/Hunter | Implement exponential backoff, spread requests across time |
| Invalid email (bounce) | Bad email from scraping | Verify with Hunter.io email verification before sending |
| Low open rates (<5%) | Poor subject lines or spam filters | A/B test subjects, check SPF/DKIM/DMARC, warm up domain |
| CRM sync failure | API timeout or auth expired | Retry with backoff, refresh OAuth tokens, log failures |
| Scraping blocked | IP blocked by target site | Rotate user agents, use proxy pool, respect robots.txt |
| Score drift | ICP criteria changed but model not updated | Re-score all leads when ICP changes, version the criteria |

## Common Patterns

- **Batch processing**: Process multiple items in parallel for throughput
- **Retry with backoff**: Handle transient failures gracefully
- **Rate limiting**: Respect API limits with configurable delays
- **Logging**: Structured logging for debugging and audit trails


### Daily Signal Scan → Score → Outreach Pipeline

```bash
#!/bin/bash
# Run daily via cron: 0 9 * * 1-5

# 1. Scan for new signals
python3 scan_signals.py --sources linkedin,crunchbase,builtwith

# 2. Score new leads
python3 score_leads.py --new-only --icp icp_v2.json

# 3. Generate outreach for A/B grade leads
python3 generate_outreach.py --min-grade B --sequence cold

# 4. Send scheduled outreach (respects rate limits)
python3 send_outreach.py --today --respect-quiet-hours

# 5. Generate daily report
python3 pipeline_report.py --period daily | mail -s "Daily Lead Gen Report" you@email.com
```

### ICP Definition Template

```json
{
  "version": "v2",
  "industry": ["SaaS", "FinTech", "E-commerce"],
  "company_size": {"min": 10, "max": 500},
  "revenue": {"min": 1000000},
  "roles": ["CTO", "VP Engineering", "Head of Product"],
  "geography": ["US", "UK", "EU"],
  "tech_stack": ["AWS", "Kubernetes", "Python"],
  "signals_weight": {
    "hiring_ml": 20,
    "recent_funding": 25,
    "tech_migration": 15,
    "expansion": 10
  }
}
```

## How to Use

1. Define ideal customer profile (ICP) and buyer personas
2. Build lead list from qualified sources
3. Craft personalized outreach sequences
4. Track engagement and follow up on signals
5. Qualify leads through discovery calls
6. Present solution tailored to pain points
7. Handle objections with value reframing
8. Close and hand off to onboarding

## Red Flags

- **Lead response time > 5 minutes**: Conversion drops 80% after 5 min. Automate instant response.
- **Pipeline has stale deals**: Deals stuck 30+ days need re-qualification or disqualification.
- **Low email reply rates (<3%)**: Messaging is too generic. Personalize with research.
- **High churn in first 90 days**: Onboarding gap. Fix handoff from sales to success.
- **Discounting above 20%**: Value perception problem. Reframe ROI, don't cut price.
