---
name: detecting-t1055-process-injection-with-sysmon
description: Detect process injection techniques (T1055) including classic DLL injection, process hollowing, and APC injection
  by analyzing Sysmon events for cross-process memory operations, remote thread creation, and anomalous DLL loading patterns.
domain: cybersecurity
tags:
- threat-hunting
- process-injection
- sysmon
- mitre-t1055
- defense-evasion
- dll-injection
- process-hollowing
subdomain: threat-hunting
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- Executable Denylisting
- Execution Isolation
- File Metadata Consistency Validation
- Content Format Conversion
- File Content Analysis
nist_csf:
- DE.CM-01
- DE.AE-02
- DE.AE-07
- ID.RA-05
---
# Detecting T1055 Process Injection With Sysmon

## When to Use

- When hunting for defense evasion techniques that hide malicious code inside legitimate processes
- After EDR alerts for suspicious cross-process memory access or remote thread creation
- When investigating malware that injects into svchost.exe, explorer.exe, or other system processes
- During purple team exercises testing detection of process injection variants
- When validating Sysmon configuration coverage for injection detection

## Prerequisites

- Sysmon deployed with comprehensive configuration capturing Events 1, 7, 8, 10, 25
- Event ID 8 (CreateRemoteThread) enabled for remote thread detection
- Event ID 10 (ProcessAccess) configured with appropriate access mask filters
- Event ID 7 (ImageLoaded) for DLL injection detection
- Event ID 25 (ProcessTampering) for process hollowing on Sysmon 13+
- SIEM platform for correlation and alerting

## Workflow

1. **Define Detection Scope** — Identify the specific t1055 process injection techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for t1055 process injection.
3. **Build Detection Queries** — Write sysmon queries targeting t1055 process injection indicators. Use platform-specific query language for optimal performance.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **sysmon** — Primary tool for this skill
- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All t1055 process injection procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
