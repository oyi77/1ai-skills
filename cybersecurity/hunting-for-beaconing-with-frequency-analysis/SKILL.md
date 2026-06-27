---
name: hunting-for-beaconing-with-frequency-analysis
description: Identify command-and-control beaconing patterns in network traffic by applying statistical frequency analysis,
  jitter calculation, and coefficient of variation scoring to detect periodic callbacks from compromised endpoints.
domain: cybersecurity
tags:
- threat-hunting
- beaconing
- c2-detection
- frequency-analysis
- network-traffic
- RITA
- jitter-detection
- mitre-t1071
subdomain: threat-hunting
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- File Metadata Consistency Validation
- Certificate Analysis
- Application Protocol Command Analysis
- Content Format Conversion
- File Content Analysis
nist_csf:
- DE.CM-01
- DE.AE-02
- DE.AE-07
- ID.RA-05
---
# Hunting For Beaconing With Frequency Analysis

## When to Use

- When proactively searching for compromised endpoints calling back to C2 infrastructure
- After threat intelligence reports indicate active C2 frameworks targeting your sector
- When network logs show periodic outbound connections to unfamiliar destinations
- During purple team exercises validating C2 detection capabilities
- When investigating a potential breach and need to identify active C2 channels

## Prerequisites

- Network proxy/firewall logs with timestamps and destination data (minimum 24 hours)
- Zeek conn.log, dns.log, and ssl.log or equivalent NetFlow/IPFIX data
- SIEM platform with statistical analysis capability (Splunk, Elastic, Microsoft Sentinel)
- RITA (Real Intelligence Threat Analytics) or AC-Hunter for automated beacon analysis
- Threat intelligence feeds for domain/IP reputation enrichment

## Workflow

1. **Define Detection Scope** — Identify the specific  techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for .
3. **Build Detection Queries** — Write beaconing with frequency analysis queries targeting  indicators. Use platform-specific query language for optimal performance.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **beaconing with frequency analysis** — Primary tool for this skill
- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All  procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
