---
name: detecting-anomalies-in-industrial-control-systems
description: 'This skill covers deploying anomaly detection systems for industrial control environments using machine learning
  models trained on OT network baselines, physics-based process models, and behavioral analysis of industrial protocol communications.
  It addresses building normal behavior profiles for SCADA polling patterns, detecting deviations in Modbus/DNP3/OPC UA traffic,
  identifying rogue devices, and correlating network anomalies with physical process data from historians.

  '
domain: cybersecurity
tags:
- ot-security
- ics
- scada
- industrial-control
- iec62443
- anomaly-detection
- machine-learning
subdomain: ot-ics-security
version: 1.0.0
author: mahipal
license: Apache-2.0
atlas_techniques:
- AML.T0043
- AML.T0018
nist_ai_rmf:
- MEASURE-2.7
- MEASURE-2.5
- MAP-5.1
nist_csf:
- PR.IR-01
- DE.CM-01
- ID.AM-05
- GV.OC-02
---
# Detecting Anomalies In Industrial Control Systems

## Overview

Cybersecurity skill for detecting anomalies in industrial control systems. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "detecting anomalies in industrial control systems"
- "This skill covers deploying anomaly detection systems for industrial control env"


- When deploying continuous monitoring for OT environments that lack intrusion detection
- When building behavior-based detection to complement signature-based IDS in OT networks
- When establishing baselines for deterministic SCADA communications to detect deviations
- When integrating machine learning anomaly detection with OT security monitoring platforms
- When investigating alerts from Nozomi Guardian or Dragos Platform that require deeper analysis

**Do not use** for signature-based detection of known exploits (see detecting-attacks-on-scada-systems), for IT network anomaly detection without OT protocols, or as a replacement for process safety systems (SIS).


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Passive network monitoring sensors on OT network SPAN/TAP ports
- Minimum 2-4 weeks of baseline traffic capture during normal operations
- Python 3.9+ with scikit-learn, numpy, pandas for ML model training
- Process historian access for physical process correlation data
- Understanding of normal operational patterns including shift changes, batch processes, and maintenance windows

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

1. **Define Detection Scope** — Identify the specific anomalies in industrial control systems techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for anomalies in industrial control systems.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting anomalies in industrial control systems indicators.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All anomalies in industrial control systems procedures executed completely and documented
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