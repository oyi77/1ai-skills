---
name: integrating-dast-with-owasp-zap-in-pipeline
description: 'This skill covers integrating OWASP ZAP (Zed Attack Proxy) for Dynamic Application Security Testing in CI/CD
  pipelines. It addresses configuring baseline, full, and API scans against running applications, interpreting ZAP findings,
  tuning scan policies, and establishing DAST quality gates in GitHub Actions and GitLab CI.

  '
domain: cybersecurity
tags:
- devsecops
- cicd
- dast
- owasp-zap
- dynamic-testing
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
# Integrating Dast With Owasp Zap In Pipeline

## When to Use

- When testing running web applications for vulnerabilities like XSS, SQLi, CSRF, and misconfigurations
- When SAST alone is insufficient and runtime behavior testing is required
- When compliance mandates dynamic security testing of web applications before production
- When testing APIs (REST/GraphQL) for authentication, authorization, and injection flaws
- When establishing continuous DAST scanning in staging environments before production deployment

**Do not use** for scanning source code (use SAST), for scanning dependencies (use SCA), or for infrastructure configuration scanning (use IaC scanning tools).

## Prerequisites

- OWASP ZAP Docker image or installed locally (zaproxy/zap-stable or zaproxy/action-*)
- Running target application accessible from the CI/CD runner (staging URL or Docker service)
- ZAP scan rules configuration (optional, for tuning)
- OpenAPI/Swagger specification for API scanning (optional)

## Workflow

1. **Define Objectives** — Clarify the goals and scope for dast.
2. **Gather Resources** — Collect tools, data, and access needed for dast.
3. **Execute Process** — Carry out dast operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **owasp zap in pipeline** — Primary tool for this skill
- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All dast procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
