---
name: detecting-modbus-command-injection-attacks
description: 'Detect command injection attacks against Modbus TCP/RTU protocol in ICS environments by monitoring for unauthorized
  write operations, anomalous function codes, malformed frames, and deviations from established communication baselines using
  ICS-aware IDS and protocol deep packet inspection.

  '. Use when working with detecting modbus command injection attacks.
domain: cybersecurity
tags:
- ot-security
- ics
- modbus
- command-injection
- protocol-analysis
- ids
- scada
- threat-detection
subdomain: ot-ics-security
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- DE.CM-01
- ID.AM-05
- GV.OC-02
---
# Detecting Modbus Command Injection Attacks

## Overview

Cybersecurity skill for detecting modbus command injection attacks. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "detecting modbus command injection attacks"
- "Detect command injection attacks against Modbus TCP/RTU protocol in ICS environm"


- When deploying intrusion detection for environments using Modbus TCP (port 502) or Modbus RTU
- When investigating suspected unauthorized modifications to PLC registers or coils
- When building detection analytics for OT SOC monitoring Modbus-heavy environments
- When responding to FrostyGoop-style attacks that leverage Modbus TCP for operational impact
- When performing baseline validation after a suspected compromise of a Modbus master

**Do not use** for detecting attacks on non-Modbus protocols (see detecting-dnp3-protocol-anomalies for DNP3), for general IT network intrusion detection, or for Modbus device configuration (see performing-ot-vulnerability-scanning-safely).


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Network SPAN/TAP on the segment carrying Modbus TCP traffic (typically port 502)
- Baseline of normal Modbus communication patterns (masters, slaves, function codes, register ranges, polling intervals)
- Suricata, Zeek, or commercial OT IDS deployed with Modbus protocol parsers enabled
- Understanding of Modbus function codes used in the environment (read vs write operations)
- Access to PLC programming documentation to validate expected register ranges

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

1. **Define Detection Scope** — Identify the specific modbus command injection attacks techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for modbus command injection attacks.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting modbus command injection attacks indicators.
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

- [ ] All modbus command injection attacks procedures executed completely and documented
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