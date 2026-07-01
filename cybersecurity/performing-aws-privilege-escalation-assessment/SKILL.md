---
name: performing-aws-privilege-escalation-assessment
description: 'Performing authorized privilege escalation assessments in AWS environments to identify IAM misconfigurations
  that allow users or roles to elevate their permissions using Pacu, CloudFox, Principal Mapper, and manual IAM policy analysis
  techniques.

  '. Use when working with performing aws privilege escalation assessment.
domain: cybersecurity
tags:
- cloud-security
- aws
- privilege-escalation
- iam
- pacu
- offensive-security
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
# Performing Aws Privilege Escalation Assessment

## Overview

Cybersecurity skill for performing aws privilege escalation assessment. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "performing aws privilege escalation assessment"
- "Performing authorized privilege escalation assessments in AWS environments to id"


- When conducting authorized penetration testing of AWS IAM configurations
- When validating that IAM policies follow the principle of least privilege
- When assessing the blast radius of a compromised AWS credential
- When building security reviews for IAM role and policy changes in CI/CD pipelines
- When evaluating cross-account trust relationships for privilege escalation risks

**Do not use** for unauthorized testing against AWS accounts, for assessing non-IAM attack vectors (SSRF, application vulnerabilities), or as a substitute for comprehensive cloud penetration testing. Always obtain written authorization before testing.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Written authorization for privilege escalation testing in the target AWS account
- Test IAM user or role with limited permissions as the starting point
- Pacu installed (`pip install pacu`)
- CloudFox installed (`go install github.com/BishopFox/cloudfox@latest`)
- PMapper (Principal Mapper) installed (`pip install principalmapper`)
- AWS CLI configured with test credentials and CloudTrail logging enabled for audit trail

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

1. **Plan Operations** — Define objectives, scope, and success criteria for aws privilege escalation assessment operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for aws privilege escalation assessment.
3. **Execute Core Workflow** — Perform the aws privilege escalation assessment operations following established procedures.
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

- [ ] All aws privilege escalation assessment procedures executed completely and documented
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