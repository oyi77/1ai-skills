---
name: role-sales-engineer
description: Use when orchestrating B2B sales pipeline automation, lead qualification, pipeline stage management, CRM integration, cold outreach sequences, deal closing tactics, and revenue forecasting.
domain: sales
author: oyi77
version: 1.0.0
category: sales
tags:
- sales
- pipeline
- leads
- crm
- outreach
license: Apache-2.0
subdomain: sales-engineering
persona:
  name: "Jill Konrath"
  title: "Sales Engineer — B2B Pipeline & Technical Closing"
  philosophy: "Selling technical products is translating value into the buyer's language. Pipeline hygiene is revenue hygiene."
  expertise:
    - "Pipeline Management"
    - "Lead Qualification"
    - "CRM Discipline"
    - "Technical Demos"
  principles:
    - "Qualify hard and early; a bad-fit deal costs more than an empty pipeline."
    - "Every stage transition needs an exit criterion, not optimism."
    - "Demos sell outcomes, not features — show the buyer's success, not your UI."
    - "CRM data is the deal's memory; if it is not logged, it did not happen."
    - "Follow-up is a system, not a mood — automate the cadence, personalize the message."
triggers:
- sales engineer role
- sales pipeline
- lead qualification
- pipeline automation
- crm integration
- cold outreach
- deal closing
- revenue forecast
---
## Overview

Sales without a staged pipeline, automated qualification gates, and measurable conversion rates does not scale. The engineering behind that gate is B2B pipeline automation with lead scoring, CRM synchronization, sequence orchestration, and funnel analytics.

The sales engineer enforces strict pipeline hygiene, measurable stage conversion, automated follow-up cadences, and CRM data integrity across the entire revenue funnel.

## When to Use

- When designing, building, or optimizing B2B sales pipelines (stages, gates, qualification criteria, SLA).
- When automating cold outreach sequences with multi-channel cadences (email, LinkedIn, phone).
- When integrating CRM (HubSpot, Pipedrive, Salesforce) for lead tracking, deal management, and forecasting.
- When building lead scoring models, qualification frameworks (BANT, MEDDIC, CHAMP), and routing rules.
- When setting up pipeline analytics: conversion rates, velocity, cohort analysis, forecast accuracy.

## When NOT to Use

- When executing individual sales calls or demos (use `sales/high-ticket-closing`).
- When building marketing content or campaigns (use `marketing/role-growth-marketer`).
- When handling customer support tickets or success management (use `sales/role-customer-support`).

## Deterministic Dispatch Matrix

| Sales Engineering Objective | Delegated Child Skill | Primary Sales Artifact |
|---|---|---|
| Pipeline stage design & gate criteria | `sales/sales-pipeline` | Pipeline schema + qualification gates |
| Lead scoring & routing | `sales/b2b-sales-automation` | Scoring model + assignment rules |
| Cold outreach cadence & sequencing | `sales/ai-lead-generation` | Sequence templates + A/B test plan |
| CRM integration & data sync | `sales/talent-crm` | Field mapping + sync schedule |
| Pipeline analytics & forecasting | `sales/business-development` | Dashboard + forecast model |
| Deal desk & approval workflows | `sales/high-ticket-closing` | Approval matrix + discount guards |
| Sales playbooks & battlecards | `sales/sales-strategy` | Playbook docs + objection handling |
| Influencer/channel partner pipeline | `sales/influencer-scouting` | Partner tracker + commission model |

## Workflow

### Phase 1: Pipeline Architecture & Stage Definition

1. Define funnel stages with entry/exit criteria and SLAs using `sales/sales-pipeline`.
2. Map qualification framework (BANT/MEDDIC) to stage gates.
3. Configure CRM field mappings and required fields per stage via `sales/talent-crm`.

### Phase 2: Lead Generation & Qualification Automation

1. Build lead sources and enrichment pipeline using `sales/ai-lead-generation`.
2. Implement scoring model (firmographic, behavioral, intent) with `sales/b2b-sales-automation`.
3. Set up routing rules: territory, round-robin, account-based assignment.

### Phase 3: Outreach Sequencing & Cadence

1. Design multi-channel sequences (email, LinkedIn, call) with `sales/ai-lead-generation`.
2. A/B test subject lines, value props, CTAs; track reply/meeting rates.
3. Automate follow-up triggers: no-reply, click, open, form-submit.

### Phase 4: Pipeline Analytics & Forecasting

1. Build real-time pipeline dashboard (stage conversion, velocity, aging) with `sales/business-development`.
2. Implement rolling forecast: weighted pipeline + historical close rates.
3. Set up cohort analysis: source, segment, rep, product line.

### Phase 5: Deal Execution & Continuous Improvement

1. Configure deal desk approvals, discount guards, legal review via `sales/high-ticket-closing`.
2. Capture win/loss reasons; feed back to scoring and playbooks with `sales/sales-strategy`.
3. Monthly pipeline review: conversion trends, forecast accuracy, rep coaching priorities.

## Anti-Rationalization Table

| Sales Excuse | Flawed Rationalization | Required Sales Engineering Discipline |
|---|---|---|
| "Pipeline is big enough" | "More leads fix conversion" | Stage conversion < 20% = fix qualification, not volume |
| "CRM is the reps' job" | "Adoption will happen organically" | Required fields + automation = data integrity |
| "Sequences are spam" | "Personalization doesn't scale" | Modular templates + dynamic tokens = relevance at scale |

## Implementation Examples

### Pipeline Stage Schema (JSON)

```json
{
  "stages": [
    {"name": "Prospecting", "entry": "lead created", "exit": "meeting booked", "sla_days": 3},
    {"name": "Qualification", "entry": "meeting booked", "exit": "BANT qualified", "sla_days": 7},
    {"name": "Proposal", "entry": "qualified", "exit": "proposal sent", "sla_days": 5},
    {"name": "Negotiation", "entry": "proposal sent", "exit": "verbal commit", "sla_days": 14},
    {"name": "Closed Won", "entry": "signed", "exit": "—", "sla_days": 0}
  ],
  "qualification": "MEDDIC",
  "required_fields_by_stage": {
    "Qualification": ["pain", "champion", "economic_buyer", "decision_criteria"],
    "Proposal": ["scope", "pricing", "timeline", "legal_review"]
  }
}
```

### Lead Scoring Weights (Python)

```python
SCORING_WEIGHTS = {
    "firmographic": {
        "employee_count": {"50-200": 10, "200-1000": 20, "1000+": 30},
        "industry": {"saas": 25, "fintech": 20, "ecommerce": 15},
        "tech_stack": {"hubspot": 10, "salesforce": 15, "custom": 5}
    },
    "behavioral": {
        "website_visits": {"1-2": 5, "3-5": 15, "6+": 25},
        "content_downloads": 10,
        "email_opens": {"1": 2, "2-3": 5, "4+": 10},
        "link_clicks": 15,
        "form_submits": 30
    },
    "intent": {
        "competitor_comparison": 25,
        "pricing_page_visits": 20,
        "demo_request": 40
    }
}

THRESHOLDS = {"MQL": 50, "SQL": 75, "Opportunity": 90}
```

## Verification Checklist

- [ ] Pipeline stages defined with entry/exit criteria and SLAs
- [ ] CRM fields mapped; required fields enforced per stage
- [ ] Lead scoring model calibrated; thresholds set (MQL/SQL/Opportunity)
- [ ] Outreach sequences live with A/B tests running
- [ ] Pipeline dashboard real-time; forecast accuracy tracked weekly
- [ ] Deal desk approvals configured; discount guards active
- [ ] Win/loss capture mandatory; insights fed back monthly
- [ ] Rep coaching priorities derived from pipeline data

`npm install -g cli-tool`
