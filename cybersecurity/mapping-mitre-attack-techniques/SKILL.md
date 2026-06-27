---
name: mapping-mitre-attack-techniques
description: 'Maps observed adversary behaviors, security alerts, and detection rules to MITRE ATT&CK techniques and sub-techniques
  to quantify detection coverage and guide control prioritization. Use when building an ATT&CK-based coverage heatmap, tagging
  SIEM alerts with technique IDs, aligning security controls to adversary playbooks, or reporting threat exposure to executives.
  Activates for requests involving ATT&CK Navigator, Sigma rules, MITRE D3FEND, or coverage gap analysis.

  '
domain: cybersecurity
tags:
- MITRE-ATT&CK
- ATT&CK-Navigator
- Sigma
- D3FEND
- TTP
- detection-engineering
- NIST-CSF
subdomain: threat-intelligence
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
d3fend_techniques:
- Executable Denylisting
- Execution Isolation
- File Metadata Consistency Validation
- Content Format Conversion
- File Content Analysis
nist_csf:
- ID.RA-01
- ID.RA-05
- DE.CM-01
- DE.AE-02
---
# Mapping Mitre Attack Techniques

## When to Use

Use this skill when:
- Generating an ATT&CK coverage heatmap to show which techniques your detection stack addresses
- Tagging existing SIEM use cases or Sigma rules with ATT&CK technique IDs for structured reporting
- Aligning your security program roadmap to specific adversary groups known to target your sector

**Do not use** this skill for real-time incident triage — ATT&CK mapping is an analytical activity best performed post-detection or during threat hunting planning.

## Prerequisites

- Access to MITRE ATT&CK knowledge base (https://attack.mitre.org) or local ATT&CK STIX data bundle
- ATT&CK Navigator web app or local installation (https://mitre-attack.github.io/attack-navigator/)
- Inventory of existing detection rules (Sigma, Splunk, Sentinel KQL) to assess current coverage
- ATT&CK Python library: `pip install mitreattack-python`

## Workflow

1. **Define Objectives** — Clarify the goals and scope for mitre attack techniques.
2. **Gather Resources** — Collect tools, data, and access needed for mitre attack techniques.
3. **Execute Process** — Carry out mitre attack techniques operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All mitre attack techniques procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
