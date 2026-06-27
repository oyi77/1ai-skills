---
name: configuring-windows-defender-advanced-settings
description: 'Configures Microsoft Defender for Endpoint (MDE) advanced protection settings including attack surface reduction
  rules, controlled folder access, network protection, and exploit protection. Use when hardening Windows endpoints beyond
  default Defender settings, deploying enterprise-grade endpoint protection, or meeting compliance requirements for advanced
  malware defense. Activates for requests involving Windows Defender configuration, ASR rules, MDE tuning, or Microsoft endpoint
  security.

  '
domain: cybersecurity
tags:
- endpoint
- windows-security
- Microsoft-Defender
- ASR
- exploit-protection
- MDE
subdomain: endpoint-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- PR.PS-02
- DE.CM-01
- PR.IR-01
---
# Configuring Windows Defender Advanced Settings

## Overview

Cybersecurity skill for configuring windows defender advanced settings. Follows industry best practices and security standards.

## When to Use

Use this skill when:
- Configuring Microsoft Defender for Endpoint (MDE) beyond default settings for enhanced protection
- Implementing Attack Surface Reduction (ASR) rules to block common attack techniques
- Enabling controlled folder access for ransomware protection
- Configuring network protection and exploit protection features
- Deploying Defender settings via Intune, SCCM, or Group Policy at enterprise scale

**Do not use** this skill for third-party EDR deployment (CrowdStrike, SentinelOne) or for Microsoft Defender for Cloud (Azure workload protection).


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Windows 10/11 Enterprise with Microsoft Defender Antivirus enabled
- Microsoft 365 E5 or Microsoft Defender for Endpoint Plan 2 license (for full MDE features)
- Microsoft Intune or SCCM for enterprise policy deployment
- Microsoft 365 Defender portal access (security.microsoft.com)
- Endpoints not running third-party AV in active mode (Defender enters passive mode)

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

1. **Define Objectives** — Clarify the goals and scope for windows defender advanced settings.
2. **Gather Resources** — Collect tools, data, and access needed for windows defender advanced settings.
3. **Execute Process** — Carry out windows defender advanced settings operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All windows defender advanced settings procedures executed completely and documented
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