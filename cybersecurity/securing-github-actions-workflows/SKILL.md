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

## Overview

Cybersecurity skill for securing github actions workflows. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "securing github actions workflows"
- "This skill covers hardening GitHub Actions workflows against supply chain attack"


- When GitHub Actions is the CI/CD platform and workflows need hardening against supply chain attacks
- When workflows handle secrets, deploy to production, or have elevated permissions
- When preventing script injection via untrusted PR titles, branch names, or commit messages
- When requiring audit trails and approval gates for workflow modifications
- When third-party actions pose supply chain risk through mutable version tags

**Do not use** for securing other CI/CD platforms (see platform-specific hardening guides), for application vulnerability scanning (use SAST/DAST), or for secret detection in code (use Gitleaks).


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- GitHub repository with GitHub Actions enabled
- GitHub organization admin access for organization-level settings
- Understanding of GitHub Actions workflow syntax and events

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

1. **Define Objectives** — Clarify the goals and scope for github actions workflows.
2. **Gather Resources** — Collect tools, data, and access needed for github actions workflows.
3. **Execute Process** — Carry out github actions workflows operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run securing github actions workflows workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All github actions workflows procedures executed completely and documented
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