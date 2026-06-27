---
name: automating-ioc-enrichment
description: Automates the enrichment of raw indicators of compromise with multi-source threat intelligence context using
  SOAR platforms, Python pipelines, or TIP playbooks to reduce analyst triage time and standardize enrichment outputs. Use
  when building automated enrichment workflows integrated with SIEM alerts, email submission pipelines, or bulk IOC processing
  from threat feeds.
domain: cybersecurity
tags:
- SOAR
- enrichment
- IOC
- Cortex-XSOAR
- Splunk-SOAR
- VirusTotal
- automation
- CTI
- NIST-CSF
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
# Automating Ioc Enrichment

## When to Use

Use this skill when:
- Building a SOAR playbook that automatically enriches SIEM alerts with threat intelligence context before routing to analysts
- Creating a Python pipeline for bulk IOC enrichment from phishing email submissions
- Reducing analyst mean time to triage (MTTT) by pre-populating alert context with VT, Shodan, and MISP data

**Do not use** this skill for fully automated blocking decisions without human review — enrichment automation should inform decisions, not execute blocks autonomously for high-impact actions.

## Prerequisites

- SOAR platform (Cortex XSOAR, Splunk SOAR, Tines, or n8n) or Python 3.9+ environment
- API keys: VirusTotal, AbuseIPDB, Shodan, and at minimum one TIP (MISP or OpenCTI)
- SIEM integration endpoint for alert consumption
- Rate limit budgets documented per API (VT: 4/min free, 500/min enterprise)

## Workflow

1. **Define Objectives** — Clarify the goals and scope for ioc enrichment.
2. **Gather Resources** — Collect tools, data, and access needed for ioc enrichment.
3. **Execute Process** — Carry out ioc enrichment operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All ioc enrichment procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
