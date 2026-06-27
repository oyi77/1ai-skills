---
name: triaging-security-incident-with-ir-playbook
description: Classify and prioritize security incidents using structured IR playbooks to determine severity, assign response
  teams, and initiate appropriate response procedures.
domain: cybersecurity
tags:
- incident-response
- triage
- playbook
- severity-classification
- soc
subdomain: incident-response
mitre_attack:
- T1190
- T1566
- T1078
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- RS.MA-01
- RS.MA-02
- RS.AN-03
- RC.RP-01
---
# Triaging Security Incident With Ir Playbook

## When to Use
- New security alert received from SIEM, EDR, or other detection sources
- SOC analyst needs to determine if an alert is a true positive requiring response
- Incident needs severity classification and team assignment
- Multiple concurrent incidents require prioritization
- Automated triage rules need validation or tuning

## Prerequisites
- SIEM platform with alert correlation (Splunk, Elastic, QRadar, Sentinel)
- Incident response playbook library (by incident type)
- Severity classification matrix approved by CISO
- On-call rotation and escalation procedures
- Ticketing system for incident tracking (ServiceNow, Jira, TheHive)
- Threat intelligence feeds for IOC enrichment

## Workflow

1. **Define Objectives** — Clarify the goals and scope for security incident.
2. **Gather Resources** — Collect tools, data, and access needed for security incident.
3. **Execute Process** — Carry out security incident operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **ir playbook** — Primary tool for this skill
- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All security incident procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
