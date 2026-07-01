---
name: detecting-living-off-the-land-attacks
description: 'Detect abuse of legitimate Windows binaries (LOLBins) used for living off the land attacks. Monitors process
  creation, command-line arguments, and parent-child relationships to identify suspicious LOLBin execution patterns.

  '
domain: cybersecurity
tags:
- lolbins
- lotl
- fileless-attacks
- process-monitoring
subdomain: threat-detection
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
- DE.CM-01
- DE.AE-02
- DE.AE-06
- ID.RA-05
---
# Detecting Living Off The Land Attacks

## Overview

Cybersecurity skill for detecting living off the land attacks. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "detecting living off the land attacks"
- "Detect abuse of legitimate Windows binaries (LOLBins) used for living off the la"


- Building detection rules for SIEM or EDR platforms to catch LOLBin abuse in real time
- Investigating alerts where legitimate system binaries appear in unexpected execution contexts
- Threat hunting across endpoint telemetry for fileless attack indicators
- Hardening application whitelisting policies (AppLocker, WDAC) to restrict dangerous LOLBin usage
- Creating Sysmon configurations tuned to capture LOLBin-related process creation events
- Responding to incidents where adversaries bypassed AV by using only built-in OS tools

**Do not use** for blocking all LOLBin execution outright; these are legitimate system tools with valid administrative uses. Detection must focus on anomalous context (parent process, command-line arguments, network activity) rather than binary presence alone.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Sysmon v15+ installed on Windows endpoints with a tuned configuration (SwiftOnSecurity or Olaf Hartong baseline)
- SIEM platform ingesting Sysmon Event IDs 1 (Process Create), 3 (Network Connection), 7 (Image Loaded), 11 (File Create)
- Windows Event Log forwarding for Security Event IDs 4688 (Process Creation with command-line logging enabled)
- LOLBAS project reference: https://lolbas-project.github.io/
- Python 3.8+ with `evtx`, `pandas` for offline log analysis
- Sigma rule repository for cross-platform detection rule authoring

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

1. **Define Detection Scope** — Identify the specific living off the land attacks techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for living off the land attacks.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting living off the land attacks indicators.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All living off the land attacks procedures executed completely and documented
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