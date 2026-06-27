---
name: implementing-secret-scanning-with-gitleaks
description: 'This skill covers implementing Gitleaks for detecting and preventing hardcoded secrets in git repositories.
  It addresses configuring pre-commit hooks, CI/CD pipeline integration, custom rule authoring for organization-specific secrets,
  baseline management for existing repositories, and remediation workflows for exposed credentials.

  '
domain: cybersecurity
tags:
- devsecops
- cicd
- secret-scanning
- gitleaks
- pre-commit
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
# Implementing Secret Scanning With Gitleaks

## Overview

Cybersecurity skill for implementing secret scanning with gitleaks. Follows industry best practices and security standards.

## When to Use

- When developers may accidentally commit API keys, passwords, tokens, or private keys to repositories
- When establishing pre-commit gates that prevent secrets from entering the git history
- When scanning existing repository history for previously committed secrets that need rotation
- When compliance requirements mandate secret detection across all source code repositories
- When migrating from manual secret audits to automated continuous scanning

**Do not use** for detecting secrets in running applications or memory (use runtime secret detection), for managing secrets after detection (use Vault or AWS Secrets Manager), or for scanning container images (use Trivy or Grype).


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Gitleaks v8.18+ installed via binary, Go install, or Docker
- Pre-commit framework installed for local hook integration
- Git repository with history to scan
- CI/CD platform access (GitHub Actions, GitLab CI, or equivalent)

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

1. **Assess Requirements** — Evaluate current environment and define secret scanning implementation requirements.
2. **Design Architecture** — Plan the secret scanning architecture, including components, integrations, and data flows.
3. **Configure Components** — Set up gitleaks for secret scanning according to vendor best practices and security guidelines.
4. **Test Integration** — Validate that all components work together. Run functional and security tests.
5. **Deploy to Production** — Roll out the implementation with monitoring and rollback capabilities.
6. **Validate and Document** — Verify the implementation meets requirements. Document configuration and runbooks.

## Tools

- **gitleaks** — Primary tool for this skill
- **Configuration Management** — Infrastructure as code and automation
- **Monitoring Stack** — Observability and alerting
- **Documentation Platform** — Runbooks and architecture docs

## Verification

- [ ] All secret scanning procedures executed completely and documented
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