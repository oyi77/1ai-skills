---
name: performing-security-headers-audit
description: Auditing HTTP security headers including CSP, HSTS, X-Frame-Options, and cookie attributes to identify missing
  or misconfigured browser-level protections.
domain: cybersecurity
tags:
- penetration-testing
- security-headers
- csp
- hsts
- owasp
- web-security
- hardening
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
# Performing Security Headers Audit

## Overview

Cybersecurity skill for performing security headers audit. Follows industry best practices and security standards.

## When to Use

- During authorized web application security assessments as a standard configuration review
- When evaluating browser-level protections against XSS, clickjacking, and data leakage
- For compliance assessments requiring security header implementation (PCI DSS, SOC 2)
- When performing initial reconnaissance to identify easy-win security improvements
- During CI/CD pipeline security gate checks for new deployments


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- **Authorization**: Written scope for the target application (header review is low-risk)
- **curl**: For fetching response headers from target endpoints
- **SecurityHeaders.com**: Online scanner for quick header assessment
- **Mozilla Observatory**: Mozilla's web security testing tool
- **Burp Suite**: For comprehensive header analysis across multiple pages
- **Browser DevTools**: For examining headers and CSP violations in real-time

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

1. **Plan Operations** — Define objectives, scope, and success criteria for security headers audit operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for security headers audit.
3. **Execute Core Workflow** — Perform the security headers audit operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All security headers audit procedures executed completely and documented
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