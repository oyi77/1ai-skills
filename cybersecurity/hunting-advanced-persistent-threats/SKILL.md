---
name: hunting-advanced-persistent-threats
description: 'Proactively hunts for Advanced Persistent Threat (APT) activity within enterprise environments using hypothesis-driven
  searches across endpoint telemetry, network logs, and memory artifacts. Use when conducting scheduled threat hunting cycles,
  investigating anomalous behavior flagged by UEBA, or validating that known APT TTPs are not present in the environment.
  Activates for requests involving MITRE ATT&CK, Velociraptor, osquery, Zeek, or threat hunting playbooks.

  '
domain: cybersecurity
tags:
- MITRE-ATT&CK
- threat-hunting
- APT
- Velociraptor
- osquery
- Zeek
- TTP
- NIST-CSF
- EDR
subdomain: threat-intelligence
version: 1.0.0
author: mahipal
license: Apache-2.0
d3fend_techniques:
- File Metadata Consistency Validation
- Application Protocol Command Analysis
- Identifier Analysis
- Content Format Conversion
- Message Analysis
nist_csf:
- ID.RA-01
- ID.RA-05
- DE.CM-01
- DE.AE-02
---
# Hunting Advanced Persistent Threats

## When to Use

Use this skill when:
- Conducting proactive threat hunting sprints (typically 2–4 week cycles) based on newly published APT intelligence
- A UEBA alert or anomaly detection system flags behavioral deviations warranting deeper investigation
- A peer organization or ISAC sharing partner reports active APT compromise and you need to validate your own exposure

**Do not use** this skill as a substitute for incident response when a confirmed breach is in progress — escalate to IR procedures (NIST SP 800-61).

## Prerequisites

- EDR platform with telemetry retention (CrowdStrike Falcon, Microsoft Defender for Endpoint, or SentinelOne) covering 30+ days
- Access to MITRE ATT&CK Navigator for hypothesis development
- Network flow data (NetFlow, Zeek, or Suricata logs) in a queryable SIEM
- Threat hunting platform or query interface (Velociraptor, osquery fleet, or Splunk ES)

## Workflow

1. **Define Detection Scope** — Identify the specific advanced persistent threats techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for advanced persistent threats.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting advanced persistent threats indicators.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All advanced persistent threats procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
