---
name: detecting-process-hollowing-technique
description: Detect process hollowing (T1055.012) by analyzing memory-mapped sections, hollowed process indicators, and parent-child
  process anomalies in EDR telemetry.
domain: cybersecurity
tags:
- threat-hunting
- mitre-attack
- process-hollowing
- process-injection
- edr
- t1055
- proactive-detection
subdomain: threat-hunting
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- Platform Monitoring
- Process Code Segment Verification
- Segment Address Offset Randomization
- Process Analysis
- Application Hardening
nist_csf:
- DE.CM-01
- DE.AE-02
- DE.AE-07
- ID.RA-05
---
# Detecting Process Hollowing Technique

## When to Use

- When investigating suspected fileless malware or in-memory threats
- After EDR alerts on process injection or suspicious memory operations
- When hunting for defense evasion techniques in a compromised environment
- When threat intel reports indicate process hollowing in active campaigns
- During purple team exercises validating T1055.012 detection coverage

## Prerequisites

- EDR with memory protection monitoring (CrowdStrike, MDE, SentinelOne)
- Sysmon with Event IDs 1 (Process Create), 8 (CreateRemoteThread), 25 (ProcessTampering)
- Windows ETW providers for process hollowing (Microsoft-Windows-Kernel-Process)
- Memory forensics capabilities (Volatility, WinDbg)
- Process integrity monitoring tools

## Workflow

1. **Define Detection Scope** — Identify the specific process hollowing technique techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for process hollowing technique.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting process hollowing technique indicators.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All process hollowing technique procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
