---
name: correlating-threat-campaigns
description: Correlates disparate security incidents, IOCs, and adversary behaviors across time and organizations to identify
  unified threat campaigns, attribute them to common threat actors, and extract shared indicators for improved detection.
  Use when multiple incidents exhibit overlapping indicators, when sector-wide attack campaigns require cross-organizational
  analysis, or when building campaign-level intelligence products.
domain: cybersecurity
tags:
- campaign-analysis
- correlation
- MISP
- ATT&CK
- threat-actor
- intrusion-set
- clustering
- CTI
subdomain: threat-intelligence
version: 1.0.0
author: team-cybersecurity
license: Apache-2.0
nist_csf:
- ID.RA-01
- ID.RA-05
- DE.CM-01
- DE.AE-02
---
# Correlating Threat Campaigns

## When to Use

Use this skill when:
- Multiple unrelated-appearing incidents share IOCs (same C2 IP, same malware hash, similar TTPs)
- An ISAC partner shares indicators from an incident that match your own historical events
- Building a campaign report linking adversary activity over weeks or months to a single operation

**Do not use** this skill to force correlation based on weak signals — false campaign attribution misleads defenders and wastes resources on incorrect threat models.

## Prerequisites

- TIP or SIEM with historical indicator and event data (90+ days recommended)
- MISP correlation engine enabled with event sharing configured
- Graph analysis tool (Maltego, Neo4j, or OpenCTI) for relationship visualization
- Reference to MITRE ATT&CK intrusion set and campaign objects for structuring output

## Workflow

1. **Define Objectives** — Clarify the goals and scope for threat campaigns.
2. **Gather Resources** — Collect tools, data, and access needed for threat campaigns.
3. **Execute Process** — Carry out threat campaigns operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All threat campaigns procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
