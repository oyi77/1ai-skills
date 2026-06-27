---
name: detecting-attacks-on-historian-servers
description: 'Detect cyber attacks targeting OT historian servers (OSIsoft PI, Ignition, Wonderware) that sit at the IT/OT
  boundary and serve as pivot points for lateral movement between enterprise and control networks, including data manipulation,
  unauthorized queries, and exploitation of historian-specific vulnerabilities.

  '
domain: cybersecurity
tags:
- ot-security
- ics
- historian
- osisoft-pi
- ignition
- pivot-point
- data-integrity
- lateral-movement
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
# Detecting Attacks On Historian Servers

## Overview

Cybersecurity skill for detecting attacks on historian servers. Follows industry best practices and security standards.

## When to Use

- When monitoring historian servers that bridge IT and OT networks for compromise indicators
- When detecting unauthorized queries or data manipulation in process historian databases
- When investigating lateral movement through historian servers between IT and OT zones
- When responding to alerts about exploitation of historian-specific vulnerabilities (CVE-2025-0921)
- When validating historian data integrity after a suspected OT security incident

**Do not use** for general database security monitoring (see database security skills), for historian deployment and configuration, or for IT-only data warehouse security.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Historian server inventory (OSIsoft PI, Ignition, GE Proficy, Wonderware InSQL)
- Network monitoring on historian network segments (both IT-facing and OT-facing interfaces)
- Historian API access for data integrity validation
- Baseline of normal historian query patterns (which applications query which tags)
- Understanding of historian architecture (data sources, interfaces, client connections)

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

1. **Define Detection Scope** — Identify the specific attacks on historian servers techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for attacks on historian servers.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting attacks on historian servers indicators.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All attacks on historian servers procedures executed completely and documented
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