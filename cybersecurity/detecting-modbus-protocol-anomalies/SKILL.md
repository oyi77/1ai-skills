---
name: detecting-modbus-protocol-anomalies
description: 'This skill covers detecting anomalies in Modbus/TCP and Modbus RTU communications in industrial control systems.
  It addresses function code monitoring, register range validation, timing analysis, unauthorized client detection, and deep
  packet inspection for malformed Modbus frames. The skill leverages Zeek with Modbus protocol analyzers, Suricata IDS with
  OT rules, and custom Python-based detection using Markov chain models for normal Modbus transaction sequences.

  '
domain: cybersecurity
tags:
- ot-security
- ics
- scada
- industrial-control
- iec62443
- modbus
- protocol-anomaly
subdomain: ot-ics-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_ai_rmf:
- MEASURE-2.7
- MAP-5.1
- MANAGE-2.4
atlas_techniques:
- AML.T0070
- AML.T0066
- AML.T0082
nist_csf:
- PR.IR-01
- DE.CM-01
- ID.AM-05
- GV.OC-02
---
# Detecting Modbus Protocol Anomalies

## Overview

Cybersecurity skill for detecting modbus protocol anomalies. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "detecting modbus protocol anomalies"
- "This skill covers detecting anomalies in Modbus/TCP and Modbus RTU communication"


- When deploying Modbus-specific intrusion detection in an OT environment
- When building baseline models for deterministic Modbus polling patterns
- When investigating suspicious Modbus traffic flagged by OT monitoring tools
- When implementing function code allowlisting on industrial firewalls
- When detecting unauthorized Modbus write commands that could manipulate process setpoints

**Do not use** for securing Modbus communications end-to-end (Modbus has no native security; see implementing-network-segmentation-for-ot for firewall-based controls), for non-Modbus protocol monitoring (see detecting-anomalies-in-industrial-control-systems for multi-protocol), or for active fuzzing of Modbus implementations (see performing-plc-firmware-security-analysis).


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Network SPAN/TAP access to monitor Modbus/TCP traffic (port 502)
- Zeek (formerly Bro) with Modbus protocol analyzer or Suricata with OT rulesets
- Python 3.9+ with scapy and pymodbus for custom analysis
- Baseline capture of normal Modbus traffic (minimum 1-2 weeks)
- Documentation of authorized Modbus clients, function codes, and register maps

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

1. **Define Detection Scope** — Identify the specific modbus protocol anomalies techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for modbus protocol anomalies.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting modbus protocol anomalies indicators.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All modbus protocol anomalies procedures executed completely and documented
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