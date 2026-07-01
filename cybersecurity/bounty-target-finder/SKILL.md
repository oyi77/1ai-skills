---
name: bounty-target-finder
description: Find and prioritize high-paying bug bounty programs. Use when discovering new targets, comparing bounty payouts,
  filtering programs by scope, or building a target pipeline for continuous hunting.
domain: cybersecurity
tags:
- bounty
- cybersecurity
- finder
- pipeline
- security
- target
- threat-defense
---
# Bounty Target Finder

## Overview

Cybersecurity skill for bounty target finder. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "bounty target finder"
- "Starting a new bug bounty hunting cycle"
- "Looking for fresh targets with less competition"
- "Comparing payouts across platforms"


- Starting a new bug bounty hunting cycle
- Looking for fresh targets with less competition
- Comparing payouts across platforms
- Building a continuous hunting pipeline
- Finding programs that match your skill set


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Access to relevant log sources and security tools
- Understanding of target finder fundamentals
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

1. **Define Objectives** — Clarify the goals and scope for target finder.
2. **Gather Resources** — Collect tools, data, and access needed for target finder.
3. **Execute Process** — Carry out target finder operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run bounty target finder workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All target finder procedures executed completely and documented
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