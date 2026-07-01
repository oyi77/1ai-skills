---
name: testing-for-broken-access-control
description: Systematically testing web applications for broken access control vulnerabilities including privilege escalation,
  missing function-level checks, and insecure direct object references. Use when working with testing for broken access control.
domain: cybersecurity
tags:
- penetration-testing
- access-control
- authorization
- owasp
- privilege-escalation
- web-security
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
# Testing For Broken Access Control

## Overview

Cybersecurity skill for testing for broken access control. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "testing for broken access control"
- "Systematically testing web applications for broken access control vulnerabilitie"


- During authorized penetration tests as the primary assessment for OWASP A01:2021 - Broken Access Control
- When evaluating role-based access control (RBAC) implementations across all application endpoints
- For testing multi-tenant applications where users in one organization should not access another's data
- When assessing API endpoints for missing or inconsistent authorization checks
- During security audits where privilege escalation and unauthorized access are primary concerns


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- **Authorization**: Written penetration testing agreement for the target
- **Burp Suite Professional**: With Authorize extension for automated access control testing
- **Multiple test accounts**: Accounts at each role level (admin, manager, user, guest)
- **Application role matrix**: Documentation of what each role should and should not access
- **curl/httpie**: For manual endpoint testing with different authentication contexts
- **ffuf**: For discovering hidden endpoints that may lack access controls

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
3. **Exploit Development/Selection** — Use broken access control to identify and test  vulnerabilities.
4. **Execution** — Execute the  test in a controlled manner with proper authorization.
5. **Post-Exploitation** — Document the impact and extent of successful exploitation.
6. **Reporting** — Write detailed findings with reproduction steps, impact assessment, and remediation guidance.

## Tools

- **broken access control** — Primary tool for this skill
- **Vulnerability Scanner** — Automated weakness identification
- **Exploitation Framework** — Controlled exploitation testing
- **Reporting Tool** — Findings documentation and tracking


## Process

1. **Design** — Define interface, identify patterns, plan implementation
1. **Implement** — Write code following existing conventions, add tests
1. **Verify** — Run tests, check integration, validate behavior

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