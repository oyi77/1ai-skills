---
name: performing-dmarc-policy-enforcement-rollout
description: Execute a phased DMARC rollout from p=none monitoring through p=quarantine to p=reject enforcement, ensuring
  all legitimate email sources are authenticated before blocking unauthorized senders.
domain: cybersecurity
subdomain: phishing-defense
tags:
- dmarc
- spf
- dkim
- email-authentication
- anti-spoofing
- phishing
- dns
- email-security
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.AT-01
- DE.CM-09
- RS.CO-02
- DE.AE-02
---
# Performing DMARC Policy Enforcement Rollout

## Overview
Domain-based Message Authentication, Reporting and Conformance (DMARC) is the cornerstone of email anti-spoofing protection. A DMARC rollout progresses through three phases: monitoring (p=none), quarantine (p=quarantine), and full enforcement (p=reject). When configured at p=reject, any email that fails both SPF and DKIM checks is outright rejected. Google and Yahoo now require DMARC for bulk senders (5,000+ emails), driving a 65% reduction in unauthenticated messages. The rollout typically takes 3-6 months for safe deployment.


## When to Use
**Trigger phrases:**
- "performing dmarc policy enforcement rollout"
- "Execute a phased DMARC rollout from p=none monitoring through p=quarantine to p="


- When conducting security assessments that involve performing dmarc policy enforcement rollout
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites
- Administrative access to DNS management for the domain
- Understanding of SPF, DKIM, and DMARC protocols (RFC 7208, 6376, 7489)
- Complete inventory of all legitimate email sending sources
- DMARC reporting analysis tool (EasyDMARC, DMARCLY, Valimail, or dmarcian)
- Email gateway with DMARC enforcement capability

## Key Concepts

This section covers key concepts for performing dmarc policy enforcement rollout.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### DMARC Policy Levels
| Policy | Behavior | Use Case |
|---|---|---|
| p=none | Monitor only, no action on failures | Discovery phase |
| p=quarantine | Send failing messages to spam/junk | Transition phase |
| p=reject | Block failing messages entirely | Full enforcement |

### DMARC Record Anatomy
```
v=DMARC1; p=quarantine; pct=25; rua=mailto:dmarc-agg@company.com; ruf=mailto:dmarc-forensic@company.com; adkim=r; aspf=r; fo=1
```
- **p**: Policy for organizational domain
- **sp**: Policy for subdomains
- **pct**: Percentage of messages subject to policy (for gradual rollout)
- **rua**: Aggregate report destination (daily XML reports)
- **ruf**: Forensic report destination (per-failure reports)
- **adkim**: DKIM alignment mode (r=relaxed, s=strict)
- **aspf**: SPF alignment mode (r=relaxed, s=strict)
- **fo**: Failure reporting options (0=both fail, 1=either fails)

### SPF and DKIM Alignment
- **SPF Alignment**: The domain in the Return-Path (envelope sender) must match the From header domain
- **DKIM Alignment**: The d= domain in the DKIM signature must match the From header domain
- **Relaxed**: Organizational domain match (sub.example.com matches example.com)
- **Strict**: Exact domain match required

## Workflow

1. **Scope the task** — define objectives, boundaries, and success criteria
2. **Gather information** — collect all necessary data and context before proceeding
3. **Execute the core workflow** — follow the domain-specific steps methodically
4. **Validate results** — verify outputs against expected outcomes or baselines
5. **Document findings** — record results, anomalies, and recommendations
### Step 1: Inventory All Sending Sources (Week 1-2)
- Audit all systems sending email as your domain (marketing, CRM, ticketing, transactional)
- Document third-party services: Salesforce, Mailchimp, SendGrid, Zendesk, etc.
- Identify internal mail servers, applications, and relay hosts
- Check for shadow IT email sending (departments using unauthorized services)

### Step 2: Configure SPF and DKIM (Week 2-4)
- Consolidate SPF record with all legitimate sending IPs and includes
- Ensure SPF record stays under 10 DNS lookup limit
- Generate and publish DKIM keys for each sending source
- Verify DKIM signing works for all outbound mail paths
- Test with MX Toolbox or dmarcian SPF/DKIM validators

### Step 3: Deploy DMARC in Monitoring Mode (Week 4-6)
- Publish initial DMARC record: `v=DMARC1; p=none; rua=mailto:dmarc@company.com; fo=1`
- Wait 1-2 weeks to collect representative aggregate reports
- Analyze reports to identify unauthorized senders and alignment failures
- Fix SPF/DKIM for all legitimate sources showing failures
- Iterate until all legitimate mail passes DMARC

### Step 4: Move to Quarantine with pct Tag (Week 6-12)
- Update to quarantine at 10%: `v=DMARC1; p=quarantine; pct=10; rua=...`
- Monitor for false positives (legitimate mail being quarantined)
- Increase pct gradually: 10% -> 25% -> 50% -> 75% -> 100%
- Each increase: wait 1-2 weeks and review reports before advancing
- Fix any remaining alignment issues discovered at each stage

### Step 5: Advance to Reject Policy (Week 12-20)
- After stable quarantine at 100%, move to reject at 10%: `v=DMARC1; p=reject; pct=10; rua=...`
- Gradually increase pct: 10% -> 25% -> 50% -> 100%
- Monitor closely for legitimate mail being rejected
- Establish emergency rollback procedure (revert to quarantine)
- Apply subdomain policy: `sp=reject` for subdomains

### Step 6: Ongoing Monitoring and Maintenance
- Continuously monitor DMARC aggregate reports
- Add new sending sources before they start sending
- Review forensic reports for spoofing attempts
- Maintain SPF record as sending infrastructure changes
- Rotate DKIM keys annually

## When NOT to Use

- You don't have explicit written authorization to test
- Task is about defense/detection, not offense (use detection skills)
- You need to implement security controls (use implementing-* skills)
- Task requires compliance auditing (use auditing-* skills)
- You're investigating an incident (use incident response skills)
- Target is out of scope for your engagement
- Task is about vulnerability scanning only (use scanning tools)


## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Treating compliance checklists as security guarantees rather than minimum baselines
- Failing to document exceptions and risk acceptance decisions
- Relying on point-in-time audits instead of continuous monitoring

## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Results validated against known-good baselines or reference implementations
- Documentation complete enough for another analyst to reproduce findings

## Tools & Resources
- **EasyDMARC**: DMARC monitoring dashboard with aggregate/forensic report analysis
- **DMARCLY**: SPF, DKIM, DMARC monitoring with auto-DNS updates
- **dmarcian**: DMARC deployment and management platform
- **Valimail**: Automated DMARC enforcement with hosted authentication
- **MX Toolbox**: DNS record lookup and DMARC validator
- **Google Admin Toolbox**: DMARC check and diagnostic tools

## Validation
- DMARC record published and resolving correctly at _dmarc.domain.com
- All legitimate sending sources pass SPF and/or DKIM alignment
- Aggregate reports show >99% legitimate mail passing DMARC
- Spoofed messages from unauthorized senders are rejected
- No legitimate mail blocked after full p=reject enforcement
- Subdomain policy (sp=) also set to reject

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |