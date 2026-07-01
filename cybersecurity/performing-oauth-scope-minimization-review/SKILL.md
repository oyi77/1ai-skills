---
name: performing-oauth-scope-minimization-review
description: 'Performs OAuth 2.0 scope minimization review to identify over-permissioned third-party application integrations,
  excessive API scopes, unused token grants, and risky OAuth consent patterns across identity providers and SaaS platforms.
  Activates for requests involving OAuth scope audit, API permission review, third-party app risk assessment, or consent grant
  minimization.

  '. Use when working with performing oauth scope minimization review.
domain: cybersecurity
tags:
- OAuth
- scope-minimization
- API-security
- consent-review
- third-party-risk
- token-audit
subdomain: identity-access-management
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.AA-01
- PR.AA-02
- PR.AA-05
- PR.AA-06
---
# Performing Oauth Scope Minimization Review

## Overview

Cybersecurity skill for performing oauth scope minimization review. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "performing oauth scope minimization review"
- "Performs OAuth 2"


- Annual or quarterly review of third-party application OAuth permissions
- After a security incident involving compromised OAuth tokens or unauthorized data access
- Compliance audit requiring documentation of third-party data access (GDPR Article 28, SOC 2)
- Discovery of shadow IT applications accessing organizational data via OAuth grants
- Migration or consolidation of SaaS applications requiring permission cleanup
- Implementing least-privilege principle for API integrations

**Do not use** for reviewing first-party application permissions within the same trust boundary; OAuth scope minimization focuses on third-party and cross-boundary consent grants.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Admin access to identity providers (Microsoft Entra ID, Okta, Google Workspace)
- Microsoft Graph API permissions: Application.Read.All, OAuth2PermissionGrant.ReadWrite.All
- Inventory of approved third-party integrations from procurement or IT governance
- OAuth scope risk classification framework
- Tools for token analysis (jwt.io for manual review, automated scripts for bulk analysis)

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

1. **Plan Operations** — Define objectives, scope, and success criteria for oauth scope minimization review operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for oauth scope minimization review.
3. **Execute Core Workflow** — Perform the oauth scope minimization review operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Design** — Define interface, identify patterns, plan implementation
1. **Implement** — Write code following existing conventions, add tests
1. **Verify** — Run tests, check integration, validate behavior

## Verification

- [ ] All oauth scope minimization review procedures executed completely and documented
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