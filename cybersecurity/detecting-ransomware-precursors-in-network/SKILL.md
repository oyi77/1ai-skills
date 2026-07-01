---
name: detecting-ransomware-precursors-in-network
description: >  Detects early-stage ransomware indicators in network traffic before encryption begins, including initial access
  broker activity, command-and-control beaconing, credential harvesting, reconnaissance scanning, and staging behavior. Uses
  network detection tools (Zeek, Suricata, Arkime), SIEM correlation rules, and threat intelligence feeds to identify ransomware
  precursor patterns such as Cobalt Strike beacons, Mimikatz network signatures, and RDP brute-force attempts.
domain: cybersecurity
tags:
- ransomware
- detection
- network-security
- incident-response
- defense
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
# Detecting Ransomware Precursors In Network

## Overview

Cybersecurity skill for detecting ransomware precursors in network. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "detecting ransomware precursors in network"
- "Detects early-stage ransomware indicators in network traffic before encryption b"


- Building detection rules for pre-ransomware network activity (the average time from Cobalt Strike deployment to encryption is 17 minutes)
- Monitoring for initial access broker (IAB) indicators that precede ransomware deployment
- Creating SIEM correlation rules that chain multiple precursor events into high-confidence alerts
- Tuning network detection systems to distinguish ransomware staging from normal administrative activity
- Investigating suspicious network patterns that may indicate ransomware operators have established a foothold

**Do not use** for post-encryption response (see recovering-from-ransomware-attack). This skill focuses on the pre-encryption detection window where containment can prevent data loss.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Network detection platform (Zeek/Bro, Suricata, or Arkime/Moloch) deployed on network TAP or SPAN ports
- SIEM platform (Splunk, Elastic Security, Microsoft Sentinel, or QRadar) ingesting network logs
- Threat intelligence feeds covering ransomware IOCs (CISA, abuse.ch, OTX, MISP)
- Network flow data (NetFlow/IPFIX) from core routers and firewalls
- DNS query logging from internal resolvers
- Full packet capture capability for incident investigation

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

1. **Define Detection Scope** — Identify the specific ransomware precursors in network techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for ransomware precursors in network.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting ransomware precursors in network indicators.
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

- [ ] All ransomware precursors in network procedures executed completely and documented
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