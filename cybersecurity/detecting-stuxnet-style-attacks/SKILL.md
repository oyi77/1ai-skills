---
name: detecting-stuxnet-style-attacks
description: 'This skill covers detecting sophisticated cyber-physical attacks that follow the Stuxnet attack pattern of modifying
  PLC logic while spoofing sensor readings to hide the manipulation from operators. It addresses PLC logic integrity monitoring,
  physics-based process anomaly detection, engineering workstation compromise indicators, USB-borne attack vectors, and multi-stage
  attack chain detection spanning IT-to-OT lateral movement through to process manipulation.

  '
domain: cybersecurity
tags:
- ot-security
- ics
- scada
- industrial-control
- iec62443
- stuxnet
- plc-integrity
- apt
subdomain: ot-ics-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- DE.CM-01
- ID.AM-05
- GV.OC-02
---
# Detecting Stuxnet Style Attacks

## When to Use

- When implementing advanced threat detection for high-value OT targets (nuclear, chemical, critical infrastructure)
- When building detection for APT-style attacks targeting PLC logic and process manipulation
- When establishing PLC logic integrity monitoring to detect unauthorized modifications
- When investigating suspected process anomalies that may indicate cyber-physical attacks
- When designing defense-in-depth strategies against nation-state level OT threats

**Do not use** for basic OT intrusion detection (see detecting-attacks-on-scada-systems), for malware analysis of Stuxnet samples (see malware reverse engineering skills), or for PLC programming and logic development.

## Prerequisites

- Detailed understanding of the Stuxnet attack chain and MITRE ATT&CK for ICS framework
- PLC logic backup repository with known-good baseline copies of all PLC programs
- Engineering workstation monitoring (EDR with OT awareness)
- Physics-based process models for the controlled physical process
- Network monitoring for industrial protocol traffic analysis

## Workflow

1. **Define Detection Scope** — Identify the specific stuxnet style attacks techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for stuxnet style attacks.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting stuxnet style attacks indicators.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All stuxnet style attacks procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
