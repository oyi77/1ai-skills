---
name: auditing-kubernetes-cluster-rbac
description: 'Auditing Kubernetes cluster RBAC configurations to identify overly permissive roles, wildcard permissions, dangerous
  ClusterRoleBindings, service account abuse, and privilege escalation paths using kubectl, rbac-tool, KubiScan, and Kubeaudit.

  '
domain: cybersecurity
tags:
- cloud-security
- kubernetes
- rbac
- access-control
- eks
- gke
- aks
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
# Auditing Kubernetes Cluster Rbac

## Overview

Cybersecurity skill for auditing kubernetes cluster rbac. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "auditing kubernetes cluster rbac"
- "Auditing Kubernetes cluster RBAC configurations to identify overly permissive ro"


- When performing security assessments of Kubernetes clusters (EKS, GKE, AKS, or self-managed)
- When validating that RBAC policies enforce least privilege for users and service accounts
- When investigating potential lateral movement or privilege escalation within a Kubernetes cluster
- When compliance audits require documentation of access controls and permissions
- When onboarding new teams to a shared cluster and defining appropriate RBAC policies

**Do not use** for network policy auditing (use Cilium or Calico network policy tools), for container image scanning (use Trivy or Grype), or for runtime security monitoring (use Falco or Sysdig Secure).


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- kubectl configured with cluster-admin or equivalent read permissions to the target cluster
- rbac-tool installed (`kubectl krew install rbac-tool` or binary from GitHub)
- KubiScan installed (`pip install kubiscan`)
- Kubeaudit installed (`brew install kubeaudit` or from GitHub releases)
- Access to the cluster's audit logs for correlating RBAC findings with actual API access

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

1. **Define Objectives** — Clarify the goals and scope for kubernetes cluster rbac.
2. **Gather Resources** — Collect tools, data, and access needed for kubernetes cluster rbac.
3. **Execute Process** — Carry out kubernetes cluster rbac operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All kubernetes cluster rbac procedures executed completely and documented
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