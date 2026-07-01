---
name: social-engineer
description: Social engineering and phishing for authorized security assessments. Use when testing human attack vectors, conducting
  phishing simulations, or assessing organizational security awareness.
domain: cybersecurity
tags:
- cybersecurity
- engineer
- security
- social
- social-media
- testing
- threat-defense
---
# Social Engineer

## Overview

Cybersecurity skill for social engineer. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "social engineer"
- "Authorized phishing simulations"
- "Social engineering assessments"
- "Security awareness training"


- Authorized phishing simulations
- Social engineering assessments
- Security awareness training
- Physical security testing
- Pretexting for authorized penetration tests

**WARNING**: Social engineering without authorization is illegal. Always have written authorization before testing.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Access to relevant log sources and security tools
- Understanding of engineer fundamentals
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

1. **Define Objectives** — Clarify the goals and scope for engineer.
2. **Gather Resources** — Collect tools, data, and access needed for engineer.
3. **Execute Process** — Carry out engineer operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Research** — Analyze target audience, competitors, and trending topics
1. **Create** — Generate content following brand guidelines and best practices
1. **Publish & Optimize** — Distribute to target platforms, track performance, iterate

## Verification

- [ ] All engineer procedures executed completely and documented
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