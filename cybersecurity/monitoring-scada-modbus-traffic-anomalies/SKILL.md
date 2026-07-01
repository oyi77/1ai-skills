---
name: monitoring-scada-modbus-traffic-anomalies
description: Monitors Modbus TCP traffic on SCADA and ICS networks to detect anomalous function code usage, unauthorized register
  writes, and suspicious communication patterns. The analyst uses deep packet inspection with pymodbus, Scapy, and Zeek to
  baseline normal PLC/RTU communication behavior, then applies statistical and rule-based anomaly detection to identify reconnaissance,
  parameter manipulation, and denial-of-service attacks targeting Modbus devices on port 502.
domain: cybersecurity
tags:
- Modbus-TCP
- SCADA
- ICS-security
- deep-packet-inspection
- anomaly-detection
- OT-monitoring
subdomain: ot-security
version: 1.0.0
author: mukul975
license: Apache-2.0
nist_csf:
- PR.IR-01
- DE.CM-01
- ID.AM-05
---
# Monitoring Scada Modbus Traffic Anomalies

## Overview

Cybersecurity skill for monitoring scada modbus traffic anomalies. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "monitoring scada modbus traffic anomalies"
- "Monitors Modbus TCP traffic on SCADA and ICS networks to detect anomalous functi"


- Monitoring OT/ICS networks for unauthorized Modbus commands targeting PLCs, RTUs, or HMIs
- Detecting reconnaissance activity such as Modbus device enumeration (function code 43, Read Device Identification)
- Identifying unauthorized write operations (function codes 05, 06, 15, 16) to coils and holding registers that could alter physical process parameters
- Baselining normal Modbus communication patterns and alerting on deviations in function code distribution, register access ranges, or timing intervals
- Investigating suspected sabotage or insider threats manipulating SCADA process values through Modbus register writes

**Do not use** on networks without authorization from the asset owner, for active injection or fuzzing against production SCADA systems, or as a replacement for safety-instrumented systems (SIS) that provide physical process protection.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Network tap or SPAN port on the OT network segment carrying Modbus TCP traffic (port 502)
- Python 3.9+ with pymodbus (>=3.6), scapy (>=2.5), and pandas for traffic analysis
- Zeek (formerly Bro) installed with the Modbus protocol analyzer enabled for passive traffic logging
- Wireshark or tshark for initial packet capture and validation of Modbus frame structure
- A baseline period of normal operations (minimum 48-72 hours) to establish communication profiles per device pair
- Network diagram identifying Modbus master-slave relationships, device IP addresses, and expected function code usage

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

1. **Define Objectives** — Clarify the goals and scope for scada modbus traffic anomalies.
2. **Gather Resources** — Collect tools, data, and access needed for scada modbus traffic anomalies.
3. **Execute Process** — Carry out scada modbus traffic anomalies operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All scada modbus traffic anomalies procedures executed completely and documented
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