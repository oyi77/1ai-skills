---
name: detecting-lateral-movement-with-splunk
description: Detect adversary lateral movement across networks using Splunk SPL queries against Windows authentication logs,
  SMB traffic, and remote service abuse. Use when detecting adversary lateral movement across networks using splunk spl queries.
domain: cybersecurity
tags:
- threat-hunting
- mitre-attack
- lateral-movement
- splunk
- siem
- proactive-detection
- ta0008
subdomain: threat-hunting
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- Application Protocol Command Analysis
- Network Isolation
- Network Traffic Analysis
- Client-server Payload Profiling
- Network Traffic Community Deviation
nist_csf:
- DE.CM-01
- DE.AE-02
- DE.AE-07
- ID.RA-05
---
# Detecting Lateral Movement With Splunk

## Overview

Cybersecurity skill for detecting lateral movement with splunk. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "detecting lateral movement with splunk"
- "Detect adversary lateral movement across networks using Splunk SPL queries again"


- When hunting for adversary movement between compromised systems
- After detecting credential theft to trace subsequent lateral activity
- When investigating unusual authentication patterns across the network
- During incident response to scope the breadth of compromise
- When proactively hunting for TA0008 (Lateral Movement) techniques


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Splunk Enterprise or Splunk Cloud with Windows event data ingested
- Windows Security Event Logs forwarded (4624, 4625, 4648, 4672, 4768, 4769)
- Sysmon deployed for process creation and network connection data
- Network flow data or firewall logs for SMB/RDP/WinRM correlation
- Active Directory user and group membership reference data

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

1. **Define Detection Scope** — Identify the specific lateral movement techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for lateral movement.
3. **Build Detection Queries** — Write splunk queries targeting lateral movement indicators. Use platform-specific query language for optimal performance.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **splunk** — Primary tool for this skill
- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis


## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- [ ] All lateral movement procedures executed completely and documented
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