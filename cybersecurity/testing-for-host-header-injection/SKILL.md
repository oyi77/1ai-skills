---
name: testing-for-host-header-injection
description: Test web applications for HTTP Host header injection vulnerabilities to identify password reset poisoning, web
  cache poisoning, SSRF, and virtual host routing manipulation risks.
domain: cybersecurity
tags:
- host-header-injection
- password-reset-poisoning
- cache-poisoning
- virtual-host
- web-security
- header-manipulation
- ssrf
subdomain: web-application-security
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- ID.RA-01
- PR.DS-10
- DE.CM-01
---
# Testing For Host Header Injection

## Overview

Cybersecurity skill for testing for host header injection. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "testing for host header injection"
- "Test web applications for HTTP Host header injection vulnerabilities to identify"

- When testing password reset functionality for token theft via host manipulation
- During assessment of web caching behavior influenced by Host header values
- When testing virtual host routing and server-side request processing
- During penetration testing of applications behind reverse proxies or load balancers
- When evaluating SSRF potential through Host header manipulation


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites
- Burp Suite for intercepting and modifying Host headers
- Understanding of HTTP Host header role in virtual hosting and routing
- Knowledge of alternative host headers (X-Forwarded-Host, X-Host, X-Original-URL)
- Access to an attacker-controlled domain for receiving poisoned requests
- Burp Collaborator or interact.sh for out-of-band detection
- Multiple test accounts for password reset testing


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

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

1. **Reconnaissance** — Gather information about the target related to . Identify attack surface.
2. **Vulnerability Identification** — Enumerate potential  weaknesses using automated and manual techniques.
3. **Exploit Development/Selection** — Use host header injection to identify and test  vulnerabilities.
4. **Execution** — Execute the  test in a controlled manner with proper authorization.
5. **Post-Exploitation** — Document the impact and extent of successful exploitation.
6. **Reporting** — Write detailed findings with reproduction steps, impact assessment, and remediation guidance.

## Tools

- **host header injection** — Primary tool for this skill
- **Vulnerability Scanner** — Automated weakness identification
- **Exploitation Framework** — Controlled exploitation testing
- **Reporting Tool** — Findings documentation and tracking

## Verification

- [ ] All  procedures executed completely and documented
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