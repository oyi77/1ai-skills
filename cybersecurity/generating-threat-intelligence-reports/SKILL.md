---
name: generating-threat-intelligence-reports
description: Generates structured cyber threat intelligence reports at strategic, operational, and tactical levels tailored
  to specific audiences including executives, security operations teams, and technical analysts. Use when producing finished
  intelligence products from raw collection data, creating sector threat briefings, or delivering post-incident intelligence
  assessments.
domain: cybersecurity
tags:
- CTI
- threat-intelligence
- intelligence-products
- TLP
- PIR
- report-writing
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
# Generating Threat Intelligence Reports

## When to Use

Use this skill when:
- Producing weekly, monthly, or quarterly threat intelligence summaries for security leadership
- Creating a rapid intelligence assessment in response to a breaking threat (e.g., new zero-day, active ransomware campaign)
- Generating sector-specific threat briefings for executive decision-making on security investments

**Do not use** this skill for raw IOC distribution — use TIP/MISP for automated IOC sharing and reserve report generation for analyzed, finished intelligence.

## Prerequisites

- Completed analysis from collection and processing phase (PIRs partially or fully answered)
- Audience profile: technical level, decision-making authority, information classification clearance
- TLP classification decision for the product
- Organization-specific reporting template aligned to audience expectations

## Workflow

1. **Define Objectives** — Clarify the goals and scope for threat intelligence reports.
2. **Gather Resources** — Collect tools, data, and access needed for threat intelligence reports.
3. **Execute Process** — Carry out threat intelligence reports operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All threat intelligence reports procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
