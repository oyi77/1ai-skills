---
name: vendor
version: 1.0.0
severity: mandatory
scope: [all]
pairs-with: [finance, security, incident, decision, roles]
description: Vendor registry, selection criteria, dependency risk, SLA monitoring, renewal, offboarding
---

# VENDOR.md — Vendor Management Protocol

> Every external service this company depends on is a risk. This protocol makes that risk visible,
> bounded, and manageable. No vendor is used without an entry in the registry. No vendor is dropped
> without a clean exit. No critical path goes without a fallback.

---

## §1 — VENDOR REGISTRY

Every external service — SaaS tool, API, cloud provider, CDN, payment processor, or any paid/free
third-party dependency — MUST have a registry entry before first use.

**Registry location:** `~/.1ai/data/vendors/registry.json`

**Required fields per entry:**

```json
{
  "id": "vendor-slug",
  "name": "Display Name",
  "url": "https://vendor.com",
  "purpose": "One sentence: what problem this solves and which agent/workflow uses it",
  "category": "infrastructure | api | saas-tool | payment | analytics | communication | storage | other",
  "criticality": "critical | standard | optional",
  "tier": "paid | free | free-tier",
  "monthly_cost_usd": 0,
  "data_classification": "none | operational | customer-pii | financial | credentials",
  "owner_agent": "agent-id responsible for this integration",
  "sla_claimed": "99.9% uptime / response < 200ms / etc.",
  "renewal_date": "YYYY-MM-DD or null if month-to-month",
  "contract_term": "monthly | annual | perpetual | none",
  "fallback_vendor": "vendor-slug or null",
  "added_date": "YYYY-MM-DD",
  "last_audited": "YYYY-MM-DD",
  "deprecation_status": "active | watch | migration-planned | deprecated"
}
```

**Registry rules:**
- Adding a vendor without an entry = ROLES.md violation. Any agent invoking an unregistered
  API key or service endpoint must file an entry retroactively within 24 hours and notify the owner.
- `owner_agent` is accountable for monitoring, renewals, and incident response for that vendor.
- If `owner_agent` is decommissioned, registry entry must be reassigned before decommissioning completes.
- Registry is reviewed quarterly (see §9).

---

## §2 — VENDOR SELECTION CRITERIA

Before adopting any new paid service — or any free service with `data_classification` of
`customer-pii`, `financial`, or `credentials` — the requesting agent MUST complete this checklist.
All 6 points must be answered. Checklist is submitted as part of DECISION.md proposal.

**Vendor Selection Checklist:**

```
VENDOR SELECTION PROPOSAL
Agent: [agent-id]
Vendor: [name + URL]
Date: [YYYY-MM-DD]

[ ] 1. NECESSITY — Is there an existing vendor in the registry that covers this need?
        Current registry checked: yes/no
        Nearest existing alternative: [vendor-slug or "none"]
        Reason existing alternative is insufficient: [specific gap]

[ ] 2. COST — What is the total cost of ownership over 12 months?
        Monthly cost: $[amount]
        Annual total: $[amount]
        Hidden costs: [setup fees, per-seat pricing, overage rates, egress fees]
        Compared to budget line: [finance category from FINANCE.md §2]

[ ] 3. SECURITY — Does this vendor meet minimum security standards?
        SOC 2 Type II or ISO 27001 certified: yes / no / unknown
        Data residency: [region]
        Encryption at rest and in transit: yes / no / unknown
        If any "no" or "unknown": owner approval required before adoption.

[ ] 4. FALLBACK — What happens if this vendor goes down or terminates service?
        Fallback vendor: [name or "none — justify below"]
        Migration time estimate: [hours/days]
        Data portability: [can we export our data? format?]
        If no fallback and criticality = critical: BLOCKED until fallback is identified.

[ ] 5. DATA EXPOSURE — What data will this vendor receive?
        Data classification: [none | operational | customer-pii | financial | credentials]
        Data shared: [enumerate specifically — e.g. "customer email addresses, purchase amounts"]
        Vendor's data retention policy: [days or "unknown — check before adopting"]
        If customer-pii or financial: DPA or data processing agreement required.

[ ] 6. EXIT PLAN — How do we leave this vendor if needed?
        Data export mechanism: [API / CSV download / manual request / none]
        Export completeness: [all data / partial / unclear]
        Estimated migration effort: [hours]
        Lock-in risk: [none / moderate / high — describe]
```

Owner approval (L5) required if:
- Any security criterion is "no" or "unknown"
- criticality = critical and no fallback exists
- data_classification = customer-pii or financial
- Monthly cost > $50

---

## §3 — SINGLE-POINT-OF-FAILURE RULE

No critical-path workflow may have zero fallback for any vendor with `criticality: critical`.

### 3.1 Criticality Classification

| Criticality | Definition | Examples |
|---|---|---|
| `critical` | Outage blocks revenue, breaks production service, or prevents customer delivery for >1 hour | Payment processor, primary hosting, primary database, primary LLM API |
| `standard` | Outage degrades experience or slows work but revenue pipeline is intact | Analytics, secondary notification channel, non-primary API |
| `optional` | Outage is invisible to customers; affects convenience only | Internal dev tooling, optional enrichment APIs |

**Classification is set by the owner agent at registration.** When uncertain, classify up.

### 3.2 Redundancy Requirements

| Criticality | Fallback Requirement |
|---|---|
| `critical` | MUST have a named `fallback_vendor` in registry. Fallback must be tested within 30 days of primary adoption and re-tested annually. |
| `standard` | SHOULD have a fallback. If none: document risk acceptance in DECISION.md with owner signature. |
| `optional` | No fallback required. |

### 3.3 Failover Procedure Requirement

Every `critical` vendor MUST have a named runbook in `~/.1ai/runbooks/vendor-failover-[vendor-slug].md`.
Minimum runbook contents:
1. How to detect the primary is down (specific signal, not "check if it works")
2. Exact steps to switch to fallback (commands, config changes, environment variable swaps)
3. How to verify fallback is operational
4. Steps to switch back when primary recovers
5. Who to notify (see COMMS.md notification matrix)

If no runbook exists for a `critical` vendor, the owner agent must create it within 7 days of
vendor registration. Missing runbook = SEV3 finding reported in the next vendor audit (§9).

---

## §4 — API DEPENDENCY RISK

For any vendor integrated via API (REST, GraphQL, SDK, webhook):

### 4.1 Versioning Discipline

- Pin to a specific API version at integration time. Never use `latest`, `stable`, or versionless
  endpoints unless the vendor provides no versioning.
- Store pinned version in registry entry under `api_version` field.
- When bumping API version: treat as a migration (§4.3), not a routine update.

### 4.2 Deprecation Notice Monitoring

The owner agent for each API vendor is responsible for:

- Checking the vendor's changelog, developer blog, or deprecation RSS/email at minimum monthly.
- Monitoring the configured alerting channel for vendor-sent deprecation emails.
- Adding a GitHub issue immediately upon detecting any deprecation notice affecting an in-use
  endpoint, parameter, or authentication method.

Deprecation notice GitHub issue must include:
```
VENDOR DEPRECATION NOTICE
Vendor: [name]
Affected: [endpoint / feature / auth method]
Vendor deadline: [YYYY-MM-DD]
Our usage: [which agents/workflows call this]
Risk if not migrated by deadline: [service break / degradation / security gap]
Assigned to: [agent-id]
```

### 4.3 Migration Trigger Conditions

Initiate a migration immediately (do not wait) when any of the following are true:

| Condition | Action |
|---|---|
| Vendor announces EOL for endpoint in use | File migration issue, start migration before deadline - 30 days |
| Vendor changes auth model (e.g. token type change) | Treat as SEV2 dependency risk; migrate within 14 days |
| API version in use reaches vendor-stated end of support | Migrate to supported version within 30 days |
| Error rate on vendor API exceeds 5% for 7 consecutive days | Investigate root cause; if version-related, migrate |
| Vendor acquired by another company | Re-run §2 checklist on combined entity within 30 days |

---

## §5 — VENDOR SLA MONITORING

Vendor SLA claims in the registry (`sla_claimed`) must be compared against observed reality.

### 5.1 Monitoring Responsibilities

The owner agent for each `critical` or `standard` vendor must:

- Configure an uptime check (synthetic ping or health endpoint probe) running at minimum every
  5 minutes for `critical` vendors, every 30 minutes for `standard` vendors.
- Log availability data to `~/.1ai/data/vendors/uptime/[vendor-slug]-[YYYY-MM].json`.
- Calculate actual monthly uptime percentage at end of month.
- Flag any deviation: if observed uptime is >0.5 percentage points below SLA claim for two
  consecutive months, file a vendor performance issue.

### 5.2 SLA Breach Protocol

When a vendor fails to meet claimed SLA:

1. **Document the outage:** start time, end time, affected functionality, impact on our operations.
   Log in `~/.1ai/data/vendors/incidents/[vendor-slug]-[YYYY-MM-DD].md`.
2. **Check vendor's status page:** confirm vendor acknowledged the outage. Screenshot or archive URL.
3. **Quantify impact:** did we lose revenue, miss SLAs to our own customers, incur extra costs?
4. **SLA credit eligibility:** check vendor contract/ToS for credit terms. If credit available and
   outage is documented: file claim per vendor's process within their stated claim window.
5. **Escalate if pattern:** two or more SLA breaches in a 90-day window → add vendor to
   `deprecation_status: watch` and begin §2 evaluation for replacement.

### 5.3 Vendor Status Pages

Maintain a list of vendor status page URLs in registry. Owner agent subscribes to status page
notifications (email or webhook) for all `critical` vendors. Subscription must be re-verified
quarterly — vendors change status page locations.

---

## §6 — RENEWAL AND CANCELLATION PROTOCOL

### 6.1 Renewal Approval

**Automatic renewal is NOT the default.** Before any subscription renews:

| Condition | Required action |
|---|---|
| Annual contract, cost ≤ $50/yr | Owner agent may renew; log in DECISION.md |
| Annual contract, cost > $50/yr | Owner (L5) approval required 14 days before renewal date |
| Price increased > 10% from prior period | Owner (L5) approval required regardless of amount |
| Vendor had ≥ 2 SLA breaches in past 90 days | Owner review required; default is to evaluate alternatives |
| `deprecation_status: watch` | Block renewal; owner must explicitly approve continuation |

**Advance notice:** Owner agent sends renewal reminder to the owner notification channel
30 days before renewal date for all paid subscriptions, and 7 days before as a final reminder.
Silence is NOT approval. If 48 hours before renewal date owner has not approved, the subscription
is cancelled (§6.2 procedure applies).

### 6.2 Cancellation Procedure

Before cancelling any vendor subscription, execute in order:

1. **Export all data** the vendor holds: use vendor's export feature, API, or support request.
   Store exported data in `~/.1ai/data/vendors/exports/[vendor-slug]-[YYYY-MM-DD]/`.
2. **Verify export completeness:** open at least 3 sample records, confirm they are readable and
   complete. Log: "Export verified: N records, formats [list]."
3. **Update all dependencies:** search codebase and config for all references to vendor's API keys,
   base URLs, SDK imports. Replace or remove before cancelling account.
4. **Revoke credentials:** rotate or delete any API keys, OAuth tokens, or service accounts
   associated with this vendor. Update `~/.1ai/config/secrets/` accordingly.
5. **Cancel subscription:** follow vendor's cancellation procedure. Screenshot confirmation.
6. **Update registry:** set `deprecation_status: deprecated`, add `cancelled_date` field.
7. **Post-cancellation verification (7 days later):** confirm no billing occurred after
   cancellation date. If billed: dispute charge immediately, notify owner.

---

## §7 — VENDOR INCIDENT RESPONSE

When a vendor suffers an outage or incident that impacts our operations:

### 7.1 Triage

| Impact | Our Classification | Response |
|---|---|---|
| `critical` vendor fully down | SEV2 (escalate to SEV1 if revenue blocked) | Declare incident per INCIDENT.md §3 |
| `critical` vendor degraded (>10% error rate or >2x latency) | SEV3 | Monitor actively; prepare failover |
| `standard` vendor fully down | SEV3 | File issue; activate workaround if available |
| `optional` vendor any outage | No incident | Note in daily standup; file issue if >24h |

### 7.2 Immediate Actions

1. **Confirm it's the vendor, not us:** check our own error logs, vendor status page, and
   independent downtime monitors (e.g. isdown.today, downdetector). Do not assume vendor fault
   without external confirmation.
2. **Check RUNBOOK:** `~/.1ai/runbooks/vendor-failover-[vendor-slug].md`. Execute failover if
   severity warrants it.
3. **Notify owner:** for SEV1/SEV2 per INCIDENT.md §3 Step 4.
4. **Open vendor support ticket:** include: timestamp, error codes, affected endpoints, sample
   request/response (scrubbed of secrets). Log ticket ID in the incident issue.
5. **Communicate status internally:** post in the configured operations channel every 30 minutes
   during active SEV1/SEV2 until resolved.

### 7.3 Post-Vendor-Incident Actions

Once vendor confirms resolution:
- Verify our services are back to normal (concrete test, not assumption).
- Log total downtime duration in vendor's uptime file (§5.1).
- If outage qualifies for SLA credit, file claim (§5.2 Step 4).
- Update incident record with resolution time and root cause (vendor's postmortem if published).
- If this is the second breach in 90 days: set `deprecation_status: watch` in registry.

---

## §8 — FREE-TIER RISK MANAGEMENT

Services used on a free tier carry specific risks: sudden rate limiting, feature removal, forced
migration, or complete shutdown with minimal notice. Rules for managing these:

### 8.1 Classification

Any service where our usage is bounded by a free tier limit (requests/month, seats, storage,
bandwidth) must be tagged `"tier": "free-tier"` in the registry.

### 8.2 Usage Monitoring

Owner agent for each free-tier service MUST:
- Track current usage against the free-tier limit monthly.
- Alert the owner when usage exceeds 70% of the free limit: include current usage, limit,
  trend, and estimated date of breach.
- Never assume the free tier is stable. Check vendor pricing page quarterly for changes.

### 8.3 Free-Tier Dependency Rules

| Scenario | Required action |
|---|---|
| Free-tier service is `criticality: critical` | BLOCKED. Critical services must use paid tier or have a paid fallback already active. |
| Free-tier service holds `customer-pii` or `financial` data | Owner explicit approval required. Re-evaluated every 90 days. |
| Free-tier service announces shutdown or paid-only migration | Treat as SEV2 dependency risk. Migrate within 14 days or immediately if less notice given. |
| Free-tier service enforces rate limits we are hitting | Immediate: implement request throttling. Within 7 days: upgrade or migrate. |
| Free-tier service not used in 60 days | Candidate for offboarding (§10). Owner reviews. |

### 8.4 Free-Tier Alternatives

Maintain at least one alternative for every free-tier service with `criticality: standard` or higher.
The alternative does not have to be free — it just must be documented and tested annually.

---

## §9 — VENDOR DATA AUDIT

### 9.1 Audit Frequency

| Data classification | Audit frequency |
|---|---|
| `customer-pii` | Quarterly |
| `financial` | Quarterly |
| `credentials` | Monthly (verify no stored credentials beyond what is needed) |
| `operational` | Semi-annual |
| `none` | Annual |

### 9.2 Audit Procedure

For each vendor in scope, the owner agent runs the following checklist:

```
VENDOR DATA AUDIT
Vendor: [name]
Date: [YYYY-MM-DD]
Auditor: [agent-id]

[ ] 1. DATA INVENTORY — What does this vendor currently hold?
        Access vendor's account/settings/data export to enumerate stored data.
        List: [categories of data, e.g. "customer emails, purchase history, IP logs"]
        Matches what registry says we share: yes / no — if no, document discrepancy.

[ ] 2. RETENTION COMPLIANCE — Is vendor deleting data per stated retention policy?
        Vendor's stated retention period: [days/months]
        Sample check: request or view oldest accessible records.
        Evidence of deletion after retention period: yes / no / cannot verify

[ ] 3. SUB-PROCESSORS — Does vendor share our data with sub-processors?
        Vendor's sub-processor list reviewed: yes / no
        New sub-processors since last audit: [list or "none"]
        Any new sub-processor in high-risk jurisdiction: yes — notify owner / no

[ ] 4. ACCESS CONTROL — Who at the vendor can access our data?
        Admin accounts on vendor platform: [count and owners]
        Any orphaned accounts (former employees/agents): [list or "none"]
        MFA enabled on all admin accounts: yes / no

[ ] 5. DATA MINIMIZATION — Are we sharing more than necessary?
        Review what data we send to this vendor.
        Anything that could be redacted, hashed, or omitted: [list or "none"]

[ ] 6. DELETION REQUEST TEST (for customer-pii vendors, annual only)
        Submit a test deletion request for a synthetic record.
        Vendor confirmed deletion within their stated SLA: yes / no / not tested
```

Audit findings filed in `~/.1ai/data/vendors/audits/[vendor-slug]-[YYYY-MM-DD].md`.
Critical findings (orphaned access, data beyond retention, undisclosed sub-processors) notify
owner immediately and are logged in DECISION.md.

---

## §10 — VENDOR OFFBOARDING

When a vendor relationship ends — whether by cancellation, replacement, or vendor shutdown —
the following checklist must be completed in full before the relationship is considered closed.

**Offboarding record location:** `~/.1ai/data/vendors/offboarding/[vendor-slug]-[YYYY-MM-DD].md`

```
VENDOR OFFBOARDING RECORD
Vendor: [name]
Offboarding date: [YYYY-MM-DD]
Reason: [cancelled / replaced-by-[slug] / vendor-shutdown / cost / security / performance]
Owner agent: [agent-id]

PHASE 1 — DATA EXPORT (must complete before cancellation)
[ ] Full data export requested and received
[ ] Export stored at: ~/.1ai/data/vendors/exports/[vendor-slug]-[YYYY-MM-DD]/
[ ] Export verified: [N records, readable, complete]
[ ] Export encrypted at rest: yes / no

PHASE 2 — CREDENTIAL REVOCATION
[ ] All API keys issued by this vendor: revoked at vendor and deleted from our config
[ ] All OAuth tokens: revoked
[ ] All webhook secrets: rotated or removed from our systems
[ ] All service account passwords: changed or accounts deleted
[ ] Confirmation: searched codebase for vendor's domain/API base URL — no remaining references

PHASE 3 — CODE AND CONFIG CLEANUP
[ ] All integrations removed from codebase (imports, SDK calls, env var references)
[ ] All environment variables for this vendor removed from all deployment environments
[ ] CI/CD secrets for this vendor deleted
[ ] Monitoring checks for this vendor disabled or removed

PHASE 4 — REGISTRY UPDATE
[ ] Registry entry: deprecation_status set to "deprecated"
[ ] Registry entry: cancelled_date set to [YYYY-MM-DD]
[ ] Any other vendor with this vendor as fallback_vendor: updated to new fallback or null

PHASE 5 — POST-CANCELLATION VERIFICATION (complete 7 days after cancellation)
[ ] No billing from vendor after cancellation date confirmed
[ ] Vendor has sent data deletion confirmation (for customer-pii vendors)
[ ] Account login confirmed inaccessible (attempt login, verify failure)

PHASE 6 — KNOWLEDGE TRANSFER
[ ] Any runbooks referencing this vendor updated to remove or replace vendor-specific steps
[ ] DECISION.md entry: offboarding complete, data export location, credential revocation confirmed
```

**Data leakage verification for customer-pii vendors:**
After offboarding a vendor that held `customer-pii`, the owner agent submits a formal deletion
request to the vendor citing applicable data protection requirements. The vendor's confirmation
response is stored in the offboarding record. If no confirmation received within 30 days:
owner is notified and the vendor is reported as non-compliant in SECURITY.md audit log.

---

## §11 — VENDOR ALERTS

The owner agent for a vendor MUST notify the human owner immediately (not at next review) when:

| # | Condition | Alert content |
|---|---|---|
| V1 | A `critical` vendor has been down > 15 minutes and failover is not yet active | Vendor, downtime duration, failover status, ETA |
| V2 | A vendor sends a deprecation notice for any endpoint or feature we use | Vendor, affected feature, deadline, migration effort estimate |
| V3 | A vendor announces pricing change > 20% or removal of free tier we depend on | Vendor, new pricing, current cost, migration options |
| V4 | A vendor's security incident may have exposed our data | Vendor, disclosed scope, our data classification, action taken |
| V5 | A vendor is acquired, merges, or announces shutdown | Vendor, effective date, continuity status, recommended action |
| V6 | A vendor is found to have sub-processors or data sharing not in the registry | Vendor, undisclosed party, data involved, compliance risk |
| V7 | Free-tier usage hits 70% of limit with < 14 days to month reset | Vendor, usage %, limit, trend, options |

**Alert format:**
```
VENDOR ALERT [V-number]
Vendor: [name]
Detail: [one sentence]
Our exposure: [what we have at risk]
Action taken: [what agent did — monitored, failover activated, support ticket filed]
Owner decision needed: [yes — describe / no]
```

Alerts sent to owner's configured notification channel. Every alert logged in DECISION.md.

---

Current version: 1.0.0
Last reviewed: 2026-07-05
Next scheduled review: 2027-01-05 (semi-annual)
