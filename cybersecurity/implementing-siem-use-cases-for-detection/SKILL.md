---
name: implementing-siem-use-cases-for-detection
description: 'Implements SIEM detection use cases by designing correlation rules, threshold alerts, and behavioral analytics
  mapped to MITRE ATT&CK techniques across Splunk, Elastic, and Sentinel. Use when SOC teams need to expand detection coverage,
  formalize use case lifecycle management, or build a detection library aligned to organizational threat profile.

  '
domain: cybersecurity
tags:
- soc
- siem
- use-cases
- detection-engineering
- mitre-attack
- splunk
- elastic
- sentinel
subdomain: soc-operations
version: '1.0'
author: mahipal
license: Apache-2.0
nist_ai_rmf:
- MEASURE-2.7
- MAP-5.1
- MANAGE-2.4
atlas_techniques:
- AML.T0070
- AML.T0066
- AML.T0082
d3fend_techniques:
- Token Binding
- Restore Access
- Password Authentication
- Reissue Credential
- Strong Password Policy
nist_csf:
- DE.CM-01
- DE.AE-02
- RS.MA-01
- DE.AE-06
---
# Implementing Siem Use Cases For Detection

## Overview

Cybersecurity skill for implementing siem use cases for detection. Follows industry best practices and security standards.

## When to Use

Use this skill when:
- SOC teams need to build or expand their SIEM detection library from scratch
- Threat assessments identify ATT&CK technique gaps requiring new detection rules
- Detection engineers need a structured process for use case design, testing, and deployment
- Compliance requirements mandate specific detection capabilities (PCI DSS, HIPAA, SOX)

**Do not use** for ad-hoc hunting queries — use cases are formalized, tested, and maintained detection rules, not exploratory searches.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- SIEM platform (Splunk ES, Elastic Security, or Microsoft Sentinel) with production data
- ATT&CK Navigator for coverage gap analysis
- Log sources normalized to CIM/ECS field standards
- Use case documentation framework (wiki, Git repo, or detection engineering platform)
- Testing environment with attack simulation tools (Atomic Red Team, MITRE Caldera)

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

1. **Assess Requirements** — Evaluate current environment and define siem use cases implementation requirements.
2. **Design Architecture** — Plan the siem use cases architecture, including components, integrations, and data flows.
3. **Configure Components** — Set up detection for siem use cases according to vendor best practices and security guidelines.
4. **Test Integration** — Validate that all components work together. Run functional and security tests.
5. **Deploy to Production** — Roll out the implementation with monitoring and rollback capabilities.
6. **Validate and Document** — Verify the implementation meets requirements. Document configuration and runbooks.

## Tools

- **detection** — Primary tool for this skill
- **Configuration Management** — Infrastructure as code and automation
- **Monitoring Stack** — Observability and alerting
- **Documentation Platform** — Runbooks and architecture docs

## Verification

- [ ] All siem use cases procedures executed completely and documented
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