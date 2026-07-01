---
name: monitoring-darkweb-sources
description: Monitors dark web forums, marketplaces, paste sites, and ransomware leak sites for mentions of organizational
  assets, leaked credentials, threatened attacks, and threat actor communications to provide early warning intelligence. Use
  when establishing dark web monitoring coverage, investigating specific data breach claims, or enriching incident investigations
  with dark web context.
domain: cybersecurity
tags:
- dark-web
- OSINT
- credential-monitoring
- ransomware-leaks
- Recorded-Future
- SpiderFoot
- CTI
subdomain: threat-intelligence
version: 1.0.0
author: team-cybersecurity
license: Apache-2.0
nist_ai_rmf:
- MEASURE-2.7
- MAP-5.1
- MANAGE-2.4
atlas_techniques:
- AML.T0070
- AML.T0066
- AML.T0082
nist_csf:
- ID.RA-01
- ID.RA-05
- DE.CM-01
- DE.AE-02
---
# Monitoring Darkweb Sources

## Overview

Cybersecurity skill for monitoring darkweb sources. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "monitoring darkweb sources"
- "Monitors dark web forums, marketplaces, paste sites, and ransomware leak sites f"


Use this skill when:
- Establishing continuous monitoring for organizational domain names, executive names, and product brands on dark web forums
- Investigating a reported data breach claim found on a ransomware leak site or paste site
- Enriching an incident investigation with context about stolen credentials or planned attacks

**Do not use** this skill without proper operational security measures — dark web browsing without isolation exposes analyst infrastructure to adversary counter-intelligence.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Commercial dark web monitoring service (Recorded Future, Flashpoint, Intel 471, or Cybersixgill)
- Isolated operational environment: Whonix OS or Tails OS running in a VM with no persistent storage
- Keyword watchlist: organization domain, key executive names, product names, IP ranges, known credentials
- Legal guidance confirming passive monitoring is authorized in your jurisdiction

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

1. **Define Objectives** — Clarify the goals and scope for darkweb sources.
2. **Gather Resources** — Collect tools, data, and access needed for darkweb sources.
3. **Execute Process** — Carry out darkweb sources operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All darkweb sources procedures executed completely and documented
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