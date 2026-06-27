---
name: detecting-attacks-on-scada-systems
description: 'This skill covers detecting cyber attacks targeting Supervisory Control and Data Acquisition (SCADA) systems
  including man-in-the-middle attacks on industrial protocols, unauthorized command injection into PLCs, HMI compromise, historian
  data manipulation, and denial-of-service against control system communications. It leverages OT-specific intrusion detection
  systems, industrial protocol anomaly detection, and process data analytics to identify attacks that traditional IT security
  tools miss.

  '
domain: cybersecurity
tags:
- ot-security
- ics
- scada
- industrial-control
- iec62443
- intrusion-detection
- threat-detection
subdomain: ot-ics-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_ai_rmf:
- MEASURE-2.7
- MAP-5.1
- MANAGE-2.4
atlas_techniques:
- AML.T0070
- AML.T0066
- AML.T0082
nist_csf:
- PR.IR-01
- DE.CM-01
- ID.AM-05
- GV.OC-02
---
# Detecting Attacks On Scada Systems

## When to Use

- When deploying intrusion detection capabilities in a SCADA environment for the first time
- When investigating suspected cyber attacks against industrial control systems
- When building detection rules for OT-specific attack patterns (Stuxnet, TRITON, Industroyer)
- When integrating OT network monitoring with an enterprise SOC for unified threat visibility
- When responding to alerts from OT security monitoring tools (Dragos, Nozomi, Claroty)

**Do not use** for detecting attacks on IT-only networks without SCADA/ICS components, for building generic network IDS rules (see building-detection-rules-with-sigma), or for incident response procedures after an attack is confirmed (see performing-ot-incident-response).

## Prerequisites

- Passive network monitoring sensors deployed on SPAN/TAP ports at OT network boundaries
- OT intrusion detection system (Dragos Platform, Nozomi Guardian, Claroty xDome, or Suricata with OT rulesets)
- Understanding of industrial protocols in use (Modbus, DNP3, OPC UA, EtherNet/IP, S7comm)
- Baseline of normal SCADA communication patterns (polling intervals, function codes, register ranges)
- Access to process historian data for physical process anomaly correlation

## Workflow

1. **Define Detection Scope** — Identify the specific attacks on scada systems techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for attacks on scada systems.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting attacks on scada systems indicators.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All attacks on scada systems procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
