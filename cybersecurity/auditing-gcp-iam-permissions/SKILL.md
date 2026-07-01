---
name: auditing-gcp-iam-permissions
description: 'Auditing Google Cloud Platform IAM permissions to identify overly permissive bindings, primitive role usage,
  service account key proliferation, and cross-project access risks using gcloud CLI, Policy Analyzer, and IAM Recommender.

  '. Use when working with auditing gcp iam permissions.
domain: cybersecurity
tags:
- cloud-security
- gcp
- iam
- permissions-audit
- service-accounts
- policy-analyzer
subdomain: cloud-security
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- ID.AM-08
- GV.SC-06
- DE.CM-01
---
# Auditing Gcp Iam Permissions

## Overview

Cybersecurity skill for auditing gcp iam permissions. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "auditing gcp iam permissions"
- "Auditing Google Cloud Platform IAM permissions to identify overly permissive bin"


- When performing security assessments of GCP organization or project IAM configurations
- When identifying service accounts with excessive permissions or unused access
- When compliance requirements mandate review of access controls and role assignments
- When investigating potential lateral movement through IAM misconfigurations
- When reducing the blast radius of compromised credentials by scoping down permissions

**Do not use** for VPC firewall rule auditing (use network security tools), for GKE RBAC auditing (use Kubernetes-specific RBAC tools), or for real-time threat detection on IAM actions (use SCC Event Threat Detection).


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- GCP organization or project with `roles/iam.securityReviewer` and `roles/cloudAsset.viewer`
- gcloud CLI authenticated with appropriate permissions
- Cloud Asset API enabled (`gcloud services enable cloudasset.googleapis.com`)
- IAM Recommender API enabled (`gcloud services enable recommender.googleapis.com`)
- Policy Analyzer API enabled (`gcloud services enable policyanalyzer.googleapis.com`)

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

1. **Define Objectives** — Clarify the goals and scope for gcp iam permissions.
2. **Gather Resources** — Collect tools, data, and access needed for gcp iam permissions.
3. **Execute Process** — Carry out gcp iam permissions operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run auditing gcp iam permissions workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All gcp iam permissions procedures executed completely and documented
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