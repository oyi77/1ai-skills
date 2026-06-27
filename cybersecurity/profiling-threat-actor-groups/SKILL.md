---
name: profiling-threat-actor-groups
description: Develops comprehensive threat actor profiles for APT groups, criminal organizations, and hacktivist collectives
  by aggregating TTP documentation, historical campaign data, tooling fingerprints, and attribution indicators from multiple
  intelligence sources. Use when briefing executives on sector-specific threats, updating threat model assumptions, or prioritizing
  defensive controls against specific adversaries.
domain: cybersecurity
tags:
- MITRE-ATT&CK
- threat-actor
- APT
- CrowdStrike
- Mandiant
- attribution
- kill-chain
- NIST-CSF
subdomain: threat-intelligence
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- ID.RA-01
- ID.RA-05
- DE.CM-01
- DE.AE-02
---
# Profiling Threat Actor Groups

## When to Use

Use this skill when:
- Updating the organization's threat model with profiles of adversary groups recently observed targeting your sector
- Preparing an executive briefing on APT groups that align with geopolitical events affecting your business
- Enabling SOC analysts to understand attacker objectives and TTPs to improve detection tuning

**Do not use** this skill for real-time incident attribution — attribution during active incidents should be deprioritized in favor of containment. Profile refinement occurs post-incident.

## Prerequisites

- Access to MITRE ATT&CK Groups database (https://attack.mitre.org/groups/)
- Commercial threat intelligence subscription (Mandiant Advantage, CrowdStrike Falcon Intelligence, or Recorded Future)
- Sector-specific ISAC membership for targeted intelligence (FS-ISAC, H-ISAC, E-ISAC)
- Structured profile template (see workflow below)

## Workflow

1. **Define Objectives** — Clarify the goals and scope for threat actor groups.
2. **Gather Resources** — Collect tools, data, and access needed for threat actor groups.
3. **Execute Process** — Carry out threat actor groups operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All threat actor groups procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
