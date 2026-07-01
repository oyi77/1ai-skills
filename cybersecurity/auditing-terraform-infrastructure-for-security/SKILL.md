---
name: auditing-terraform-infrastructure-for-security
description: 'Auditing Terraform infrastructure-as-code for security misconfigurations using Checkov, tfsec, Terrascan, and
  OPA/Rego policies to detect overly permissive IAM policies, public resource exposure, missing encryption, and insecure defaults
  before cloud deployment.

  '. Use when working with auditing terraform infrastructure for security.
domain: cybersecurity
tags:
- cloud-security
- terraform
- infrastructure-as-code
- checkov
- tfsec
- policy-as-code
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
# Auditing Terraform Infrastructure For Security

## Overview

Cybersecurity skill for auditing terraform infrastructure for security. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "auditing terraform infrastructure for security"
- "Auditing Terraform infrastructure-as-code for security misconfigurations using C"


- When integrating security scanning into CI/CD pipelines for Terraform deployments
- When reviewing Terraform plans and modules for security best practices before applying
- When building policy-as-code guardrails for cloud infrastructure provisioning
- When auditing existing Terraform state files to identify deployed misconfigurations
- When enforcing organizational security standards across multiple Terraform projects

**Do not use** for runtime security monitoring (use CSPM tools), for application security testing (use SAST/DAST tools), or for cloud configuration drift detection (use AWS Config or Azure Policy after deployment).


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Checkov installed (`pip install checkov`)
- tfsec installed (`brew install tfsec` or binary from GitHub)
- Terrascan installed (`brew install terrascan`)
- Terraform v1.0+ for plan generation
- OPA (Open Policy Agent) for custom policy enforcement
- Git repository with Terraform code to audit

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

1. **Define Objectives** — Clarify the goals and scope for terraform infrastructure.
2. **Gather Resources** — Collect tools, data, and access needed for terraform infrastructure.
3. **Execute Process** — Carry out terraform infrastructure operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **security** — Primary tool for this skill
- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- [ ] All terraform infrastructure procedures executed completely and documented
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