---
name: performing-soc-tabletop-exercise
description: 'Performs tabletop exercises for SOC teams simulating security incidents through discussion-based scenarios to
  test incident response procedures, communication workflows, and decision-making under pressure without impacting production
  systems. Use when organizations need to validate IR playbooks, train analysts, or meet compliance requirements for incident
  response testing.

  '
domain: cybersecurity
tags:
- soc
- tabletop
- exercise
- incident-response
- training
- nist
- playbook-validation
subdomain: soc-operations
mitre_attack:
- T1566
- T1486
- T1078
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- DE.CM-01
- DE.AE-02
- RS.MA-01
- DE.AE-06
---
# Performing Soc Tabletop Exercise

## When to Use

Use this skill when:
- Annual or semi-annual incident response testing is required (NIST, ISO 27001, PCI DSS compliance)
- New SOC analysts need exposure to major incident scenarios in a controlled environment
- Updated playbooks need validation before next real incident
- Cross-functional coordination (SOC, IT, Legal, PR, Executive) needs rehearsal
- Post-incident reviews reveal gaps requiring scenario-based training

**Do not use** as a replacement for technical purple team exercises — tabletop exercises test processes and decision-making, not technical detection capabilities.

## Prerequisites

- Exercise facilitator with incident response experience
- Participant list: SOC analysts (Tier 1-3), SOC manager, IT operations, Legal, HR, Communications
- Conference room or video call with screen sharing capability
- Printed or digital scenario injects with timed release schedule
- Evaluation scorecard for assessing participant responses
- Existing incident response plan and playbooks for reference during exercise

## Workflow

1. **Plan Operations** — Define objectives, scope, and success criteria for soc tabletop exercise operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for soc tabletop exercise.
3. **Execute Core Workflow** — Perform the soc tabletop exercise operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All soc tabletop exercise procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
