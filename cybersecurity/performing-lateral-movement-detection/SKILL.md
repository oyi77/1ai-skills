---
name: performing-lateral-movement-detection
description: 'Detects lateral movement techniques including Pass-the-Hash, PsExec, WMI execution, RDP pivoting, and SMB-based
  spreading using SIEM correlation of Windows event logs, network flow data, and endpoint telemetry mapped to MITRE ATT&CK
  Lateral Movement (TA0008) techniques.

  '
domain: cybersecurity
tags:
- soc
- lateral-movement
- mitre-attack
- pass-the-hash
- psexec
- wmi
- rdp
- smb
- detection
subdomain: soc-operations
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- Token Binding
- Execution Isolation
- Restore Access
- Application Protocol Command Analysis
- Process Termination
nist_csf:
- DE.CM-01
- DE.AE-02
- RS.MA-01
- DE.AE-06
---
# Performing Lateral Movement Detection

## Overview

Cybersecurity skill for performing lateral movement detection. Follows industry best practices and security standards.

## When to Use

Use this skill when:
- SOC teams need to detect attackers pivoting between systems after initial compromise
- Incident investigations require tracking an attacker's movement path through the network
- Detection engineering needs lateral movement rules mapped to ATT&CK TA0008 techniques
- Red/purple team exercises identify lateral movement detection gaps

**Do not use** for detecting initial access or external attacks — lateral movement detection focuses on internal host-to-host pivot activity.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Windows Security Event Logs (EventCode 4624, 4625, 4648, 4672) from all endpoints and servers
- Sysmon deployed with process creation (EventCode 1), network connections (EventCode 3), and named pipe (EventCode 17/18)
- Network flow data (NetFlow/sFlow, Zeek connection logs) for internal traffic analysis
- SIEM with cross-source correlation capability
- Baseline of normal internal authentication patterns

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

1. **Plan Operations** — Define objectives, scope, and success criteria for lateral movement detection operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for lateral movement detection.
3. **Execute Core Workflow** — Perform the lateral movement detection operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All lateral movement detection procedures executed completely and documented
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