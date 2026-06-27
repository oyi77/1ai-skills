---
name: hunting-for-persistence-via-wmi-subscriptions
description: Hunt for adversary persistence through Windows Management Instrumentation event subscriptions by monitoring WMI
  consumer, filter, and binding creation events that execute malicious code triggered by system events.
domain: cybersecurity
tags:
- threat-hunting
- wmi-persistence
- mitre-t1546-003
- event-subscription
- windows
- endpoint-detection
subdomain: threat-hunting
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- Application Protocol Command Analysis
- Network Isolation
- Network Traffic Analysis
- Client-server Payload Profiling
- Platform Monitoring
nist_csf:
- DE.CM-01
- DE.AE-02
- DE.AE-07
- ID.RA-05
---
# Hunting For Persistence Via Wmi Subscriptions

## Overview

Cybersecurity skill for hunting for persistence via wmi subscriptions. Follows industry best practices and security standards.

## When to Use

- When proactively searching for fileless persistence mechanisms in Windows environments
- After threat intelligence reports indicate WMI-based persistence by APT groups (APT29, APT32, FIN8)
- When investigating systems where malware persists across reboots despite cleanup attempts
- During incident response when standard persistence locations (Run keys, scheduled tasks) are clean
- When WmiPrvSe.exe is observed spawning unexpected child processes


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Sysmon Event ID 19, 20, 21 (WMI Event Filter/Consumer/Binding) enabled
- Windows Event ID 5861 (WMI activity logging) from Microsoft-Windows-WMI-Activity
- PowerShell logging enabled (Script Block Logging, Module Logging)
- WMI repository access for enumeration
- SIEM platform for event correlation

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

1. **Define Detection Scope** — Identify the specific  techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for .
3. **Build Detection Queries** — Write persistence via wmi subscriptions queries targeting  indicators. Use platform-specific query language for optimal performance.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **persistence via wmi subscriptions** — Primary tool for this skill
- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All  procedures executed completely and documented
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