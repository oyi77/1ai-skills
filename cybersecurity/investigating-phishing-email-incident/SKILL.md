---
name: investigating-phishing-email-incident
description: 'Investigates phishing email incidents from initial user report through header analysis, URL/attachment detonation,
  impacted user identification, and containment actions using SOC tools like Splunk, Microsoft Defender, and sandbox analysis
  platforms. Use when a reported phishing email requires full incident investigation to determine scope and impact.

  '
domain: cybersecurity
tags:
- soc
- phishing
- incident-response
- email-security
- splunk
- defender
- sandbox
subdomain: soc-operations
mitre_attack:
- T1566.001
- T1566.002
- T1204.001
- T1598.003
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- DE.CM-01
- DE.AE-02
- RS.MA-01
- DE.AE-06
---
# Investigating Phishing Email Incident

## Overview

Cybersecurity skill for investigating phishing email incident. Follows industry best practices and security standards.

## When to Use

Use this skill when:
- A user reports a suspicious email via the phishing report button or helpdesk ticket
- Email security gateway flags a message that bypassed initial filters
- Automated detection identifies credential harvesting URLs or malicious attachments
- A phishing campaign targeting the organization requires scope assessment

**Do not use** for spam or marketing emails without malicious intent — route those to email administration for filter tuning.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Access to email gateway logs (Proofpoint, Mimecast, or Microsoft Defender for Office 365)
- Splunk or SIEM with email log ingestion (O365 Message Trace, Exchange tracking logs)
- Sandbox access (Any.Run, Joe Sandbox, or Hybrid Analysis) for URL/attachment detonation
- Microsoft Graph API or Exchange Admin Center for email search and purge operations
- URLScan.io and VirusTotal API keys

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

1. **Define Objectives** — Clarify the goals and scope for phishing email incident.
2. **Gather Resources** — Collect tools, data, and access needed for phishing email incident.
3. **Execute Process** — Carry out phishing email incident operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All phishing email incident procedures executed completely and documented
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