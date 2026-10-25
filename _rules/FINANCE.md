---
name: finance
version: 1.1.0
severity: mandatory
scope: [all]
pairs-with: [decision, roles, okr, security]
description: Budget approval, spending limits, invoicing, and revenue tracking
---

# FINANCE.md — Financial Protocol

> Every dollar in and out of BerkahKarya/1ai must be logged, authorized, and reviewed.
> Agents do not spend money without authority. Agents do not hide transactions.
> No autonomous spend without a matching log entry in DECISION.md.

---

## §1 SPENDING AUTHORITY LEVELS

Authority levels map to role levels defined in ROLES.md.

| Level | Role | Per-Transaction Limit | Monthly Limit | Restrictions |
|-------|------|-----------------------|---------------|--------------|
| L1 | Junior Agent | $0 | $0 | Cannot initiate any spend |
| L2 | Standard Agent | $0 | $0 | Cannot initiate any spend |
| L3 | Senior Agent | $10 | $50 | Pre-approved categories only (§2) |
| L4 | Lead Agent | $100 | $500 | Must log every transaction in DECISION.md |
| L5 | Owner (human) | Unlimited | Unlimited | All spending decisions are final |

Rules:
- Authority is per-agent, not per-session. An agent cannot claim higher authority because it is running an urgent task.
- Combined spend across multiple L3 agents in the same 24-hour window counts toward the monthly L3 cap collectively.
- If a transaction would push cumulative monthly spend past the limit, it requires the next authority level's approval before execution.
- Approval granted in a prior session does NOT carry forward. Each transaction requires current-session authorization unless covered by §2.

---

## §2 PRE-APPROVED SPENDING CATEGORIES

L3 agents may spend within limits (§1) in these categories without per-transaction approval:

### 2.1 API Calls
- Services in the owner-maintained approved-services list (stored in `~/.1ai/config/approved-services.json`)
- Rate: must not exceed the monthly API budget line in the current budget
- Condition: service is already in use (not a new integration)

### 2.2 Infrastructure — Renewals Only
- Hosting, VPS, domain renewals for services already running
- No new infrastructure without L5 approval
- Renewals must match current tier — no auto-upgrades

### 2.3 Tool Renewals
- Software subscriptions already active, renewing at the same price tier
- If price has increased >10% from last renewal → escalate for L5 approval before renewing

### 2.4 Explicitly Out of Scope (always requires approval)
- New services, new integrations, new accounts
- One-time purchases above $10
- Any spend not clearly matching a line above
- Advertising or paid promotion of any kind
- Freelancer or contractor payments

---

## §3 APPROVAL PROCESS FOR NEW SPENDING

When an agent needs to spend outside §2 or above its authority level:

**Step 1 — Proposal (agent)**
Agent submits spend proposal with:
```
SPEND PROPOSAL
Agent: [agent id]
Amount: $[amount] ([currency])
Vendor/Service: [name]
Category: [new service / upgrade / one-time / other]
Business justification: [1-2 sentences — what problem does this solve?]
KR it advances: [OKR key result reference from OKR.md]
Alternatives considered: [what was ruled out and why]
Reversible: [yes/no — can this be cancelled/refunded?]
```

**Step 2 — Owner review**
- Owner approves or rejects within 24 hours via the configured channel.
- Silence is NOT approval. Agent waits.
- If 24 hours pass with no response: agent re-notifies once, then waits another 24 hours. If still no response: task is paused, not executed.

**Step 3 — Logging**
Upon approval:
- Agent logs in DECISION.md: proposal text, owner approval statement (verbatim), timestamp, transaction ID or receipt reference.
- Receipt or confirmation must be attached (screenshot, email forward, or URL) within 48 hours of transaction.

**Step 4 — Monthly report inclusion**
Every approved spend automatically appears in the next monthly finance report (§6).

---

## §4 REVENUE TRACKING

Every revenue event — regardless of amount — must be logged within 24 hours.

**Required fields per revenue event:**
```
Revenue Event
Date: [YYYY-MM-DD]
Source: [platform / client name]
Product/Service: [what was sold]
Amount: [gross amount] [currency]
Net after fees: [amount after payment processor fees]
Payment method: [Stripe / bank transfer / etc.]
Invoice number: [if applicable]
Notes: [optional — recurring, one-time, refund, partial]
```

**Revenue log location:** `~/.1ai/data/finance/revenue-[YYYY-MM].json`

**Finance Agent responsibilities:**
- Aggregate all revenue events into a monthly total by the 2nd of each month
- Flag any revenue source not seen in the prior 3 months (new = verify legitimacy)
- Flag any refund or chargeback immediately on detection
- Generate monthly revenue report for §6 review

---

## §5 INVOICE PROTOCOL

Every invoice issued to a client must include:

| Field | Requirement |
|-------|-------------|
| Invoice number | Sequential, format: INV-[YYYY]-[NNN] (e.g. INV-2026-001) |
| Issue date | Date invoice was sent |
| Due date | Issue date + 7 days (Net 7 default; override requires owner instruction) |
| Billed to | Client name, entity, address |
| Itemized services | Each line: description, quantity/hours, unit rate, line total |
| Subtotal | Sum before tax |
| Tax | If applicable, stated as line item with percentage |
| Total due | Final amount in agreed currency |
| Payment methods | All accepted methods listed with account details |
| Late payment terms | "Invoices unpaid after 14 days incur 1.5% monthly interest" |
| BerkahKarya contact | Owner email for disputes |

**Invoice numbering** is maintained by the Finance Agent. Gap in sequence = must be explained.

**Overdue tracking:** Finance Agent checks outstanding invoices weekly. At 7 days overdue: send reminder. At 14 days: notify owner. At 30 days: owner decides on escalation.

---

## §6 MONTHLY FINANCE REVIEW

**When:** First Monday of each month, owner reviews the monthly finance package.

**Finance Agent prepares by end of last day of month:**

1. **Revenue summary**
   - Total gross revenue
   - Revenue by source/product
   - MoM change (amount and %)
   - Outstanding invoices

2. **Spend summary**
   - Total spend by category
   - Budget vs. actual (per category)
   - Largest transactions (top 5)
   - Any transactions flagged by §7

3. **Runway estimate**
   - Current cash/balance
   - Monthly burn rate (3-month average)
   - Estimated runway in months

4. **Exceptions log**
   - Any escalations triggered (§7)
   - Any spend proposals approved or rejected
   - Any invoices overdue

**Report location:** `~/.1ai/data/finance/monthly-report-[YYYY-MM].md`

Owner verdict after review: APPROVED / APPROVED WITH NOTES / REQUIRES ACTION.
Verdict logged in DECISION.md with date.

---

## §7 FINANCIAL ALERTS

Finance Agent or any agent executing a financial action MUST notify the owner **immediately** (not at next review) when:

| # | Condition | Alert Content |
|---|-----------|---------------|
| F1 | Monthly spend has reached 80% of budget | Current spend, remaining budget, projected end-of-month total |
| F2 | Revenue drops >20% week-over-week | Week-over-week comparison, suspected cause if known |
| F3 | Any single transaction >$50 attempted without current-session approval | Transaction details, which agent attempted it, stopped or allowed |
| F4 | A payment processor flags a chargeback or dispute | Client name, invoice number, amount, current status |
| F5 | An invoice is 14+ days overdue | Client, amount, days overdue, history of contact attempts |
| F6 | Any unrecognized charge appears in connected accounts | Vendor, amount, date, action taken (flagged/disputed) |

**Alert format (minimum):**
```
FINANCE ALERT [F-number]
Amount: $[amount]
Detail: [one sentence description]
Action taken: [what agent did — stopped, flagged, logged]
Owner input needed: [yes/no — if yes, what specifically?]
```

Alerts sent to owner's configured notification channel (Telegram by default).
Every alert is also logged in DECISION.md.

---

## §8 FINANCIAL DATA INTEGRITY

- All finance logs are append-only. No deletion, no retroactive edits.
- If an error is found in a past entry: add a correction entry with timestamp and reason. Never overwrite.
- Finance data files are included in the daily backup scope (see SECURITY.md).
- Finance Agent does not have authority to approve its own spend proposals.
- No agent may read another agent's API keys or payment credentials unless explicitly granted in ROLES.md.


---

## §9 FRAUD DETECTION & ANOMALY THRESHOLDS

> Finance Agent and Monitoring Agent both run these checks. Either may trigger an alert.

### Automatic Alert Triggers

The following conditions MUST trigger an immediate Telegram alert to L5 Owner, regardless of business hours:

| Condition | Threshold | Alert severity | Action before alerting |
|---|---|---|---|
| Single outbound transaction | > $200 | P0 | Log in DECISION.md, halt transaction if not yet executed |
| Daily outbound spend total | > $300 | P0 | Log all transactions in DECISION.md |
| Monthly spend run-rate | > 80% of monthly budget before month midpoint | P1 | Generate spend breakdown |
| Unrecognized vendor | Any spend to a vendor not in approved vendor list | P1 | Flag transaction, do not pay until approved |
| MRR drop | > 15% in a single day | P0 | Pull churn/failed-charge report from Stripe |
| Failed charge volume | > 5 failed charges in 24h | P1 | Pull Stripe failed_payment_intent list |
| Duplicate transaction | Same vendor + same amount within 48h | P1 | Cross-check against DECISION.md log |
| New subscription added | Any recurring charge not in approved vendor list | P1 | Identify source, flag for approval |
| API key spend spike | Any single API provider bill > 2× prior month | P1 | Pull usage breakdown before alerting |

### Approved Vendor List
Maintained in `finance/approved-vendors.csv`. Format: `vendor_name, category, max_monthly_usd, approved_by, approved_date`.
New vendors require L4 approval (≤ $50/month) or L5 approval (> $50/month) before first payment.

### Anomaly Response Protocol
1. **Detect** — Monitoring Agent or Finance Agent identifies threshold breach.
2. **Halt** — If transaction is pending: do not execute until reviewed. If already executed: flag in log.
3. **Log** — Append entry to `logs/finance/anomalies/YYYY-MM-DD.md` with: what, amount, vendor, timestamp, trigger rule.
4. **Alert** — Telegram to L5 with full context (see §5 alert format).
5. **Await** — Do not resume affected spend category until L5 responds.
6. **Resolve** — L5 approves (proceed) or rejects (reverse if possible, document if not).

Current version: 1.1.0
Last reviewed: 2026-07-06
Next scheduled review: 2027-01-06 (semi-annual)
