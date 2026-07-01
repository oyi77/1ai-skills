---
name: performing-web-application-penetration-test
description: Performs systematic security testing of web applications following the OWASP Web Security Testing Guide (WSTG)
  methodology to identify vulnerabilities in authentication, authorization, input validation, session management, and business
  logic. The tester uses Burp Suite as the primary interception proxy alongside manual testing techniques to find flaws that
  automated scanners miss.
domain: cybersecurity
tags:
- web-application-pentest
- OWASP
- Burp-Suite
- WSTG
- application-security
subdomain: penetration-testing
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- ID.RA-01
- ID.RA-06
- GV.OV-02
- DE.AE-07
---
# Performing Web Application Penetration Test

## Overview

Cybersecurity skill for performing web application penetration test. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "performing web application penetration test"
- "Performs systematic security testing of web applications following the OWASP Web"


- Testing web applications before production deployment to identify exploitable vulnerabilities
- Conducting compliance-driven security assessments (PCI-DSS requirement 6.6, SOC 2 Type II)
- Validating remediation of previously identified web application vulnerabilities during retesting
- Assessing third-party web applications before integration into the organization's environment
- Evaluating custom-developed web applications where automated scanning alone is insufficient

**Do not use** against web applications without written authorization, against production systems during peak traffic hours without explicit approval, or for denial-of-service testing of web infrastructure.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Signed statement of work (SoW) defining the target application URLs, environments (staging/production), and testing boundaries
- Burp Suite Professional license with up-to-date extensions (Active Scan++, Autorize, JSON Beautifier, Logger++)
- Valid test accounts at each privilege level (unauthenticated, standard user, administrator) for authorization testing
- Application documentation including API specifications (OpenAPI/Swagger), sitemap, and technology stack details
- Browser configured with Burp Suite proxy (FoxyProxy recommended) and Burp CA certificate installed

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

1. **Plan Operations** — Define objectives, scope, and success criteria for web application penetration test operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for web application penetration test.
3. **Execute Core Workflow** — Perform the web application penetration test operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Design** — Define interface, identify patterns, plan implementation
1. **Implement** — Write code following existing conventions, add tests
1. **Verify** — Run tests, check integration, validate behavior

## Verification

- [ ] All web application penetration test procedures executed completely and documented
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