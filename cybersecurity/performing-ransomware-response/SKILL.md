---
name: performing-ransomware-response
description: 'Executes a structured ransomware incident response from initial detection through containment, forensic analysis,
  decryption assessment, recovery, and post-incident hardening. Addresses ransom negotiation considerations, backup integrity
  verification, and regulatory notification requirements. Activates for requests involving ransomware response, ransomware
  recovery, crypto-ransomware, data encryption attack, ransom payment decision, or ransomware containment.

  '
domain: cybersecurity
tags:
- ransomware
- encryption-recovery
- backup-restoration
- ransom-negotiation
- CISA-guidance
subdomain: incident-response
mitre_attack:
- T1486
- T1490
- T1489
- T1021
- T1570
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- RS.MA-01
- RS.MA-02
- RS.AN-03
- RC.RP-01
---
# Performing Ransomware Response

## Overview

Cybersecurity skill for performing ransomware response. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "performing ransomware response"
- "Executes a structured ransomware incident response from initial detection throug"


- Ransomware has been detected executing or file encryption is actively occurring
- Users report inability to open files with unfamiliar extensions appended
- A ransom note is discovered on one or more systems
- EDR detects mass file modification patterns consistent with encryption behavior
- Threat intelligence warns of an imminent ransomware campaign targeting the organization

**Do not use** for general malware incidents that do not involve file encryption or extortion; use malware incident response procedures instead.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Ransomware-specific incident response playbook reviewed and approved by executive leadership
- Tested and verified offline backup strategy with air-gapped or immutable copies
- Incident retainer with a specialized ransomware response firm (e.g., Mandiant, CrowdStrike Services, Kroll)
- Legal counsel pre-engaged for OFAC sanctions screening and regulatory notification
- Cyber insurance carrier contact information and policy coverage details
- Bitcoin/cryptocurrency analysis capability or third-party engagement for payment tracing

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

1. **Plan Operations** — Define objectives, scope, and success criteria for ransomware response operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for ransomware response.
3. **Execute Core Workflow** — Perform the ransomware response operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All ransomware response procedures executed completely and documented
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