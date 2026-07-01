---
name: hunting-for-unusual-service-installations
description: Detect suspicious Windows service installations (MITRE ATT&CK T1543.003) by parsing System event logs for Event
  ID 7045, analyzing service binary paths, and identifying indicators of persistence mechanisms.
domain: cybersecurity
subdomain: threat-hunting
tags:
- threat-hunting
- T1543.003
- service-installation
- persistence
- Event-7045
- Sysmon
- Windows-services
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- Platform Hardening
- System Configuration Permissions
- Restore Object
- Restore Database
- Asset Inventory
nist_csf:
- DE.CM-01
- DE.AE-02
- DE.AE-07
- ID.RA-05
---

# Hunting for Unusual Service Installations

## Overview

Attackers frequently install malicious Windows services for persistence and privilege escalation (MITRE ATT&CK T1543.003 — Create or Modify System Process: Windows Service). Event ID 7045 in the System event log records every new service installation. This skill parses .evtx log files to extract service installation events, flags suspicious binary paths (temp directories, PowerShell, cmd.exe, encoded commands), and correlates with known attack patterns.


## When to Use
**Trigger phrases:**
- "hunting for unusual service installations"
- "Detect suspicious Windows service installations (MITRE ATT&CK T1543"


- When investigating security incidents that require hunting for unusual service installations
- When building detection rules or threat hunting queries for this domain
- When SOC analysts need structured procedures for this analysis type
- When validating security monitoring coverage for related attack techniques

## Prerequisites

- Python 3.9+ with `python-evtx`, `lxml`
- Windows System event log (.evtx) files
- Access to live System event log (optional, for real-time monitoring)
- Sysmon logs for enhanced process tracking (optional)

## Steps

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

1. Parse System.evtx for Event ID 7045 (new service installed)
2. Extract service name, binary path, service type, and account
3. Flag services with suspicious binary paths (temp dirs, encoded commands)
4. Detect PowerShell-based service creation patterns
5. Identify services running as LocalSystem with unusual paths
6. Cross-reference with known legitimate service baselines
7. Generate threat hunting report with MITRE ATT&CK T1543.003 mapping

## Expected Output

- JSON report listing all new service installations with risk scores, suspicious indicators, and remediation recommendations
- Timeline of service installation events with binary path analysis
## When NOT to Use

- You're responding to a known incident (use IR skills)
- Task is about analyzing confirmed malware (use analyzing-* skills)
- You need to implement detection rules (use implementing-* skills)
- Task is about vulnerability scanning (use scanning tools)
- You don't have access to endpoint/network data
- Task requires compliance auditing (use auditing-* skills)


## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Acting on threat intelligence without validating source reliability
- Sharing classified or sensitive indicators without proper handling procedures
- Alerting threat actors to detection capabilities through visible response actions
## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Results validated against known-good baselines or reference implementations
- Documentation complete enough for another analyst to reproduce findings

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |