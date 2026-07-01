---
name: performing-user-behavior-analytics
description: 'Performs User and Entity Behavior Analytics (UEBA) to detect anomalous user activities including impossible
  travel, unusual access patterns, privilege abuse, and insider threats using SIEM-based behavioral baselines and statistical
  analysis. Use when SOC teams need to identify compromised accounts or insider threats through deviation from established
  behavioral norms.

  '
domain: cybersecurity
tags:
- soc
- ueba
- user-behavior
- insider-threat
- anomaly-detection
- splunk
- baseline
subdomain: soc-operations
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- DE.CM-01
- DE.AE-02
- RS.MA-01
- DE.AE-06
---
# Performing User Behavior Analytics

## Overview

Cybersecurity skill for performing user behavior analytics. Follows industry best practices and security standards.

## When to Use

Use this skill when:
- SOC teams need to detect compromised accounts through abnormal authentication patterns
- Insider threat programs require behavioral monitoring beyond rule-based detection
- Impossible travel or geographic anomalies indicate credential compromise
- Privileged account monitoring requires baseline deviation detection

**Do not use** as the sole basis for disciplinary action — UEBA findings are indicators requiring investigation, not proof of malicious intent.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- SIEM with 30+ days of authentication and access log history for baseline creation
- VPN, O365, and Active Directory authentication logs normalized to CIM
- GeoIP database (MaxMind GeoLite2) for location-based anomaly detection
- Identity enrichment data (department, role, manager, typical work hours)
- Splunk Enterprise Security with UBA module or equivalent UEBA capability

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

1. **Plan Operations** — Define objectives, scope, and success criteria for user behavior analytics operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for user behavior analytics.
3. **Execute Core Workflow** — Perform the user behavior analytics operations following established procedures.
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

- [ ] All user behavior analytics procedures executed completely and documented
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