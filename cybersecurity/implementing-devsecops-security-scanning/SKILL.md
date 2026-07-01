---
name: implementing-devsecops-security-scanning
description: 'Integrates Static Application Security Testing (SAST), Dynamic Application Security Testing (DAST), and Software
  Composition Analysis (SCA) into CI/CD pipelines using open-source tools. Covers Semgrep for SAST, Trivy for SCA and container
  scanning, OWASP ZAP for DAST, and Gitleaks for secrets detection. Activates for requests involving DevSecOps pipeline setup,
  automated security scanning in CI/CD, SAST/DAST/SCA integration, or shift-left security implementation.

  '
domain: cybersecurity
tags:
- devsecops
- SAST
- DAST
- SCA
- semgrep
- trivy
- owasp-zap
- gitleaks
- CI-CD
- shift-left
subdomain: application-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- PR.PS-04
- ID.RA-01
- PR.DS-10
---
# Implementing Devsecops Security Scanning

## Overview

Cybersecurity skill for implementing devsecops security scanning. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "implementing devsecops security scanning"
- "Integrates Static Application Security Testing (SAST), Dynamic Application Secur"


- Setting up automated security scanning in a new or existing CI/CD pipeline
- Shifting security left by catching vulnerabilities before code reaches production
- Meeting compliance requirements (SOC 2, PCI-DSS, ISO 27001) that mandate automated security testing
- Integrating SAST, DAST, and SCA together to achieve comprehensive application security coverage
- Establishing security gates that block deployments containing critical or high-severity vulnerabilities

**Do not use** as a replacement for manual penetration testing. Automated scanning catches common vulnerability patterns but cannot replace human-driven security assessments for business logic flaws and complex attack chains.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- CI/CD platform: GitHub Actions, GitLab CI, Jenkins, or Azure DevOps
- Container runtime (Docker) for running scanning tools
- A staging environment URL for DAST scanning (DAST cannot test static code)
- Repository access with permissions to modify CI/CD workflow files
- Tool-specific requirements:
  - Semgrep: free for open-source rulesets (p > security-audit, p > owasp-top-ten)
  - Trivy: free, no account required
  - OWASP ZAP: free, Docker image available
  - Gitleaks: free, no account required

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

1. **Assess Requirements** — Evaluate current environment and define devsecops security scanning implementation requirements.
2. **Design Architecture** — Plan the devsecops security scanning architecture, including components, integrations, and data flows.
3. **Configure Components** — Set up and configure each devsecops security scanning component according to best practices.
4. **Test Integration** — Validate that all components work together. Run functional and security tests.
5. **Deploy to Production** — Roll out the implementation with monitoring and rollback capabilities.
6. **Validate and Document** — Verify the implementation meets requirements. Document configuration and runbooks.

## Tools

- **Configuration Management** — Infrastructure as code and automation
- **Monitoring Stack** — Observability and alerting
- **Documentation Platform** — Runbooks and architecture docs


## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- [ ] All devsecops security scanning procedures executed completely and documented
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