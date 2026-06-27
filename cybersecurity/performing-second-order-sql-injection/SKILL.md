---
name: performing-second-order-sql-injection
description: Detect and exploit second-order SQL injection vulnerabilities where malicious input is stored in a database and
  later executed in an unsafe SQL query during a different application operation.
domain: cybersecurity
tags:
- second-order-sqli
- stored-sql-injection
- sql-injection
- database-security
- web-security
- blind-injection
- persistent-sqli
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
# Performing Second Order Sql Injection

## Overview

Cybersecurity skill for performing second order sql injection. Follows industry best practices and security standards.

## When to Use
- When first-order SQL injection testing reveals proper input sanitization at storage time
- During penetration testing of applications with user-generated content stored in databases
- When testing multi-step workflows where stored data feeds subsequent database queries
- During assessment of admin panels that display or process user-submitted data
- When evaluating stored procedure execution paths that use previously stored data


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites
- Burp Suite Professional for request tracking across application flows
- SQLMap with second-order injection support (--second-url flag)
- Understanding of SQL injection fundamentals and blind extraction techniques
- Two or more application functions (one for storing data, another for triggering execution)
- Database error message monitoring or blind technique knowledge
- Multiple user accounts for testing stored data across different contexts

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

1. **Plan Operations** — Define objectives, scope, and success criteria for second order sql injection operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for second order sql injection.
3. **Execute Core Workflow** — Perform the second order sql injection operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All second order sql injection procedures executed completely and documented
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