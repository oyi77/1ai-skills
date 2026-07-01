---
name: performing-privilege-escalation-assessment
description: Performs privilege escalation assessments on compromised Linux and Windows systems to identify paths from low-privilege
  access to root or SYSTEM-level control. The tester enumerates misconfigurations, vulnerable services, kernel exploits, SUID
  binaries, unquoted service paths, and credential stores to demonstrate the full impact of an initial compromise.
domain: cybersecurity
tags:
- privilege-escalation
- post-exploitation
- Linux-privesc
- Windows-privesc
- local-exploitation
subdomain: penetration-testing
version: 1.0.0
author: mahipal
license: Apache-2.0
d3fend_techniques:
- Executable Denylisting
- Execution Isolation
- File Metadata Consistency Validation
- Restore Access
- Password Authentication
nist_csf:
- ID.RA-01
- ID.RA-06
- GV.OV-02
- DE.AE-07
---
# Performing Privilege Escalation Assessment

## Overview

Cybersecurity skill for performing privilege escalation assessment. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "performing privilege escalation assessment"
- "Performs privilege escalation assessments on compromised Linux and Windows syste"


- After gaining initial low-privilege access during a penetration test to demonstrate full system compromise
- Assessing the security hardening of Linux and Windows servers against local privilege escalation attacks
- Evaluating whether endpoint detection and response (EDR) tools detect common privilege escalation techniques
- Testing the effectiveness of least-privilege policies and application whitelisting on endpoints
- Validating that container breakout and VM escape controls are properly configured

**Do not use** without written authorization, against production systems where exploitation could cause downtime, or for deploying kernel exploits on systems without prior approval and rollback capability.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Low-privilege shell access (reverse shell, SSH, RDP) to the target system obtained through authorized means
- Privilege escalation enumeration scripts: linPEAS (Linux), winPEAS (Windows), Linux Smart Enumeration (LSE)
- Compiled kernel exploits for common CVEs or access to compilation tools on the target
- GTFOBins reference for Linux SUID/sudo binary abuse and LOLBAS reference for Windows living-off-the-land binaries
- Precompiled post-exploitation binaries for the target architecture if compilation is not available on the target

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

1. **Plan Operations** — Define objectives, scope, and success criteria for privilege escalation assessment operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for privilege escalation assessment.
3. **Execute Core Workflow** — Perform the privilege escalation assessment operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All privilege escalation assessment procedures executed completely and documented
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