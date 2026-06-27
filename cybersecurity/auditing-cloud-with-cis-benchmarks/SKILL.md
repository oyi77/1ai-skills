---
name: auditing-cloud-with-cis-benchmarks
description: 'This skill details how to conduct cloud security audits using Center for Internet Security benchmarks for AWS,
  Azure, and GCP. It covers interpreting CIS Foundations Benchmark controls, running automated assessments with tools like
  Prowler and ScoutSuite, remediating failed controls, and maintaining continuous compliance monitoring against CIS v5 for
  AWS, v4 for Azure, and v4 for GCP.

  '
domain: cybersecurity
tags:
- cis-benchmarks
- cloud-audit
- compliance-assessment
- prowler
- security-hardening
subdomain: cloud-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_ai_rmf:
- GOVERN-1.1
- GOVERN-4.2
- MAP-2.3
nist_csf:
- PR.IR-01
- ID.AM-08
- GV.SC-06
- DE.CM-01
---
# Auditing Cloud With Cis Benchmarks

## When to Use

- When performing initial security audits of cloud environments against industry-standard benchmarks
- When preparing for SOC 2, ISO 27001, or regulatory audits that reference CIS controls
- When establishing a measurable security baseline for new cloud accounts or subscriptions
- When tracking compliance improvement over time with periodic reassessment
- When evaluating the security posture of acquired or inherited cloud environments

**Do not use** for runtime threat detection (see detecting-cloud-threats-with-guardduty), for application-level security testing (see conducting-cloud-penetration-testing), or for compliance frameworks not based on CIS (refer to specific regulatory skill files).

## Prerequisites

- Read-only access to target cloud accounts (AWS SecurityAudit policy, Azure Reader role, GCP Viewer role)
- Prowler, ScoutSuite, or cloud-native CSPM tools installed and configured
- Understanding of CIS benchmark structure: sections, controls, profiles (Level 1 and Level 2)
- Remediation access for implementing fixes (separate from audit credentials)

## Workflow

1. **Define Objectives** — Clarify the goals and scope for cloud.
2. **Gather Resources** — Collect tools, data, and access needed for cloud.
3. **Execute Process** — Carry out cloud operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **cis benchmarks** — Primary tool for this skill
- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All cloud procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
