---
name: continuous-hunter
description: Automated continuous bug hunting pipeline that runs 24/7 across multiple targets. Use when setting up persistent
  hunting, automating the find-report cycle, or scaling bug bounty income through automation.
domain: cybersecurity
tags:
- continuous
- cybersecurity
- hunter
- pipeline
- security
- threat-defense
---
# Continuous Hunter

## Overview

Cybersecurity skill for continuous hunter. Follows industry best practices and security standards.

## When to Use

- Scaling from manual hunting to automated pipeline
- Running overnight/weekend scans across target portfolio
- Monitoring targets for new vulnerabilities
- Building passive income from bug bounties
- Maximizing findings per hour of effort


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Access to relevant log sources and security tools
- Understanding of hunter fundamentals
- Appropriate permissions for data access and tool operation

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

1. **Define Objectives** — Clarify the goals and scope for hunter.
2. **Gather Resources** — Collect tools, data, and access needed for hunter.
3. **Execute Process** — Carry out hunter operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All hunter procedures executed completely and documented
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