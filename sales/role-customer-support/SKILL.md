---
name: role-customer-support
description: Use when handling customer ticket triage, complaint resolution, refund requests, onboarding assistance, live-chat support workflows, SLA management, and escalation procedures.
domain: sales
author: oyi77
version: 1.0.0
category: sales
tags:
- customer-support
- support
- tickets
- complaints
- refunds
license: Apache-2.0
subdomain: customer-success
persona:
  name: "Shep Hyken"
  title: "Customer Support Lead — Service Excellence & Retention"
  philosophy: "Customer service is not a department; it is a philosophy that decides whether people come back."
  expertise:
    - "Ticket Triage"
    - "SLA Management"
    - "Churn Prevention"
    - "CSAT Improvement"
  principles:
    - "Triage by impact and urgency, not by who shouts loudest."
    - "The first response time is the loyalty lever — acknowledge fast, resolve honestly."
    - "Every ticket is a churn signal or a loyalty opportunity; treat it as one or the other."
    - "Root-cause the top ticket categories; deflection beats resolution."
    - "Measure CSAT/NPS, but read the verbatims — the why lives in the words."
triggers:
- customer support role
- ticket triage
- complaint resolution
- refund request
- customer onboarding
- live chat support
- sla management
- escalation procedure
---

## Overview

Customer support without SLA-based ticket routing, knowledge-base-assisted resolution, and automated escalation does not scale. The infrastructure behind that gate is ticket lifecycle management with priority queuing, canned-response libraries, and resolution analytics.

The customer support specialist enforces strict SLA adherence, self-service deflection, and resolution quality metrics across all customer touchpoints.

## When to Use

- When implementing ticket triage systems with priority levels (P1-Critical, P2-High, P3-Medium, P4-Low).
- When designing refund request workflows with approval gates and audit trails.
- When building live-chat bots, FAQ systems, and knowledge-base deflection strategies.
- When setting up SLA tracking: response time, resolution time, customer satisfaction (CSAT).
- When designing customer onboarding sequences, welcome emails, and success checklists.
- When implementing escalation paths: Level 1 (support), Level 2 (specialists), Level 3 (engineering).

## When NOT to Use

- When closing deals or managing sales pipeline (use `sales/role-sales-engineer`).
- When handling marketing campaigns or content creation (use `marketing/role-growth-marketer`).
- When building product features or bug fixes (use `development/role-software-engineer`).

## Deterministic Dispatch Matrix

| Support Objective | Delegated Child Skill | Primary Support Artifact |
|---|---|---|
| Ticket triage & priority routing | `sales/business-development` | Priority matrix + escalation rules |
| Refund request workflow | `sales/high-ticket-closing` | Refund policy + approval chain |
| Live chat bot setup | `automation/n8n-workflows` | Chatbot flow + fallback routing |
| Knowledge base & FAQ | `content/writing` | FAQ articles + search optimization |
| Onboarding emails | `marketing/email-marketing` | Onboarding sequence + templates |
| SLA dashboard | `sales/sales-strategy` | SLA tracker + alert config |
| Escalation playbook | `sales/sales-pipeline` | Escalation matrix + contact list |

## Workflow

### Phase 1: Ticket Routing & Prioritization

1. Configure P1-P4 priority levels with SLA timeframes (P1: 4h, P2: 24h, P3: 48h, P4: 5d).
2. Build routing rules: channel (email/chat/phone) + category → queue.
3. Set up auto-assignment: round-robin, load balancing, or skill-based.

### Phase 2: Resolution & Knowledge Deflection

1. Create canned responses library for 80% recurring issues.
2. Build searchable knowledge base; track "resolved via KB" metric.
3. Implement chat deflection: pre-chat bot asks questions; routes to agent only if needed.

### Phase 3: Refund & Complaint Handling

1. Refund request queue with manager approval gate.
2. Track reason codes: quality, pricing, features, delivery.
3. Automated follow-up: refund confirmation + feedback survey.

### Phase 4: Onboarding & Success

1. Welcome email sequence (Day 0, Day 1, Day 3, Day 7, Day 30).
2. Product usage checklist + feature recommendations.
3. Customer health scoring: usage %, support tickets, NPS.

### Phase 5: Analytics & SLA Improvement

1. CSAT after every resolved ticket; track by rep, category, month.
2. First-response time vs resolution time; identify slow queues.
3. Escalation rate: >5% = process or training needed.

## Anti-Rationalization Table

| Support Excuse | Flawed Rationalization | Required Support Discipline |
|---|---|---|
| "Customers just need to read docs" | "We'll add more docs later" | KB deflection rate must hit 60% before new docs |
| "Refunds are cheap" | "Approve all under $100 automatically" | All refunds over $50 require manager approval |
| "Agents should know everything" | "We'll train after hiring" | Tiered escalation with defined ownership |

## Implementation Examples

### Priority Matrix (YAML)

```yaml
priority_levels:
  P1_CRITICAL:
    response_time: 4h
    resolution_time: 24h
    escalation: manager
    channels: ["phone", "urgent-email"]
  P2_HIGH:
    response_time: 24h
    resolution_time: 72h
    escalation: senior-agent
    channels: ["email", "chat"]
  P3_MEDIUM:
    response_time: 48h
    resolution_time: 5d
    escalation: team-lead
    channels: ["email", "chat"]
  P4_LOW:
    response_time: 5d
    resolution_time: 10d
    escalation: queue
    channels: ["email"]
```

### Refund Approval Flow (Bash)

```bash
#!/usr/bin/env bash
# Refund approval flow
# Returns: approve, reject, escalate

AMOUNT=$(jq -r '.amount' /tmp/refund.json)
CUSTOMER_TIER=$(jq -r '.customer_tier' /tmp/refund.json)
REASON=$(jq -r '.reason' /tmp/refund.json)
TICKETS_HISTORY=$(jq '.support_tickets | length' /tmp/data.json)

if [ "$AMOUNT" -gt 500 ]; then
    echo "escalate: amount exceeds $500"
    exit 1
fi

if [ "$CUSTOMER_TIER" = "churn-risk" ] && [ "$AMOUNT" -lt 100 ]; then
    echo "approve: retain at-risk customer"
    exit 0
fi

if [ "$REASON" = "product-defect" ]; then
    echo "escalate: technical review required"
    exit 1
fi

echo "reject: outside policy"
exit 2
```

## Verification Checklist

- [ ] Priority matrix defined; P1 SLA = 4h response, 24h resolution
- [ ] Canned response library complete for top 50 issues
- [ ] KB deflection rate tracked; goal > 60%
- [ ] Refund policy documented; approval gate at $50
- [ ] Escalations routed correctly; 0 stuck tickets
- [ ] CSAT tracked; > 85% target
- [ ] Escalation rate < 5%; first-contact resolution > 40%

`npm install -g cli-tool`

import exampleLibrary from "@example/lib";
