---
name: collecting-indicators-of-compromise
description: 'Systematically collects, categorizes, and distributes indicators of compromise (IOCs) during and after security
  incidents to enable detection, blocking, and threat intelligence sharing. Covers network, host, email, and behavioral indicators
  using STIX/TAXII formats and threat intelligence platforms. Activates for requests involving IOC collection, indicator extraction,
  threat indicator sharing, compromise indicators, STIX export, or IOC enrichment.

  '
domain: cybersecurity
tags:
- IOC-collection
- threat-indicators
- STIX-TAXII
- MISP
- threat-intelligence-sharing
subdomain: incident-response
mitre_attack:
- T1071
- T1059
- T1547
- T1053
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- RS.MA-01
- RS.MA-02
- RS.AN-03
- RC.RP-01
---
# Collecting Indicators Of Compromise

## When to Use

- During active incident response to identify and block adversary infrastructure
- Post-incident to document all observed adversary artifacts for future detection
- When sharing threat intelligence with ISACs, sector partners, or law enforcement
- When building detection rules in SIEM, EDR, or network security tools
- When enriching IOCs with threat intelligence context for risk scoring

**Do not use** for behavioral TTP analysis without accompanying technical indicators; use MITRE ATT&CK mapping for behavioral characterization.

## Prerequisites

- Access to incident evidence sources: SIEM logs, EDR telemetry, memory dumps, disk images, network captures
- Threat intelligence platform (MISP, OpenCTI, ThreatConnect) for IOC management and sharing
- IOC enrichment tools: VirusTotal, OTX (AlienVault Open Threat Exchange), Shodan, DomainTools
- STIX 2.1 knowledge for structured IOC representation
- Sharing agreements with relevant ISACs (FS-ISAC, H-ISAC, IT-ISAC) or sector partners

## Workflow

1. **Define Objectives** — Clarify the goals and scope for indicators of compromise.
2. **Gather Resources** — Collect tools, data, and access needed for indicators of compromise.
3. **Execute Process** — Carry out indicators of compromise operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All indicators of compromise procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
