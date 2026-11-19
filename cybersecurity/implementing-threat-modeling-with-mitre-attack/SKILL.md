---
name: implementing-threat-modeling-with-mitre-attack
description: 'Use when implements threat modeling using the MITRE ATT&CK framework
  to map adversary TTPs against organizational assets, assess detection coverage gaps,
  and prioritize defensive investments. Use when SOC teams need to align detection
  engineering with threat landscape, conduct threat assessments for new environments,
  or justify security tool procurement.

  '
domain: cybersecurity
tags:
- soc
- mitre-attack
- threat-modeling
- ttp
- detection-coverage
- attack-navigator
- risk-assessment
subdomain: soc-operations
version: '1.0'
author: oyi77
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
- File Metadata Consistency Validation
- Application Protocol Command Analysis
- Identifier Analysis
- Content Format Conversion
- Message Analysis
nist_csf:
- DE.CM-01
- DE.AE-02
- RS.MA-01
- DE.AE-06
category: cybersecurity
---

# Implementing Threat Modeling With Mitre Attack

## Overview

Cybersecurity skill for implementing threat modeling with mitre attack. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "implementing threat modeling with mitre attack"
- "SOC teams need to assess detection coverage against relevant threat actors and t"
- "Security leadership requires threat-informed defense prioritization"
- "New environments (cloud migration, OT integration) need detection strategy plann"


Use this skill when:
- SOC teams need to assess detection coverage against relevant threat actors and their TTPs
- Security leadership requires threat-informed defense prioritization
- New environments (cloud migration, OT integration) need detection strategy planning
- Purple team exercises require structured adversary emulation based on threat models
- Annual risk assessments need ATT&CK-based threat landscape analysis

**Do not use** as a one-time exercise — threat models must be continuously updated as adversary TTPs evolve and organizational attack surface changes.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- MITRE ATT&CK framework knowledge (Enterprise, ICS, Mobile, or Cloud matrices)
- ATT&CK Navigator tool (web or local) for layer visualization
- Current detection rule inventory mapped to ATT&CK technique IDs
- Threat intelligence on adversary groups targeting your sector
- Organizational asset inventory with criticality classifications

## Workflow

1. **Scope the model** — pick one system/environment (Enterprise, Cloud, ICS, or Mobile matrix), its critical assets, trust boundaries, and data flows. A model without a named scope is unfalsifiable.
2. **Select adversary set** — choose threat actor groups or campaign patterns relevant to sector/geography from current intel; record source + date so staleness is visible.
3. **Map TTPs to the environment** — for each tactic (Initial Access → Exfiltration), list techniques that are actually reachable given this stack and identity/network topology. Do not paste the full matrix as “coverage”.
4. **Inventory existing detection** — map every implemented rule/alert to technique IDs in ATT&CK Navigator layers (one layer per environment). Techniques with no telemetry are gaps, not “covered by intuition”.
5. **Score residual risk** — rank uncovered techniques by likelihood × impact on scoped assets; use qualitative tiers with written rationale, not invented numeric scores.
6. **Prioritize investment** — link top uncovered techniques to concrete controls/log sources needed; feed procurement backlog with evidence, not fear.
7. **Version and review cadence** — store layers + assumptions in version control; re-run after major architecture change, new intel on an active actor, or quarterly at minimum.

### Output artifacts

- ATT&CK Navigator layer JSON per environment (detection coverage)
- Gap register: technique ID, missing telemetry, owning team, remediation ticket
- Assumption log: scope, actor set, data vintage, reviewer

Rollback: keep prior layer files; revert to previous commit if a re-map introduces regressions.

## Tools

- **mitre attack** — Primary tool for this skill
- **Configuration Management** — Infrastructure as code and automation
- **Monitoring Stack** — Observability and alerting
- **Documentation Platform** — Runbooks and architecture docs


## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- [ ] All threat modeling procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |