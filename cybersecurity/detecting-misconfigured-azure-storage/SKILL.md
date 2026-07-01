---
name: detecting-misconfigured-azure-storage
description: 'Detecting misconfigured Azure Storage accounts including publicly accessible blob containers, missing encryption
  settings, overly permissive SAS tokens, disabled logging, and network access violations using Azure CLI, PowerShell, and
  Microsoft Defender for Storage.

  '. Use when working with detecting misconfigured azure storage.
domain: cybersecurity
tags:
- cloud-security
- azure
- storage-security
- blob-storage
- sas-tokens
- data-protection
subdomain: cloud-security
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
nist_csf:
- PR.IR-01
- ID.AM-08
- GV.SC-06
- DE.CM-01
---
# Detecting Misconfigured Azure Storage

## Overview

Cybersecurity skill for detecting misconfigured azure storage. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "detecting misconfigured azure storage"
- "Detecting misconfigured Azure Storage accounts including publicly accessible blo"


- When performing a security audit of Azure Storage accounts across subscriptions
- When responding to Microsoft Defender for Storage alerts about anonymous access or data exfiltration
- When compliance requires verification of encryption, network restrictions, and access logging
- When investigating potential data exposure through publicly accessible blob containers
- When onboarding Azure subscriptions and establishing storage security baselines

**Do not use** for Azure SQL or Cosmos DB security auditing (use dedicated database security tools), for real-time threat detection on storage operations (use Defender for Storage), or for Azure Files or Data Lake Gen2 specific auditing without adapting the checks.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Azure CLI installed and authenticated (`az login`) with Reader and Storage Account Contributor roles
- Az PowerShell module installed for advanced queries (`Install-Module Az.Storage`)
- Microsoft Defender for Storage enabled for threat detection
- Access to Azure Resource Graph for cross-subscription queries
- ScoutSuite or Prowler Azure provider for automated assessment

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

1. **Define Detection Scope** — Identify the specific misconfigured azure storage techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for misconfigured azure storage.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting misconfigured azure storage indicators.
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

- [ ] All misconfigured azure storage procedures executed completely and documented
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