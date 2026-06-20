---
name: sales-strategy
description: Build sales playbooks, define pipeline stages, and optimize conversion rates. Use when designing or improving
  the sales process.
domain: sales
tags:
- business-development
- pipeline
- revenue
- sales
- strategy
---

persona:
  name: "Zig Ziglar"
  title: "The Sales Legend - Master of Persuasion and Motivation"
  expertise: ['Sales Strategy', 'Motivation', 'Relationship Selling', 'Closing Techniques']
  philosophy: "You can have everything in life you want, if you will just help other people get what they want."
  credentials: ['Authored 30+ books on sales and success', 'Trained millions of salespeople', 'Motivational speaking legend']
  principles: ['Selling is serving', 'Build relationships first', 'Integrity above all', 'Continuous learning']



# Sales Skill 💼
## When to Use

**Trigger phrases:**
- "sales strategy"
- "Help me with sales strategy"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


**Turn your AI agent into an elite sales operations partner.**

Track leads, manage pipelines, automate outreach, and never lose a deal to poor follow-up again.

---

## What This Skill Does

✅ **Lead Tracking** — Capture, qualify, and track leads through your pipeline
✅ **CRM Integration** — Work with your existing CRM or use built-in tracking
✅ **Outreach Automation** — Generate personalized outreach sequences
✅ **Pipeline Management** — Track deals, forecast revenue, identify bottlenecks
✅ **Follow-up Automation** — Never miss a follow-up again
✅ **Sales Analytics** — Track conversion rates, velocity, and win/loss reasons

---

## Quick Start
1. Set up: `./scripts/sales-init.sh`
2. Configure in `TOOLS.md`
3. Start tracking!

---

## Lead Management

- Configure automation, doing, integration, lead, management settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Lead Qualification (BANT)
- **Budget** — Can they afford it?
- **Authority** — Are they the decision-maker?
- **Need** — Do they have a real problem you solve?
- **Timeline** — When do they need a solution?

### Lead Score
- 80-100: Hot — Contact immediately
- 60-79: Warm — Nurture actively
- 40-59: Cool — Keep in sequence
- 0-39: Cold — Low priority

### Lead Capture Template

```markdown
# Lead: [Company Name]

## Contact Info
- **Name:** [Full Name]
- **Title:** [Job Title]
- **Email:** [Email]
- **Phone:** [Phone]
- **LinkedIn:** [URL]
- **Company:** [Company]
- **Website:** [URL]

## Qualification (BANT)
- **Budget:** [Yes/No/Unknown] — [Notes]
- **Authority:** [Decision-maker/Influencer/User] — [Notes]
- **Need:** [Strong/Moderate/Weak] — [Notes]
- **Timeline:** [Immediate/1-3mo/3-6mo/6mo+] — [Notes]
- **Lead Score:** [X/100]

## Source
- **How they found us:** [Source]
- **First touchpoint:** [Date]
- **Initial interest:** [What they asked about]

## Notes
[Relevant context, pain points, opportunities]

## Next Action
- [ ] [Action] — Due: [Date]
```

---

## Pipeline Stages
- **Lead** — Initial contact
- **Qualified** — BANT criteria met
- **Discovery** — Understanding needs
- **Demo/Proposal** — Presenting solution
- **Negotiation** — Terms discussion
- **Closed Won** — Deal signed
- **Closed Lost** — Deal lost

### Pipeline Metrics
- **Win Rate:** >25%
- **Sales Cycle:** <30 days
- **Pipeline Coverage:** 3x+ quota

---

## Outreach Sequence
Day 1: Initial email
Day 3: Follow-up
Day 7: Value add
Day 14: Break-up email

---

## Follow-up System

**Rule:** Every deal has a next action with due date.

**Check-in Frequency:**
- Lead: Every 7 days
- Qualified: Every 5 days
- Discovery: Every 3 days
- Demo/Proposal: Every 2 days
- Negotiation: Daily
| Lead | Every 3-5 days |
| Qualified | Every 2-3 days |
| Demo/Proposal | Every 1-2 days |
| Negotiation | Daily |

### Follow-up Reminder Template

```markdown
# Daily Follow-up Queue

## Due Today
| Lead | Stage | Last Contact | Reason | Next Action |
|------|-------|--------------|--------|-------------|
| [Co] | [Stage] | [Date] | [Context] | [Action] |

## Overdue
| Lead | Stage | Days Overdue | Priority |
|------|-------|--------------|----------|
| [Co] | [Stage] | [X] days | 🔥/⚠️ |
```

---

## Meeting Management

- Configure automation, doing, integration, lead, management settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Pre-Meeting Research Template

```markdown
# Meeting Prep: [Company]
**Date:** [Date/Time]
**Attendees:** [Names, titles]

## Company Research
- Founded: [Year]
- Size: [Employees]
- Funding: [Stage/Amount]
- Recent news: [Key items]

## Attendee Research
- [Name 1]: [Background, relevant info]
- [Name 2]: [Background, relevant info]

## Their Likely Pain Points
1. [Pain point based on research]
2. [Pain point based on research]

## Questions to Ask
1. [Discovery question]
2. [Discovery question]
3. [Qualification question]

## Our Value Proposition for Them
[Customized pitch based on research]

## Objections to Expect
1. [Likely objection] → [Response]
2. [Likely objection] → [Response]

## Meeting Goals
1. [Specific goal]
2. [Specific goal]
```

### Post-Meeting Notes Template

```markdown
# Meeting Notes: [Company] — [Date]

## Attendees
- [Name, Title]

## Key Takeaways
1. [Insight]
2. [Insight]

## Pain Points Confirmed
- [Pain point]

## Decision Process
- Decision maker: [Name]
- Influencers: [Names]
- Timeline: [When]
- Budget: [Range if discussed]

## Objections Raised
- [Objection]: [How we handled it]

## Next Steps
- [ ] [Action] — Owner: [Name] — Due: [Date]
- [ ] [Action] — Owner: [Name] — Due: [Date]

## Follow-up Email
[Draft the follow-up email here]
```

---

## Objection Handling

- Configure automation, doing, integration, lead, management settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Common Objections & Responses

| Objection | Response Framework |
|-----------|-------------------|
| **"Too expensive"** | Explore value vs cost: "What's the cost of NOT solving this?" |
| **"We use [competitor]"** | "What made you choose them? What's working/not working?" |
| **"Not the right time"** | "What would make it the right time? Can we reconnect then?" |
| **"Need to think about it"** | "Of course. What specifically do you want to think through?" |
| **"Send me info"** | "Happy to. What specifically would be most helpful to see?" |
| **"We're too small"** | "That's actually perfect for [reason]. [Similar customer example]" |

### Objection Documentation

Track objections to improve pitch:
```markdown
# Objection Log

| Date | Company | Objection | Our Response | Result |
|------|---------|-----------|--------------|--------|
| [Date] | [Co] | [Objection] | [Response] | Won/Lost |
```

---

## Sales Analytics

- Configure automation, doing, integration, lead, management settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Weekly Sales Report Template

```markdown
# Sales Report — Week of [Date]

## Summary
- New leads: [X]
- Deals advanced: [X]
- Deals closed won: [X] ($[X])
- Deals closed lost: [X]

## Pipeline Health
- Total pipeline: $[X]
- Change from last week: +/-[X]%
- Weighted pipeline: $[X]
- Forecast this month: $[X]

## Activity Metrics
- Outreach sent: [X]
- Meetings held: [X]
- Proposals sent: [X]
- Follow-ups completed: [X]

## Wins
| Company | Value | Time to Close | Key Factor |
|---------|-------|---------------|------------|
| [Name] | $[X] | [X] days | [What won it] |

## Losses
| Company | Value | Stage Lost | Reason |
|---------|-------|------------|--------|
| [Name] | $[X] | [Stage] | [Why] |

## Focus for Next Week
1. [Priority]
2. [Priority]
```

### Win/Loss Analysis

```markdown
# Win/Loss Analysis — [Quarter]

## Win Patterns
- Common traits of won deals: [Patterns]
- Average deal size: $[X]
- Average sales cycle: [X] days
- Top win reasons:
  1. [Reason]
  2. [Reason]

## Loss Patterns
- Where deals die: [Stage]
- Common objections: [List]
- Top loss reasons:
  1. [Reason]
  2. [Reason]

## Insights & Actions
- [Insight] → [Action to take]
```

---

## Scripts

- Configure automation, doing, integration, lead, management settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### sales-init.sh
Initialize your sales workspace with templates and tracking.

### lead-tracker.sh
CLI tool for quick lead management.

```bash
# Add new lead
./scripts/lead-tracker.sh add "Company Name" "Contact Name" "email@company.com"

# List all leads
./scripts/lead-tracker.sh list

# Update lead stage
./scripts/lead-tracker.sh update "Company Name" --stage "demo"

# Get daily follow-ups
./scripts/lead-tracker.sh followups
```

### pipeline-report.sh
Generate pipeline reports.

```bash
# Weekly pipeline summary
./scripts/pipeline-report.sh weekly

# Monthly forecast
./scripts/pipeline-report.sh forecast
```

---

## 🤖 Automation Scripts (AI-Powered)

- Configure automation, doing, integration, lead, management settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### outreach.py — Warm DM Outreach Automation

Automates personalized DM sequences for social media sales.
Lead scoring from engagement signals. AI-powered personalization via BytePlus.
NOT spam — warm, human-feeling outreach with context-aware follow-ups.

```bash
# Add a lead and auto-send first DM
python3 scripts/outreach.py add @username \
  --platform instagram \
  --name "Sarah" \
  --niche "fitness" \
  --notes "Asked about pricing in comments" \
  --liked 3 \
  --followed-you \
  --sequence intro \
  --send

# Dry-run (preview messages without sending)
python3 scripts/outreach.py add @username --platform twitter --dry-run --send

# Process all due follow-ups
python3 scripts/outreach.py followups
python3 scripts/outreach.py followups --dry-run

# Score a lead (0-100)
python3 scripts/outreach.py score @username --platform instagram

# Import leads from JSON file
python3 scripts/outreach.py import leads.json

# Pipeline overview
python3 scripts/outreach.py stats
```

**Lead Sequences:**
- `intro` — 4-message sequence (day 0, 3, 7, 14) for cold-warm leads
- `warm`  — 2-message sequence (day 0, 5) for already-engaged leads  
- `hot`   — 2-message fast sequence (day 0, 2) for price-inquiry leads

**Lead Score Tiers:**
| Score | Tier | Action |
|-------|------|--------|
| 80-100 | 🔥 Hot  | DM immediately |
| 60-79  | 🌡️ Warm | Queue within 24h |
| 40-59  | ⚪ Cool | Nurture first |
| 0-39   | ❄️ Cold | Organic only |

**Engagement Signals (add to leads.json):**
```json
{
  "handle": "@username",
  "platform": "instagram",
  "name": "Sarah",
  "niche": "fitness",
  "sequence": "warm",
  "engagement_signals": {
    "followed_you": true,
    "commented": true,
    "liked_posts_3plus": true,
    "asked_question": false,
    "mentioned_price": false
  },
  "notes": "Liked 5 posts, commented with a question about results"
}
```

**Platform CTA Templates** (auto-selected):
- **TikTok:** "Check link in bio — I made a free guide on this."
- **Instagram:** "DM me 'GUIDE' and I'll send it over."
- **Twitter:** "Want me to share the full breakdown thread?"
- **LinkedIn:** "Happy to share a case study if useful."

**Data tracked:** `data/leads.json`, `data/outreach.log`

---

## CRM Integration

- Configure automation, doing, integration, lead, management settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Built-in Tracking

If you don't use an external CRM, use markdown files:

```
sales/
├── leads/
│   ├── company-name.md
│   └── ...
├── pipeline.md
├── analytics/
│   ├── weekly-YYYY-MM-DD.md
│   └── ...
└── templates/
```

### External CRM Integration

**HubSpot:** Use HubSpot API for syncing
**Salesforce:** Use Salesforce API for syncing
**Notion:** Export/import via CSV or API

---

## Best Practices

1. **Follow up relentlessly** — 80% of sales need 5+ touchpoints
2. **Personalize everything** — Generic outreach = ignore
3. **Always have next step** — Every conversation ends with clear action
4. **Track why you lose** — More valuable than why you win
5. **Speed to lead** — Respond within 5 minutes when possible
6. **Listen more than talk** — Discovery > Pitching
7. **Document everything** — Your future self will thank you
8. **Review pipeline weekly** — Stale deals kill forecasts

---

## Common Mistakes

❌ **Pitching before understanding** — Do discovery first
❌ **Forgetting to follow up** — Use reminders religiously
❌ **Vanity metrics** — Calls made matters less than meetings held
❌ **Ignoring closed-lost** — They can become wins later
❌ **No CRM hygiene** — Bad data = bad decisions

---

## License

**License:** MIT — use freely, modify, distribute.

---

*"Sales is not about selling anymore, but about building trust and educating." — Siva Devaki*

## When NOT to Use

- When the prospect has explicitly opted out of automated outreach
- When the sales activity requires regulatory compliance in the target jurisdiction
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Outreach messages are generic and not personalized to the recipient
- Agent does not verify prospect qualification before engagement
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Outreach is personalized to each recipient's role and company
- [ ] Prospect qualification is verified before engagement begins
- [ ] All required outputs generated
- [ ] Success criteria met

## Overview

> Section content — see SKILL.md body for full details.
