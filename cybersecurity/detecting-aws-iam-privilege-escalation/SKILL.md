---
name: detecting-aws-iam-privilege-escalation
description: Detect AWS IAM privilege escalation paths using boto3 and Cloudsplaining policy analysis to identify overly permissive
  policies, dangerous permission combinations, and least-privilege violations
domain: cybersecurity
subdomain: cloud-security
tags:
- aws
- iam
- privilege-escalation
- cloudsplaining
- boto3
- policy-analysis
- least-privilege
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- ID.AM-08
- GV.SC-06
- DE.CM-01
---

# Detecting AWS IAM Privilege Escalation

## Overview

This skill uses boto3 and Cloudsplaining-style analysis to identify IAM privilege escalation paths in AWS accounts. It downloads the account authorization details, analyzes each policy for dangerous permission combinations (iam:PassRole + lambda:CreateFunction, iam:CreatePolicyVersion, sts:AssumeRole), and flags policies that violate least-privilege principles.


## When to Use

- When investigating security incidents that require detecting aws iam privilege escalation
- When building detection rules or threat hunting queries for this domain
- When SOC analysts need structured procedures for this analysis type
- When validating security monitoring coverage for related attack techniques

## Prerequisites

- Python 3.8+ with boto3 library
- AWS credentials with IAM read-only access (iam:GetAccountAuthorizationDetails)
- Optional: cloudsplaining Python package for HTML report generation

## Steps

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

1. **Download IAM Authorization Details** — Call iam:GetAccountAuthorizationDetails to retrieve all users, groups, roles, and policies
2. **Analyze Policies for Privilege Escalation** — Check each policy for known escalation permission combinations
3. **Identify Wildcard Resource Policies** — Flag policies using Resource: "*" with dangerous actions
4. **Map Principal-to-Policy Relationships** — Build a graph of which principals can access which escalation paths
5. **Score and Prioritize Findings** — Rank findings by severity based on escalation vector type
6. **Generate Report** — Produce structured JSON report with remediation guidance

## Expected Output

- JSON report of privilege escalation findings with severity scores
- List of dangerous permission combinations per principal
- Wildcard resource policy audit results
- Remediation recommendations for each finding
## When NOT to Use

- You need to perform the attack to test detection (use performing-* skills)
- Task is about analyzing past incidents (use analyzing-* skills)
- You need to implement detection rules (use implementing-* skills)
- Task is about threat hunting proactively (use hunting-* skills)
- You don't have access to logs or monitoring data
- Task requires incident response (use IR skills)


## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Modifying cloud IAM policies or security groups without approval
- Exposing cloud credentials or secrets in logs or reports
- Running scans that generate excessive API calls and trigger billing alerts
## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Cloud resource changes reverted or documented as intentional
- IAM policies reviewed for least-privilege compliance after testing
- No residual test resources left running (cost and security check)

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |