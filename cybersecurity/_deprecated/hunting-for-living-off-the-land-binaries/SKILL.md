---
name: hunting-for-living-off-the-land-binaries
description: Proactively hunt for adversary abuse of legitimate system binaries (LOLBins) to execute malicious payloads while
  evading detection.
domain: cybersecurity
tags:
- threat-hunting
- mitre-attack
- lolbins
- edr
- siem
- proactive-detection
- defense-evasion
subdomain: threat-hunting
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- Executable Denylisting
- Execution Isolation
- File Metadata Consistency Validation
- Application Protocol Command Analysis
- Content Format Conversion
nist_csf:
- DE.CM-01
- DE.AE-02
- DE.AE-07
- ID.RA-05
---
# Hunting For Living Off The Land Binaries

## When to Use

- When investigating fileless malware campaigns that bypass traditional AV
- During proactive threat hunts targeting defense evasion techniques
- When EDR alerts fire on legitimate binaries executing unusual child processes
- After threat intelligence reports indicate LOLBin abuse in active campaigns
- During red team/purple team exercises validating detection coverage for T1218

## Prerequisites

- Access to EDR telemetry (CrowdStrike, Microsoft Defender for Endpoint, SentinelOne)
- SIEM with process creation logs (Sysmon Event ID 1, Windows Security 4688)
- Familiarity with LOLBAS Project (lolbas-project.github.io) reference list
- PowerShell command-line logging enabled (Module Logging, Script Block Logging)
- Network proxy or firewall logs for correlating outbound connections

## Workflow

1. **Define Detection Scope** — Identify the specific  techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for .
3. **Build Detection Queries** — Write living off the land binaries queries targeting  indicators. Use platform-specific query language for optimal performance.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **living off the land binaries** — Primary tool for this skill
- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All  procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
