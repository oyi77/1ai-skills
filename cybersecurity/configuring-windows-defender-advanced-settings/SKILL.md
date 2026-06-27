---
name: configuring-windows-defender-advanced-settings
description: 'Configures Microsoft Defender for Endpoint (MDE) advanced protection settings including attack surface reduction
  rules, controlled folder access, network protection, and exploit protection. Use when hardening Windows endpoints beyond
  default Defender settings, deploying enterprise-grade endpoint protection, or meeting compliance requirements for advanced
  malware defense. Activates for requests involving Windows Defender configuration, ASR rules, MDE tuning, or Microsoft endpoint
  security.

  '
domain: cybersecurity
tags:
- endpoint
- windows-security
- Microsoft-Defender
- ASR
- exploit-protection
- MDE
subdomain: endpoint-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- PR.PS-02
- DE.CM-01
- PR.IR-01
---
# Configuring Windows Defender Advanced Settings

## When to Use

Use this skill when:
- Configuring Microsoft Defender for Endpoint (MDE) beyond default settings for enhanced protection
- Implementing Attack Surface Reduction (ASR) rules to block common attack techniques
- Enabling controlled folder access for ransomware protection
- Configuring network protection and exploit protection features
- Deploying Defender settings via Intune, SCCM, or Group Policy at enterprise scale

**Do not use** this skill for third-party EDR deployment (CrowdStrike, SentinelOne) or for Microsoft Defender for Cloud (Azure workload protection).

## Prerequisites

- Windows 10/11 Enterprise with Microsoft Defender Antivirus enabled
- Microsoft 365 E5 or Microsoft Defender for Endpoint Plan 2 license (for full MDE features)
- Microsoft Intune or SCCM for enterprise policy deployment
- Microsoft 365 Defender portal access (security.microsoft.com)
- Endpoints not running third-party AV in active mode (Defender enters passive mode)

## Workflow

1. **Define Objectives** — Clarify the goals and scope for windows defender advanced settings.
2. **Gather Resources** — Collect tools, data, and access needed for windows defender advanced settings.
3. **Execute Process** — Carry out windows defender advanced settings operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All windows defender advanced settings procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
