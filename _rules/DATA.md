---
name: data
version: 1.0.0
severity: mandatory
scope: [all]
pairs-with: [security, incident, ethics, finance, roles]
description: Data classification, retention, deletion, backup, access control, breach response, and agent data hygiene
---

# DATA.md — Data Governance Protocol

> Every piece of data BerkahKarya/1ai touches belongs somewhere, expires sometime, and may only move to authorized places.
> Agents do not accumulate data beyond task scope. Agents do not transmit data without checking this file first.
> When in doubt: classify higher, retain shorter, share less.

---

## §1 — DATA CLASSIFICATION

Four classes. Every data asset — file, database record, API payload, log line, context variable — must be assigned one class before it is stored, processed, or transmitted.

### PUBLIC
Data intentionally published and freely shareable.

Examples:
- Published blog posts, social media captions, public newsletters
- Open-source repository code published under a public license
- Product landing page copy, public pricing pages
- Published API documentation

Rules:
- No access restriction required before sharing
- Still must not contain accidentally embedded INTERNAL or above data (agents must check before publishing)
- Once published, treat as permanently public — no expectation of removal

### INTERNAL
Data created for company use; not secret, but not for external distribution.

Examples:
- Internal roadmaps, OKR drafts before publishing
- Agent system prompts and configurations
- Operational runbooks, SOPs, PROCESS.md contents
- Supplier names, vendor contracts, tool stack details
- Performance metrics, OKR scores not published externally
- Agent-to-agent communication logs
- Source code in private repositories

Rules:
- Shared freely between authorized agents and the human owner
- Not sent to external parties, third-party APIs, or public channels without explicit approval
- Logged in DECISION.md if shared outside the company for the first time

### CONFIDENTIAL
Sensitive business or user data where exposure causes meaningful harm.

Examples:
- Customer names, email addresses, purchase history
- Client contracts, negotiated pricing, SLAs
- Revenue figures, detailed financial reports before external publication
- Agent API keys scoped to production systems (non-secret but not public)
- User behavior analytics tied to identifiable users
- Prospect lists, pipeline data, outreach contact records

Rules:
- Encrypted at rest (AES-256 or equivalent) and in transit (TLS 1.2 minimum)
- Access logged: who accessed, when, purpose
- Not transmitted outside the company without encryption and explicit approval per transfer
- Deleted or anonymized on schedule per §3
- Breach or unauthorized access = SEV1 incident (INCIDENT.md §2)

### RESTRICTED
Highest sensitivity. Exposure causes severe harm — legal, financial, reputational, or regulatory.

Examples:
- Full payment card data, bank account numbers
- Government-issued ID numbers (KTP, passport, tax ID) of customers or the owner
- OAuth tokens, session tokens, webhook signing secrets, private keys
- Database credentials, infrastructure passwords
- Any data subject to explicit legal hold or regulatory requirement

Rules:
- Same rules as CONFIDENTIAL, plus:
- Never logged, even partially (mask to `[RESTRICTED:redacted]` in all logs)
- Never included in agent context windows or prompts — must be injected at runtime via secret manager only
- Never transmitted in any form to a third-party service without owner approval logged in DECISION.md
- Suspected exposure = immediate SEV1 — rotate/revoke before investigating (SECURITY.md §2)

**Default rule:** If classification is uncertain, assign one level higher. An agent that cannot determine classification must ask before acting, not guess.

---

## §2 — PII DEFINITION AND INVENTORY

### What Counts as PII in This Company

PII (Personally Identifiable Information) is any data point that, alone or combined with other data points, can identify a specific natural person.

**Direct PII — always PII regardless of context:**
- Full name (first + last together)
- Email address
- Phone number
- Physical mailing address
- Government ID numbers (KTP, SIM, NPWP, passport number)
- Payment card numbers, bank account numbers
- IP address linked to an individual
- Device identifier linked to an individual

**Indirect PII — PII when combined with other data:**
- First name alone (not PII); first name + company name + city (PII)
- Job title alone (not PII); job title + employer + industry + location (PII)
- Purchase category alone (not PII); purchase category + timestamp + account ID (PII)

**PII Classification Level:** All PII is classified CONFIDENTIAL at minimum. PII that includes financial or government ID data is RESTRICTED.

### PII Inventory

Agents that create or receive PII must register it in the PII inventory within 24 hours of first collection.

**Inventory location:** `~/.1ai/data/governance/pii-inventory.json`

**Required fields per PII asset:**
```json
{
  "asset_id": "pii-[YYYY]-[NNN]",
  "description": "what data is held",
  "source": "where it came from (form, API, manual entry)",
  "data_class": "CONFIDENTIAL or RESTRICTED",
  "subjects": "customers / prospects / owner / other",
  "fields": ["email", "name", "..."],
  "storage_location": "path or service name",
  "retention_days": 365,
  "collected_date": "YYYY-MM-DD",
  "deletion_due": "YYYY-MM-DD",
  "legal_basis": "consent / contract / legitimate interest / legal obligation",
  "registered_by": "agent-id"
}
```

Any PII not in the inventory is a governance violation. Finance Agent audits the inventory monthly.

---

## §3 — RETENTION SCHEDULE

Data must be deleted or anonymized when its retention period expires. Expiry is calculated from the date the data was last updated or the triggering event, whichever is later.

| Data Type | Classification | Retention Period | Deletion Trigger |
|-----------|---------------|-----------------|-----------------|
| Customer email + name (active customer) | CONFIDENTIAL | Duration of relationship + 12 months | Account closure + 12 months |
| Customer email + name (prospect, no purchase) | CONFIDENTIAL | 6 months from last contact | 6 months with no engagement |
| Purchase history and transaction records | CONFIDENTIAL | 7 years | 7 years after transaction date (tax/legal requirement) |
| Payment card data | RESTRICTED | 0 days — never persist | Delete immediately after payment processor confirms |
| Government ID data | RESTRICTED | Duration of KYC need only | Verified identity confirmed; purge within 30 days |
| API call logs (external services) | INTERNAL | 90 days rolling | Automatic rolling deletion after 90 days |
| Agent decision logs | INTERNAL | 1 year | 1 year after log creation |
| Audit trail entries (§10) | INTERNAL | 2 years | 2 years after entry creation — never before |
| Finance records (revenue, spend) | CONFIDENTIAL | 7 years | 7 years after fiscal year close |
| Security incident records | CONFIDENTIAL | 3 years | 3 years after incident closure |
| Internal roadmaps, OKR records | INTERNAL | 2 years after superseded | Replaced by newer version + 2 years |
| Agent system prompt versions | INTERNAL | 1 year after decommission | Agent decommissioned + 1 year |
| Backup files | Inherits source | Source retention + 30 days | Backup generation date + source retention + 30 days |
| Temporary working files (agent scratch) | INTERNAL | Session end | Agent session terminates |

**Retention review:** Finance Agent generates a retention report on the 1st of each month listing all data assets approaching expiry within 30 days. Owner reviews and confirms deletion or grants extension with written justification in DECISION.md.

**Extension rule:** Retention may only be extended once, by up to 6 months, with owner approval. After that, data must be deleted or reclassified with new justification.

---

## §4 — DELETION PROTOCOL

### Soft Delete vs. Hard Delete

**Soft delete** (mark as deleted, retain in storage):
- Permitted ONLY for: finance records within legal retention period, audit trail entries, incident records
- Implementation: add `deleted_at` timestamp and `deleted_by` field; exclude from all queries by default
- Soft-deleted records are invisible to normal operations but remain in storage until hard delete date
- Soft-deleted records are still subject to access controls — no looser permissions because they are "deleted"

**Hard delete** (actual removal from storage):
- Required for: all PII at retention expiry, all RESTRICTED data at retention expiry, all data on customer deletion request
- Implementation requirements:
  1. Delete from primary database (DELETE, not UPDATE)
  2. Delete from all read replicas and caches within 24 hours
  3. Delete from search indexes within 24 hours
  4. Delete from backups: overwrite in next backup cycle; annotate backup manifest that record was deleted
  5. Delete from any third-party system where data was sent (send deletion request to vendor)
  6. Log deletion event in audit trail (§10) — log the fact of deletion, not the deleted data

### Verifiable Deletion Checklist

For every hard delete of CONFIDENTIAL or RESTRICTED data, the executing agent must complete and log:

```
DELETION RECORD
Asset: [asset_id from PII inventory or description]
Deleted by: [agent-id]
Deletion date: [YYYY-MM-DD]
Trigger: [retention expiry / customer request / incident / other]
Locations cleared:
  [ ] Primary database
  [ ] Read replicas
  [ ] Cache layer
  [ ] Search index
  [ ] Backups annotated
  [ ] Third-party systems: [list each, confirmation method]
Audit log entry: [log entry ID]
Owner notified: [yes/no — yes required for RESTRICTED data deletions]
```

This record is stored in `~/.1ai/data/governance/deletion-log.json` and retained for 2 years (it is audit data, not the deleted data itself).

### Customer-Requested Deletion

When a customer requests deletion of their data:
1. Log the request immediately with timestamp and request source
2. Execute hard delete across all systems within 30 days
3. Notify customer of completion with the list of systems cleared
4. Retain only: transaction records required by law (7-year finance rule), anonymized aggregate analytics
5. Anonymization means: replace all PII fields with random tokens; retain non-PII fields (purchase amount, product category) only if they cannot re-identify the person

---

## §5 — BACKUP RULES

### Backup Scope

| Data Type | Backup Required | Frequency | Retention |
|-----------|----------------|-----------|-----------|
| Finance records | Yes — mandatory | Daily | 7 years |
| Customer PII (CONFIDENTIAL) | Yes — mandatory | Daily | Match source retention + 30 days |
| Audit trail logs | Yes — mandatory | Daily | 2 years |
| Source code (private repos) | Yes — via git remote | Continuous (every push) | Indefinitely |
| Agent configurations and prompts | Yes — mandatory | Daily | 1 year after decommission |
| Operational databases | Yes — mandatory | Daily full + hourly incremental | 90 days rolling |
| Temporary scratch files | No | — | — |
| Public content already published | Optional | — | — |

### Storage

- Primary backup storage: owner-designated cloud storage bucket (configured in `~/.1ai/config/backup.json`)
- Backup storage must be in a different region or provider from primary storage
- Backups encrypted at rest using a key stored separately from the backup data
- Backup encryption key stored in the secret manager, not in any backup file

### Verification

- **Weekly:** Automated restore test — restore a random subset of backup files to a staging location and verify checksums match the source
- **Monthly:** Full restore drill — restore the previous month's database backup to a staging environment and run a smoke test query set
- **On any restore attempt from production incident:** Verify backup integrity before treating restore as authoritative

Verification results logged in `~/.1ai/data/governance/backup-verification.json`.

If a weekly verification fails: escalate to owner immediately; treat as potential data loss incident until confirmed otherwise.

### Access

- Backup files: read access limited to the designated Backup Agent and the human owner
- No other agent may read backup files without owner approval logged in DECISION.md
- Backup encryption keys: RESTRICTED classification; follow SECURITY.md §2 for all access

---

## §6 — ACCESS CONTROL

Access to data assets is determined by agent role (ROLES.md) and data classification. The table below is the authoritative permission matrix. Any access not listed here is denied by default.

### Permission Matrix

| Data Class | L1 Junior Agent | L2 Standard Agent | L3 Senior Agent | L4 Lead Agent | L5 Owner |
|------------|----------------|-------------------|-----------------|---------------|----------|
| PUBLIC — read | ✓ | ✓ | ✓ | ✓ | ✓ |
| PUBLIC — write/publish | ✗ | ✓ (task scope only) | ✓ | ✓ | ✓ |
| INTERNAL — read | ✗ | ✓ (task scope only) | ✓ | ✓ | ✓ |
| INTERNAL — write | ✗ | ✓ (task scope only) | ✓ | ✓ | ✓ |
| INTERNAL — delete | ✗ | ✗ | ✓ | ✓ | ✓ |
| CONFIDENTIAL — read | ✗ | ✗ | ✓ (task scope only) | ✓ | ✓ |
| CONFIDENTIAL — write | ✗ | ✗ | ✓ (task scope only) | ✓ | ✓ |
| CONFIDENTIAL — delete | ✗ | ✗ | ✗ | ✓ | ✓ |
| RESTRICTED — read | ✗ | ✗ | ✗ | ✓ (read-only, logged) | ✓ |
| RESTRICTED — write | ✗ | ✗ | ✗ | ✗ | ✓ |
| RESTRICTED — delete | ✗ | ✗ | ✗ | ✗ | ✓ |

### Access Rules

- **Task scope only** means: an agent may access that data class only for the specific task it is currently executing. It may not read-ahead, cache, or retain data beyond the task's completion.
- Access must be revoked when the task ends. An agent that completes a task retains no data access from it into the next session.
- No agent reads another agent's working memory, context, or intermediate outputs unless explicitly designed to do so and documented in ROLES.md.
- The Finance Agent may read CONFIDENTIAL finance data within its defined role scope. It may not read CONFIDENTIAL customer PII unless a task explicitly requires it.
- Access exceptions require owner approval and a DECISION.md entry. No self-granted exceptions.

### Access Logging

Every access to CONFIDENTIAL or RESTRICTED data must produce an audit log entry (§10). Minimum fields: who, what data class, what specific record or query, when, task context.

---

## §7 — DATA BREACH RESPONSE

### Detection Triggers

The following conditions must be treated as a potential breach immediately — no waiting for confirmation:

| Trigger | Detection Method |
|---------|-----------------|
| CONFIDENTIAL or RESTRICTED data appears in a log, prompt output, or external API response where it should not | Agent output review, log scanning |
| Agent sends data to an unapproved external endpoint | Outbound request monitoring |
| Backup file is accessed by an agent not in the authorized list | Backup access log alert |
| PII found in a public repository, public URL, or published content | Automated PII scan on publish pipeline |
| Third-party service reports a breach involving data we sent them | Vendor notification |
| Unauthorized read of RESTRICTED data detected in audit log | Audit trail alert rule |
| Customer reports receiving another customer's data | Customer support escalation |

### Response Sequence

**Within 15 minutes of detection:**
1. Declare SEV1 incident in INCIDENT.md §2 — do this before investigating
2. Identify the data involved: classification, record count, specific fields, affected individuals
3. Contain the leak: revoke the API key or token involved, close the exposed endpoint, remove the exposed file — stop further exposure before root cause analysis

**Within 1 hour:**
4. Notify owner via primary channel (Telegram) with: what was exposed, how many records, containment action taken, next steps
5. Begin scope determination: how far did the data travel? Which systems received it? Which logs contain it?

**Within 24 hours:**
6. Complete scope assessment
7. Determine whether customer notification is required (see threshold below)
8. If third-party systems received the data: contact each vendor with deletion request and incident reference

**Within 72 hours:**
9. Complete postmortem draft (INCIDENT.md §5)
10. If customer notification required: send notification (see template below)

### Customer Notification Threshold

Notify affected customers when ANY of these are true:
- More than 0 customers' RESTRICTED data was exposed (zero tolerance for RESTRICTED breach without notification)
- More than 10 customers' CONFIDENTIAL PII was exposed
- Any exposure where there is reasonable risk of harm to the affected individual (financial fraud, identity theft)
- Legal or regulatory obligation requires notification (check applicable laws for the customer's jurisdiction)

**Notification must include:**
- What data was affected (specific fields, not vague)
- When the exposure occurred (date range)
- How it was exposed
- What BerkahKarya/1ai has done to contain it
- What the customer should do (if anything — e.g., change password, monitor accounts)
- A contact point for questions

Notification sent within 72 hours of confirming customer impact. Owner reviews notification before sending. Notification logged in incident record.

---

## §8 — THIRD-PARTY DATA SHARING RULES

### Approved Sending Conditions

Data may only be sent to an external service when ALL of the following are true:
1. The service is in the approved integrations list (`~/.1ai/config/approved-services.json`)
2. The data class is permitted for that service (table below)
3. The transfer uses an encrypted channel (HTTPS/TLS 1.2+)
4. The transfer is logged in the audit trail (§10)

### Permitted Data by Service Category

| Service Category | PUBLIC | INTERNAL | CONFIDENTIAL | RESTRICTED |
|-----------------|--------|----------|--------------|------------|
| Payment processors (Stripe, Midtrans) | ✓ | ✗ | Payment fields only (contractual) | Minimum required by processor |
| Email delivery services (for transactional email) | ✓ | ✗ | Recipient email + first name only | ✗ |
| Analytics services (aggregate, non-PII) | ✓ | ✗ | Anonymized only | ✗ |
| AI/LLM API providers | ✓ | Task content only (no PII) | ✗ | ✗ |
| Cloud infrastructure providers (hosting) | ✓ | ✓ | ✓ (encrypted at rest) | ✓ (encrypted, owner-approved) |
| CRM or marketing platforms | ✓ | ✗ | Email + name with consent only | ✗ |
| Error monitoring / observability (e.g., Sentry) | ✓ | ✓ | Masked only — no PII in error traces | ✗ |

### LLM/AI API Special Rule

This is the most important third-party rule for an AI-agent company:

- **Never send CONFIDENTIAL or RESTRICTED data to any LLM API (OpenAI, Anthropic, Google, etc.) as part of a prompt or context.**
- This includes: customer emails, names, purchase history, financial data, internal pricing, credentials.
- If a task requires an LLM to process customer data: anonymize or synthesize first. Use `[CUSTOMER]`, `[EMAIL_REDACTED]`, `[AMOUNT]` placeholders.
- This rule applies even if the LLM provider claims data is not used for training. The classification rule is about transmission, not storage.

### New Third-Party Integration

Sending data to any service not in the approved list requires:
1. Owner approval, logged in DECISION.md
2. Data sharing agreement or DPA (Data Processing Agreement) in place if vendor handles PII
3. Service added to `approved-services.json` with permitted data classes specified
4. One-time is not an exception — if a service receives our data, it must be in the list

---

## §9 — AGENT DATA HYGIENE

Rules for agents handling data in memory and context windows.

### Context Window Rules

- Load only the data required for the current task. Do not preload data "in case it's needed."
- Customer PII in a context window is task-scoped. When the task ends, the context is discarded — do not summarize PII into persistent memory or notes files.
- When processing multiple customer records in sequence, clear the previous customer's data from working state before loading the next customer's data.
- Do not include raw CONFIDENTIAL or RESTRICTED data in agent-to-agent messages. Pass record IDs or references; let the receiving agent retrieve only what it needs.

### Memory and Persistence Rules

- Agents with persistent memory capabilities (vector stores, memory files, brain saves) must not persist CONFIDENTIAL or RESTRICTED data.
- What may be persisted: task outcomes (counts, statuses, IDs), business logic decisions, non-PII operational context.
- What must not be persisted: customer names, emails, financial figures tied to individuals, any RESTRICTED field.
- Memory entries containing PII that were written before this rule existed must be audited and purged. Finance Agent schedules this audit quarterly.

### Logging Hygiene

- Before writing any log line, the agent must check whether the message contains data classified CONFIDENTIAL or above.
- If yes: mask the sensitive fields before logging. Format: `[CONFIDENTIAL:field_name]` or hash the value.
- Log lines must never contain: email addresses, full names, payment data, credentials, IP addresses tied to individuals.
- This applies to: application logs, error traces, debug output, agent decision logs, DECISION.md entries.

### Prompt Construction Rules

- When building a prompt that requires context about a customer, use the minimum identifying information needed.
- Prefer: "the customer with order ID ORD-2026-042" over including the customer's name and email in the prompt.
- If a task genuinely requires PII in a prompt (e.g., writing a personalized email), the PII is task-ephemeral — it exists in that session only and is not persisted anywhere after the task.
- Agents must not construct prompts that ask an LLM to "remember" or "store" customer data for future use.

### Scope Termination

When an agent's task completes:
1. Release all in-memory references to CONFIDENTIAL or RESTRICTED data
2. Do not write task-scope data to any persistent store unless explicitly required by the task spec
3. If the agent wrote temporary files during the task, delete them before declaring the task done
4. Log task completion with data classes handled (not the data itself): e.g., `"handled: CONFIDENTIAL (customer record read), no data persisted"`

---

## §10 — AUDIT TRAIL

### What Must Be Logged

Every data operation listed below requires an audit log entry. "Logging the action" means recording the event, not the data value.

| Operation | Log Required | Minimum Fields |
|-----------|-------------|----------------|
| Read of any CONFIDENTIAL record | Yes | who, record-id, timestamp, task-context |
| Read of any RESTRICTED record | Yes | who, record-id, timestamp, task-context, owner-approval-ref |
| Write of any CONFIDENTIAL record | Yes | who, record-id, fields-modified, timestamp, task-context |
| Write of any RESTRICTED record | Yes | who, record-id, fields-modified, timestamp, task-context, owner-approval-ref |
| Delete of any record (hard delete) | Yes | who, asset-id, deletion-trigger, timestamp, deletion-checklist-ref |
| Export of CONFIDENTIAL data to any external system | Yes | who, destination, record-count, data-class, timestamp, approval-ref |
| Failed access attempt to CONFIDENTIAL or RESTRICTED | Yes | who, what-was-attempted, timestamp, outcome: denied |
| PII inventory addition | Yes | who, asset-id, data-class, timestamp |
| Backup verification outcome | Yes | who, backup-date, verification-method, outcome, timestamp |
| Third-party data transfer | Yes | who, service, data-class, record-count, timestamp |

### Log Format

Every audit log entry is a JSON object:

```json
{
  "log_id": "audit-[YYYY]-[NNNNNN]",
  "timestamp": "2026-07-05T14:32:00Z",
  "agent_id": "agent-id or owner",
  "operation": "READ | WRITE | DELETE | EXPORT | FAILED_ACCESS | OTHER",
  "data_class": "PUBLIC | INTERNAL | CONFIDENTIAL | RESTRICTED",
  "resource": "table:record-id or service:endpoint or file:path",
  "task_context": "task-id or description of why",
  "approval_ref": "DECISION.md entry ID if required, else null",
  "outcome": "SUCCESS | DENIED | ERROR",
  "notes": "optional — unusual circumstances only"
}
```

### Log Storage and Integrity

- **Location:** `~/.1ai/data/governance/audit-log-[YYYY-MM].jsonl` (newline-delimited JSON, one entry per line)
- **Append-only:** No entry may be edited or deleted after creation. If an error exists in an entry, add a correction entry referencing the original `log_id`.
- **Retention:** 2 years from entry creation date
- **Backup:** Included in daily backup scope (§5)
- **Access:** Read access: L4 Lead Agent and Owner only. No agent may write to the audit log file except through the designated logging function — no direct file manipulation.

### Log Monitoring

- Finance Agent reviews audit logs weekly for anomalies:
  - Unusual access patterns (high volume reads by a single agent in short time)
  - Failed access attempts (3+ in 24 hours by the same agent = alert to owner)
  - RESTRICTED data reads without an approval reference
  - Gaps in the log sequence (missing `log_id` values in sequence = potential tampering)
- Anomalies flagged to owner immediately via the configured notification channel.
- Audit log gap = treated as a potential security incident until explained.

---

Current version: 1.0.0
Last reviewed: 2026-07-05
Next scheduled review: 2027-01-05 (semi-annual)
