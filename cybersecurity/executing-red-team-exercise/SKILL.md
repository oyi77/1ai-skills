---
name: executing-red-team-exercise
description: Executes comprehensive red team exercises that simulate real-world adversary operations against an organization's
  people, processes, and technology. The red team operates with stealth as a primary objective, employing the full attack
  lifecycle from initial reconnaissance through objective completion while testing the organization's detection and response
  capabilities. This differs from penetration testing by focusing on adversary emulation rather than vulnerability identification.
domain: cybersecurity
tags:
- red-team
- adversary-emulation
- MITRE-ATT&CK
- Cobalt-Strike
- detection-assessment
subdomain: penetration-testing
version: 1.0.0
author: mahipal
license: Apache-2.0
d3fend_techniques:
- File Metadata Consistency Validation
- Application Protocol Command Analysis
- Identifier Analysis
- Content Format Conversion
- Message Analysis
nist_csf:
- ID.RA-01
- ID.RA-06
- GV.OV-02
- DE.AE-07
---
# Executing Red Team Exercise

## When to Use

- Assessing an organization's ability to detect, respond to, and contain a realistic adversary operation
- Testing the effectiveness of the security operations center (SOC), incident response team, and threat hunting capabilities
- Validating security investments by simulating attacks that chain multiple vulnerabilities and techniques
- Evaluating the organization's security posture against specific threat actors (nation-state, ransomware groups, insider threats)
- Meeting regulatory requirements for adversary simulation (TIBER-EU, CBEST, AASE, iCAST)

**Do not use** without executive-level authorization and a detailed Rules of Engagement document, against systems where disruption could affect safety or critical operations, or as a replacement for basic vulnerability management (fix known vulnerabilities first).

## Prerequisites

- Executive-level written authorization with clearly defined objectives, scope, and off-limits systems
- Red team command and control (C2) infrastructure: primary and backup C2 channels with domain fronting or redirectors
- Operator workstations with OPSEC-hardened toolsets (Cobalt Strike, Sliver, Brute Ratel, or Mythic)
- Threat intelligence on adversary groups relevant to the target organization for adversary emulation planning
- Trusted agent (white cell) within the target organization who manages the exercise boundaries without alerting defenders
- MITRE ATT&CK matrix for mapping planned and executed techniques


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## Workflow

1. **Define Objectives** — Clarify the goals and scope for red team exercise.
2. **Gather Resources** — Collect tools, data, and access needed for red team exercise.
3. **Execute Process** — Carry out red team exercise operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All red team exercise procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
