---
name: performing-cloud-penetration-testing-with-pacu
description: 'Performing authorized AWS penetration testing using Pacu, the open-source AWS exploitation framework, to enumerate
  IAM configurations, discover privilege escalation paths, test credential harvesting, and validate security controls through
  systematic attack simulation.

  '. Use when working with performing cloud penetration testing with pacu.
domain: cybersecurity
tags:
- cloud-security
- aws
- pacu
- penetration-testing
- offensive-security
- iam-exploitation
subdomain: cloud-security
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- ID.AM-08
- GV.SC-06
- DE.CM-01
---
# Performing Cloud Penetration Testing With Pacu

## Overview

Cybersecurity skill for performing cloud penetration testing with pacu. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "performing cloud penetration testing with pacu"
- "Performing authorized AWS penetration testing using Pacu, the open-source AWS ex"


- When conducting authorized penetration testing of AWS environments
- When validating the effectiveness of IAM policies, SCPs, and permission boundaries
- When assessing the blast radius of a compromised set of AWS credentials
- When testing detection capabilities of GuardDuty, Security Hub, and custom alerting
- When building red team exercises against AWS cloud infrastructure

**Do not use** for unauthorized testing of any AWS account, for testing AWS infrastructure itself (covered by shared responsibility), for DDoS or volumetric attacks without AWS approval, or for production account testing without explicit authorization and breakglass procedures.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Written authorization from the AWS account owner with defined scope and rules of engagement
- Pacu v1.5+ installed (`pip install pacu`)
- Test AWS credentials with limited starting permissions (simulates compromised credential scenario)
- CloudTrail logging enabled to capture all Pacu activity for post-engagement review
- GuardDuty enabled to validate detection of Pacu activities
- Emergency contact and rollback procedures documented

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

1. **Plan Operations** — Define objectives, scope, and success criteria for cloud penetration testing operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for cloud penetration testing.
3. **Execute Core Workflow** — Use pacu to perform cloud penetration testing operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **pacu** — Primary tool for this skill
- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Design** — Define interface, identify patterns, plan implementation
1. **Implement** — Write code following existing conventions, add tests
1. **Verify** — Run tests, check integration, validate behavior

## Verification

- [ ] All cloud penetration testing procedures executed completely and documented
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