---
name: generating-threat-intelligence-reports
description: Generates structured cyber threat intelligence reports at strategic, operational, and tactical levels tailored
  to specific audiences including executives, security operations teams, and technical analysts. Use when producing finished
  intelligence products from raw collection data, creating sector threat briefings, or delivering post-incident intelligence
  assessments.
domain: cybersecurity
tags:
- CTI
- threat-intelligence
- intelligence-products
- TLP
- PIR
- report-writing
- NIST-CSF
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
# Generating Threat Intelligence Reports

## Overview

Cybersecurity skill for generating threat intelligence reports. Follows industry best practices and security standards.

## When to Use

Use this skill when:
- Producing weekly, monthly, or quarterly threat intelligence summaries for security leadership
- Creating a rapid intelligence assessment in response to a breaking threat (e.g., new zero-day, active ransomware campaign)
- Generating sector-specific threat briefings for executive decision-making on security investments

**Do not use** this skill for raw IOC distribution — use TIP/MISP for automated IOC sharing and reserve report generation for analyzed, finished intelligence.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Completed analysis from collection and processing phase (PIRs partially or fully answered)
- Audience profile: technical level, decision-making authority, information classification clearance
- TLP classification decision for the product
- Organization-specific reporting template aligned to audience expectations

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

1. **Define Objectives** — Clarify the goals and scope for threat intelligence reports.
2. **Gather Resources** — Collect tools, data, and access needed for threat intelligence reports.
3. **Execute Process** — Carry out threat intelligence reports operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All threat intelligence reports procedures executed completely and documented
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