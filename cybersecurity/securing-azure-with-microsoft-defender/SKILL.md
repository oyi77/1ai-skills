---
name: securing-azure-with-microsoft-defender
description: 'This skill instructs security practitioners on deploying Microsoft Defender for Cloud as a cloud-native application
  protection platform for Azure, multi-cloud, and hybrid environments. It covers enabling Defender plans for servers, containers,
  storage, and databases, configuring security recommendations, managing Secure Score, and integrating with the unified Defender
  portal for centralized threat management.

  '
domain: cybersecurity
tags:
- microsoft-defender
- azure-security
- cnapp
- secure-score
- cloud-workload-protection
subdomain: cloud-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_ai_rmf:
- MEASURE-2.7
- MAP-5.1
- MANAGE-2.4
atlas_techniques:
- AML.T0070
- AML.T0066
- AML.T0082
nist_csf:
- PR.IR-01
- ID.AM-08
- GV.SC-06
- DE.CM-01
---
# Securing Azure With Microsoft Defender

## When to Use

- When deploying cloud workload protection across Azure subscriptions and resource groups
- When establishing a Secure Score baseline and prioritizing security recommendations
- When extending threat protection to multi-cloud environments including AWS and GCP
- When enabling container security for AKS clusters and Azure Container Registry
- When integrating AI workload security with the Data and AI security dashboard

**Do not use** for AWS-only environments (see implementing-aws-security-hub), for identity provider configuration (see managing-cloud-identity-with-okta), or for network-level firewall rule management (see implementing-cloud-waf-rules).

## Prerequisites

- Azure subscription with Security Admin or Contributor role
- Azure Policy initiative for Defender for Cloud enabled at the management group level
- Log Analytics workspace provisioned for security data collection
- Microsoft Defender for Cloud plans licensed (P1 or P2 for server protection)

## Workflow

1. **Define Objectives** — Clarify the goals and scope for azure.
2. **Gather Resources** — Collect tools, data, and access needed for azure.
3. **Execute Process** — Carry out azure operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **microsoft defender** — Primary tool for this skill
- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All azure procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
