---
name: integrating-sast-into-github-actions-pipeline
description: 'This skill covers integrating Static Application Security Testing (SAST) tools—CodeQL and Semgrep—into GitHub
  Actions CI/CD pipelines. It addresses configuring automated code scanning on pull requests and pushes, tuning rules to reduce
  false positives, uploading SARIF results to GitHub Advanced Security, and establishing quality gates that block merges when
  high-severity vulnerabilities are detected.

  '
domain: cybersecurity
tags:
- devsecops
- cicd
- sast
- codeql
- semgrep
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
# Integrating Sast Into Github Actions Pipeline

## When to Use

- When development teams need automated code-level vulnerability detection on every pull request
- When security teams require consistent SAST enforcement across all repositories in an organization
- When migrating from manual or periodic security reviews to continuous security testing
- When compliance frameworks (SOC 2, PCI DSS, NIST SSDF) require evidence of automated code analysis
- When multiple languages coexist in a monorepo and need unified scanning under one workflow

**Do not use** for runtime vulnerability detection (use DAST instead), for scanning third-party dependencies (use SCA tools like Snyk), or for infrastructure-as-code scanning (use Checkov or tfsec).

## Prerequisites

- GitHub repository with GitHub Actions enabled
- GitHub Advanced Security license (required for CodeQL on private repos; free for public repos)
- Semgrep account for managed rules and Semgrep App dashboard (free tier available)
- Repository code in a supported language: Python, JavaScript/TypeScript, Java, C/C++, C#, Go, Ruby, Swift, Kotlin

## Workflow

1. **Define Objectives** — Clarify the goals and scope for sast into github actions pipeline.
2. **Gather Resources** — Collect tools, data, and access needed for sast into github actions pipeline.
3. **Execute Process** — Carry out sast into github actions pipeline operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All sast into github actions pipeline procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
