---
name: performing-entitlement-review-with-sailpoint-iiq
description: 'Performs entitlement review and access certification campaigns using SailPoint IdentityIQ including manager
  certifications, targeted entitlement reviews, role-based access validation, SOD violation remediation, and automated revocation
  workflows. Activates for requests involving access reviews, entitlement certifications, SailPoint IIQ governance, or periodic
  user access recertification.

  '
domain: cybersecurity
tags:
- SailPoint
- IdentityIQ
- access-review
- entitlement-certification
- IGA
- access-governance
subdomain: identity-access-management
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.AA-01
- PR.AA-02
- PR.AA-05
- PR.AA-06
---
# Performing Entitlement Review With Sailpoint Iiq

## Overview

Cybersecurity skill for performing entitlement review with sailpoint iiq. Follows industry best practices and security standards.

## When to Use

- Quarterly or annual access certification campaigns are required for compliance (SOX, HIPAA, PCI-DSS)
- Organization needs automated manager-based access reviews for all direct reports
- Targeted entitlement reviews are needed for sensitive applications or high-privilege roles
- Separation of Duties (SOD) violations must be identified and remediated
- Orphaned accounts and excessive entitlements need to be discovered and cleaned up
- Audit findings require evidence of periodic access review and remediation tracking

**Do not use** for real-time access control decisions; IdentityIQ certifications are periodic review processes designed for governance and compliance validation.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- SailPoint IdentityIQ 8.2+ deployed with database backend (Oracle, MySQL, or SQL Server)
- Application connectors configured for all in-scope systems (Active Directory, LDAP, databases, SaaS applications)
- Identity cubes aggregated with current entitlement data from all connected sources
- Email server configured for certification notifications
- Manager hierarchy defined in the identity model
- Business roles and entitlement glossary populated for reviewer context

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

1. **Plan Operations** — Define objectives, scope, and success criteria for entitlement review operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for entitlement review.
3. **Execute Core Workflow** — Use sailpoint iiq to perform entitlement review operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **sailpoint iiq** — Primary tool for this skill
- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All entitlement review procedures executed completely and documented
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