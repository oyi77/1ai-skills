---
name: auditing-terraform-infrastructure-for-security
description: 'Auditing Terraform infrastructure-as-code for security misconfigurations using Checkov, tfsec, Terrascan, and
  OPA/Rego policies to detect overly permissive IAM policies, public resource exposure, missing encryption, and insecure defaults
  before cloud deployment.

  '
domain: cybersecurity
tags:
- cloud-security
- terraform
- infrastructure-as-code
- checkov
- tfsec
- policy-as-code
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
# Auditing Terraform Infrastructure For Security

## When to Use

- When integrating security scanning into CI/CD pipelines for Terraform deployments
- When reviewing Terraform plans and modules for security best practices before applying
- When building policy-as-code guardrails for cloud infrastructure provisioning
- When auditing existing Terraform state files to identify deployed misconfigurations
- When enforcing organizational security standards across multiple Terraform projects

**Do not use** for runtime security monitoring (use CSPM tools), for application security testing (use SAST/DAST tools), or for cloud configuration drift detection (use AWS Config or Azure Policy after deployment).

## Prerequisites

- Checkov installed (`pip install checkov`)
- tfsec installed (`brew install tfsec` or binary from GitHub)
- Terrascan installed (`brew install terrascan`)
- Terraform v1.0+ for plan generation
- OPA (Open Policy Agent) for custom policy enforcement
- Git repository with Terraform code to audit

## Workflow

1. **Define Objectives** — Clarify the goals and scope for terraform infrastructure.
2. **Gather Resources** — Collect tools, data, and access needed for terraform infrastructure.
3. **Execute Process** — Carry out terraform infrastructure operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **security** — Primary tool for this skill
- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All terraform infrastructure procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
