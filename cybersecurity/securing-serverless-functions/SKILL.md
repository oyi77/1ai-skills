---
name: securing-serverless-functions
description: 'This skill covers security hardening for serverless compute platforms including AWS Lambda, Azure Functions,
  and Google Cloud Functions. It addresses least privilege IAM roles, dependency vulnerability scanning, secrets management
  integration, input validation, function URL authentication, and runtime monitoring to protect against injection attacks,
  credential theft, and supply chain compromises.

  '
domain: cybersecurity
tags:
- serverless-security
- aws-lambda
- azure-functions
- function-hardening
- supply-chain
subdomain: cloud-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- ID.AM-08
- GV.SC-06
- DE.CM-01
---
# Securing Serverless Functions

## Overview

Cybersecurity skill for securing serverless functions. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "securing serverless functions"
- "This skill covers security hardening for serverless compute platforms including "


- When deploying Lambda functions or Azure Functions with access to sensitive data or cloud APIs
- When auditing existing serverless workloads for overly permissive IAM roles
- When integrating serverless functions into a DevSecOps pipeline with automated security scanning
- When hardcoded secrets or vulnerable dependencies are discovered in function code
- When establishing runtime monitoring for serverless workloads to detect injection or credential theft

**Do not use** for container-based compute security (see securing-kubernetes-on-cloud), for API Gateway configuration (see implementing-cloud-waf-rules), or for serverless architecture design decisions.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- AWS Lambda, Azure Functions, or GCP Cloud Functions with deployment access
- CI/CD pipeline with dependency scanning tools (npm audit, Snyk, Dependabot)
- AWS Secrets Manager, Azure Key Vault, or HashiCorp Vault for secrets management
- CloudWatch, Application Insights, or Cloud Logging for function monitoring

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

1. **Define Objectives** — Clarify the goals and scope for serverless functions.
2. **Gather Resources** — Collect tools, data, and access needed for serverless functions.
3. **Execute Process** — Carry out serverless functions operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run securing serverless functions workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All serverless functions procedures executed completely and documented
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