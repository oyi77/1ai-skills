---
name: performing-serverless-function-security-review
description: 'Performing security reviews of serverless functions across AWS Lambda, Azure Functions, and GCP Cloud Functions
  to identify overly permissive execution roles, insecure environment variables, injection vulnerabilities, and missing runtime
  protections.

  '
domain: cybersecurity
tags:
- cloud-security
- serverless
- lambda
- azure-functions
- cloud-functions
- security-review
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
# Performing Serverless Function Security Review

## Overview

Cybersecurity skill for performing serverless function security review. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "performing serverless function security review"
- "Performing security reviews of serverless functions across AWS Lambda, Azure Fun"


- When auditing serverless applications before production deployment
- When investigating potential data exposure through function environment variables or logs
- When assessing the blast radius of a compromised serverless function execution role
- When compliance reviews require documentation of serverless security controls
- When building secure-by-default templates for serverless deployments

**Do not use** for container or VM security assessments (use container scanning tools), for API security testing (use DAST tools on the API Gateway layer), or for real-time serverless threat detection (use AWS Lambda Extensions with security agents).


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- AWS CLI, Azure CLI, and gcloud CLI configured with appropriate permissions
- Access to read function configurations, policies, and execution roles
- Prowler or Checkov for automated serverless security scanning
- SAM CLI or Serverless Framework for local function analysis
- CloudTrail, Azure Monitor, or Cloud Audit Logs enabled for function invocation monitoring

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

1. **Plan Operations** — Define objectives, scope, and success criteria for serverless function security review operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for serverless function security review.
3. **Execute Core Workflow** — Perform the serverless function security review operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All serverless function security review procedures executed completely and documented
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