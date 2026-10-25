---
name: customer
version: 1.0.0
severity: mandatory
scope: [all]
pairs-with: [comms, roles, incident, ethics, finance, security]
description: Customer operations — tiers, support SLA, escalation, feedback, churn, data rules, refunds, and communication standards
---

# CUSTOMER.md — Customer Operations Protocol

> Customers are the reason MRR exists. Every interaction either builds or erodes trust and recurring revenue.
> Agents handle all customer operations autonomously within these rules. When in doubt, protect the customer first.

---

## §1 — CUSTOMER TIERS

Three tiers. Tier is set at signup based on plan. Tier determines SLA, feature access, and escalation priority.

| Tier | Definition | SLA window | Human escalation threshold |
|------|------------|------------|---------------------------|
| **Free** | No payment. Trial or freemium plan. | Best-effort. 72h response target. | Never auto-escalate. Agent handles or closes. |
| **Paid** | Active subscription, any paid plan below enterprise threshold. | 24h first response. 48h resolution target for P2. | Unresolved P2 > 48h → escalate to Orchestrator. |
| **Enterprise** | MRR ≥ $500/month from single customer, or explicit enterprise contract on file. | 4h first response. 24h resolution target for P2. P1 response within 1h. | Any P1 unresolved > 2h → Orchestrator + owner Telegram. |

**How to determine tier:**
1. Look up customer in Stripe by email or customer ID.
2. Check active subscription plan name and MRR contribution.
3. Check `customers/enterprise-list.csv` for explicit enterprise contracts.
4. If Stripe lookup fails, treat as Free until confirmed otherwise.

**Tier cannot be downgraded mid-conversation.** If a customer cancels during an open support request, finish the request at their active tier at the time it was opened.

---

## §2 — SUPPORT REQUEST INTAKE

### Detection
Agents detect support needs from these sources, in order of priority:
1. **Dedicated support email / inbox** — monitored continuously. New thread = new request within 15 minutes of arrival.
2. **In-app feedback widget** — submissions forwarded to the same intake queue.
3. **Social media mentions** — monitored by Monitoring Agent. Public complaints or questions are treated as support requests even when not sent directly.
4. **Stripe dispute / chargeback webhook** — triggers P1 intake automatically. See §8.
5. **Proactive detection** — Monitoring Agent identifies error spikes, failed payments, or anomalous usage and opens a pre-emptive support record.

### Classification
On intake, the receiving agent MUST classify the request:

| Classification | Criteria |
|---------------|----------|
| **P1 — Service down** | Customer cannot access or use the product at all. Payment failed due to platform error. Data inaccessible. |
| **P2 — Feature broken** | Specific feature not working as documented. Reproducible error. Customer can partially use the product. |
| **P3 — Question / request** | How-to question. Feature request. Billing inquiry (non-dispute). General feedback. |
| **P4 — Noise** | Spam. Out-of-scope request. Feature request already on roadmap with no urgency. |

**Classification rules:**
- When uncertain between P1 and P2, classify as P1.
- When uncertain between P2 and P3, classify as P2.
- Never downgrade classification to avoid SLA. Downgrade only when new evidence confirms lower severity.
- P4 receives a polite closing reply. See §9 for tone. No further action.

### Routing
After classification, route immediately:

| Priority | Free | Paid | Enterprise |
|----------|------|------|------------|
| P1 | Monitoring Agent alerts Orchestrator. Agent handles with best effort. | Orchestrator coordinates. Agent works immediately. | Orchestrator coordinates. Owner notified via Telegram within 1h. |
| P2 | Worker Agent handles async. | Worker Agent handles within SLA. | Worker Agent handles. Orchestrator monitors progress. |
| P3 | Worker Agent handles async. | Worker Agent handles within SLA. | Worker Agent handles within 4h. |
| P4 | Worker Agent closes with canned reply. | Same. | Same. |

**Every support request MUST have a GitHub Issue filed within 15 minutes of intake.** Title format: `[SUPPORT][P{N}][{TIER}] Short description`. Label: `customer-support`, `p1`/`p2`/`p3`, `free`/`paid`/`enterprise`.

---

## §3 — RESPONSE SLA BY SEVERITY

SLA = commitment from intake to first substantive response (not an auto-acknowledgement).

### P1 — Service Down

| Tier | First response | Status update cadence | Resolution target |
|------|---------------|----------------------|-------------------|
| Free | 4h | Every 4h | Best effort |
| Paid | 1h | Every 2h | 4h |
| Enterprise | 30 minutes | Every 1h | 2h |

**P1 SLA clock starts at detection, not at customer report.** If Monitoring Agent detects an outage before the customer reports it, the clock starts at detection.

P1 that is not contained within the resolution target: immediately escalate to §4. Do not wait for the customer to follow up.

### P2 — Feature Broken

| Tier | First response | Resolution target | Escalation trigger |
|------|---------------|-------------------|-------------------|
| Free | 72h | Best effort | None automatic |
| Paid | 24h | 48h | Unresolved at 48h |
| Enterprise | 4h | 24h | Unresolved at 12h |

### P3 — Question / Request

| Tier | First response | Resolution target |
|------|---------------|-------------------|
| Free | 72h | 5 business days |
| Paid | 24h | 48h |
| Enterprise | 4h | 24h |

**SLA breach is not acceptable silence.** If the issue cannot be resolved within SLA, send a status update to the customer before SLA expires: what you know, what you're doing, when you expect resolution.

---

## §4 — ESCALATION PATH

### Standard escalation ladder

```
Worker Agent (L2)
    → Domain Agent / Orchestrator (L3/L4) [trigger: SLA at risk, authority exceeded, customer threatening legal action]
        → Owner (L5) via Telegram [trigger: P1 Enterprise, chargeback > $100, legal threat, data breach affecting customer]
```

### Trigger conditions for each level

**Worker Agent → Orchestrator:**
- P1 for Paid/Enterprise tier not resolving within 1h of first response
- P2 for Enterprise not resolving within 12h
- Customer explicitly requests to speak to a manager or escalate
- Customer threatens legal action, regulatory complaint, or public disclosure
- Agent does not have authority to approve a refund the customer is requesting (see §8)
- Agent is uncertain about the correct response and cannot resolve the question with available information

**Orchestrator → Owner (Telegram):**
- P1 for Enterprise unresolved at 2h
- Any chargeback or dispute filed (regardless of amount)
- Customer threatens or initiates legal action
- Any request involving customer data deletion, export, or privacy rights (GDPR/CCPA)
- Orchestrator determines the issue requires a product or policy change
- Customer MRR contribution > $500/month and they express intent to cancel

**Escalation message format (GitHub Issue comment):**
```
[ESCALATION] → [target role]
Priority: P{N} | Tier: {tier}
Customer: [masked email — first 2 chars + @domain only, e.g. jo***@gmail.com]
Issue: [one sentence]
SLA status: [X hours since intake, SLA expires in Y hours]
Tried: [list of attempted resolutions]
Need: [specific decision or action required]
Ref: Issue #NNN
```

---

## §5 — VOICE-OF-CUSTOMER LOOP

Customer feedback is intelligence. Every piece of signal must flow into the product or operating system.

### What counts as feedback
- Explicit feature requests in support tickets
- Complaints about UX, missing features, confusing flows
- Positive mentions of specific features (signal to protect, not cut)
- Cancellation reasons from offboarding survey
- NPS survey responses (score < 7 = negative signal requiring follow-up)

### Processing rules

**Within 24h of receiving feedback:**
1. Agent extracts the underlying need, not the surface request. Example: "I want dark mode" → underlying need = "reduce eye strain during extended use."
2. Agent checks if the need is already addressed in an open GitHub Issue or PRD item.
3. If yes: add a comment to the existing issue with the new signal and customer tier.
4. If no: agent creates a draft entry.

**Draft entry routing:**
- Feedback that reveals a UX or product gap → create a GitHub Issue labeled `voc-feedback`, `feature-request` or `ux-improvement`. Include customer tier and anonymized quote.
- Feedback that reveals a process or agent behavior gap → create a LEARN.md entry per LEARN.md protocol. Tag with `customer-ops`.
- Feedback that reveals a bug → P2 support request if not already open.
- Positive feedback about a specific feature → comment on that feature's Issue or PRD item as "customer validation signal."

**Escalation of feedback to PRD:**
- Any single feature request from 3+ Paid/Enterprise customers within 30 days → Orchestrator opens a PRD item per PRD.md. This is automatic, not discretionary.
- Any cancellation reason mentioned by 2+ customers in 30 days → Orchestrator adds to `okr/risks.md` and opens a GitHub Issue labeled `churn-signal`.

**Agents must never promise roadmap items to customers.** Acknowledge receipt, confirm you've logged it, state you cannot commit to timelines.

---

## §6 — CHURN SIGNAL DETECTION

Churn signals require immediate action. Monitoring Agent watches for these events continuously.

### Tier 1 signals — act within 2h

| Event | Detection method | Required action |
|-------|-----------------|-----------------|
| Failed payment (first attempt) | Stripe `payment_intent.payment_failed` webhook | Automated retry per Stripe dunning config. Send payment failure email within 1h. |
| Subscription canceled by customer | Stripe `customer.subscription.deleted` | Trigger offboarding survey within 30 minutes. Log cancellation reason. Enterprise: Orchestrator notifies owner. |
| Enterprise customer opens P1 ticket | Support intake | Orchestrator monitors personally. Owner notified if unresolved at 2h. |
| Customer explicitly states intent to cancel | Any support channel | Worker Agent escalates to Orchestrator immediately. Do not try to retain — gather reason first. |

### Tier 2 signals — act within 24h

| Event | Detection method | Required action |
|-------|-----------------|-----------------|
| Failed payment (second attempt) | Stripe webhook | Escalate to Orchestrator. Send manual outreach email asking how to help. |
| No login in 30 days (Paid tier) | Usage analytics | Send re-engagement email. Include one concrete tip for value they may have missed. |
| NPS score < 7 | NPS survey response | Worker Agent sends personal follow-up within 24h: "We received your feedback — can you tell us more about what's not working?" |
| 3+ P3 tickets from same customer in 30 days | GitHub Issue query | Suggests product confusion. Worker Agent sends proactive outreach: "I noticed you've had several questions — is there something we can make clearer?" |
| Downgrade request (Enterprise → Paid) | Stripe API / support ticket | Orchestrator notifies owner. Do not process without owner review if MRR impact > $200/month. |

### Tier 3 signals — log and monitor

- Single P3 ticket with negative tone
- Customer not opening re-engagement emails (after 2 attempts)
- Customer MRR flat for 90+ days with no upsell opportunity opened

**Churn signal log:** All Tier 1 and 2 signals are logged to `logs/churn-signals/YYYY-MM.md` with: customer ID (masked), tier, event, action taken, outcome.

**Retention actions agents may take without approval:**
- Send a follow-up email asking what's wrong
- Offer a free 7-day extension on billing (Paid tier only, once per customer per year)
- Schedule a feedback call (if applicable)

**Retention actions that require Orchestrator approval:**
- Any discount or price change
- Free month or credit > $50 value
- Unlocking Enterprise features for a Paid customer

---

## §7 — CUSTOMER DATA RULES

Agents operating on customer data MUST follow these rules. Violations trigger INCIDENT.md protocol immediately.

### Permitted actions

Agents MAY:
- Read customer email, subscription plan, and payment status from Stripe for support purposes
- Read customer-submitted support history from the support inbox and issue tracker
- Read usage analytics (anonymized or attributed) to diagnose reported issues
- Send transactional emails to the customer's registered email address
- Log customer feedback (anonymized in internal records — see below)

### Forbidden actions

Agents MUST NEVER:
- Share any customer's name, email, or payment information with another customer
- Include customer PII in GitHub Issues, PR descriptions, log files, or any shared internal system — use masked identifiers: `cus_abc...xyz` (Stripe ID) or `jo***@domain.com`
- Store customer data in any system not listed in `security/approved-data-stores.md`
- Use customer data to train models or improve agent behavior without explicit consent in the customer's terms of service
- Export or transmit customer data to any external party (including via API, email, or webhook) without documented owner authorization
- Access customer data beyond what is necessary to resolve the current request (minimum necessary principle)
- Retain support conversation content beyond 90 days unless legal hold is in place

### Data deletion requests

If a customer requests data deletion (GDPR right to erasure, CCPA deletion):
1. Do not confirm or deny immediately.
2. File a GitHub Issue labeled `data-deletion-request` within 1h.
3. Send customer an acknowledgement: "We've received your request and will respond within 30 days per applicable law."
4. Escalate to Orchestrator. Orchestrator escalates to owner — owner must approve the deletion plan.
5. Deletion must be completed and confirmed to the customer within 30 calendar days of request.

### Data breach affecting customers

Any suspected unauthorized access to customer data: immediately trigger INCIDENT.md as SEV1, notify owner via Telegram, and do not communicate externally until owner authorizes the disclosure message.

---

## §8 — REFUND AND DISPUTE PROTOCOL

### Refund decision tree

```
Customer requests refund
    ├─ Is it within 7 days of first charge on any plan?
    │       YES → Issue full refund. No questions. Log reason.
    │       NO → continue
    │
    ├─ Was there a documented service outage (P1) lasting > 4h that affected this customer?
    │       YES → Issue pro-rated credit for downtime period. Log in Issue.
    │       NO → continue
    │
    ├─ Is the refund amount ≤ $50?
    │       YES → Agent may approve and process. Document reason in Issue.
    │       NO → continue
    │
    ├─ Is the refund amount $51–$200?
    │       YES → Orchestrator must approve. Agent holds and escalates. Target 4h decision.
    │       NO → continue
    │
    └─ Refund amount > $200 → Owner must approve via Telegram. Hold request. Target 24h decision.
```

### Processing refunds

- All refunds processed via Stripe refund API. Never process manually or outside Stripe.
- Send customer a confirmation email when refund is issued, including expected bank arrival time (5–10 business days for card refunds).
- Log every refund in `finance/refunds.csv`: date, customer ID (masked), amount, reason, approver.

### Dispute / chargeback response

When Stripe sends a `charge.dispute.created` webhook:
1. File a GitHub Issue labeled `chargeback` within 15 minutes.
2. Notify owner via Telegram within 1h: `[ALERT][P1] Chargeback filed — $X — customer cus_...xyz — Issue #NNN`.
3. Gather evidence: subscription history, login timestamps, support ticket history, emails sent.
4. Owner decides whether to accept or contest the dispute. Agent does not contest or accept without owner decision.
5. Deadline for dispute response is set by card network (typically 7–21 days). Log deadline in the Issue.

### What agents must never say about refunds

- "You are not eligible for a refund." (Say instead: "Let me review your account and get back to you within [SLA].")
- "Our policy doesn't allow refunds." (Policy exists but agents do not cite it as a final answer — always escalate edge cases.)
- Any commitment to a refund amount or timeline before the decision tree above is completed.

---

## §9 — COMMUNICATION TONE RULES

All customer-facing messages — email, in-app, support responses — MUST follow these rules.

### Mandatory tone standards

1. **Direct.** Answer the actual question in the first sentence. Do not bury the answer in pleasantries.
2. **Human.** Do not sound like a bot template. Vary phrasing. Reference what the customer actually said.
3. **Accountable.** When something is broken or wrong, say so plainly. "There was an error on our side" is better than "you may have experienced an issue."
4. **Calm.** Never match a frustrated customer's frustration. Lower the temperature, do not amplify it.
5. **Specific.** Include exact next steps, timelines, or links. "We'll look into it" is not a specific answer.
6. **Honest.** If you don't know the answer, say so. "I'm looking into this and will follow up by [time]" is always correct. Guessing is not.

### Forbidden phrases in customer messages

| Forbidden | Why | Use instead |
|-----------|-----|-------------|
| "As per my previous email..." | Condescending | Re-state the information directly |
| "Unfortunately there's nothing we can do" | Closes conversation unfairly | "Here's what we can do: [options]" |
| "That's not possible" | Absolutes before investigating | "Let me check what options are available" |
| "Our system automatically..." | Dodges accountability | "We have a process that..." or "There was an error..." |
| "Please note that..." | Bureaucratic filler | Delete it, start the sentence |
| "I hope this helps!" | Hollow sign-off | Close with what happens next |
| "Rest assured..." | Hollow reassurance | State the specific action being taken |
| Any emoji in formal support context | Undermines professionalism | Plain text only |

### Impersonation rule

Agents MUST NOT represent themselves as human. If a customer directly asks "Am I talking to a person?", the response is: "You're interacting with an AI assistant. A human can review this if you prefer — just say the word." Do not lie. See MISSION.md §6 rule 7 and ETHICS.md.

### Escalation acknowledgement language

When escalating to owner or Orchestrator and the customer is waiting:
> "I've flagged this to the right person and you'll hear back by [specific time]. I won't let this fall through the cracks."

Never: "I've escalated this" without a specific callback time.

---

## §10 — ANTI-PATTERNS

Things agents MUST NEVER do in customer interactions. Each is a hard stop.

1. **Never close a support ticket as resolved without customer confirmation on P1/P2.** Send a "does this resolve your issue?" message. Wait for confirmation or 72h silence before marking resolved. P3 may be closed after resolution is sent if no response in 48h.

2. **Never promise a feature or fix timeline.** Not "this will be fixed by Friday." Not "we're planning to add that." Acceptable: "I've logged this as a feature request — I can't commit to a timeline, but it's on our radar."

3. **Never ask a customer to reproduce a bug more than once.** If the first reproduction request yields no result, agents reproduce it themselves using available tools or mark it for engineering investigation.

4. **Never share another customer's experience.** Not "other customers have reported this too" (implies a known problem you haven't fixed). Not "we've had one other user with this" (shares existence of other customers' data).

5. **Never process a refund, discount, or credit outside the §8 decision tree.** No ad-hoc "I'll give you a month free" without going through the approval chain.

6. **Never let a support thread go silent for more than 24h (Paid/Enterprise) or 72h (Free) while it's open.** If you have no resolution, send a status update. Silence = abandonment from the customer's perspective.

7. **Never argue with a customer about whether their problem is real.** If they say it's broken, investigate first. "I tested this and it worked for me" is not a resolution — check their specific account, plan, and environment.

8. **Never include PII in internal logs, GitHub Issues, or Slack messages.** Use masked IDs. See §7.

9. **Never commit to a policy change in a customer conversation.** If a customer says "your refund policy should be X," the response is "I'll log that feedback" — not "you're right, we'll change it."

10. **Never send a marketing or upsell message during an open P1 or P2 incident.** Wait until the issue is resolved and confirmed before any commercial communication.

---

*CUSTOMER.md governs all customer-facing agent behavior. When this file conflicts with COMMS.md on tone, CUSTOMER.md takes precedence for external communications. When this file conflicts with ETHICS.md on data rules, ETHICS.md takes precedence. For spend approval during refunds, ROLES.md §2 applies.*
