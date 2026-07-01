---
name: performing-power-grid-cybersecurity-assessment
description: >  This skill covers conducting cybersecurity assessments of electric power grid infrastructure including generation
  facilities, transmission substations, distribution systems, and energy management system (EMS) control centers. It addresses
  NERC CIP compliance verification, substation automation security, IEC 61850 protocol analysis, synchrophasor (PMU) network
  security, and the unique threat landscape targeting power grid operations as demonstrated by Industroyer/CrashOverride and
  related.
domain: cybersecurity
tags:
- ot-security
- ics
- scada
- industrial-control
- iec62443
- nerc-cip
- power-grid
- substation
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
# Performing Power Grid Cybersecurity Assessment

## Overview

Cybersecurity skill for performing power grid cybersecurity assessment. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "performing power grid cybersecurity assessment"
- "This skill covers conducting cybersecurity assessments of electric power grid in"


- When conducting periodic cybersecurity assessments of power grid facilities per NERC CIP requirements
- When assessing substation automation systems using IEC 61850 GOOSE and MMS protocols
- When evaluating the security of an Energy Management System (EMS) or SCADA control center
- When assessing synchrophasor (PMU) networks and wide-area monitoring systems
- When preparing for regional entity compliance audits or internal security reviews

**Do not use** for non-BES systems below NERC registration thresholds, for general OT assessment without power grid specifics (see performing-ot-network-security-assessment), or for physical security assessment of generation facilities without cyber scope.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Understanding of electric power grid architecture (generation, transmission, distribution)
- Familiarity with NERC CIP standards and BES Cyber System categorization
- Knowledge of power grid protocols (IEC 61850, IEC 60870-5-104, DNP3, ICCP/TASE.2)
- Passive monitoring tools for substation network traffic analysis
- Access to EMS/SCADA architecture documentation and network diagrams

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

1. **Plan Operations** — Define objectives, scope, and success criteria for power grid cybersecurity assessment operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for power grid cybersecurity assessment.
3. **Execute Core Workflow** — Perform the power grid cybersecurity assessment operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- [ ] All power grid cybersecurity assessment procedures executed completely and documented
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