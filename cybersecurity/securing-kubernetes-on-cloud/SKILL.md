---
name: securing-kubernetes-on-cloud
description: 'This skill covers hardening managed Kubernetes clusters on EKS, AKS, and GKE by implementing Pod Security Standards,
  network policies, workload identity, RBAC scoping, image admission controls, and runtime security monitoring. It addresses
  cloud-specific security features including IRSA for EKS, Workload Identity for GKE, and Managed Identities for AKS.

  '
domain: cybersecurity
tags:
- kubernetes-security
- eks
- aks
- gke
- pod-security-standards
- container-runtime
subdomain: cloud-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- ID.AM-08
- GV.SC-06
- DE.CM-01
---
# Securing Kubernetes On Cloud

## When to Use

- When deploying new managed Kubernetes clusters in production with security requirements
- When hardening existing EKS, AKS, or GKE clusters after a security audit or pentest finding
- When implementing workload identity to eliminate static cloud credentials in pods
- When enforcing pod security policies across namespaces to prevent container escapes
- When integrating runtime security monitoring for detecting container-level threats

**Do not use** for non-Kubernetes container deployments like ECS Fargate or Azure Container Instances, for application-level security within containers (see securing-serverless-functions), or for CI/CD pipeline security (see implementing-cloud-devsecops).

## Prerequisites

- Managed Kubernetes cluster provisioned on EKS, AKS, or GKE with admin access
- kubectl configured with cluster admin credentials
- Familiarity with Kubernetes RBAC, namespaces, and security contexts
- Container network interface plugin supporting network policies (Calico, Cilium)

## Workflow

1. **Define Objectives** — Clarify the goals and scope for kubernetes on cloud.
2. **Gather Resources** — Collect tools, data, and access needed for kubernetes on cloud.
3. **Execute Process** — Carry out kubernetes on cloud operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All kubernetes on cloud procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
