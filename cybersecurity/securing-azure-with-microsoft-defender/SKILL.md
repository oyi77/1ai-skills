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

## Overview

Cybersecurity skill for securing azure with microsoft defender. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "securing azure with microsoft defender"
- "This skill instructs security practitioners on deploying Microsoft Defender for "


- When deploying cloud workload protection across Azure subscriptions and resource groups
- When establishing a Secure Score baseline and prioritizing security recommendations
- When extending threat protection to multi-cloud environments including AWS and GCP
- When enabling container security for AKS clusters and Azure Container Registry
- When integrating AI workload security with the Data and AI security dashboard

**Do not use** for AWS-only environments (see implementing-aws-security-hub), for identity provider configuration (see managing-cloud-identity-with-okta), or for network-level firewall rule management (see implementing-cloud-waf-rules).


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Azure subscription with Security Admin or Contributor role
- Azure Policy initiative for Defender for Cloud enabled at the management group level
- Log Analytics workspace provisioned for security data collection
- Microsoft Defender for Cloud plans licensed (P1 or P2 for server protection)

## Workflow

```python
# Example: IOC detection
import re

IOC_PATTERNS = {
    "ip": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "domain": r"\b[a-z0-9-]+\.[a-z]{2,}\b",
    "hash_md5": r"\b[a-f0-9]{32}\b",
    "hash_sha256": r"\b[a-f0-9]{64}\b",
}

def extract_iocs(text: str) -> dict:
    return {k: re.findall(v, text) for k, v in IOC_PATTERNS.items()}
```

1. **Define Objectives** — Clarify the goals and scope for azure.
2. **Gather Resources** — Collect tools, data, and access needed for azure.
3. **Execute Process** — Carry out azure operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **microsoft defender** — Primary tool for this skill
- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run securing azure with microsoft defender workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All azure procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |