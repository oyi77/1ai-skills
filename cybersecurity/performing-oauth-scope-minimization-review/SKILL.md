---
name: performing-oauth-scope-minimization-review
description: 'Performs OAuth 2.0 scope minimization review to identify over-permissioned third-party application integrations,
  excessive API scopes, unused token grants, and risky OAuth consent patterns across identity providers and SaaS platforms.
  Activates for requests involving OAuth scope audit, API permission review, third-party app risk assessment, or consent grant
  minimization.

  '
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

## When to Use

- Annual or quarterly review of third-party application OAuth permissions
- After a security incident involving compromised OAuth tokens or unauthorized data access
- Compliance audit requiring documentation of third-party data access (GDPR Article 28, SOC 2)
- Discovery of shadow IT applications accessing organizational data via OAuth grants
- Migration or consolidation of SaaS applications requiring permission cleanup
- Implementing least-privilege principle for API integrations

**Do not use** for reviewing first-party application permissions within the same trust boundary; OAuth scope minimization focuses on third-party and cross-boundary consent grants.

## Prerequisites

- Admin access to identity providers (Microsoft Entra ID, Okta, Google Workspace)
- Microsoft Graph API permissions: Application.Read.All, OAuth2PermissionGrant.ReadWrite.All
- Inventory of approved third-party integrations from procurement or IT governance
- OAuth scope risk classification framework
- Tools for token analysis (jwt.io for manual review, automated scripts for bulk analysis)

## Workflow

1. **Plan Operations** — Define objectives, scope, and success criteria for oauth scope minimization review operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for oauth scope minimization review.
3. **Execute Core Workflow** — Perform the oauth scope minimization review operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All oauth scope minimization review procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
