---
name: detecting-t1003-credential-dumping-with-edr
description: Detect OS credential dumping techniques targeting LSASS memory, SAM database, NTDS.dit, and cached credentials
  using EDR telemetry, Sysmon process access monitoring, and Windows security event correlation.
domain: cybersecurity
tags:
- threat-hunting
- credential-dumping
- lsass
- mitre-t1003
- edr
- mimikatz
- ntds
- sam-database
subdomain: threat-hunting
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- Token Binding
- Execution Isolation
- File Metadata Consistency Validation
- Restore Access
- Application Protocol Command Analysis
nist_csf:
- DE.CM-01
- DE.AE-02
- DE.AE-07
- ID.RA-05
---
# Detecting T1003 Credential Dumping With Edr

## When to Use

- When hunting for credential theft activity in the environment
- After compromise indicators suggest attacker has elevated privileges
- When EDR alerts fire for LSASS access or suspicious process memory reads
- During incident response to determine scope of credential compromise
- When auditing LSASS protection controls (Credential Guard, RunAsPPL)

## Prerequisites

- EDR agent deployed with LSASS access monitoring (CrowdStrike, Defender for Endpoint, SentinelOne)
- Sysmon Event ID 10 (ProcessAccess) with LSASS-specific filters
- Windows Security Event ID 4656/4663 (Object Access Auditing)
- LSASS SACL auditing enabled (Windows 10+)
- Registry auditing for SAM hive access

## Workflow

1. **Define Detection Scope** — Identify the specific t1003 credential dumping techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for t1003 credential dumping.
3. **Build Detection Queries** — Write edr queries targeting t1003 credential dumping indicators. Use platform-specific query language for optimal performance.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **edr** — Primary tool for this skill
- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All t1003 credential dumping procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
