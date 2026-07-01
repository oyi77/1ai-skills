---
name: b2b-sales-automation
description: "|\n  >\n    Full B2B sales pipeline automation for BerkahKarya — from cold prospect to onboarded client.\n \
  \   Covers ICP definition, lead sourcing, outreach sequences, proposal generation, CRM tracking,\n    and deal alerts via\
  \ Telegram. Targets Indonesian SMEs needing AI automation, digital products,\n    and content services.\n"
domain: sales
tags:
- sales
- b2b
- crm
- outreach
- proposal
- pipeline
- indonesian
version: 1.0.0
author: Vilona / BerkahKarya
language: id-ID / en
scripts: "|\n  - scripts/lead_scorer.py\n    - scripts/proposal_gen.py\n    - scripts/outreach_sequencer.py\n"
---
# B2B Sales Automation

## When to Use

**Trigger phrases:**
- "b2b sales automation"
- "Help me with b2b sales automation"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


Complete B2B sales pipeline: **Prospect → Qualify → Demo → Proposal → Negotiate → Close → Onboard**

---


## When NOT to Use

- When the prospect is not a good fit for your product
- For markets where you have no distribution channel
- When the deal size does not justify the effort


## Overview

B2B Sales Automation drives revenue generation with systematic processes.

## Pipeline Stages

1. **Prospect** — Identify and qualify potential customers
2. **Connect** — Initial outreach and conversation
3. **Discover** — Understand needs and pain points
4. **Propose** — Present tailored solution
5. **Close** — Negotiate and finalize agreement
6. **Onboard** — Hand off to success team

## Key Metrics

- Pipeline velocity (deals × value × win rate ÷ cycle time)
- Conversion rate per stage
- Average deal size
- Customer lifetime value (CLV)
- Win/loss ratio

## Best Practices

- Qualify early — disqualify fast
- Listen more than you talk (70/30 rule)
- Follow up consistently (5+ touches)
- Track everything in CRM
- Ask for referrals after every closed deal


## Workflow

```python
# Example: Lead scoring
def score_lead(lead: dict) -> int:
    score = 0
    if lead.get("company_size", 0) > 100: score += 20
    if lead.get("budget", 0) > 10000: score += 25
    if lead.get("timeline") == "immediate": score += 30
    if lead.get("engagement_level", 0) > 3: score += 25
    return min(score, 100)
```

1. **Understand requirements** — Clarify objectives and scope
2. **Set up tools** — Configure required tools and access
3. **Execute** — Perform the core operations
4. **Validate** — Verify results meet quality standards
5. **Document** — Record findings and decisions

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Cold outreach does not work" | It works when personalized and targeted. Generic spam does not. |
| "I will follow up later" | 80% of sales require 5+ follow-ups. Follow up consistently. |
| "Price is the only factor" | Value, trust, and timing matter more than price. Sell outcomes. |


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run b2b sales automation workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings