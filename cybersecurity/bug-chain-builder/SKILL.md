---
name: bug-chain-builder
description: Chain multiple low-severity bugs into critical impact for maximum bounty payouts. Use when combining vulnerabilities,
  escalating impact, or when a single bug isn't enough for a high-severity report.
domain: cybersecurity
tags:
- bug
- builder
- chain
- cybersecurity
- security
- threat-defense
---
# Bug Chain Builder

## Overview

Cybersecurity skill for bug chain builder. Follows industry best practices and security standards.

## When to Use

- Found a low-severity bug that feels "not impactful enough"
- Need to escalate impact for a higher bounty
- Multiple findings on the same target that could combine
- Report marked as "informative" — chain it to critical
- Want to maximize payout from a single target


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Access to relevant log sources and security tools
- Understanding of chain builder fundamentals
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

1. **Define Objectives** — Clarify the goals and scope for chain builder.
2. **Gather Resources** — Collect tools, data, and access needed for chain builder.
3. **Execute Process** — Carry out chain builder operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Design** — Define interface, identify patterns, plan implementation
1. **Implement** — Write code following existing conventions, add tests
1. **Verify** — Run tests, check integration, validate behavior

## Verification

- [ ] All chain builder procedures executed completely and documented
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