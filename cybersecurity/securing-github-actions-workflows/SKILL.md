---
name: securing-github-actions-workflows
description: 'This skill covers hardening GitHub Actions workflows against supply chain attacks, credential theft, and privilege
  escalation. It addresses pinning actions to SHA digests, minimizing GITHUB_TOKEN permissions, protecting secrets from exfiltration,
  preventing script injection in workflow expressions, and implementing required reviewers for workflow changes.

  '
domain: cybersecurity
tags:
- devsecops
- cicd
- github-actions
- supply-chain
- workflow-security
- secure-sdlc
subdomain: devsecops
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- GV.SC-07
- ID.IM-04
- PR.PS-04
---
# Securing Github Actions Workflows

## When to Use

- When GitHub Actions is the CI/CD platform and workflows need hardening against supply chain attacks
- When workflows handle secrets, deploy to production, or have elevated permissions
- When preventing script injection via untrusted PR titles, branch names, or commit messages
- When requiring audit trails and approval gates for workflow modifications
- When third-party actions pose supply chain risk through mutable version tags

**Do not use** for securing other CI/CD platforms (see platform-specific hardening guides), for application vulnerability scanning (use SAST/DAST), or for secret detection in code (use Gitleaks).

## Prerequisites

- GitHub repository with GitHub Actions enabled
- GitHub organization admin access for organization-level settings
- Understanding of GitHub Actions workflow syntax and events

## Workflow

1. **Define Objectives** — Clarify the goals and scope for github actions workflows.
2. **Gather Resources** — Collect tools, data, and access needed for github actions workflows.
3. **Execute Process** — Carry out github actions workflows operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All github actions workflows procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
