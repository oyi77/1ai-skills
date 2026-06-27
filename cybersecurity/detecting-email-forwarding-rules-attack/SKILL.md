---
name: detecting-email-forwarding-rules-attack
description: Detect malicious email forwarding rules created by adversaries to maintain persistent access to email communications
  for intelligence collection and BEC attacks.
domain: cybersecurity
tags:
- threat-hunting
- mitre-attack
- email-forwarding
- persistence
- bec
- t1114
- proactive-detection
subdomain: threat-hunting
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- Restore Object
- Restore Configuration
- Application Configuration Hardening
- Application Hardening
- Disable Remote Access
nist_csf:
- DE.CM-01
- DE.AE-02
- DE.AE-07
- ID.RA-05
---
# Detecting Email Forwarding Rules Attack

## When to Use

- When proactively hunting for indicators of detecting email forwarding rules attack in the environment
- After threat intelligence indicates active campaigns using these techniques
- During incident response to scope compromise related to these techniques
- When EDR or SIEM alerts trigger on related indicators
- During periodic security assessments and purple team exercises

## Prerequisites

- EDR platform with process and network telemetry (CrowdStrike, MDE, SentinelOne)
- SIEM with relevant log data ingested (Splunk, Elastic, Sentinel)
- Sysmon deployed with comprehensive configuration
- Windows Security Event Log forwarding enabled
- Threat intelligence feeds for IOC correlation

## Workflow

1. **Define Detection Scope** — Identify the specific email forwarding rules attack techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for email forwarding rules attack.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting email forwarding rules attack indicators.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All email forwarding rules attack procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
