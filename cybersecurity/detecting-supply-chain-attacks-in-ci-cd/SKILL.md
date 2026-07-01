---
name: detecting-supply-chain-attacks-in-ci-cd
description: 'Scans GitHub Actions workflows and CI/CD pipeline configurations for supply chain attack vectors including unpinned
  actions, script injection via expressions, dependency confusion, and secrets exposure. Uses PyGithub and YAML parsing for
  automated audit. Use when hardening CI/CD pipelines or investigating compromised build systems.

  '
domain: cybersecurity
tags:
- detecting
- supply
- chain
- attacks
subdomain: security-operations
version: '1.0'
author: mahipal
license: Apache-2.0
atlas_techniques:
- AML.T0010
- AML.T0104
nist_ai_rmf:
- GOVERN-5.2
- MAP-1.6
- MANAGE-2.2
nist_csf:
- DE.CM-01
- RS.MA-01
- GV.OV-01
- DE.AE-02
---
# Detecting Supply Chain Attacks In Ci Cd

## Overview

Cybersecurity skill for detecting supply chain attacks in ci cd. Follows industry best practices and security standards.

## When to Use

- When investigating security incidents that require detecting supply chain attacks in ci cd
- When building detection rules or threat hunting queries for this domain
- When SOC analysts need structured procedures for this analysis type
- When validating security monitoring coverage for related attack techniques


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Familiarity with security operations concepts and tools
- Access to a test or lab environment for safe execution
- Python 3.8+ with required dependencies installed
- Appropriate authorization for any testing activities

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

1. **Define Detection Scope** — Identify the specific supply chain attacks in ci cd techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for supply chain attacks in ci cd.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting supply chain attacks in ci cd indicators.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis


## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- [ ] All supply chain attacks in ci cd procedures executed completely and documented
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