---
name: performing-ot-network-security-assessment
description: 'This skill covers conducting comprehensive security assessments of Operational Technology (OT) networks including
  SCADA systems, DCS architectures, and industrial control system communication paths. It addresses the Purdue Reference Model
  layers, identifies IT/OT convergence risks, evaluates firewall rules between zones, and maps industrial protocol traffic
  (Modbus, DNP3, OPC UA, EtherNet/IP) to detect misconfigurations, unauthorized connections, and attack surfaces in critical
  infrastructure.

  '
domain: cybersecurity
tags:
- ot-security
- ics
- scada
- industrial-control
- iec62443
- network-assessment
subdomain: ot-ics-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- DE.CM-01
- ID.AM-05
- GV.OC-02
---
# Performing Ot Network Security Assessment

## Overview

Cybersecurity skill for performing ot network security assessment. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "performing ot network security assessment"
- "This skill covers conducting comprehensive security assessments of Operational T"


- When conducting an initial security baseline of an OT/ICS environment for a new client
- When evaluating the security posture of a facility after an IT/OT convergence initiative
- When preparing for IEC 62443 or NERC CIP compliance audits
- When assessing risk following a merger or acquisition involving industrial facilities
- When investigating whether an OT network has been compromised or has unmonitored pathways to corporate IT

**Do not use** for IT-only network assessments without OT components, for application-layer vulnerability scanning of IT web applications (see performing-web-app-penetration-test), or for active exploitation of live OT systems without explicit authorization and safety controls in place.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Written authorization from the asset owner and operations management for all assessment activities
- Understanding of the Purdue Reference Model and IEC 62443 zone/conduit architecture
- Passive network monitoring tools (Nozomi Guardian, Dragos Platform, or Wireshark with industrial protocol dissectors)
- Access to network diagrams, firewall rule sets, and asset inventories (or the ability to perform passive discovery)
- Safety briefing on the physical processes controlled by the OT systems under assessment

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

1. **Plan Operations** — Define objectives, scope, and success criteria for ot network security assessment operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for ot network security assessment.
3. **Execute Core Workflow** — Perform the ot network security assessment operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All ot network security assessment procedures executed completely and documented
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