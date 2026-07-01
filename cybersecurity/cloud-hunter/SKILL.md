---
name: cloud-hunter
description: Cloud infrastructure misconfiguration hunting for AWS, GCP, and Azure. Use when testing cloud assets, finding
  exposed S3 buckets, hunting IAM misconfigs, or testing serverless applications.
domain: cybersecurity
tags:
- aws
- azure
- cloud
- cybersecurity
- gcp
- hunter
- security
- testing
---
# Cloud Hunter

## Overview

Cybersecurity skill for cloud hunter. Follows industry best practices and security standards.

## When to Use

- Testing cloud-hosted applications
- Hunting exposed S3/GCS/Azure Blob storage
- Auditing IAM policies and roles
- Testing serverless functions (Lambda/Cloud Functions)
- Finding cloud metadata endpoint access
- Assessing container security (EKS/GKE/AKS)


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Access to relevant log sources and security tools
- Understanding of hunter fundamentals
- Appropriate permissions for data access and tool operation

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

1. **Define Objectives** — Clarify the goals and scope for hunter.
2. **Gather Resources** — Collect tools, data, and access needed for hunter.
3. **Execute Process** — Carry out hunter operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- [ ] All hunter procedures executed completely and documented
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