---
name: investigating-insider-threat-indicators
description: 'Investigates insider threat indicators including data exfiltration attempts, unauthorized access patterns, policy
  violations, and pre-departure behaviors using SIEM analytics, DLP alerts, and HR data correlation. Use when SOC teams receive
  insider threat referrals from HR, detect anomalous data movement by employees, or need to build investigation timelines
  for potential insider threats.

  '
domain: cybersecurity
tags:
- soc
- insider-threat
- data-exfiltration
- dlp
- ueba
- investigation
- hr-correlation
subdomain: soc-operations
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- DE.CM-01
- DE.AE-02
- RS.MA-01
- DE.AE-06
---
# Investigating Insider Threat Indicators

## When to Use

Use this skill when:
- HR refers a departing employee for monitoring during their notice period
- DLP alerts indicate bulk data downloads or transfers to personal storage
- UEBA detects anomalous access patterns deviating significantly from peer baselines
- Management reports concerns about an employee accessing sensitive data outside their role

**Do not use** without proper legal authorization — insider threat investigations must be coordinated with HR, Legal, and Privacy teams before monitoring begins.

## Prerequisites

- Legal authorization and HR referral documenting investigation justification
- SIEM with DLP, endpoint, email, proxy, and authentication log sources
- Data Loss Prevention (DLP) system (Microsoft Purview, Symantec, Forcepoint) with policy alerts
- Endpoint monitoring capability (EDR with USB/removable media logging)
- HR data feed providing employment status, notice dates, and access entitlements
- Chain of custody procedures for evidence preservation

## Workflow

1. **Define Objectives** — Clarify the goals and scope for insider threat indicators.
2. **Gather Resources** — Collect tools, data, and access needed for insider threat indicators.
3. **Execute Process** — Carry out insider threat indicators operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All insider threat indicators procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
