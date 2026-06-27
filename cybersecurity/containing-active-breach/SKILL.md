---
name: containing-active-breach
description: 'Executes containment strategies to stop active adversary operations and prevent lateral movement during a confirmed
  security breach. Implements short-term and long-term containment using network segmentation, endpoint isolation, credential
  revocation, and access control modifications. Activates for requests involving breach containment, lateral movement prevention,
  network isolation, active threat containment, or live incident response.

  '
domain: cybersecurity
tags:
- breach-containment
- lateral-movement
- network-isolation
- credential-revocation
- live-response
subdomain: incident-response
mitre_attack:
- T1021
- T1570
- T1210
- T1072
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- RS.MA-01
- RS.MA-02
- RS.AN-03
- RC.RP-01
---
# Containing Active Breach

## When to Use

- A confirmed intrusion is in progress with an active adversary on the network
- Malware is spreading laterally across endpoints or servers
- A compromised account is being used for unauthorized access to systems
- Ransomware encryption has been detected and is actively propagating
- An attacker has established command-and-control communications from internal hosts

**Do not use** for post-incident cleanup when the adversary is no longer active; use eradication procedures instead.

## Prerequisites

- Confirmed incident classification with P1 or P2 severity from triage
- EDR console access with host isolation capabilities (CrowdStrike Falcon, Microsoft Defender for Endpoint, SentinelOne)
- Network firewall and switch management access for segmentation
- Active Directory or identity provider administrative access for credential actions
- Pre-approved containment authority documented in the incident response plan
- Evidence preservation plan to avoid destroying forensic artifacts during containment

## Workflow

1. **Define Objectives** — Clarify the goals and scope for active breach.
2. **Gather Resources** — Collect tools, data, and access needed for active breach.
3. **Execute Process** — Carry out active breach operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All active breach procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
