---
name: detecting-evasion-techniques-in-endpoint-logs
description: 'Detects defense evasion techniques used by adversaries in endpoint logs including log tampering, timestomping,
  process injection, and security tool disabling. Use when investigating suspicious endpoint behavior, building detection
  rules for evasion tactics, or conducting threat hunting for stealthy adversary activity. Activates for requests involving
  evasion detection, defense evasion analysis, log tampering detection, or MITRE ATT&CK TA0005.

  '
domain: cybersecurity
tags:
- endpoint
- edr
- threat-hunting
- defense-evasion
- MITRE-ATT&CK
- detection-engineering
subdomain: endpoint-security
version: 1.0.0
author: mahipal
license: Apache-2.0
d3fend_techniques:
- File Metadata Consistency Validation
- Content Format Conversion
- File Content Analysis
- Platform Hardening
- File Format Verification
nist_csf:
- PR.PS-01
- PR.PS-02
- DE.CM-01
- PR.IR-01
---
# Detecting Evasion Techniques In Endpoint Logs

## When to Use

Use this skill when:
- Hunting for adversary defense evasion techniques (MITRE ATT&CK TA0005) in endpoint telemetry
- Building detection rules for common evasion methods (process injection, timestomping, log clearing)
- Investigating incidents where adversaries disabled or bypassed security tools
- Analyzing endpoint logs for indicators of living-off-the-land binary (LOLBin) abuse

**Do not use** this skill for network-level evasion (use network traffic analysis) or for malware reverse engineering.

## Prerequisites

- Sysmon installed and configured with comprehensive logging rules (SwiftOnSecurity or Olaf Hartong config)
- Windows Security Event Log with advanced audit policy enabled
- EDR telemetry (CrowdStrike, SentinelOne, Microsoft Defender for Endpoint)
- SIEM platform for log correlation (Splunk, Elastic, Sentinel)
- MITRE ATT&CK Enterprise matrix for technique reference

## Workflow

1. **Define Detection Scope** — Identify the specific evasion techniques in endpoint logs techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for evasion techniques in endpoint logs.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting evasion techniques in endpoint logs indicators.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All evasion techniques in endpoint logs procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
