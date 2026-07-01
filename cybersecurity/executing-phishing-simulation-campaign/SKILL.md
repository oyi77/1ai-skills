---
name: executing-phishing-simulation-campaign
description: Executes authorized phishing simulation campaigns to assess an organization's susceptibility to email-based social
  engineering attacks. The tester designs realistic phishing scenarios, builds credential harvesting infrastructure, sends
  targeted phishing emails, and tracks open rates, click-through rates, and credential submission rates to measure human security
  awareness. Use when working with executing phishing simulation campaign.
domain: cybersecurity
tags:
- phishing-simulation
- social-engineering
- GoPhish
- email-security
- security-awareness
subdomain: penetration-testing
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- ID.RA-01
- ID.RA-06
- GV.OV-02
- DE.AE-07
---
# Executing Phishing Simulation Campaign

## Overview

Cybersecurity skill for executing phishing simulation campaign. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "executing phishing simulation campaign"
- "Executes authorized phishing simulation campaigns to assess an organization's su"


- Measuring employee susceptibility to phishing attacks as part of a security awareness program
- Testing the effectiveness of email security controls (secure email gateway, DMARC, SPF, DKIM)
- Conducting the social engineering component of a red team exercise to gain initial access
- Establishing a baseline for phishing susceptibility before deploying security awareness training
- Validating that incident response procedures work when employees report suspicious emails

**Do not use** without explicit written authorization from the organization's leadership, for actual credential theft beyond the authorized scope, for targeting individuals personally rather than professionally, or for sending phishing emails that could cause psychological harm or legal liability.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Written authorization from executive leadership specifying the campaign scope, target groups, and escalation procedures
- Coordination with the IT/security team to whitelist the sending infrastructure (or test whether it bypasses controls, depending on scope)
- GoPhish or equivalent phishing platform configured with a sending domain, SMTP relay, and landing page infrastructure
- Phishing domain registered and configured with SPF, DKIM, and DMARC records to maximize deliverability
- Employee email list from HR, organized by department for targeted campaigns
- Incident response team briefed on the campaign timeline and escalation procedures

## Workflow

```python
# Example: IOC detection
import re

IOC_PATTERNS = {
    "ip": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "domain": r"\b[a-z0-9-]+\.[a-z]{2,}\b",
    "hash_md5": r"\b[a-f0-9]{32}\b",
    "hash_sha256": r"\b[a-f0-9]{64}\b",
}

def extract_iocs(text: str) -> dict:
    return {k: re.findall(v, text) for k, v in IOC_PATTERNS.items()}
```

1. **Define Objectives** — Clarify the goals and scope for phishing simulation campaign.
2. **Gather Resources** — Collect tools, data, and access needed for phishing simulation campaign.
3. **Execute Process** — Carry out phishing simulation campaign operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- [ ] All phishing simulation campaign procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |