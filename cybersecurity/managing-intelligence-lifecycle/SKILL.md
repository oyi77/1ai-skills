---
name: managing-intelligence-lifecycle
description: Manages the end-to-end cyber threat intelligence lifecycle from planning and direction through collection, processing,
  analysis, dissemination, and feedback to ensure intelligence products meet stakeholder requirements and continuously improve.
  Use when establishing or maturing a CTI program, defining intelligence requirements with business stakeholders, or building
  feedback loops between intelligence consumers and producers.
domain: cybersecurity
tags:
- CTI
- intelligence-lifecycle
- PIR
- NIST-SP-800-150
- threat-intelligence-program
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
# Managing Intelligence Lifecycle

## When to Use

Use this skill when:
- Establishing a formal CTI program and defining its operational model
- Conducting quarterly intelligence requirements reviews with business stakeholders
- Evaluating CTI program maturity against established frameworks (FIRST CTI-SIG maturity model)

**Do not use** this skill for day-to-day IOC triage or incident-specific intelligence tasks — those use operational intelligence workflows, not lifecycle management.

## Prerequisites

- Executive sponsorship and defined CTI team structure (1+ dedicated analysts)
- Stakeholder map identifying intelligence consumers (SOC, IR, executive team, vulnerability management)
- Existing feed subscriptions or ISAC memberships for collection baseline
- CTI platform (MISP, ThreatConnect, OpenCTI) for lifecycle management

## Workflow

1. **Define Objectives** — Clarify the goals and scope for intelligence lifecycle.
2. **Gather Resources** — Collect tools, data, and access needed for intelligence lifecycle.
3. **Execute Process** — Carry out intelligence lifecycle operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All intelligence lifecycle procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
