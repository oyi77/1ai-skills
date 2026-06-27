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

## Overview

Cybersecurity skill for integrating sast into github actions pipeline. Follows industry best practices and security standards.

## When to Use

- When development teams need automated code-level vulnerability detection on every pull request
- When security teams require consistent SAST enforcement across all repositories in an organization
- When migrating from manual or periodic security reviews to continuous security testing
- When compliance frameworks (SOC 2, PCI DSS, NIST SSDF) require evidence of automated code analysis
- When multiple languages coexist in a monorepo and need unified scanning under one workflow

**Do not use** for runtime vulnerability detection (use DAST instead), for scanning third-party dependencies (use SCA tools like Snyk), or for infrastructure-as-code scanning (use Checkov or tfsec).


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- GitHub repository with GitHub Actions enabled
- GitHub Advanced Security license (required for CodeQL on private repos; free for public repos)
- Semgrep account for managed rules and Semgrep App dashboard (free tier available)
- Repository code in a supported language: Python, JavaScript/TypeScript, Java, C/C++, C#, Go, Ruby, Swift, Kotlin

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

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |