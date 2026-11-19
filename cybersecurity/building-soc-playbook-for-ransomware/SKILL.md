---
name: building-soc-playbook-for-ransomware
description: 'Use when builds a structured SOC incident response playbook for ransomware
  attacks covering detection, containment, eradication, and recovery phases with specific
  SIEM queries, isolation procedures, and decision trees. Use when SOC teams need
  formalized response procedures for ransomware incidents aligned to NIST SP 800-61
  and MITRE ATT&CK ransomware techniques.

  '
domain: cybersecurity
tags:
- soc
- ransomware
- incident-response
- playbook
- nist
- mitre-attack
- containment
subdomain: soc-operations
mitre_attack:
- T1486
- T1490
- T1489
- T1570
version: '1.0'
author: oyi77
license: Apache-2.0
d3fend_techniques:
- Platform Hardening
- Restore Object
- Restore Configuration
- Restore Software
- Software Update
nist_csf:
- DE.CM-01
- DE.AE-02
- RS.MA-01
- DE.AE-06
category: cybersecurity
---

# Building Soc Playbook For Ransomware

## Overview

Cybersecurity skill for building soc playbook for ransomware. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "building soc playbook for ransomware"
- "SOC teams need a standardized ransomware response playbook for Tier 1-3 analysts"
- "An organization lacks documented procedures for ransomware containment and recov"
- "Tabletop exercises reveal gaps in ransomware response coordination"


Use this skill when:
- SOC teams need a standardized ransomware response playbook for Tier 1-3 analysts
- An organization lacks documented procedures for ransomware containment and recovery
- Tabletop exercises reveal gaps in ransomware response coordination
- Compliance requirements (NIST CSF, ISO 27001) mandate documented incident playbooks

**Do not use** during an active ransomware incident as the sole guide — have pre-built playbooks tested and rehearsed before incidents occur.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- SIEM platform (Splunk ES, Elastic Security, or Sentinel) with endpoint and network data
- EDR solution (CrowdStrike, SentinelOne, or Microsoft Defender for Endpoint) with network isolation capability
- Backup infrastructure with tested recovery procedures and offline/immutable backups
- Communication plan with legal, executive leadership, and external IR retainer contacts
- MITRE ATT&CK knowledge for ransomware technique chains

## Workflow

1. **Pre-authorize the playbook** — before an incident, define severity triggers, incident commander, legal/executive/communications contacts, external IR retainer, ransom-payment policy (owner is legal/executive, not SOC), backup restore ownership, and evidence-preservation rules.
2. **Detect and triage** — recognize indicators (mass file rename/extension change, shadow-copy deletion, backup deletion, EDR ransomware behavior, C2 beaconing). Assign severity and open an incident record with time, scope, and host list.
3. **Contain** — isolate affected hosts/segments via EDR/network controls, disable compromised accounts, block known IOCs, and protect backups. Do not power off hosts destructively; preserve memory/disk evidence per forensic guidance.
4. **Assess scope and persistence** — enumerate affected systems, accounts, and data; check for lateral movement and persistence; verify backup integrity and whether backups were also compromised.
5. **Eradicate** — remove ransomware artifacts and persistence, patch the initial-access vector, rotate all potentially exposed credentials, and validate clean state with scanning.
6. **Recover** — restore from verified clean backups in a controlled order, monitor closely after restore, and validate business-critical services before broad reconnection.
7. **Communicate** — follow the pre-approved escalation and disclosure obligations; keep legal/executive in the loop; do not negotiate or contact the attacker without explicit executive/legal authorization.
8. **Post-incident** — document timeline, root cause, blast radius, recovery evidence, lessons learned, and control improvements with owners and due dates.

## Tools

- **ransomware** — Primary tool for this skill
- **Configuration Management** — Infrastructure as code and automation
- **Monitoring Stack** — Observability and alerting
- **Documentation Platform** — Runbooks and architecture docs


## Process

1. **Design** — Define interface, identify patterns, plan implementation
1. **Implement** — Write code following existing conventions, add tests
1. **Verify** — Run tests, check integration, validate behavior

## Verification

- [ ] All soc playbook procedures executed completely and documented
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