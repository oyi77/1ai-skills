---
name: crypto-breaker
description: Cryptographic attack techniques for breaking implementations, side-channel attacks, and exploiting crypto weaknesses.
  Use when assessing crypto implementations, finding side-channel leaks, or breaking custom cryptography.
domain: cybersecurity
tags:
- breaker
- crypto
- cybersecurity
- security
- threat-defense
---
# Crypto Breaker

## Overview

Cybersecurity skill for crypto breaker. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "crypto breaker"
- "Assessing cryptographic implementations"
- "Finding side-channel vulnerabilities"
- "Breaking custom/homegrown cryptography"


- Assessing cryptographic implementations
- Finding side-channel vulnerabilities
- Breaking custom/homegrown cryptography
- Analyzing TLS/SSL configurations
- Testing encryption in transit and at rest
- JWT/token security assessment


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Access to relevant log sources and security tools
- Understanding of breaker fundamentals
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

1. **Define Objectives** — Clarify the goals and scope for breaker.
2. **Gather Resources** — Collect tools, data, and access needed for breaker.
3. **Execute Process** — Carry out breaker operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run crypto breaker workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All breaker procedures executed completely and documented
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