---
name: ai-hacker
description: AI and LLM security testing — prompt injection, model manipulation, data exfiltration via AI. Use when testing
  AI-powered applications, finding prompt injection vulnerabilities, or assessing LLM-integrated systems.
domain: cybersecurity
tags:
- cybersecurity
- hacker
- security
- testing
- threat-defense
---
# Ai Hacker

## Overview

Cybersecurity skill for ai hacker. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "ai hacker"
- "Testing applications with AI/LLM features"
- "Finding prompt injection vulnerabilities"
- "Assessing AI-powered chatbots and assistants"


- Testing applications with AI/LLM features
- Finding prompt injection vulnerabilities
- Assessing AI-powered chatbots and assistants
- Testing AI code generation tools
- Evaluating AI content moderation bypasses
- Finding data leakage through AI models


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Access to relevant log sources and security tools
- Understanding of hacker fundamentals
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

1. **Define Objectives** — Clarify the goals and scope for hacker.
2. **Gather Resources** — Collect tools, data, and access needed for hacker.
3. **Execute Process** — Carry out hacker operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- [ ] All hacker procedures executed completely and documented
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