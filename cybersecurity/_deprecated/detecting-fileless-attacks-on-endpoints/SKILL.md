---
name: detecting-fileless-attacks-on-endpoints
description: 'Detects fileless malware and in-memory attacks that execute entirely in RAM without writing persistent files
  to disk, evading traditional antivirus. Use when building detections for PowerShell-based attacks, reflective DLL injection,
  WMI persistence, and registry-resident malware. Activates for requests involving fileless malware detection, in-memory attacks,
  PowerShell exploitation, or living-off-the-land techniques.

  '
domain: cybersecurity
tags:
- endpoint
- fileless-malware
- memory-attacks
- PowerShell
- detection-engineering
subdomain: endpoint-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- PR.PS-02
- DE.CM-01
- PR.IR-01
---
# Detecting Fileless Attacks On Endpoints

## Overview

Cybersecurity skill for detecting fileless attacks on endpoints. Follows industry best practices and security standards.

## When to Use

Use this skill when:
- Building detection rules for fileless malware that operates entirely in memory
- Hunting for PowerShell-based attacks, reflective DLL injection, and WMI abuse
- Configuring endpoint telemetry (Sysmon, AMSI, PowerShell logging) to capture fileless indicators
- Investigating incidents where traditional AV found no malicious files

**Do not use** for detecting file-based malware or for malware reverse engineering.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Sysmon with process creation and WMI event logging enabled
- PowerShell Script Block Logging and Module Logging enabled
- AMSI (Antimalware Scan Interface) enabled for script content inspection
- EDR with behavioral detection capabilities (MDE, CrowdStrike, SentinelOne)

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

1. **Define Detection Scope** — Identify the specific fileless attacks on endpoints techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for fileless attacks on endpoints.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting fileless attacks on endpoints indicators.
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

- [ ] All fileless attacks on endpoints procedures executed completely and documented
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