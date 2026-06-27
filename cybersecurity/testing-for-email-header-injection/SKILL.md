---
name: testing-for-email-header-injection
description: Test web application email functionality for SMTP header injection vulnerabilities that allow attackers to inject
  additional email headers, modify recipients, and abuse contact forms for spam relay.
domain: cybersecurity
tags:
- email-injection
- smtp-injection
- crlf-injection
- header-injection
- spam-relay
- contact-form
- email-security
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
# Testing For Email Header Injection

## Overview

Cybersecurity skill for testing for email header injection. Follows industry best practices and security standards.

## When to Use
- When testing contact forms, feedback forms, or "email a friend" functionality
- During assessment of password reset email functionality
- When testing newsletter subscription or notification email systems
- During penetration testing of applications that send emails based on user input
- When auditing email-related API endpoints for header injection


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites
- Burp Suite for intercepting and modifying HTTP requests
- Understanding of SMTP protocol and email header structure
- Knowledge of CRLF injection techniques (\r\n sequences)
- Test email accounts for receiving injected emails
- Access to application features that trigger email sending
- SMTP server logs access for monitoring injection attempts

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
3. **Exploit Development/Selection** — Use email header injection to identify and test  vulnerabilities.
4. **Execution** — Execute the  test in a controlled manner with proper authorization.
5. **Post-Exploitation** — Document the impact and extent of successful exploitation.
6. **Reporting** — Write detailed findings with reproduction steps, impact assessment, and remediation guidance.

## Tools

- **email header injection** — Primary tool for this skill
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