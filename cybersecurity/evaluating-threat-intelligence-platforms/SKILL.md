---
name: evaluating-threat-intelligence-platforms
description: 'Evaluates and selects Threat Intelligence Platform (TIP) products based on organizational requirements including
  feed integration capability, STIX/TAXII support, workflow automation, analyst interface, and total cost of ownership. Use
  when conducting a TIP procurement, migrating between TIP solutions, or assessing whether the current TIP meets program maturity
  requirements. Activates for requests involving ThreatConnect, MISP, OpenCTI, Anomali, EclecticIQ, or TIP procurement decisions.

  '
domain: cybersecurity
tags:
- TIP
- ThreatConnect
- MISP
- OpenCTI
- Anomali
- EclecticIQ
- STIX-TAXII
- CTI-program
- procurement
subdomain: threat-intelligence
version: 1.0.0
author: team-cybersecurity
license: Apache-2.0
nist_csf:
- ID.RA-01
- ID.RA-05
- DE.CM-01
- DE.AE-02
---
# Evaluating Threat Intelligence Platforms

## Overview

Cybersecurity skill for evaluating threat intelligence platforms. Follows industry best practices and security standards.

## When to Use

Use this skill when:
- Conducting a formal RFP or vendor evaluation for a TIP solution
- Assessing whether the current TIP (e.g., MISP) needs to be replaced or augmented as the CTI program scales
- Establishing evaluation criteria aligned to organizational maturity and budget

**Do not use** this skill for evaluating feed quality independently of the TIP — feed evaluation is a separate workflow focused on data quality rather than platform capabilities.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Documented CTI program requirements: team size, feed sources, integration targets, use cases
- Budget range and procurement timeline
- Technical staff who will administer the platform (Python/API experience for open-source TIPs)
- List of current and planned integrations (SIEM, SOAR, EDR, firewalls)

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

1. **Define Objectives** — Clarify the goals and scope for threat intelligence platforms.
2. **Gather Resources** — Collect tools, data, and access needed for threat intelligence platforms.
3. **Execute Process** — Carry out threat intelligence platforms operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All threat intelligence platforms procedures executed completely and documented
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