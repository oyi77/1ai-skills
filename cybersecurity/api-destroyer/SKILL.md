---
name: api-destroyer
description: Aggressive API security testing for REST, GraphQL, gRPC, and WebSocket endpoints. Use when testing APIs for authorization
  flaws, injection, rate limiting bypass, or business logic abuse.
domain: cybersecurity
tags:
- api
- aws
- cybersecurity
- destroyer
- graphql
- rest-api
- security
- testing
---
# Api Destroyer

## Overview

Cybersecurity skill for api destroyer. Follows industry best practices and security standards.

## When to Use

- Testing REST/GraphQL/gRPC/WebSocket APIs
- Hunting IDOR/BOLA on API endpoints
- Bypassing API rate limiting and authentication
- Testing business logic via API manipulation
- API-first application security assessments


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Access to relevant log sources and security tools
- Understanding of destroyer fundamentals
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

1. **Define Objectives** — Clarify the goals and scope for destroyer.
2. **Gather Resources** — Collect tools, data, and access needed for destroyer.
3. **Execute Process** — Carry out destroyer operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All destroyer procedures executed completely and documented
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