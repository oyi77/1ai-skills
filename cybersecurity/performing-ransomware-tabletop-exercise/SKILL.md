---
name: performing-ransomware-tabletop-exercise
description: Plans and facilitates tabletop exercises simulating ransomware incidents to test organizational readiness, decision-making,
  and communication procedures. Designs realistic scenarios based on current ransomware threat actors (LockBit, ALPHV/BlackCat,
  Cl0p), injects covering double extortion, backup destruction, and regulatory notification requirements. Evaluates participant
  responses against NIST CSF and CISA guidelines.
domain: cybersecurity
tags:
- ransomware
- incident-response
- tabletop-exercise
- defense
- preparedness
subdomain: ransomware-defense
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.DS-11
- RS.MA-01
- RC.RP-01
- PR.IR-01
---
# Performing Ransomware Tabletop Exercise

## When to Use

- Testing organizational ransomware response procedures annually or after major infrastructure changes
- Validating decision-making processes for ransom payment, regulatory notification, and public disclosure
- Training executives, IT, legal, PR, and operations teams on their roles during a ransomware incident
- Meeting cyber insurance policy requirements for documented incident response testing
- Identifying gaps in recovery playbooks, communication plans, and backup procedures

**Do not use** as a substitute for technical controls testing. Tabletop exercises validate procedures and decision-making, not technical detection or prevention capabilities.

## Prerequisites

- Documented incident response plan (IRP) that participants should have read before the exercise
- Identified exercise participants from: executive leadership, IT/security, legal, communications/PR, HR, operations, and external counsel
- Facilitator who is independent from the IR team (to provide objective evaluation)
- Ransomware scenario designed with injects that escalate over multiple rounds
- Evaluation criteria aligned to NIST CSF Respond/Recover functions
- Conference room or virtual meeting for 2-4 hours with no interruptions

## Workflow

1. **Plan Operations** — Define objectives, scope, and success criteria for ransomware tabletop exercise operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for ransomware tabletop exercise.
3. **Execute Core Workflow** — Perform the ransomware tabletop exercise operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All ransomware tabletop exercise procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
