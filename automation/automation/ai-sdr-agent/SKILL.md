---
name: ai-sdr-agent
description: AI Sales Development Representative — fully automated cold outreach via email + LinkedIn + WhatsApp. Find prospects, personalize messages, follow up automatically, book meetings without human involvement. Use when: building B2B pipeline, running cold email campaigns, LinkedIn outreach at scale, or automating meeting booking. Revenue potential per client: $2,000–15,000/month. Triggers on "cold outreach", "SDR automation", "book meetings AI", "B2B pipeline automation".
---
persona:
  name: "Domain Expert"
  title: "Master of Ai Sdr Agent"
  expertise: ['Automation Excellence', 'Best Practices', 'Professional Standards']
  philosophy: "Excellence is not a skill, it's an attitude."
  credentials: ['Industry leader', 'Practiced professional', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based', 'Customer focused']



# AI SDR Agent (Sales Development Representative)

## Overview

Replaces a $4,000–8,000/month SDR with AI automation. Finds prospects, personalizes 1:1 messages, handles objections, and books meetings automatically across email, LinkedIn, and WhatsApp.

**Market**: $23B sales automation market  
**Client ROI**: 5–20x pipeline growth vs manual SDR  
**Revenue per client**: $2,000–15,000/month for agency  
**Indonesia niche**: B2B SaaS, import/export, manufacturing, agencies

---

## When to Use

- Client wants consistent B2B meeting flow without hiring SDR
- Running cold email campaign for lead gen
- LinkedIn outreach automation at scale
- Post-inbound lead follow-up (automated qualification)
- Reactivating cold/dormant leads in CRM
- Building agency pipeline for BerkahKarya clients

---

## Core Pipeline

```
Step 1: ICP Definition → Who is the ideal customer?
Step 2: Prospecting → Find companies + contacts
Step 3: Data Enrichment → Email, phone, LinkedIn
Step 4: Personalization → Research-based openers
Step 5: Outreach → Multi-channel sequence
Step 6: Follow-up → 3–5 touch automated sequence
Step 7: Reply handling → Classify + route to human
Step 8: Meeting booking → Calendar sync
```

---

## Stack Options

### Option A: All-in-One (Recommended)
```
Instantly.ai / Apollo.io / Smartlead
- Built-in prospecting + email warm-up
- Deliverability management
- AI personalization
- $99–499/month
```

### Option B: Custom Stack (High control)
```
Prospecting: Apollo.io API / Hunter.io
Enrichment: Clearbit / People Data Labs  
Email sending: Mailgun / AWS SES
Sequence: Custom Python scheduler
CRM: Airtable / Notion
```

### Option C: n8n + AI (BerkahKarya-native)
```
n8n workflow automation (already have skill)
+ OpenAI for personalization
+ Gmail API for sending
+ Airtable for CRM
Total cost: ~$50/month
```

---

## Quick Start — n8n-based SDR

### Workflow: Cold Email SDR
```json
{
  "name": "AI SDR Cold Email Pipeline",
  "nodes": [
    {
      "name": "Trigger",
      "type": "n8n-nodes-base.cron",
      "schedule": "0 8 * * 1-5"
    },
    {
      "name": "Get Prospects",
      "type": "n8n-nodes-base.airtable",
      "operation": "list",
      "filter": "status = 'new'"
    },
    {
      "name": "Personalize via AI",
      "type": "@n8n/n8n-nodes-langchain.openAi",
      "prompt": "Write a personalized cold email for: {{prospect}}"
    },
    {
      "name": "Send Email",
      "type": "n8n-nodes-base.gmail",
      "operation": "send"
    },
    {
      "name": "Update CRM",
      "type": "n8n-nodes-base.airtable",
      "operation": "update",
      "data": {"status": "contacted", "sentAt": "{{$now}}"}
    }
  ]
}
```

---

## Email Sequence Template (SaaS B2B)

### Email 1 (Day 0) — The Hook
```
Subject: [Company] + [Your Company] = ?

Hi [FirstName],

Noticed [Company] just [specific trigger — hiring, funding, new product].

We help [ICP description] companies like yours [specific outcome — "increase qualified demos by 3x"] without [pain — "hiring more SDRs"].

Worth a 15-minute call this week?

[Your name]
```

### Email 2 (Day 3) — The Value
```
Subject: How [Similar Company] got [result]

Hi [FirstName],

Quick follow-up — [Similar Company] was in a similar position: [pain].

After [solution], they [specific result with number].

I've got a few ideas for [Company] specifically. Calendar link if timing works: [link]
```

### Email 3 (Day 7) — The Breakup
```
Subject: Should I close your file?

Hi [FirstName],

Haven't heard back — totally understand if timing isn't right.

Either way, I wanted to share this quick resource: [relevant content link]

If not now, maybe next quarter? Just reply "later" and I'll reach back in 90 days.
```

---

## Python SDR Script

```python
#!/usr/bin/env python3
# scripts/ai_sdr_pipeline.py

import json
import os
from datetime import datetime, timedelta

class AISDRAgent:
    def __init__(self):
        self.prospects_file = "data/prospects.json"
        self.sent_log = "data/outreach_log.json"
    
    def load_prospects(self) -> list:
        """Load prospects from JSON/CSV"""
        try:
            with open(self.prospects_file) as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def personalize_email(self, prospect: dict) -> dict:
        """Generate personalized email using AI"""
        # Use oracle or direct OpenAI call
        company = prospect.get("company", "")
        name = prospect.get("first_name", "")
        trigger = prospect.get("recent_trigger", "")
        
        subject = f"Quick question about {company}"
        
        body = f"""Hi {name},

I saw {company} {trigger if trigger else 'recently'} — congrats on the growth!

We help companies like yours automate B2B outreach and generate 2–3x more qualified meetings.

Worth a quick 15-minute call this week?

Best,
[Your name]"""
        
        return {"subject": subject, "body": body, "to": prospect.get("email")}
    
    def check_followup_due(self) -> list:
        """Return prospects due for follow-up today"""
        try:
            with open(self.sent_log) as f:
                log = json.load(f)
        except:
            log = []
        
        due = []
        today = datetime.now().date()
        
        for entry in log:
            sent_date = datetime.fromisoformat(entry["sent_at"]).date()
            step = entry.get("step", 1)
            
            # Follow-up schedule: Day 3, Day 7, Day 14
            followup_days = {1: 3, 2: 7, 3: 14}
            days_gap = followup_days.get(step, 999)
            
            if (today - sent_date).days >= days_gap and step < 3:
                due.append({**entry, "next_step": step + 1})
        
        return due
    
    def log_outreach(self, prospect_id: str, step: int, channel: str):
        """Log sent outreach"""
        try:
            with open(self.sent_log) as f:
                log = json.load(f)
        except:
            log = []
        
        log.append({
            "prospect_id": prospect_id,
            "step": step,
            "channel": channel,
            "sent_at": datetime.now().isoformat()
        })
        
        with open(self.sent_log, "w") as f:
            json.dump(log, f, indent=2)
    
    def run_daily(self):
        """Daily SDR run — find prospects, send outreach, follow up"""
        print(f"AI SDR run: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # New outreach
        prospects = self.load_prospects()
        new_prospects = [p for p in prospects if p.get("status") == "new"]
        
        print(f"New prospects to contact: {len(new_prospects)}")
        for prospect in new_prospects[:20]:  # max 20/day
            email = self.personalize_email(prospect)
            print(f"  → {prospect.get('email')}: {email['subject']}")
            # TODO: send via Gmail API / SMTP
            self.log_outreach(prospect.get("id"), 1, "email")
        
        # Follow-ups
        follow_ups = self.check_followup_due()
        print(f"Follow-ups due: {len(follow_ups)}")
        for fu in follow_ups:
            print(f"  → {fu.get('prospect_id')}: Step {fu['next_step']}")
            # TODO: send follow-up
            self.log_outreach(fu.get("prospect_id"), fu["next_step"], "email")

if __name__ == "__main__":
    agent = AISDRAgent()
    agent.run_daily()
```

---

## Metrics to Track

| Metric | Benchmark | Good | Great |
|--------|-----------|------|-------|
| Open Rate | 25% | 35% | 50%+ |
| Reply Rate | 3% | 8% | 15%+ |
| Meeting Rate | 1% | 3% | 6%+ |
| Emails/Day | 50 | 100 | 200 |

---

## Client Pricing

| Package | Price/Month | Meetings Guaranteed |
|---------|-------------|---------------------|
| Starter | IDR 3M ($200) | 5 qualified meetings |
| Growth | IDR 7.5M ($500) | 15 qualified meetings |
| Scale | IDR 15M ($1,000) | 30+ qualified meetings |

**Performance bonus**: IDR 500K per extra meeting beyond guarantee

---

## Integration with Existing Skills

- `lead-gen-pipeline` → Source prospects
- `imap-smtp-email` → Send emails
- `wa-business-automation` → WA follow-up sequence
- `sales/personal-crm` → Track all interactions
- `n8n` → Orchestrate full workflow
