---
name: collecting-open-source-intelligence
description: Collects and synthesizes open-source intelligence (OSINT) about threat actors, malicious infrastructure, and
  attack campaigns using publicly available data sources, passive reconnaissance tools, and dark web monitoring. Use when
  investigating external threat actor infrastructure, performing pre-engagement reconnaissance for authorized red team assessments,
  or enriching CTI reports with publicly available adversary context.
domain: cybersecurity
tags:
- OSINT
- Maltego
- Shodan
- Recon-ng
- SpiderFoot
- threat-intelligence
- ATT&CK-T1591
- NIST-CSF
subdomain: threat-intelligence
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- ID.RA-01
- ID.RA-05
- DE.CM-01
- DE.AE-02
---
# Collecting Open Source Intelligence

## Overview

Cybersecurity skill for collecting open source intelligence. Follows industry best practices and security standards.

## When to Use

Use this skill when:
- Investigating external infrastructure associated with a phishing campaign targeting your organization
- Enriching threat actor profiles with publicly observable indicators (WHOIS, ASN data, SSL certificates)
- Conducting authorized attack surface discovery to understand your organization's external exposure

**Do not use** this skill for active scanning against targets without explicit written authorization — OSINT collection must remain passive (no packets sent to target systems) unless scope permits active recon.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Maltego CE or commercial license for graph-based link analysis
- Shodan API key (https://shodan.io) for internet-wide device/service discovery
- OSINT Framework familiarity (https://osintframework.com) for tool selection
- SpiderFoot HX or open-source SpiderFoot for automated OSINT correlation

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

1. **Define Objectives** — Clarify the goals and scope for open source intelligence.
2. **Gather Resources** — Collect tools, data, and access needed for open source intelligence.
3. **Execute Process** — Carry out open source intelligence operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Scope** — Define research questions, identify data sources, set time boundaries
1. **Gather** — Collect data from primary sources, APIs, and public records
1. **Synthesize** — Analyze findings, identify patterns, produce actionable report

## Verification

- [ ] All open source intelligence procedures executed completely and documented
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