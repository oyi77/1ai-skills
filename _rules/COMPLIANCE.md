---
name: compliance
version: 1.0.0
severity: mandatory
scope: [all]
pairs-with: [security, ethics, incident, finance, decision]
description: Regulatory compliance scope, audit trail, GDPR/PDPA checklists, data subject rights, and breach notification
---

# COMPLIANCE.md — Regulatory Compliance Protocol

> BerkahKarya/1ai operates globally with digital products. Regulatory obligations are not optional.
> Every agent that handles user data, processes payments, or operates customer-facing systems
> must enforce this file. Ignorance of a regulation is not a defense.

---

## §1 — COMPLIANCE SCOPE

### 1.1 Regulation Trigger Matrix

| Regulation | Trigger Condition | Applies To |
|---|---|---|
| GDPR (EU) | ANY user located in EU/EEA, regardless of company location | All products with EU users |
| PDPA (Indonesia) | ANY Indonesian citizen's personal data is collected or processed | All products with ID users |
| PCI DSS | Any cardholder data (credit/debit card numbers) is stored, processed, or transmitted | Payment flows |
| CAN-SPAM / CASL | Marketing email sent to US or Canadian addresses | Email campaigns |
| COPPA | Any user under age 13 based in USA | Age-gated products |

### 1.2 Applicability Rules

- **Default assumption**: GDPR applies unless the product has zero marketing, zero analytics, and zero EU IP traffic. Proving zero requires evidence.
- **PDPA**: Applies to all products because BerkahKarya is an Indonesian entity. No trigger threshold needed.
- **Stacking**: When multiple regulations apply to the same data, the strictest rule governs. GDPR is stricter than PDPA on most provisions.
- **Agents must check scope before processing any new data category**: if a new data type (e.g., biometric, health) is introduced, escalate to human owner before collection begins.

### 1.3 Out of Scope (this file)

- Tax filing and VAT obligations — handled in FINANCE.md
- Employment law — handled in HIRING.md
- Full legal opinion on any specific jurisdiction — requires human owner + external counsel

---

## §2 — AUDIT TRAIL REQUIREMENTS

### 2.1 Actions That MUST Be Logged

Every log entry must include: `timestamp (ISO 8601 UTC)`, `actor (agent ID or user ID)`, `action`, `target resource`, `outcome`, `IP address if user-initiated`.

| Action Category | Specific Events |
|---|---|
| Authentication | Login success, login failure, MFA challenge, session creation, session revocation, API key creation/revocation |
| Data Access | Read of any PII record, export of user data, admin access to user account |
| Data Modification | Create, update, or delete of any user record, consent record, or payment record |
| Data Transfer | Sending any user data to a third-party processor, webhook delivery containing PII |
| Consent | User consent granted, consent withdrawn, consent record updated |
| Data Subject Requests | DSR received, DSR fulfilled, DSR denied with reason |
| Compliance Events | Compliance review completed, gap identified, gap closed, breach detected |
| Agent Actions | Any agent operation that touches SENSITIVE or CRITICAL data (SECURITY.md §1) |

### 2.2 Retention Periods

| Log Type | Minimum Retention | Maximum Retention | Storage Location |
|---|---|---|---|
| Authentication logs | 90 days | 1 year | append-only log store |
| PII access logs | 1 year | 3 years | append-only log store |
| Consent records | Duration of user relationship + 5 years | Indefinite | immutable records store |
| DSR records | 3 years from request date | 7 years | immutable records store |
| Payment audit trail | 5 years | 10 years | immutable records store |
| Security incident logs | 3 years | 7 years | immutable records store |
| General compliance evidence | 3 years | 5 years | compliance evidence store |

### 2.3 Tamper-Evidence Requirements

- Audit logs MUST be append-only. No agent has permission to delete or modify a log entry after it is written.
- Logs must be stored in a separate system from the application database. An application compromise must not allow log destruction.
- Log integrity: each log entry must include a hash of the previous entry (chain hash) OR logs must be shipped to an immutable external store (e.g., AWS CloudWatch Logs with log group protection, or equivalent) within 60 seconds of creation.
- Agents must NOT log PII values in free-text fields. Log record IDs, not values. Example: log `user_id=u_123 accessed field=email` not `user accessed email=bob@example.com`.
- Any gap in audit logs (missing entries, sequence breaks) triggers a SEV2 compliance incident.

---

## §3 — GDPR COMPLIANCE CHECKLIST

All eight requirements below must be satisfied before any product goes live with EU users.

### 3.1 Lawful Basis (MUST)
- Every data processing activity has a documented lawful basis: consent, contract, legal obligation, vital interests, public task, or legitimate interest.
- Legitimate interest requires a completed Legitimate Interest Assessment (LIA) stored in `~/.1ai/compliance/lia/`.
- Processing without a documented lawful basis is prohibited. Any agent discovering undocumented processing must halt and escalate.

### 3.2 Privacy Policy (MUST)
- A published Privacy Policy exists at a stable URL (e.g., `/privacy`).
- Policy discloses: identity of controller (BerkahKarya), data categories collected, purpose, lawful basis, retention periods, third-party recipients, user rights, DPA contact, right to lodge complaint with supervisory authority.
- Policy must be in plain language, not legal boilerplate.
- Policy is updated within 14 days whenever a material processing change occurs.

### 3.3 Consent Management (MUST where consent is the lawful basis)
- Consent is freely given, specific, informed, and unambiguous. Pre-ticked boxes are prohibited.
- Consent is recorded with: timestamp, version of the consent text shown, user ID, channel.
- Withdrawing consent is as easy as giving it — one-click opt-out for marketing, account deletion flow for full withdrawal.
- Consent records are stored in the immutable records store (§2.2) and never deleted even after user deletion.

### 3.4 Data Minimization (MUST)
- Only data strictly necessary for the stated purpose is collected.
- Before adding any new data field to a user record, the collecting agent must document the purpose in DECISION.md.
- Redundant or expired data fields are removed within 30 days of purpose expiry.

### 3.5 Data Subject Rights (MUST)
- All six GDPR rights are technically implementable: access (Art. 15), rectification (Art. 16), erasure (Art. 17), restriction (Art. 18), portability (Art. 20), objection (Art. 21).
- Response SLAs are defined and enforced (§8 of this file).
- DSR requests received via any channel (email, in-product form) are routed to the compliance queue within 24 hours.

### 3.6 Data Breach Notification (MUST)
- Personal data breaches are reported to the relevant EU supervisory authority within 72 hours of becoming aware, if the breach is likely to result in risk to individuals.
- Affected individuals are notified without undue delay if the breach is likely to result in high risk.
- Protocol defined in §9 of this file.

### 3.7 Data Processing Agreements (MUST)
- A signed DPA is in place with every third-party processor that receives EU personal data before data is sent.
- DPA requirements detailed in §7.
- Sending EU personal data to a processor without a signed DPA is a compliance violation and a SEV2 incident.

### 3.8 Data Transfers Outside EEA (MUST where applicable)
- Personal data transferred outside the EEA only when an adequacy decision exists (e.g., to UK, Japan) or Standard Contractual Clauses (SCCs) are in place.
- Transfer impact assessments (TIA) are completed for any transfer to a country without adequacy status.
- TIA documents stored in `~/.1ai/compliance/tia/`.

---

## §4 — PDPA (INDONESIA) COMPLIANCE CHECKLIST

All six requirements apply to all products because BerkahKarya is an Indonesian entity.

### 4.1 Registration and Notification (MUST)
- BerkahKarya complies with Kominfo (Ministry of Communication) data controller registration requirements where applicable to the product category.
- Users are notified at point of collection: what data is collected, the purpose, how long it is retained, whether it will be shared with third parties.
- Notification is in Bahasa Indonesia for Indonesian-language products, or bilingual for dual-language products.

### 4.2 Consent Requirements (MUST)
- Explicit consent is obtained before collecting sensitive personal data (health, financial, biometric, religious, sexual orientation, political views, criminal records).
- Consent is documented identically to GDPR consent records (§3.3) — the systems are shared.
- Parental consent is required for users under 17 years of age.

### 4.3 Data Security (MUST)
- Personal data is protected with technical and organizational measures appropriate to the risk.
- Minimum technical measures: encryption at rest (AES-256), encryption in transit (TLS 1.2+), access control (principle of least privilege), regular security testing.
- Organizational measures: agent access to PII is logged (§2.1), access is role-gated per ROLES.md, security incidents follow INCIDENT.md.

### 4.4 Data Retention and Deletion (MUST)
- Personal data is not retained longer than necessary for the processing purpose.
- Each data category has a documented retention period (linked from §2.2 table).
- At end of retention period, data is deleted or anonymized within 30 days. Deletion is logged.
- Retention periods are reviewed annually (§5.2).

### 4.5 Cross-Border Data Transfer (MUST)
- Personal data of Indonesian citizens may be transferred to a foreign country only if that country has adequate data protection standards OR a written agreement (equivalent to DPA) exists that ensures equivalent protection.
- Indonesian personal data transferred cross-border is logged in the transfer registry at `~/.1ai/compliance/transfer-registry.json`.

### 4.6 Data Subject Rights — Indonesian Users (MUST)
- Indonesian users have the right to: access their data, correct inaccurate data, and request deletion.
- Rights are fulfilled per §8 SLAs.
- If a user requests deletion and the data is subject to a longer legal retention period, the user is notified of the retention obligation and the reason, in writing, within the SLA window.

---

## §5 — COMPLIANCE REVIEW CADENCE

### 5.1 Quarterly Reviews

Performed within the first 7 days of each quarter (Q1: Jan, Q2: Apr, Q3: Jul, Q4: Oct).

| Review Item | Owner | Output |
|---|---|---|
| Active DSR queue — all requests resolved or in-progress with documented status | Compliance agent | DSR queue report |
| Audit log integrity check — no gaps, hashes valid | Compliance agent | Log integrity report |
| Third-party processor list — all processors have current DPAs | Compliance agent | Processor register update |
| Consent record audit — no orphaned records, withdrawal requests processed | Compliance agent | Consent audit report |
| Compliance debt register — risk levels current, no overdue items | Compliance agent | Debt register update (§10) |
| Security posture check cross-reference — SECURITY.md quarterly items | Security agent | Cross-reference note |

### 5.2 Annual Reviews

Performed in January each year.

| Review Item | Owner | Output |
|---|---|---|
| Full Privacy Policy review and update | Human owner + compliance agent | Updated policy, change log |
| Data retention schedule review — all categories, delete overdue data | Compliance agent | Retention audit report |
| Lawful basis register review — all processing activities have current basis | Compliance agent | Lawful basis register |
| Transfer impact assessments — refresh TIAs for active cross-border transfers | Compliance agent | Updated TIA documents |
| Vendor/processor re-assessment — check processor security posture | Compliance agent | Processor risk report |
| Compliance training acknowledgment — human owner confirms rules reviewed | Human owner | Acknowledgment record |
| Regulation change scan — new/updated regulations affecting the business | Compliance agent | Regulation change brief |

### 5.3 Event-Triggered Reviews

These reviews happen immediately when triggered, not on a schedule:

- New product feature that collects a new data category → lawful basis + privacy notice update before launch.
- New third-party processor onboarded → DPA signed and processor registered before data is sent.
- Data breach or suspected breach → breach assessment within 24 hours (§9).
- User complaint referencing a regulatory right → DSR opened within 24 hours.
- New regulation enacted affecting the company → impact assessment within 30 days.

---

## §6 — EVIDENCE COLLECTION

### 6.1 What Evidence Must Be Stored

Compliance claims without evidence are audit failures. Agents must collect and store evidence automatically at every compliance touchpoint.

| Compliance Touchpoint | Required Evidence | Storage Path |
|---|---|---|
| Consent given | Consent record JSON: user_id, timestamp, consent_version, channel, text_shown_hash | `~/.1ai/compliance/consent/YYYY/MM/` |
| DSR received | Request record: user_id, request_type, received_at, received_via, identity_verified | `~/.1ai/compliance/dsr/YYYY/` |
| DSR fulfilled | Fulfillment record: request_id, fulfilled_at, method, data_exported_hash or deletion_confirmation | `~/.1ai/compliance/dsr/YYYY/` |
| DPA signed | Signed DPA PDF + metadata: processor_name, date_signed, version, data_categories_covered | `~/.1ai/compliance/dpa/` |
| Data deletion | Deletion log: user_id, deleted_at, data_categories_deleted, agent_id, verification_hash | `~/.1ai/compliance/deletion/YYYY/` |
| Breach notification | Notification record: breach_id, notified_authority, notified_at, notification_content_hash | `~/.1ai/compliance/breaches/` |
| Quarterly review | Review report: review_date, items_checked, findings, actions_taken, reviewer_agent_id | `~/.1ai/compliance/reviews/YYYY/QN/` |
| Annual review | Annual report: year, all items in §5.2, sign-off timestamp from human owner | `~/.1ai/compliance/reviews/YYYY/annual/` |

### 6.2 Evidence Integrity

- Evidence files are append-only once written. No agent may modify or delete a compliance evidence file.
- Evidence files are named with ISO 8601 timestamps: `YYYYMMDD-HHMMSS-{type}-{id}.json`.
- Quarterly, the compliance agent verifies that evidence files have not been modified by checking file hashes against a separate hash register at `~/.1ai/compliance/hash-register.json`.
- If a hash mismatch is detected, declare a SEV2 compliance incident immediately.

### 6.3 Automated Collection

- Agents responsible for processing user data must emit compliance events to the compliance event bus in real time.
- Compliance event schema (minimum): `{ event_type, actor_id, user_id_hash, timestamp, data_categories, purpose, outcome }`.
- The compliance agent consumes this event bus and writes evidence files. No manual filing.
- If the compliance event bus is unavailable, the processing agent must buffer events locally and retry. It must NOT proceed with processing that cannot be logged.

---

## §7 — THIRD-PARTY PROCESSOR OBLIGATIONS

### 7.1 Definition

A third-party processor is any external service that processes personal data on behalf of BerkahKarya. This includes: email service providers, analytics platforms, payment processors, AI API providers (where user data is sent), CRM tools, customer support tools, cloud infrastructure providers with data access.

### 7.2 Before Data Is Sent — Mandatory Gates

All three gates must be passed before any personal data is sent to a new processor:

**Gate 1 — DPA exists and is signed**
- A Data Processing Agreement is signed with the processor.
- DPA must include: processing purpose, data categories, retention limits, sub-processor restrictions, deletion obligations, breach notification requirement (72 hours to BerkahKarya), audit rights.
- For GDPR: DPA must incorporate Standard Contractual Clauses if processor is outside EEA.
- Signed DPA stored at `~/.1ai/compliance/dpa/{processor-name}-{date}.pdf`.

**Gate 2 — Processor is registered**
- Processor added to the processor register at `~/.1ai/compliance/processor-register.json`.
- Register entry includes: processor name, service description, data categories sent, lawful basis for transfer, DPA file path, last reviewed date, security certification (e.g., ISO 27001, SOC 2) if available.

**Gate 3 — Minimum security standards verified**
- Processor must have: HTTPS for all data transfer, encryption at rest, documented breach notification procedure.
- Evidence of security standard: security policy URL, certification, or completed security questionnaire stored in `~/.1ai/compliance/processor-security/`.

### 7.3 Ongoing Obligations

- Processor register is reviewed quarterly (§5.1).
- If a processor announces a breach, data incident, or material change to their processing, BerkahKarya must assess impact within 48 hours.
- If a processor cannot or will not sign a DPA, they cannot receive personal data. No exceptions.
- Sub-processors used by the processor must be disclosed and subject to equivalent obligations.

---

## §8 — DATA SUBJECT RIGHTS PROTOCOL

### 8.1 Rights and Response SLAs

| Right | Regulation | Trigger | SLA | Extension Allowed |
|---|---|---|---|---|
| Access (Subject Access Request) | GDPR Art. 15 / PDPA | User requests copy of their data | 30 calendar days from verified receipt | +60 days for complex/multiple requests, user notified within original SLA |
| Rectification | GDPR Art. 16 / PDPA | User requests correction of inaccurate data | 14 calendar days | None |
| Erasure ("Right to be Forgotten") | GDPR Art. 17 / PDPA | User requests deletion | 30 calendar days | +30 days for complex cases, user notified |
| Restriction of Processing | GDPR Art. 18 | User contests accuracy or objects to processing | 14 calendar days to confirm restriction | N/A |
| Data Portability | GDPR Art. 20 | User requests machine-readable export | 30 calendar days | +60 days for large datasets |
| Objection | GDPR Art. 21 | User objects to legitimate interest processing | Immediate suspension of processing; 14 days to assess and respond | None |

### 8.2 DSR Processing Steps

1. **Receipt** — Request arrives via any channel (email to `privacy@`, in-product form, direct message).
2. **Intake** — Compliance agent logs the request within 24 hours: request_id, user_id, right requested, received_at, channel.
3. **Identity Verification** — Before fulfilling any DSR, verify the requester is the data subject. For registered users: require authenticated session or email confirmation from registered address. For unregistered requesters: require proof matching data held.
4. **Assessment** — Determine if request is valid, identify data scope, identify any exemptions (e.g., data required for legal obligation cannot be deleted).
5. **Fulfillment** — Execute the right. For deletion: purge from all stores, including backups within their next scheduled rotation cycle. For access: compile all personal data into structured JSON export.
6. **Response** — Send written response to the data subject: outcome, what was done, any exemptions applied with legal basis.
7. **Evidence** — Store all records per §6.1.

### 8.3 Denial Conditions

A DSR may be denied only when:
- The request is manifestly unfounded or excessive (document reason; user may challenge).
- Fulfilling the request would violate a legal obligation (e.g., financial records retention law).
- Fulfilling erasure would impair a legitimate legal claim in progress.

Denial must be in writing, include the reason and legal basis, and inform the user of their right to escalate to the supervisory authority. Denial is logged as a compliance event.

### 8.4 Tracking

- Open DSRs are tracked in `~/.1ai/compliance/dsr/open-queue.json`.
- Every DSR in the queue is reviewed weekly by the compliance agent for SLA breach risk.
- SLA breach on any DSR triggers a SEV2 compliance incident.

---

## §9 — COMPLIANCE INCIDENT: BREACH NOTIFICATION

### 9.1 What Triggers Notification Obligations

| Event | GDPR Obligation | PDPA Obligation |
|---|---|---|
| Personal data exposed to unauthorized party | Notify supervisory authority within 72 hours if risk to individuals is likely | Notify Kominfo as soon as reasonably practicable |
| Personal data accidentally destroyed or altered | Notify supervisory authority within 72 hours if risk likely | Notify Kominfo as soon as reasonably practicable |
| High risk to individuals' rights and freedoms | Notify supervisory authority AND affected individuals without undue delay | Notify individuals if significant harm is possible |
| Breach with no likely risk to individuals | Log internally; no external notification required | Document; assess whether notification required |

**72-hour clock starts** when BerkahKarya (any agent or the owner) first becomes aware of the breach — not when investigation is complete.

### 9.2 Breach Response Steps

**Hour 0-1: Detect and Contain**
- Declare a SEV1 incident in INCIDENT.md with tag `[COMPLIANCE-BREACH]`.
- Contain: revoke compromised credentials, disable affected endpoints, block further data exfiltration.
- Preserve evidence: do NOT delete logs, do NOT overwrite affected systems.

**Hour 1-4: Assess**
- Identify: what data was affected, how many individuals, categories of data, likely cause.
- Assess risk: is harm to individuals likely? (financial, reputational, physical, discrimination risk)
- Assign breach_id and start breach record at `~/.1ai/compliance/breaches/{breach_id}.json`.

**Hour 4-24: Document**
- Complete breach record: timeline, data categories, number of affected individuals (approximate is acceptable), likely consequences, measures taken to address.
- Determine notification obligation based on risk assessment.

**Hour 24-72: Notify Authority (if required)**
- GDPR: file notification with lead supervisory authority (country of establishment or lead EU authority). Use the authority's official online form. Content: nature of breach, categories and approximate number of affected records, contact details, likely consequences, mitigation measures.
- PDPA: notify Kominfo via official channel. Content equivalent to GDPR notification.
- Store notification submission confirmation at `~/.1ai/compliance/breaches/{breach_id}-notification.pdf`.

**If high risk to individuals — Notify individuals (no fixed deadline, but "without undue delay")**
- Notification to affected individuals: plain language description of what happened, what data was involved, likely consequences, what they can do to protect themselves, contact for questions.
- Method: email to registered address, or in-product notice if email is not available.
- Store list of notified users (hashed IDs, not raw) with timestamp.

### 9.3 Post-Breach

- Conduct a breach postmortem within 14 days: root cause, contributing factors, prevention measures.
- Postmortem stored at `~/.1ai/compliance/breaches/{breach_id}-postmortem.md`.
- Implement all prevention measures within the timeline agreed in the postmortem.
- Follow up with supervisory authority as required (some require closure notification).

---

## §10 — COMPLIANCE DEBT

### 10.1 Definition

Compliance debt is a known gap between the current state and a compliance requirement, where the gap is not yet resolved. Debt must be tracked, not ignored.

### 10.2 Debt Register

All compliance debt is recorded in `~/.1ai/compliance/debt-register.json`.

Each entry must include:

```json
{
  "id": "debt-YYYYMMDD-NNN",
  "regulation": "GDPR | PDPA | PCI-DSS | other",
  "requirement": "exact requirement not yet met",
  "current_state": "what exists today",
  "gap": "specific difference between current state and requirement",
  "risk_level": "CRITICAL | HIGH | MEDIUM | LOW",
  "risk_rationale": "why this risk level",
  "owner": "agent ID or human",
  "target_resolution_date": "YYYY-MM-DD",
  "status": "open | in_progress | resolved | accepted",
  "resolution_plan": "specific steps to close the gap",
  "opened_at": "ISO 8601",
  "last_reviewed": "ISO 8601"
}
```

### 10.3 Risk Level Definitions

| Risk Level | Definition | Maximum Age Before Escalation |
|---|---|---|
| CRITICAL | Active regulatory violation that could result in fine, enforcement action, or imminent harm to users | 14 days — escalate to human owner immediately if not resolved |
| HIGH | Non-compliant with a mandatory requirement but no current exposure or active harm | 30 days — human owner must acknowledge |
| MEDIUM | Partial compliance; mitigating controls exist but gap remains | 90 days — quarterly review |
| LOW | Best practice gap; no current regulatory requirement violated | 180 days — annual review |

### 10.4 Debt Lifecycle

- **Open**: Gap identified, not yet started. Immediately entered in register.
- **In Progress**: Resolution work has started. Expected completion date set.
- **Resolved**: Gap closed. Evidence of resolution stored (path in register entry). Quarterly review confirms closure.
- **Accepted**: Gap acknowledged as acceptable by human owner, with documented rationale and review date. Accepted status must be re-confirmed every 90 days for HIGH+ items.

### 10.5 Escalation Rules

- Any CRITICAL debt item that is not resolved within 14 days triggers a SEV2 compliance incident.
- Any HIGH debt item not resolved within 30 days requires a written acceptance decision from the human owner.
- Compliance agent reviews the debt register at every quarterly review (§5.1) and updates risk levels.
- An item cannot be closed as "resolved" without stored evidence. Claiming resolution without evidence is treated as a compliance violation.

---

## §11 — CROSS-REFERENCES

| Topic | File |
|---|---|
| Data classification (CRITICAL / SENSITIVE / INTERNAL / PUBLIC) | SECURITY.md §1 |
| Incident declaration and severity levels | INCIDENT.md §2 |
| PII prohibition in agent behavior | ETHICS.md §2.2 |
| Agent authority levels | ROLES.md |
| Vendor risk and procurement gates | FINANCE.md (spending gates) |
| Decision logging for new data processing | DECISION.md |

---

Next scheduled quarterly review: 2026-10-05
Next scheduled annual review: 2027-01-05
