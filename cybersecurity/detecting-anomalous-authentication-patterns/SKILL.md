---
name: detecting-anomalous-authentication-patterns
description: 'Detects anomalous authentication patterns using UEBA analytics, statistical baselines, and machine learning
  models to identify impossible travel, credential stuffing, brute force, password spraying, and compromised account behaviors
  across authentication logs. Activates for requests involving authentication anomaly detection, login behavior analysis,
  UEBA implementation, or suspicious sign-in investigation.

  '
domain: cybersecurity
tags:
- UEBA
- authentication-anomaly
- impossible-travel
- brute-force
- credential-stuffing
- behavioral-analytics
subdomain: identity-access-management
version: '1.0'
author: mahipal
license: Apache-2.0
atlas_techniques:
- AML.T0043
- AML.T0018
nist_ai_rmf:
- MEASURE-2.7
- MEASURE-2.5
- MAP-5.1
nist_csf:
- PR.AA-01
- PR.AA-02
- PR.AA-05
- PR.AA-06
---
# Detecting Anomalous Authentication Patterns

## Overview

Cybersecurity skill for detecting anomalous authentication patterns. Follows industry best practices and security standards.

## When to Use

- Security operations needs to identify compromised accounts from authentication log analysis
- Implementing impossible travel detection to flag geographically inconsistent logins
- Detecting brute force, password spraying, and credential stuffing attacks in real time
- Building behavioral baselines for users to identify deviations indicating account compromise
- Correlating authentication anomalies with threat intelligence for lateral movement detection
- Investigating alerts from SIEM or IdP for suspicious sign-in activity

**Do not use** for static rule-based alerting on single failed logins; anomaly detection requires statistical baselines across time and entity dimensions to reduce false positives.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Authentication log sources (Azure AD/Entra ID sign-in logs, Okta system logs, Active Directory event logs 4624/4625/4648/4768/4771)
- SIEM platform (Splunk, Microsoft Sentinel, Elastic SIEM) with at least 90 days of baseline data
- GeoIP database for location-based anomaly detection (MaxMind GeoLite2 or IP2Location)
- Python 3.9+ with pandas, scikit-learn, and scipy for custom analytics
- User identity context (department, role, typical work hours, location)

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

1. **Define Detection Scope** — Identify the specific anomalous authentication patterns techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for anomalous authentication patterns.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting anomalous authentication patterns indicators.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All anomalous authentication patterns procedures executed completely and documented
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