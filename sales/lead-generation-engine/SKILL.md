---
name: lead-generation-engine
description: "Quick reference for automated lead generation engine — prospecting, enrichment, scoring, and pipeline automation. Use when working with lead generation engine."
domain: sales
tags: [lead-generation, prospecting, automation, scoring, pipeline, sales]
version: 1.1.0
---

# Quick Reference: Lead Generation Engine

> **Full lead generation skill**: See `../ai-lead-generation/SKILL.md` for complete service templates, outreach sequences, ICP frameworks, and monetization strategies. This page focuses on the automated engine components — scoring, enrichment, and pipeline management.

## Overview

A lead generation engine automates the prospect-to-meeting pipeline: sourcing prospects from multiple channels (Apollo, LinkedIn Sales Navigator, Crunchbase), enriching with firmographic and intent data, scoring by fit, and routing qualified leads into outreach sequences. The engine runs on a daily cron cycle, processing 500-5000 prospects per batch. Key metrics: lead-to-meeting conversion of 1-5% at $20-50 cost per meeting.

## When to Use

- You're running automated B2B outbound at scale (500+ prospects/month)
- You need to score and prioritize leads by ICP fit before sending outreach
- You want to combine enrichment data (company size, tech stack, intent signals) with scoring
- You're building a daily pipeline that sources → enriches → scores → sequences → reports

## Quick Start

1. **Source prospects** — Define ICP criteria (industry, company size, roles) and pull 500+ prospects via Apollo API or LinkedIn Sales Navigator export
2. **Enrich and score** — Run enrichment (company data via Clearbit/Clay, email verification via Hunter.io) then apply a weighted scoring model based on ICP fit + intent signals
3. **Route and sequence** — Push A-grade leads (score >80) into a 5-touch multi-channel sequence (email + LinkedIn); B-grade (60-80) into a nurture drip; C-grade below threshold

## Code Example: Lead Scoring Engine

```python
import json, sqlite3
from datetime import datetime

ICP_WEIGHTS = {
    "industry_match": 25, "company_size": 15, "role_match": 20,
    "location": 10, "intent_signal": 15, "email_verified": 5,
}

def score_lead(lead: dict) -> dict:
    """Score a lead against ICP weights. Returns score 0-100 and grade."""
    breakdown = {}
    industry = (lead.get("industry") or "").lower()
    if industry in {"saas", "fintech", "e-commerce", "healthtech"}:
        breakdown["industry_match"] = ICP_WEIGHTS["industry_match"]
    size = lead.get("employees") or 0
    if 10 <= size <= 50:
        breakdown["company_size"] = ICP_WEIGHTS["company_size"]
    elif 50 < size <= 200:
        breakdown["company_size"] = ICP_WEIGHTS["company_size"] - 3
    role = (lead.get("role") or "").lower()
    if role in {"cto", "vp engineering", "ceo", "founder", "director of engineering"}:
        breakdown["role_match"] = ICP_WEIGHTS["role_match"]
    country = (lead.get("country") or "").lower()
    if country in {"us", "uk", "eu", "canada", "singapore"}:
        breakdown["location"] = ICP_WEIGHTS["location"]
    intent_count = len(lead.get("signals") or [])
    breakdown["intent_signal"] = min(intent_count * 5, ICP_WEIGHTS["intent_signal"])
    if lead.get("email_verified"):
        breakdown["email_verified"] = ICP_WEIGHTS["email_verified"]
    total = sum(breakdown.values())
    grade = "A" if total >= 80 else "B" if total >= 60 else "C" if total >= 40 else "D"
    return {"lead_id": lead.get("id"), "score": total, "grade": grade,
            "breakdown": breakdown, "scored_at": datetime.utcnow().isoformat()}

def batch_score(leads: list[dict], db_path: str = "leads.db") -> list[dict]:
    """Score and persist to SQLite."""
    conn = sqlite3.connect(db_path)
    conn.execute("""CREATE TABLE IF NOT EXISTS scores (
        lead_id TEXT PRIMARY KEY, score INTEGER, grade TEXT,
        breakdown TEXT, scored_at TEXT)""")
    results = []
    for lead in leads:
        r = score_lead(lead)
        conn.execute("INSERT OR REPLACE INTO scores VALUES (?,?,?,?,?)",
                     (r["lead_id"], r["score"], r["grade"],
                      json.dumps(r["breakdown"]), r["scored_at"]))
        results.append(r)
    conn.commit(); conn.close()
    return results

# Usage:
# prospects = [
#     {"id":"p1","industry":"SaaS","employees":45,"role":"CTO",
#      "country":"US","signals":["funding"],"email_verified":True},
#     {"id":"p2","industry":"Retail","employees":1200,"role":"Manager",
#      "country":"DE","signals":[],"email_verified":False},
# ]
# print([s["grade"] for s in batch_score(prospects)])  # ["A", "D"]
```

## Verification Checklist

- [ ] Scoring weights are calibrated against historical conversion data (not guessed)
- [ ] Prospects with grade C/D are suppressed from outreach sequences (no wasted credits)
- [ ] Enrichment data is verified (email validation via Hunter.io or NeverBounce before sending)
- [ ] Pipeline SQL reports daily: sourced → enriched → scored → sequenced → replied
- [ ] Rate limits are respected per source (Apollo: 1000/mo, LinkedIn: 100/day)
- [ ] Duplicate detection runs before enrichment (deduplicate by email + company domain)
- [ ] Sending domain is warmed up (Instantly/Smartlead) before scaling past 50 emails/day

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I need a perfect list before I start scoring" | Start with 100 imperfect prospects, calibrate weights, then scale. Scoring with real data beats perfecting the model in isolation. |
| "All leads with matching industry get an A" | Industry is only 25% of the score. A CTO at a 50-person SaaS company with funding is an A; a coordinator at a 2000-person company with no signals is a C. |
| "I'll enrich every lead regardless of fit" | Enrichment APIs cost per credit. Score on available data first, enrich only A/B-grade leads to control costs. |
| "Daily scoring is overkill — weekly is fine" | 24-hour delays lose leads to competitors. Score daily at minimum; real-time is better during campaigns. |

## Workflow
Redirected to parent skill at `../ai-lead-generation/SKILL.md`.
