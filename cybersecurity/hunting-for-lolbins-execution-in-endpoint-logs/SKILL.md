---
name: hunting-for-lolbins-execution-in-endpoint-logs
description: Hunt for adversary abuse of Living Off the Land Binaries (LOLBins) by analyzing endpoint process creation logs
  for suspicious execution patterns of legitimate Windows system binaries used for malicious purposes.
domain: cybersecurity
tags:
- threat-hunting
- lolbins
- living-off-the-land
- endpoint-detection
- process-monitoring
- mitre-t1218
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
# Hunting For Lolbins Execution In Endpoint Logs

## When to Use

- When hunting for fileless attack techniques that abuse built-in Windows binaries
- After threat intelligence indicates LOLBin-based campaigns targeting your industry
- When investigating alerts for suspicious use of certutil, mshta, rundll32, or regsvr32
- During purple team exercises testing detection of defense evasion techniques
- When assessing endpoint detection coverage for MITRE ATT&CK T1218 sub-techniques

## Prerequisites

- Sysmon Event ID 1 (Process Creation) with full command-line logging
- Windows Security Event ID 4688 with command-line auditing enabled
- EDR telemetry with parent-child process relationships
- SIEM platform for query and correlation (Splunk, Elastic, Microsoft Sentinel)
- LOLBAS project reference (lolbas-project.github.io) for known abuse patterns

## Workflow

1. **Define Detection Scope** — Identify the specific  techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for .
3. **Build Detection Queries** — Write lolbins execution in endpoint logs queries targeting  indicators. Use platform-specific query language for optimal performance.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **lolbins execution in endpoint logs** — Primary tool for this skill
- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All  procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
