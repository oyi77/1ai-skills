---
name: cost
version: 1.0.0
severity: mandatory
scope: [all]
pairs-with: [finance, decision, okr, roles, security]
description: Cost classification, attribution, unit economics, and cloud/AI spend governance
---

# COST.md — Cost Governance Protocol

> Every dollar spent is a bet against future MRR. No cost is neutral.
> Agents do not spend without classification. Untagged spend is blocked spend.
> Cost without a revenue justification is waste until proven otherwise.

---

## §1 — COST CLASSIFICATION

Every recurring and one-time cost MUST be assigned exactly one of the following four classes at the time it is logged.

### 1.1 COGS — Cost of Goods Sold (Direct)

Costs that scale directly with delivering a product or service to a paying customer.
If the cost disappears when a product is turned off, it is COGS.

Examples:
- LLM/AI API tokens consumed to serve a customer request
- Payment processor fees (Stripe, Midtrans) on a transaction
- Email delivery (per-send cost on transactional email)
- Storage cost for a specific customer's data
- Compute cost for a specific product's runtime (Lambda invocations, container uptime tied to a product)
- Third-party data API calls made on a customer's behalf

### 1.2 Infrastructure

Costs that are shared across all products and not attributable to a single product's delivery.
If the cost persists even when no customers are using any product, it is Infrastructure.

Examples:
- Base VPS or cloud instance running the agent harness
- Domain registrations and DNS fees
- Shared database cluster (not product-specific)
- Monitoring and observability stack (Grafana, Sentry shared instance)
- CI/CD pipeline compute
- Shared object storage (not attributed to a product)
- SSL certificate management

### 1.3 Tools

Software subscriptions and SaaS seats used by agents or the owner to build, manage, or operate the company.

Examples:
- IDE or coding assistant subscriptions
- Project management SaaS (Linear, Notion)
- Communication tools (Telegram bot hosting, Slack if used)
- Analytics platforms (PostHog, Mixpanel)
- Design tools
- Security scanning SaaS
- Documentation hosting

### 1.4 Marketing

Costs incurred to acquire customers or increase product visibility.

Examples:
- Paid advertising (Google Ads, Meta, TikTok Ads)
- Influencer or affiliate payouts
- SEO tooling (Ahrefs, SEMrush) — if used primarily for growth, not product ops
- Content distribution tools
- Email newsletter platform (if used for marketing, not transactional)

---

## §2 — COST ATTRIBUTION RULES

Every cost line MUST be tagged before it is logged. Untagged cost is a protocol violation.

### 2.1 Required Tags

Every cost entry MUST carry:

| Tag | Format | Example |
|-----|--------|---------|
| `class` | One of: cogs, infra, tools, marketing | `class: cogs` |
| `product` | Product slug or `overhead` | `product: chatbot-saas` |
| `vendor` | Vendor or service name | `vendor: openai` |
| `frequency` | one-time, monthly, annual | `frequency: monthly` |
| `amount_usd` | Numeric, USD | `amount_usd: 42.00` |

### 2.2 Product Attribution

- If a cost is 100% attributable to one product: tag that product.
- If a cost is shared across multiple products: split by usage ratio. Record the ratio in the cost entry. Revisit the ratio quarterly.
- If a cost supports no specific product (office-equivalent overhead): tag `overhead`.
- Infrastructure costs default to `overhead` unless a product consumes >80% of that resource — in which case tag that product.

### 2.3 Attribution Log Location

`~/.1ai/data/costs/cost-log-[YYYY-MM].json`

Each entry format:
```json
{
  "date": "YYYY-MM-DD",
  "vendor": "string",
  "description": "string",
  "class": "cogs|infra|tools|marketing",
  "product": "slug or overhead",
  "frequency": "one-time|monthly|annual",
  "amount_usd": 0.00,
  "invoice_ref": "string or null",
  "decision_ref": "DECISION-ID or null"
}
```

### 2.4 New Cost Line Protocol

No new recurring cost may be added without:
1. A cost entry in the log with all required tags.
2. A Decision Log entry (DECISION.md §4) referencing the business justification.
3. L5 approval if the cost exceeds $10/month (per FINANCE.md §2).

---

## §3 — UNIT ECONOMICS TRACKING

Unit economics are computed per product, not for the company as a whole.

### 3.1 Metrics Per Product

| Metric | Formula | Target |
|--------|---------|--------|
| MRR | Sum of all active recurring revenue for this product | Tracked, no floor |
| Monthly COGS | Sum of all `class: cogs` costs tagged to this product | < 40% of product MRR |
| Gross Margin | `(MRR - Monthly COGS) / MRR × 100` | ≥ 60% |
| COGS per Customer | `Monthly COGS / Active Customer Count` | Tracked, trend only |
| LTV:CAC Ratio | `(ARPU × Avg Lifetime Months) / CAC` | ≥ 3:1 |

### 3.2 Gross Margin Target

- Minimum acceptable gross margin per product: **60%**.
- Below 60%: Cost Agent flags for immediate review.
- Below 40%: Product is operating at unsustainable unit economics. Owner must decide: reprice, reduce COGS, or sunset. Decision within 14 days.
- New products in first 90 days: 40% floor applies (ramp period). After 90 days, full 60% target.

### 3.3 Calculation Cadence

- Monthly COGS and gross margin computed by Cost Agent on the 1st of each month, covering the prior month.
- Stored at: `~/.1ai/data/costs/unit-economics-[YYYY-MM].json`
- Format per product:
```json
{
  "product": "slug",
  "period": "YYYY-MM",
  "mrr_usd": 0.00,
  "cogs_usd": 0.00,
  "gross_margin_pct": 0.0,
  "active_customers": 0,
  "cogs_per_customer_usd": 0.00,
  "ltv_cac_ratio": 0.0,
  "flags": []
}
```

---

## §4 — SPENDING ANOMALY DETECTION

Cost Agent monitors all cost lines weekly and triggers alerts on the conditions below.

### 4.1 Alert Thresholds

| Alert ID | Condition | Severity |
|----------|-----------|----------|
| C1 | Any cost line increases >20% month-over-month | HIGH |
| C2 | Any new cost line appears that has no Decision Log entry | CRITICAL |
| C3 | Total monthly spend exceeds 80% of the monthly cost ceiling (§8) | HIGH |
| C4 | Total monthly spend exceeds 100% of the monthly cost ceiling | CRITICAL |
| C5 | Any single COGS cost line exceeds 25% of the corresponding product's MRR | HIGH |
| C6 | Gross margin on any product drops below 60% | HIGH |
| C7 | Gross margin on any product drops below 40% | CRITICAL |
| C8 | Any vendor charge appears without a matching log entry | CRITICAL |
| C9 | An annual subscription auto-renews without a tool audit (§7) completion in prior 30 days | HIGH |

### 4.2 Alert Format

```
COST ALERT [C-number]
Vendor/Product: [name]
Amount: $[amount] or [%] change
Detail: [one sentence]
Action taken: [flagged / blocked / logged]
Owner input needed: [yes/no — if yes, exactly what decision is needed]
```

Alerts sent to owner's Telegram channel immediately on detection. Every alert also logged in DECISION.md.

### 4.3 MoM Calculation

MoM increase is computed as: `(current_month - prior_month) / prior_month × 100`.
For costs with no prior-month entry (new cost line): always triggers C2 (no Decision Log entry check).

---

## §5 — CLOUD SPEND GOVERNANCE

### 5.1 Mandatory Resource Tagging

Every cloud resource (AWS, GCP, Hetzner, Vercel, Cloudflare, or equivalent) MUST carry these tags at creation:

| Tag Key | Value |
|---------|-------|
| `product` | Product slug or `overhead` |
| `env` | `production`, `staging`, or `dev` |
| `owner` | Agent ID or `human` |
| `created` | ISO date |

Untagged resources: Cost Agent flags weekly. Resources untagged for >7 days after first flag: owner notified for manual tagging or deletion.

### 5.2 Waste Detection

Cost Agent runs the following checks on the 1st and 15th of each month:

| Waste Type | Detection Rule | Action |
|-----------|---------------|--------|
| Idle compute | CPU < 5% average over 7 days AND no traffic | Flag for rightsizing or termination |
| Unused storage | S3/bucket with zero read/write operations for 30 days | Flag for deletion or archival to cold storage |
| Orphaned snapshots | Disk snapshot older than 90 days with no associated live instance | Flag for deletion |
| Oversized instance | CPU < 20% average over 30 days | Flag for downsize by one tier |
| Dev/staging resources | Any `env: dev` or `env: staging` resource running continuously for >30 days | Flag — dev should not run 24/7 |
| Unused IP addresses | Static IPs not attached to a running resource | Flag for release |

### 5.3 Rightsizing Cadence

- Monthly: Cost Agent generates a rightsizing report listing all resources matching waste rules above.
- Owner or Lead Agent reviews and executes approved downsizes within 7 days of report.
- Report location: `~/.1ai/data/costs/rightsizing-[YYYY-MM].md`

### 5.4 Commitment vs On-Demand

- Resources running continuously for >60 days: evaluate reserved/committed pricing.
- If committed pricing saves ≥20% vs on-demand at current usage: present to owner for approval.
- Never purchase reserved instances or committed use without L5 approval.

---

## §6 — LLM/AI API COST CONTROL

AI API costs are COGS for customer-facing features and Tools for agent infrastructure. Both require active management.

### 6.1 Token Budget Per Task Type

| Task Type | Max Tokens Per Call | Max Cost Per Call (USD) | Model Tier |
|-----------|--------------------|-----------------------|------------|
| Customer-facing chat completion | 8,000 | $0.05 | Standard (e.g., GPT-4o-mini, Gemini Flash) |
| Agent planning / orchestration | 16,000 | $0.20 | Standard |
| Document generation (long-form) | 32,000 | $0.50 | Standard |
| Code generation (complex) | 16,000 | $0.30 | Standard or Premium |
| Reasoning / analysis (premium) | 32,000 | $1.00 | Premium (e.g., o3, Claude Sonnet) |
| Batch / background processing | 64,000 | $0.10 | Cheapest available |

Any call that would exceed the cost ceiling for its task type MUST be split, compressed, or escalated for approval before execution.

### 6.2 Model Tier Selection Rules

- **Default**: Use the cheapest model that meets the task's quality requirement.
- **Upgrade to premium only when**: The task requires multi-step reasoning, code audit, or legal/financial analysis where errors cost more than the premium API cost.
- **Never use premium for**: Classification, summarization, simple Q&A, formatting, or any task a standard model handles with ≥90% quality.
- **Batch jobs**: Always use batch API endpoints when available (typically 50% cheaper). No batch job uses real-time endpoints.

### 6.3 Cost-Per-Agent-Action Tracking

Each agent action that consumes AI API tokens MUST log:
```json
{
  "timestamp": "ISO8601",
  "agent_id": "string",
  "task_type": "string",
  "model": "string",
  "input_tokens": 0,
  "output_tokens": 0,
  "cost_usd": 0.0000,
  "product": "slug or overhead"
}
```

Log location: `~/.1ai/data/costs/ai-usage-[YYYY-MM].jsonl` (append-only)

### 6.4 Monthly AI Spend Cap

- AI API spend cap is set per product and per `overhead` bucket.
- Default cap: 30% of product MRR for customer-facing AI costs.
- Overhead AI cap: $50/month unless owner sets a different value.
- When 80% of either cap is consumed in a month: Cost Agent alerts owner (C3 threshold applies).
- When 100% is hit: agents fall back to cheapest available model for remaining tasks in that product/bucket. No new premium calls until next month unless owner grants an exception.

### 6.5 Prompt Cost Reduction

- Agents MUST use system prompt caching where supported.
- Repetitive structured outputs MUST use JSON mode or function calling (reduces output verbosity).
- Context window stuffing is prohibited: trim context to the minimum required for the task.
- Any agent consistently using >50% of its token budget: Cost Agent flags it for prompt review.

---

## §7 — TOOL AUDIT

### 7.1 Cadence

- **Quarterly** (January, April, July, October): Full audit of all `class: tools` cost lines.
- **Annual**: Additionally review all `class: infra` subscriptions.
- Audit is performed by Cost Agent, reviewed by owner.

### 7.2 Audit Criteria Per Tool

For each tool, compute:

| Metric | Formula |
|--------|---------|
| Monthly cost | Prorated to monthly if billed annually |
| Usage frequency | Agent-reported: times used per month |
| Revenue contribution | Which products or tasks depend on this tool |
| Replacement cost | Cost of replacing with a free or cheaper alternative |
| ROI score | `(Revenue contribution score 1–10) / Monthly cost USD × 100` |

### 7.3 Cancel/Keep Decision Rule

| ROI Score | Action |
|-----------|--------|
| ≥ 50 | Keep. No action needed. |
| 20–49 | Keep with note. Re-evaluate next quarter. |
| 5–19 | Flagged. Find alternative within 30 days or justify to owner. |
| < 5 | Cancel at next billing cycle. Cost Agent initiates cancellation. |

For tools with ROI score < 5: Cost Agent issues cancellation notice, logs in DECISION.md as a Type 2 decision (per FINANCE.md §2 — subscription cancellation), and notifies owner 7 days before cancellation executes.

### 7.4 Audit Output

File: `~/.1ai/data/costs/tool-audit-[YYYY-QN].md` (e.g., `tool-audit-2026-Q3.md`)

Required sections:
1. Full tool inventory with tags and monthly cost
2. ROI scores for all tools
3. Cancel recommendations with rationale
4. Keep decisions with justification
5. Owner sign-off field

---

## §8 — COST CEILING PER PRODUCT

### 8.1 Setting the Ceiling

Every product MUST have a monthly cost ceiling set before it reaches $100/month in total spend.
Ceiling is set by the owner and stored in: `~/.1ai/config/cost-ceilings.json`

```json
{
  "product-slug": {
    "monthly_ceiling_usd": 0.00,
    "set_date": "YYYY-MM-DD",
    "review_date": "YYYY-MM-DD",
    "rationale": "string"
  },
  "overhead": {
    "monthly_ceiling_usd": 0.00,
    "set_date": "YYYY-MM-DD",
    "review_date": "YYYY-MM-DD",
    "rationale": "string"
  }
}
```

Default ceiling for a new product with no owner-set value: **$50/month** until MRR is established.

### 8.2 Ceiling Enforcement

| Spend Level | Action |
|------------|--------|
| 0–70% of ceiling | Normal operation |
| 70–80% | Cost Agent logs a warning internally |
| 80–100% | C3 alert sent to owner (§4.1). Agents continue operating. |
| 100% hit | C4 alert sent. Agents switch all AI calls to cheapest tier. No new paid-tool calls. No discretionary spend. Owner must raise ceiling or accept degraded mode. |
| 110% hit | All non-critical agent operations for that product pause until owner responds. |

### 8.3 Ceiling Review

- Ceiling is reviewed when MRR changes by ≥50%.
- Ceiling is reviewed at every quarterly tool audit.
- Owner must explicitly approve any ceiling increase. Agents cannot self-authorize a ceiling raise.

---

## §9 — COST VS REVENUE DECISION RULE

Before approving any new recurring cost (or renewing an existing one), apply this formula:

### 9.1 Justification Formula

```
Revenue Justification Score = (Expected MRR impact USD) / (Monthly cost USD)
```

| Score | Decision |
|-------|----------|
| ≥ 5.0 | Approved. Cost pays for itself 5x in MRR. |
| 2.0–4.9 | Approved with 90-day review. Must hit MRR target within 90 days. |
| 1.0–1.9 | Requires owner approval. Marginal — justify with strategic rationale. |
| < 1.0 | Rejected by default. Requires explicit L5 override with written rationale. |

### 9.2 Expected MRR Impact Estimation

For each candidate cost, the proposing agent MUST state:
- **Direct impact**: Does this cost enable a feature customers pay for? Estimate incremental MRR.
- **Indirect impact**: Does this cost reduce COGS, enabling higher margin on existing MRR? Estimate monthly savings.
- **Infrastructure/baseline**: Does this cost keep existing MRR from churning? Assign 100% of at-risk MRR as impact.

If impact cannot be estimated: treat as 0. Score will be 0 → rejected by default unless L5 overrides.

### 9.3 Sunset Rule

A cost that has been under review (Score 2.0–4.9) for 90 days and has not produced the projected MRR impact is automatically submitted for cancellation at the next tool audit. Cost Agent generates a sunset recommendation. Owner must explicitly override to keep it.

---

## §10 — COST REPORTING

### 10.1 Weekly Cost Report

**When:** Every Monday, covering the prior 7 days (Sunday–Saturday).
**Generated by:** Cost Agent.
**Stored at:** `~/.1ai/data/costs/weekly-report-[YYYY-WNN].md` (ISO week number)

Required contents:

1. **Spend summary by class**
   - COGS: total, per-product breakdown
   - Infrastructure: total
   - Tools: total
   - Marketing: total
   - Week-over-week change for each class (amount and %)

2. **AI/LLM usage**
   - Total tokens consumed (input and output)
   - Total cost
   - Cost per agent (top 5 by spend)
   - Model tier distribution (% of spend on premium vs standard vs batch)

3. **Anomaly flags**
   - All C-alerts triggered in the period (§4.1)
   - Status of each: resolved, pending, escalated

4. **Unit economics snapshot**
   - Gross margin per product (rolling 30-day)
   - Any product below 60% gross margin target

5. **Ceiling status**
   - Month-to-date spend vs ceiling for each product and overhead
   - Projected end-of-month spend at current run rate

6. **Action items**
   - Open items from prior report not yet resolved
   - New items requiring owner decision

### 10.2 Monthly Cost Report

Produced on the 1st of each month as part of the monthly finance package (FINANCE.md §6).
Cost Agent appends the following sections to the finance report:

- Full cost attribution summary (all classes, all products)
- Unit economics table (all products, all metrics from §3.1)
- Tool audit status (date of last audit, next scheduled audit)
- Rightsizing report summary (§5.3)
- Cost trend chart data (6-month history, stored as JSON for rendering)

### 10.3 Report Delivery

All reports are:
- Saved to the file path specified above (append-only, never overwrite)
- Summarized and sent to owner via Telegram (3-bullet summary: total spend, biggest anomaly, top action item)
- Indexed in `~/.1ai/data/costs/report-index.json` (filename, period, generated_at, anomaly_count)

---

Current version: 1.0.0
Last reviewed: 2026-07-05
Next scheduled review: 2027-01-05 (semi-annual)
