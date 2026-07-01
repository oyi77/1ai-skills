---
name: building-detection-rules-with-sigma
description: 'Builds vendor-agnostic detection rules using the Sigma rule format for threat detection across SIEM platforms
  including Splunk, Elastic, and Microsoft Sentinel. Use when creating portable detection logic from threat intelligence,
  mapping rules to MITRE ATT&CK techniques, or converting community Sigma rules into platform-specific queries using sigmac
  or pySigma backends.

  '
domain: cybersecurity
tags:
- soc
- sigma
- detection-rules
- siem
- mitre-attack
- splunk
- elastic
- sentinel
subdomain: soc-operations
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- Execution Isolation
- Process Termination
- Hardware-based Process Isolation
- Web Session Access Mediation
- Process Suspension
nist_csf:
- DE.CM-01
- DE.AE-02
- RS.MA-01
- DE.AE-06
---
# Building Detection Rules With Sigma

## Overview

Cybersecurity skill for building detection rules with sigma. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "building detection rules with sigma"
- "SOC engineers need to create detection rules portable across multiple SIEM platf"
- "Threat intelligence reports describe TTPs requiring new detection coverage"
- "Existing vendor-specific rules need standardization into a shareable format"


Use this skill when:
- SOC engineers need to create detection rules portable across multiple SIEM platforms
- Threat intelligence reports describe TTPs requiring new detection coverage
- Existing vendor-specific rules need standardization into a shareable format
- The team adopts Sigma as a detection-as-code standard in CI/CD pipelines

**Do not use** for real-time streaming detection (Sigma is for batch/scheduled searches) or when the target SIEM has native detection features that Sigma cannot express (e.g., Splunk RBA risk scoring).


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Python 3.8+ with `pySigma` and appropriate backend (`pySigma-backend-splunk`, `pySigma-backend-elasticsearch`, `pySigma-backend-microsoft365defender`)
- Sigma rule repository cloned: `git clone https://github.com/SigmaHQ/sigma.git`
- MITRE ATT&CK framework knowledge for technique mapping
- Understanding of target SIEM log source field mappings

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

1. **Assess Requirements** — Evaluate current environment and define detection rules implementation requirements.
2. **Design Architecture** — Plan the detection rules architecture, including components, integrations, and data flows.
3. **Configure Components** — Set up sigma for detection rules according to vendor best practices and security guidelines.
4. **Test Integration** — Validate that all components work together. Run functional and security tests.
5. **Deploy to Production** — Roll out the implementation with monitoring and rollback capabilities.
6. **Validate and Document** — Verify the implementation meets requirements. Document configuration and runbooks.

## Tools

- **sigma** — Primary tool for this skill
- **Configuration Management** — Infrastructure as code and automation
- **Monitoring Stack** — Observability and alerting
- **Documentation Platform** — Runbooks and architecture docs


## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- [ ] All detection rules procedures executed completely and documented
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