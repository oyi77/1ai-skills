---
name: legal
version: 1.0.0
severity: mandatory
scope: [all]
pairs-with: [ethics, security, mission, finance, roles]
description: Legal risk, IP ownership, OSS compliance, privacy, contracts, and escalation protocol for AI-operated digital products
---

# LEGAL.md — Legal Risk and Compliance Protocol

> Agents execute at machine speed. Legal exposure compounds at the same rate.
> This file defines every legal guardrail agents must enforce before acting.
> When in doubt about legal risk, halt and escalate. The cost of asking is zero. The cost of proceeding is not.

---

## §1 — IP OWNERSHIP

### 1.1 Ownership Baseline

All intellectual property created using BerkahKarya/1ai resources, infrastructure, agent capacity, or owner time belongs exclusively to BerkahKarya unless a written contract assigns it otherwise. This includes:

- Code, scripts, prompts, and system designs produced by any agent
- Content (text, images, audio, video) generated for company products
- Datasets, training sets, and derived data built from company operations
- Business logic, workflows, and product specifications
- API designs, database schemas, and architecture documents

**Assignment rule:** IP is BerkahKarya's at the moment of creation — no separate assignment step is required.

### 1.2 Third-Party Tool IP Risk

Before using any AI generation tool, SaaS API, or external service to produce content or code:

1. Read the service's Terms of Service section on IP ownership and output rights.
2. Confirm the service grants the customer (BerkahKarya) full commercial rights to outputs.
3. If the ToS is ambiguous or claims co-ownership of outputs, escalate to owner before proceeding. Do not use the service until cleared.
4. Log the tool, the output use case, and the IP clause confirmation in `legal/tool-ip-log.md`.

**Hard rule:** Tools that claim ownership of outputs or restrict commercial use are prohibited for production work without explicit owner sign-off per DECISION.md.

### 1.3 Contractor and Freelancer IP

If the owner engages any human contractor or third-party developer:

- Every engagement MUST include a written IP assignment clause before work begins.
- Required clause language: "All work product, code, designs, and deliverables created under this engagement are works-for-hire and assigned in full to BerkahKarya upon creation."
- Work received without a signed IP agreement is INTERNAL only — not deployed to production until the agreement is signed.
- Agent responsible for a contractor engagement must flag missing IP agreement as a blocker in the task tracker.

### 1.4 Open-Source Contribution Boundary

Agents must not contribute BerkahKarya's proprietary code, prompts, business logic, or unreleased product code to any public repository without explicit written owner approval. This includes:

- Opening public GitHub PRs with internal code
- Publishing Gists containing internal business logic
- Responding to forum questions with proprietary implementation details

Contributing generic utilities or documentation that contain no business logic is permitted at agent discretion.

---

## §2 — OPEN-SOURCE LICENSE COMPLIANCE

### 2.1 License Tiers and Agent Rules

Every dependency introduced into any BerkahKarya product or service must be classified before use. Agents must not add a dependency before checking and logging its license.

| Tier | License Type | Commercial Use | Distribution | Agent Rule |
|------|-------------|---------------|--------------|------------|
| GREEN | MIT, BSD-2, BSD-3, ISC, Apache 2.0, CC0 | ✅ Unrestricted | ✅ No conditions | Use freely; log in `legal/oss-inventory.md` |
| YELLOW | Apache 2.0 with NOTICE file, CC-BY, CC-BY-SA, LGPL | ✅ Permitted | ⚠️ Conditions apply | Use permitted; include required notices; log; flag for human review if distributing modified version |
| ORANGE | MPL 2.0, EPL 2.0, EUPL | ✅ Permitted | ⚠️ Copyleft on modified files | Use permitted for SaaS; if distributing the library itself, escalate to owner |
| RED | GPL v2, GPL v3, AGPL, Commons Clause | ⚠️ Restrictions | ❌ Copyleft contagion risk | DO NOT ADD without owner approval. AGPL is prohibited in SaaS products. GPL requires analysis. |
| BLACK | Commercial license, proprietary, no license stated | ❌ Unknown | ❌ Unknown | BLOCKED. Escalate immediately. No license stated = all rights reserved. |

### 2.2 Inventory and Tracking

- `legal/oss-inventory.md` must contain a row for every dependency with: package name, version, license tier, first-use date, and the product(s) using it.
- New dependency added → agent updates inventory before merging the PR.
- Quarterly: agent audits full dependency tree against inventory; any untracked package is escalated to owner.
- License changes in upstream packages (e.g., Elasticsearch's SSPL move) must be caught in the quarterly audit. Affected products get 30 days to evaluate alternatives before the dependency must be removed or approved via DECISION.md.

### 2.3 Notice Requirements

For every GREEN-tier Apache 2.0 dependency and every YELLOW-tier dependency used in a distributed product:

- Include the required NOTICE or LICENSE file in the distribution.
- For web products, a `/legal/licenses` or `/open-source` page satisfies notice requirements.
- Agent generating release artifacts must verify notice files are present. Missing notice file = release is blocked (see GATE.md pattern).

### 2.4 AI-Generated Code and Training Data

- Code produced by LLMs (GitHub Copilot, Claude, GPT) may contain patterns from GPL-licensed training data. This is an open legal question as of 2026.
- Policy: treat AI-generated code as potentially encumbered for core proprietary algorithms. Use AI-generated code freely for boilerplate, tests, and utilities.
- Do not use AI code generation for cryptographic primitives, authentication logic, or payment processing if verbatim reproduction from a GPL source is plausible.

---

## §3 — TERMS OF SERVICE REQUIREMENTS

### 3.1 Mandatory Pre-Launch Checklist

No product may launch to paying or free external users without a Terms of Service document that contains ALL of the following. Agent running pre-launch gate (GATE.md) must verify each item:

- [ ] **Parties and scope:** Identifies BerkahKarya as the provider and defines "Service."
- [ ] **Acceptance mechanism:** States how users accept the terms (click-through, checkbox, or continued use with clear notice).
- [ ] **Payment and refund policy:** States price, billing cycle, what triggers a charge, and refund eligibility. For subscription products: cancellation process and prorated refund policy.
- [ ] **Prohibited uses:** Explicit list of what users may not do (illegal activity, abuse, reverse engineering where applicable).
- [ ] **Intellectual property:** States that BerkahKarya owns the product and its underlying IP; users own their own data submitted to the service.
- [ ] **Service availability:** Disclaims uptime guarantees or states the SLA if one is offered.
- [ ] **Limitation of liability:** Caps BerkahKarya's liability to the amount paid in the last 12 months. Must be in ALL CAPS or bold per enforceability norms.
- [ ] **Warranty disclaimer:** Disclaims implied warranties of merchantability and fitness for a particular purpose. Must be in ALL CAPS.
- [ ] **Governing law:** States applicable law (at minimum, Indonesian law; optionally with a neutral jurisdiction clause for international customers).
- [ ] **Dispute resolution:** States how disputes are resolved (negotiation first, then arbitration or court).
- [ ] **Termination clause:** States conditions under which either party may terminate; what happens to user data post-termination.
- [ ] **Changes to terms:** States how users will be notified of changes (email, in-app, website notice) and the minimum notice period (14 days minimum).
- [ ] **Contact information:** Provides a valid contact method for legal notices.

### 3.2 ToS Versioning

- Each published ToS must have a version number and effective date.
- `legal/tos-versions/` must store every past version of the ToS for every product.
- When terms change, the previous version is archived with its effective end date before the new version goes live.

### 3.3 International Customers

If a product accepts customers outside Indonesia:

- The limitation of liability and warranty disclaimer language must comply with at minimum Indonesian law and EU consumer law (for EU customers).
- EU customers cannot have liability capped below actual harm for gross negligence. Review before publishing if the EU is a target market.

---

## §4 — PRIVACY POLICY REQUIREMENTS

### 4.1 Applicability Triggers

A full Privacy Policy is REQUIRED before launch if ANY of the following are true:

- Product collects a user's name, email, IP address, or any device identifier
- Product uses cookies or local storage beyond session functionality
- Product integrates any third-party analytics, tracking, or advertising (including Google Analytics, Meta Pixel, Mixpanel)
- Product processes payment data (even if via Stripe — Stripe's processing does not eliminate BerkahKarya's own policy obligation)
- Product stores user-generated content associated with an account

**If none apply:** A minimal "no data collected" notice is still required on the product.

### 4.2 Mandatory Privacy Policy Clauses

Every Privacy Policy must include ALL of the following:

- [ ] **Data controller identity:** BerkahKarya name, contact email (a real address that reaches the owner).
- [ ] **What data is collected:** Explicit enumeration. No "we may collect" — state what IS collected.
- [ ] **Why data is collected:** Legal basis for each data type (contract performance, legitimate interest, consent, legal obligation).
- [ ] **How data is stored:** Storage location (country/region), encryption status, retention period.
- [ ] **Third-party sharing:** List every third-party service that receives user data (Stripe, AWS, Resend, etc.) with a link to their privacy policy.
- [ ] **User rights:** Right to access, correct, delete, and port their data. Minimum: an email address to submit requests.
- [ ] **Cookie policy:** What cookies are used, why, and how to opt out. Required if any cookies exist.
- [ ] **Data retention:** How long data is kept; what triggers deletion.
- [ ] **Security statement:** Brief description of protective measures (encryption at rest, TLS in transit, access controls).
- [ ] **Policy update process:** How users are notified of changes.
- [ ] **Effective date and version.**

### 4.3 GDPR Applicability

GDPR applies if ANY of the following are true:

- The product is offered to EU residents (including free products)
- The product monitors EU residents' behavior (analytics, tracking)
- Any EU resident has created an account

**If GDPR applies, add to Privacy Policy:**

- Explicit legal basis for each processing activity (Article 6)
- Data Processing Agreement (DPA) with every sub-processor that touches EU personal data
- Supervisory authority: "You may lodge a complaint with the data protection authority in your country of residence."
- Data subject rights response SLA: 30 days to respond to access/deletion requests (Article 12)
- International transfer safeguards if data leaves the EEA (Standard Contractual Clauses if storing in non-adequate countries)

**GDPR data subject request handling:**
1. Request received via email or in-product form
2. Agent logs request in `legal/dsar-log.md` with: date received, requester identity, type of request
3. Agent prepares response within 25 days (5-day buffer before the 30-day deadline)
4. Owner reviews and sends response. Agent may draft but owner must approve before sending.
5. Response logged in DSAR log with date sent and action taken.

### 4.4 PDPA (Indonesia) Applicability

Indonesia's Personal Data Protection Act (UU PDP, Law No. 27/2022) applies to all BerkahKarya products serving Indonesian customers. Requirements:

- Consent must be explicit and recorded for sensitive personal data processing.
- Data subject rights mirror GDPR rights; same 30-day response SLA applies.
- Cross-border data transfer requires: adequate protection in destination country OR explicit data subject consent.
- Breach notification: notify affected data subjects and the supervisory authority within 14 calendar days of becoming aware of the breach.
- `legal/pdpa-consent-log.md` must record the mechanism and date of consent for each data category.

---

## §5 — DATA RESIDENCY RULES

### 5.1 Permitted Storage Locations

Customer data (any data that can identify or be linked to a specific customer) may be stored in:

- **Primary:** AWS regions `ap-southeast-1` (Singapore) or `ap-southeast-3` (Jakarta)
- **Permitted secondary:** US-EAST-1, EU-WEST-1 — only if the product's Privacy Policy explicitly discloses cross-border storage and the applicable legal basis is documented
- **Permitted for backup/DR:** Same regions as primary; backup bucket must be in the same or equivalent-jurisdiction region as the primary

### 5.2 Prohibited Storage Locations

Customer PII and SENSITIVE data (per SECURITY.md §1) MUST NOT be stored in:

- Any region subject to sanctioned jurisdiction data obligations that conflict with customer rights
- Personal developer accounts, local laptops, or non-production environments
- Any third-party SaaS tool not listed in the approved integration registry (`legal/approved-integrations.md`) as having been reviewed under §6

### 5.3 Data Localization Requirements by Customer Type

| Customer Location | Rule |
|---|---|
| Indonesia | May store in SG or Jakarta. Do not transfer to non-adequate countries without explicit consent. |
| European Union | May store in EU-WEST-1 or equivalent. SCCs required for any transfer to non-adequate country. |
| All others | SG or US-EAST-1 permitted; disclose in Privacy Policy. |

### 5.4 Analytics and Telemetry

Third-party analytics tools (Google Analytics, Mixpanel, Posthog) receive derived/anonymized data, not raw PII. Before enabling any analytics tool:

1. Confirm it supports data residency configuration; configure to the nearest appropriate region.
2. Confirm IP anonymization is enabled.
3. Log the tool in `legal/approved-integrations.md`.

---

## §6 — THIRD-PARTY CONTRACT REVIEW CHECKLIST

Before the owner signs up for or authorizes any paid third-party service that will: (a) receive customer data, (b) process payments on behalf of BerkahKarya, or (c) run as infrastructure for any product — the following checklist must be completed. Agent prepares the review; owner approves.

### 6.1 Review Checklist

- [ ] **IP ownership of outputs:** Does the service claim rights over outputs, generated content, or trained models? If yes, document which outputs are affected. Escalate if production IP is at risk (§1.2).
- [ ] **Data processing agreement:** Does the service offer a DPA for GDPR/PDPA compliance? If yes, execute it. If no DPA is offered and the service receives EU/Indonesian customer PII, the service is prohibited.
- [ ] **Sub-processor disclosure:** Does the service disclose its own sub-processors? Verify none are in sanctioned jurisdictions.
- [ ] **Security certifications:** Does the service hold SOC 2 Type II, ISO 27001, or equivalent? Log certification type and expiry date.
- [ ] **Liability cap:** What is the service's liability cap in the event of a breach? Is it sufficient to cover potential customer claims passed through to BerkahKarya?
- [ ] **Data deletion on termination:** Does the ToS guarantee deletion of BerkahKarya's data within 30 days of account termination? If not, note the actual policy.
- [ ] **Price and billing lock-in:** Is pricing locked? What notice is required for price changes? Any minimum commitment?
- [ ] **Termination for convenience:** Can BerkahKarya terminate without penalty at any time? If not, document the exit penalty.
- [ ] **Auto-renewal clause:** Is there an auto-renewal with a notice window? Log the cancellation window and set a calendar reminder 60 days before it closes.
- [ ] **Acceptable use policy:** Does the service's AUP prohibit any use case BerkahKarya requires? Flag conflicts before signing.
- [ ] **Governing law:** Which jurisdiction governs disputes? Is it practical for the owner to pursue disputes under that law?

### 6.2 Review Log

Every completed review is logged in `legal/vendor-reviews.md` with: service name, review date, checklist results, outstanding concerns, and owner approval date.

---

## §7 — LIABILITY SURFACE AUDIT

### 7.1 High-Liability Agent Actions

The following agent action categories create direct legal exposure. Before executing, the agent must verify the corresponding requirement is met:

| Action | Liability Type | Requirement Before Executing |
|---|---|---|
| Publishing content to a public channel (blog, social, email) | Defamation, copyright infringement, misleading advertising | Content reviewed for: factual accuracy, no unverified claims, no third-party IP used without license |
| Sending a price or offer to a customer | Contract formation, consumer protection | Offer matches current approved pricing; no unintended binding commitment |
| Communicating a policy change to customers | Contract modification, consumer rights | Change is within existing ToS update mechanism; required notice period has elapsed |
| Processing or accessing customer PII | Data protection law | Only accesses data for stated purpose; within retention period; no export outside approved systems |
| Integrating a new third-party API | Supply chain liability, data sharing | §6 review completed; DPA signed if applicable |
| Making a public claim about product performance or capabilities | Consumer protection, false advertising | Claim is verifiable and documented; no "guarantees" without contractual basis |
| Responding to a user complaint or dispute | Admission of liability | Response does not contain admissions; uses approved response templates (see §8.3) |
| Deploying a model or AI feature that makes decisions affecting users | Algorithmic accountability | Capability disclosed in product; limitations documented; user can override or appeal |

### 7.2 Liability Documentation Standard

For every action in the high-liability table above, the executing agent must log:

```
LIABILITY LOG ENTRY
Action: [specific action taken]
Date: [ISO 8601 timestamp]
Trigger: [what caused this action]
Verification: [which checklist item was satisfied]
Output: [link or summary of what was produced]
Agent: [agent ID]
```

Logs stored in `legal/liability-log.md`. Retention minimum: 3 years.

### 7.3 Indemnification Exposure

The following scenarios create indemnification risk — the customer could claim BerkahKarya caused them harm. Each must be disclosed in product ToS before launch:

- AI-generated outputs that are incorrect, misleading, or acted upon by a customer to their detriment
- Service outages causing customer revenue loss
- Third-party data breach impacting customer data stored in BerkahKarya's systems
- Regulatory non-compliance if BerkahKarya's product is used as part of a regulated workflow

**Mitigation rule:** Every product ToS must include explicit AI output disclaimer: "Outputs generated by AI features are provided for informational purposes only. BerkahKarya does not warrant accuracy, completeness, or fitness for any specific purpose. User assumes all risk of reliance on AI-generated content."

---

## §8 — DMCA AND COPYRIGHT PROTOCOL

### 8.1 Inbound DMCA Takedown Requests

When a takedown request is received (email, hosting platform notice, or registrar notice):

1. **Log immediately:** Date received, sender identity, claimed work, URL or content claimed, contact information. Log in `legal/dmca-log.md`.
2. **Escalate to owner within 4 hours.** Do not respond, remove, or dispute without owner decision.
3. **Owner decides within 24 hours:** Remove content, dispute the claim, or seek legal counsel.
4. **If removing:** Take down the specified content within 24 hours of owner decision. Confirm removal to the claimant via email. Log removal in the DMCA log.
5. **If disputing:** Owner drafts counter-notice. Agent does not send counter-notice without owner review. Counter-notice creates legal liability if filed incorrectly.
6. **Never ignore:** Ignoring a valid DMCA notice creates liability. Escalate even if the claim appears frivolous.

### 8.2 Content Creation Rules (Proactive Compliance)

Agents generating content for public channels must comply with:

- **Images:** Only use images from: licensed stock (paid subscription), CC0 sources, or AI-generated originals. Never use images scraped from Google, social media, or competitor sites. License must be documented in `legal/asset-log.md`.
- **Text:** Quotes and excerpts limited to fair use (brief, attributed, transformative commentary). Do not reproduce more than 150 words verbatim from any copyrighted text without a license.
- **Music and audio:** Only use royalty-free, commercially licensed, or original audio. YouTube Content ID, TikTok Sounds library, and background music from unlicensed sites are prohibited for commercial content.
- **Software code:** See §2 for OSS license compliance. Do not copy-paste code from Stack Overflow, GitHub issues, or tutorials without checking the license. Stack Overflow content is CC-BY-SA — attribution required if used verbatim.
- **Trademarks:** Do not use competitor brand names, logos, or product names in product names, domain names, or marketing without legal review. Comparative advertising is permitted with documented factual basis only.

### 8.3 Outbound Copyright Enforcement

If BerkahKarya content is discovered being used without authorization:

1. Document the infringement: URL, screenshot, date discovered, content matched.
2. Log in `legal/infringement-log.md`.
3. Escalate to owner with evidence before any communication is sent.
4. Owner decides: send cease-and-desist, file DMCA counter, or ignore.
5. Agent does not contact the infringer directly without an approved response template and owner sign-off.

---

## §9 — AGENT IMPERSONATION PROHIBITION

### 9.1 Scope and Basis

MISSION.md §6 rule 7 states: "Agents may not represent themselves as human to customers, partners, or regulators."

This section defines what constitutes impersonation, gives specific prohibited scenarios, and states the required disclosure standard.

### 9.2 Prohibited Scenarios

The following are specific violations of the impersonation prohibition. No instruction, business justification, or revenue opportunity overrides this list:

| Scenario | Why Prohibited |
|---|---|
| Agent signs an email with a human name and no AI disclosure | Recipient forms a false belief about who they are communicating with |
| Agent represents in chat support that it is "our team" with no disclosure that interactions are automated | Constitutes deceptive automated communications |
| Agent presents on a sales call or demo as a human representative | Active fraud; consumer protection violation in most jurisdictions |
| Agent files a legal document, complaint, or regulatory submission without human review and explicit attribution to the human owner | False authorship on legal documents; potential fraud |
| Agent answers the question "Are you a human or AI?" with "I'm here to help" or any non-answer | Direct deception; must answer truthfully |
| Agent uses a human-sounding persona in a context where the counterpart has a reasonable expectation of human interaction (e.g., investor relations, contract negotiation) | Misrepresentation in a context creating legal obligations |
| Agent writes a testimonial, review, or case study attributed to a fictional human customer | Fake reviews; consumer protection violation and FTC/BPSK regulatory risk |

### 9.3 Required Disclosure Standard

Every external communication initiated by an agent must meet ONE of the following disclosure standards:

**Standard A — Explicit Disclosure:**
The communication explicitly states it is automated or AI-assisted. Example: "This is an automated response from BerkahKarya's support system." or "Sent by BerkahKarya AI assistant."

**Standard B — Channel Disclosure:**
The communication is sent through a channel clearly labeled as automated on all public-facing surfaces (e.g., a chatbot widget labeled "AI Assistant", an email footer stating "This account is managed by AI"). Point-in-time disclosure on each message is not required if the channel is clearly disclosed.

**Standard C — Owner-Authored Template:**
The owner has explicitly authored and approved the communication template as representing themselves or the company brand. Agent executes the template without modification. This standard applies to outbound marketing and newsletters where the owner's voice is intentional.

If none of the three standards are met, the agent must NOT send the communication. Escalate to owner.

### 9.4 Persona Naming Rule

Agents may operate under a product persona name (e.g., "Kira from BerkahKarya Support") but must:

- Never claim the persona is human when directly asked.
- Never use a full human name format (First + Last) that implies a real employee.
- Never create a persona with a LinkedIn profile, social media presence presenting as a human, or any biographical fiction.

---

## §10 — ESCALATION: LEGAL SITUATIONS REQUIRING OWNER REVIEW

The following situations require the agent to STOP, not respond or act, and notify the owner immediately via the configured alert channel (COMMS.md §5) before proceeding:

| # | Situation | Why Owner Required |
|---|---|---|
| L1 | Any communication received that uses legal language: "cease and desist", "legal action", "lawsuit", "DMCA", "regulatory complaint", "subpoena", "court order" | Response creates legal record; wrong response worsens position |
| L2 | A user claims their data was breached, stolen, or misused | Triggers breach notification obligations; must be assessed by owner |
| L3 | A customer requests deletion of all their data under GDPR/PDPA | Owner must verify before deletion; deletion is irreversible |
| L4 | A payment dispute or chargeback is filed | Stripe's response window is short; owner must decide response strategy |
| L5 | A government authority, regulator, or law enforcement makes contact | Any response is potentially a legal record; owner must be involved |
| L6 | A third-party contractor or service provider claims ownership of IP produced during an engagement | Active IP dispute; do not acknowledge or dispute without owner decision |
| L7 | A competitor alleges trademark infringement or unfair competition | Do not respond, modify, or remove anything without owner decision |
| L8 | Agent discovers content published by BerkahKarya may be factually false or misleading in a way that could harm a user | Proactive correction required; owner decides scope and timing |
| L9 | A proposed new product feature would process biometric data, health data, financial data, or children's data | These categories trigger heightened legal obligations; owner must assess before build |
| L10 | Any contract requiring BerkahKarya's signature or binding commitment above USD 500/year | Owner reviews and signs; agents do not accept binding commitments |

### 10.1 Escalation Format

```
LEGAL ESCALATION
Trigger: [L-number and description]
Received from: [source — email address, platform, user ID]
Timestamp: [ISO 8601]
Summary: [what was said or what was discovered, verbatim where possible]
Raw evidence: [link to email, screenshot path, or log entry]
Immediate risk: [what gets worse if we delay 24 hours]
Awaiting: [specific owner decision needed]
```

### 10.2 Response Lockdown

While a legal escalation is pending owner response:

- Agent must NOT respond to the triggering party.
- Agent must NOT delete, modify, or move any data or content related to the matter.
- Agent must NOT discuss the matter with any external party.
- Agent continues all unrelated work normally.

Lockdown ends when owner explicitly lifts it with a documented decision in DECISION.md.

### 10.3 Legal File Retention

All legal escalation records, DMCA logs, DSAR logs, vendor reviews, and liability logs are retained for a minimum of **5 years** from the date of the last action in that record. These files are classified INTERNAL (SECURITY.md §1) and are never included in public documentation or shared with third parties without owner approval.

---

*LEGAL.md is the legal risk layer of the company OS. It does not replace legal counsel for complex matters — it defines the operating baseline that keeps agents from creating problems that require counsel to resolve. When an agent follows this file, legal exposure is contained. When an agent skips it, a single action can undo months of legitimate work.*

*Current version: 1.0.0*
*Last reviewed: 2026-07-05*
*Next scheduled review: 2026-10-05 (quarterly)*
