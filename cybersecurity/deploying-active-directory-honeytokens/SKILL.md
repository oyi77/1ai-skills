---
name: deploying-active-directory-honeytokens
description: 'Deploys deception-based honeytokens in Active Directory including fake privileged accounts with AdminCount=1,
  fake SPNs for Kerberoasting detection (honeyroasting), decoy GPOs with cpassword traps, and fake BloodHound paths. Monitors
  Windows Security Event IDs 4769, 4625, 4662, 5136 for honeytoken interaction. Use when implementing AD deception defenses
  for detecting lateral movement, credential theft, and reconnaissance.

  '
domain: cybersecurity
tags:
- active-directory
- honeytokens
- kerberoasting
- deception
- detection
- bloodhound
- gpo
subdomain: deception-technology
version: '1.0'
author: mukul975
license: Apache-2.0
nist_csf:
- DE.CM-01
- DE.AE-06
- PR.IR-01
---
# Deploying Active Directory Honeytokens

## Overview

Cybersecurity skill for deploying active directory honeytokens. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "deploying active directory honeytokens"
- "When deploying deception-based detection in Active Directory environments"
- "When detecting Kerberoasting attacks via fake SPN honeytokens (honeyroasting)"
- "When creating tripwire accounts to detect credential theft and lateral movement"


- When deploying deception-based detection in Active Directory environments
- When detecting Kerberoasting attacks via fake SPN honeytokens (honeyroasting)
- When creating tripwire accounts to detect credential theft and lateral movement
- When building decoy GPOs to detect Group Policy Preference password harvesting
- When creating deceptive BloodHound paths to misdirect and detect attackers
- When supplementing existing AD monitoring with high-fidelity detection signals


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Domain Admin or delegated AD administration privileges
- Active Directory domain (Windows Server 2016+ recommended)
- Windows Event Log forwarding to SIEM (Splunk, Sentinel, Elastic)
- PowerShell 5.1+ with ActiveDirectory module
- Group Policy Management Console (GPMC)
- Understanding of AD security, Kerberos, and BloodHound attack paths

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

1. **Define Objectives** — Clarify the goals and scope for active directory honeytokens.
2. **Gather Resources** — Collect tools, data, and access needed for active directory honeytokens.
3. **Execute Process** — Carry out active directory honeytokens operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Design** — Define interface, identify patterns, plan implementation
1. **Implement** — Write code following existing conventions, add tests
1. **Verify** — Run tests, check integration, validate behavior

## Verification

- [ ] All active directory honeytokens procedures executed completely and documented
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