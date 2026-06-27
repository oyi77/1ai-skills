---
name: analyzing-cyber-kill-chain
description: Analyzes intrusion activity against the Lockheed Martin Cyber Kill Chain framework to identify which phases an
  adversary has completed, where defenses succeeded or failed, and what controls would have interrupted the attack at earlier
  phases. Use when conducting post-incident analysis, building prevention-focused security controls, or mapping detection
  gaps to kill chain phases.
domain: cybersecurity
tags:
- kill-chain
- Lockheed-Martin
- MITRE-ATT&CK
- intrusion-analysis
- defense-in-depth
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
# Analyzing Cyber Kill Chain

## When to Use

Use this skill when:
- Conducting post-incident analysis to determine how far an adversary progressed through an attack sequence
- Designing layered defensive controls with the goal of interrupting attacks at the earliest possible phase
- Producing threat intelligence reports that communicate attack progression to non-technical stakeholders

**Do not use** this skill as a standalone framework — combine with MITRE ATT&CK for technique-level granularity beyond what the 7-phase kill chain provides.

## Prerequisites

- Complete incident timeline with forensic artifacts mapped to specific adversary actions
- MITRE ATT&CK Enterprise matrix for technique-level mapping within each kill chain phase
- Access to threat intelligence on the suspected adversary group's typical kill chain progression
- Post-incident report or IR timeline from responding team

## Workflow

1. **Scope the Analysis** — Define what cyber kill chain artifacts or data sources to examine and the investigation timeline.
2. **Preserve Evidence** — Create forensic copies of relevant data. Maintain chain of custody documentation.
3. **Extract Key Indicators** — Parse and extract relevant cyber kill chain data points from collected artifacts.
4. **Correlate Findings** — Cross-reference extracted data with other sources (threat intel, logs, timelines).
5. **Build Timeline** — Construct a chronological sequence of events related to cyber kill chain.
6. **Document Analysis** — Write findings report with evidence, conclusions, and recommendations.

## Tools

- **Forensic Toolkit** — Evidence collection and analysis
- **Timeline Tools** — Chronological event reconstruction
- **Log Analysis Platform** — Centralized log parsing and search

## Verification

- [ ] All cyber kill chain procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
