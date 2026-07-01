---
name: implementing-gdpr-data-subject-access-request
description: 'Automates GDPR Data Subject Access Request (DSAR) workflows including identity verification, PII discovery across
  databases and files using regex and NER, data mapping, response templating per Article 15 requirements, deadline tracking,
  and audit logging. Covers ICO/EDPB guidance compliance, exemption handling, and scalable batch processing. Use when building
  or auditing DSAR response capabilities under GDPR/UK GDPR.

  '
domain: cybersecurity
tags:
- gdpr
- dsar
- privacy
- pii-discovery
- data-subject-rights
- compliance
- article-15
subdomain: privacy-compliance
version: '1.0'
author: mukul975
license: Apache-2.0
nist_csf:
- GV.PO-01
- PR.DS-01
- GV.OC-05
---
# Implementing Gdpr Data Subject Access Request

## Overview

Cybersecurity skill for implementing gdpr data subject access request. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "implementing gdpr data subject access request"
- "When building automated DSAR processing pipelines for GDPR/UK GDPR compliance"
- "When implementing PII discovery across structured and unstructured data sources"
- "When creating response templates that satisfy Article 15 disclosure requirements"


- When building automated DSAR processing pipelines for GDPR/UK GDPR compliance
- When implementing PII discovery across structured and unstructured data sources
- When creating response templates that satisfy Article 15 disclosure requirements
- When auditing existing DSAR handling for regulatory compliance gaps
- When scaling DSAR processing from manual to automated workflows


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Python 3.8+ with required dependencies (spacy, presidio-analyzer, jinja2)
- Access to data sources where personal data resides (databases, file shares, logs)
- Understanding of GDPR Article 15 requirements and ICO/EDPB guidance
- Appropriate authorization and data protection officer (DPO) approval
- Test environment with synthetic or anonymized data for validation

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

1. **Assess Requirements** — Evaluate current environment and define gdpr data subject access request implementation requirements.
2. **Design Architecture** — Plan the gdpr data subject access request architecture, including components, integrations, and data flows.
3. **Configure Components** — Set up and configure each gdpr data subject access request component according to best practices.
4. **Test Integration** — Validate that all components work together. Run functional and security tests.
5. **Deploy to Production** — Roll out the implementation with monitoring and rollback capabilities.
6. **Validate and Document** — Verify the implementation meets requirements. Document configuration and runbooks.

## Tools

- **Configuration Management** — Infrastructure as code and automation
- **Monitoring Stack** — Observability and alerting
- **Documentation Platform** — Runbooks and architecture docs


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run implementing gdpr data subject access request workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All gdpr data subject access request procedures executed completely and documented
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