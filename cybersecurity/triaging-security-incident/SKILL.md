---
name: triaging-security-incident
description: 'Performs initial triage of security incidents to determine severity, scope, and required response actions using
  the NIST SP 800-61r3 and SANS PICERL frameworks. Classifies incidents by type, assigns priority based on business impact,
  and routes to appropriate response teams. Activates for requests involving incident triage, security alert classification,
  severity assessment, incident prioritization, or initial incident analysis.

  '
domain: cybersecurity
tags:
- incident-triage
- NIST-800-61
- SANS-PICERL
- severity-classification
- SOC-operations
subdomain: incident-response
mitre_attack:
- T1190
- T1566
- T1078
- T1059
version: 1.0.0
author: mahipal
license: Apache-2.0
d3fend_techniques:
- Executable Denylisting
- Execution Isolation
- File Metadata Consistency Validation
- Content Format Conversion
- File Content Analysis
nist_csf:
- RS.MA-01
- RS.MA-02
- RS.AN-03
- RC.RP-01
---
# Triaging Security Incident

## When to Use

- A SIEM or EDR alert fires and requires human classification before escalation
- Multiple concurrent alerts arrive and the SOC must prioritize response order
- An end user reports suspicious activity and the incident needs initial categorization
- A threat intelligence feed matches an IOC observed in the environment

**Do not use** for routine vulnerability scanning results or compliance audit findings that do not represent active security incidents.

## Prerequisites

- Access to SIEM platform (Splunk, Elastic, Microsoft Sentinel) with current alert data
- Incident classification taxonomy aligned to NIST SP 800-61r3 categories
- Predefined severity matrix mapping asset criticality to threat type
- Contact roster for escalation paths (Tier 1 through Tier 3 and CIRT)
- Asset inventory with business criticality ratings

## Workflow

1. **Define Objectives** — Clarify the goals and scope for security incident.
2. **Gather Resources** — Collect tools, data, and access needed for security incident.
3. **Execute Process** — Carry out security incident operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All security incident procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
