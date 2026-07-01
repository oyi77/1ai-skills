---
name: deploying-decoy-files-for-ransomware-detection
description: >  'Deploys canary files (honeytokens) across file systems to detect ransomware encryption activity in real time.
  Uses strategically placed decoy documents monitored via file integrity monitoring or OS-level watchdogs to trigger alerts
  when ransomware modifies or encrypts them. Activates for requests involving ransomware canary deployment, honeyfile setup,
  deception-based ransomware detection, or file integrity monitoring for encryption.

  '.
domain: cybersecurity
tags:
- ransomware
- detection
- canary-files
- honeytokens
- deception
- file-integrity
subdomain: ransomware-defense
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.DS-11
- RS.MA-01
- RC.RP-01
- PR.IR-01
---
# Deploying Decoy Files For Ransomware Detection

## Overview

Cybersecurity skill for deploying decoy files for ransomware detection. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "deploying decoy files for ransomware detection"
- "Use when working with deploying decoy files for ransomware detection"


- Setting up early-warning detection for ransomware on file servers or endpoints
- Supplementing EDR/AV with a deception-based detection layer that catches unknown ransomware variants
- Creating high-fidelity ransomware alerts that have very low false-positive rates (legitimate users have no reason to touch decoy files)
- Testing ransomware response procedures by validating that canary file modifications trigger the expected alerting pipeline
- Protecting high-value file shares (finance, HR, legal) with tripwire files that indicate unauthorized encryption activity

**Do not use** decoy files as the sole ransomware defense. They are a detection mechanism, not a prevention mechanism, and should complement backups, EDR, and access controls.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Python 3.8+ with `watchdog` library for cross-platform file system monitoring
- Administrative access to target file shares or endpoints for canary placement
- File integrity monitoring (FIM) tool or SIEM integration for alert routing
- Understanding of target directory structure to place canaries in high-value locations
- Windows: NTFS change journal or ReadDirectoryChangesW API access
- Linux: inotify support in kernel (standard in modern kernels)

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

1. **Define Objectives** — Clarify the goals and scope for decoy files.
2. **Gather Resources** — Collect tools, data, and access needed for decoy files.
3. **Execute Process** — Carry out decoy files operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **ransomware detection** — Primary tool for this skill
- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- [ ] All decoy files procedures executed completely and documented
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