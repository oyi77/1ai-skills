---
name: sales-pipeline
description: AI-powered sales pipeline inside 1ai-social. Track leads, qualify with BANT, generate proposals, schedule follow-ups, and get daily sales analytics. Integrates with 1ai-engage leads.
domain: sales
tags:
- sales
- pipeline
- crm
- lead-scoring
- proposals
- follow-up
- b2b
- berkahkarya
- 1ai-social
version: 1.0.0
author: BerkahKarya
language: id-ID / en
---

# Sales Pipeline Skill (inside 1ai-social) 💼

## Overview

**Sales Pipeline** manages the full sales cycle inside 1ai-social — from lead capture through qualification (BANT), proposal generation, follow-up scheduling, and daily analytics. Integrates with 1ai-engage for lead data.


## When to Use

**Trigger phrases:**
- "sales pipeline"
- "track deal"
- "add lead to CRM"
- "sales report"
- "follow up"
- "generate proposal"
- "lead scoring"

**Use cases:**
- Managing B2B sales pipeline from lead to close
- Scoring and qualifying leads (BANT)
- Generating proposals and outreach messages
- Tracking follow-ups and daily sales queue
- Importing 1ai-engage leads into sales pipeline

**When NOT to use:**
- For marketing/social media tasks (use other 1ai-social tools)
- For customer support (use customer-support skill)

---


## When NOT to Use

- When the prospect is not a good fit for your product
- For markets where you have no distribution channel
- When the deal size does not justify the effort


## Architecture

Sales is built INTO 1ai-social as MCP tools (prefixed `sales_`).

```
1ai-social MCP Server (75 tools total)
├── Marketing tools (55) — content, social, engagement, growth
├── 1ai-engage tools — cold outreach pipeline
└── Sales tools (20) — lead → qualify → propose → close
```

## Pipeline Stages

```
NEW → CONTACTED → QUALIFIED → DEMO → PROPOSAL → NEGOTIATION → CLOSED_WON
  🔍      📞          📋        🎯      📄          💬           🤝
                                                            └──▶ CLOSED_LOST ❌
```

| Stage | Win Probability |
|-------|-----------------|
| New | 5% |
| Contacted | 10% |
| Qualified | 25% |
| Demo | 40% |
| Proposal | 60% |
| Negotiation | 80% |
| Closed Won | 100% |

## MCP Tools (20 sales_ tools)

### Lead Management
- `sales_add_lead` — Add new lead
- `sales_list_leads` — List with stage/grade filters
- `sales_get_lead` — Full details + activities + proposals
- `sales_update_lead` — Update fields

### Qualification
- `sales_qualify_lead` — BANT (auto-advances when all 4 confirmed)

### Pipeline
- `sales_move_lead` — Move to specific stage
- `sales_advance_lead` — Auto-advance to next stage

### Activities
- `sales_log_activity` — Log call/email/meeting/note
- `sales_get_activities` — Activity history

### Proposals
- `sales_create_proposal` — Create proposal
- `sales_send_proposal` — Mark as sent
- `sales_get_proposals` — List proposals
- `sales_generate_proposal_template` — AI-generated template

### Follow-ups
- `sales_schedule_follow_up` — Schedule with due date
- `sales_complete_follow_up` — Mark done
- `sales_get_follow_ups` — List pending

### Analytics
- `sales_pipeline_report` — Full pipeline analytics
- `sales_daily_queue` — Today's priority actions

### Integration
- `sales_import_from_engage` — Guide for importing 1ai-engage leads
- `sales_generate_outreach` — Personalized email/WA/LinkedIn

## Workflow: 1ai-engage → Sales

```
1. engage_list_leads(status='replied')     → get warm leads
2. sales_add_lead(source='engage', ...)    → import to pipeline
3. sales_qualify_lead(budget=True, ...)    → BANT qualify
4. sales_advance_lead()                    → move through stages
5. sales_generate_proposal_template()      → generate proposal
6. sales_create_proposal() → sales_send_proposal()
7. sales_schedule_follow_up()              → track follow-ups
8. sales_pipeline_report()                 → analytics
```

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Cold outreach does not work" | It works when personalized and targeted. Generic spam does not. |
| "I will follow up later" | 80% of sales require 5+ follow-ups. Follow up consistently. |
| "Price is the only factor" | Value, trust, and timing matter more than price. Sell outcomes. |

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings