---
name: conducting-external-reconnaissance-with-osint
description: Conducts external reconnaissance using Open Source Intelligence (OSINT) techniques to map an organization's external
  attack surface without directly interacting with target systems. The tester gathers information from public sources including
  DNS records, certificate transparency logs, search engines, social media, code repositories, and data breach databases to
  build a comprehensive target profile. Use when working with conducting external reconnaissance with osint.
domain: cybersecurity
tags:
- OSINT
- reconnaissance
- attack-surface
- footprinting
- passive-recon
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
# Conducting External Reconnaissance With Osint

## Overview

Cybersecurity skill for conducting external reconnaissance with osint. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "conducting external reconnaissance with osint"
- "Conducts external reconnaissance using Open Source Intelligence (OSINT) techniqu"


- Performing the initial reconnaissance phase of a penetration test to gather intelligence before active scanning
- Mapping an organization's external attack surface to identify unknown or shadow IT assets
- Collecting employee information, email formats, and organizational structure for social engineering campaigns
- Identifying exposed credentials, leaked data, or sensitive documents published on the internet
- Scoping the breadth of an organization's digital footprint prior to a red team engagement

**Do not use** for stalking, harassment, or unauthorized surveillance of individuals. OSINT gathering must be conducted within the scope of an authorized engagement and comply with applicable privacy laws (GDPR, CCPA).


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Written authorization to perform reconnaissance against the target organization
- Dedicated research workstation with a VPN or Tor for anonymized queries when required
- OSINT framework tools installed: Amass, theHarvester, Shodan CLI, Recon-ng, SpiderFoot
- API keys for Shodan, Censys, SecurityTrails, Hunter.io, VirusTotal, and GitHub for enhanced results
- Disposable email accounts for accessing services that require registration during research

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

1. **Scope the Analysis** — Define what external reconnaissance artifacts or data sources to examine and the investigation timeline.
2. **Preserve Evidence** — Create forensic copies of relevant data. Maintain chain of custody documentation.
3. **Extract Key Indicators** — Use osint to parse and extract relevant external reconnaissance data points from collected artifacts.
4. **Correlate Findings** — Cross-reference extracted data with other sources (threat intel, logs, timelines).
5. **Build Timeline** — Construct a chronological sequence of events related to external reconnaissance.
6. **Document Analysis** — Write findings report with evidence, conclusions, and recommendations.

## Tools

- **osint** — Primary tool for this skill
- **Forensic Toolkit** — Evidence collection and analysis
- **Timeline Tools** — Chronological event reconstruction
- **Log Analysis Platform** — Centralized log parsing and search


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run conducting external reconnaissance with osint workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All external reconnaissance procedures executed completely and documented
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