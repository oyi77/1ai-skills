---
name: detecting-lateral-movement-in-network
description: 'Identifies lateral movement techniques in enterprise networks by analyzing authentication logs, network flows,
  SMB traffic, and RDP sessions using Zeek, Velociraptor, and SIEM correlation rules to detect attackers moving between systems.

  '. Use when working with detecting lateral movement in network.
domain: cybersecurity
tags:
- network-security
- lateral-movement
- threat-detection
- siem
- pass-the-hash
subdomain: network-security
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
- PR.IR-01
- DE.CM-01
- ID.AM-03
- PR.DS-02
---
# Detecting Lateral Movement In Network

## Overview

Cybersecurity skill for detecting lateral movement in network. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "detecting lateral movement in network"
- "Identifies lateral movement techniques in enterprise networks by analyzing authe"


- Monitoring enterprise networks for post-compromise lateral movement patterns (pass-the-hash, RDP hopping, PSExec)
- Building SIEM detection rules and alerts for common MITRE ATT&CK lateral movement techniques (T1021, T1570)
- Investigating suspected breaches by analyzing authentication patterns and network connections between internal hosts
- Hunting for anomalous east-west traffic patterns that indicate an attacker pivoting through the network
- Validating that network segmentation and access controls effectively limit lateral movement paths

**Do not use** as a substitute for endpoint detection and response (EDR) tools, for monitoring only north-south traffic while ignoring internal traffic flows, or without baseline knowledge of normal internal communication patterns.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Network security monitoring deployed at internal choke points (Zeek, Suricata, or network TAPs)
- SIEM platform (Splunk, Elastic, Microsoft Sentinel) collecting Windows Security Event Logs, DNS, and flow data
- Windows Event Log forwarding configured for Security events (4624, 4625, 4648, 4672, 4768, 4769)
- Baseline of normal internal authentication and connection patterns
- Understanding of MITRE ATT&CK Lateral Movement tactics (TA0008)

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

1. **Define Detection Scope** — Identify the specific lateral movement in network techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for lateral movement in network.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting lateral movement in network indicators.
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

- [ ] All lateral movement in network procedures executed completely and documented
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