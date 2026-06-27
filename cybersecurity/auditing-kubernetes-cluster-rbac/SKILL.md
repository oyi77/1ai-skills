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

## When to Use

- When performing security assessments of Kubernetes clusters (EKS, GKE, AKS, or self-managed)
- When validating that RBAC policies enforce least privilege for users and service accounts
- When investigating potential lateral movement or privilege escalation within a Kubernetes cluster
- When compliance audits require documentation of access controls and permissions
- When onboarding new teams to a shared cluster and defining appropriate RBAC policies

**Do not use** for network policy auditing (use Cilium or Calico network policy tools), for container image scanning (use Trivy or Grype), or for runtime security monitoring (use Falco or Sysdig Secure).

## Prerequisites

- kubectl configured with cluster-admin or equivalent read permissions to the target cluster
- rbac-tool installed (`kubectl krew install rbac-tool` or binary from GitHub)
- KubiScan installed (`pip install kubiscan`)
- Kubeaudit installed (`brew install kubeaudit` or from GitHub releases)
- Access to the cluster's audit logs for correlating RBAC findings with actual API access

## Workflow

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
