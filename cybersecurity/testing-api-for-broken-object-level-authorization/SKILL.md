---
name: testing-api-for-broken-object-level-authorization
description: Tests REST and GraphQL APIs for Broken Object Level Authorization (BOLA/IDOR) vulnerabilities where an authenticated
  user can access or modify resources belonging to other users by manipulating object identifiers in API requests. The tester
  intercepts API calls, identifies object ID parameters (numeric IDs, UUIDs, slugs), and systematically replaces them with
  IDs belonging to other users to determine if the server enforces per-object authorization.
domain: cybersecurity
tags:
- api-security
- owasp
- bola
- idor
- authorization
- rest-security
subdomain: api-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- ID.RA-01
- PR.DS-10
- DE.CM-01
---
# Testing Api For Broken Object Level Authorization

## When to Use

- Assessing REST or GraphQL APIs that use object identifiers in URL paths, query parameters, or request bodies
- Performing OWASP API Security Top 10 assessments where API1:2023 (BOLA) must be tested
- Testing multi-tenant SaaS applications where users from different tenants should not access each other's data
- Validating that API endpoints enforce per-object authorization checks beyond just authentication
- Evaluating APIs after new endpoints are added to ensure authorization middleware is applied consistently

**Do not use** without written authorization from the API owner. BOLA testing involves accessing or attempting to access other users' data, which requires explicit permission.

## Prerequisites

- Written authorization specifying the target API endpoints and scope of testing
- At least two test accounts with different privilege levels and distinct data sets
- Burp Suite Professional or OWASP ZAP configured as an intercepting proxy
- Authentication tokens (JWT, session cookies, API keys) for each test account
- API documentation (OpenAPI/Swagger spec) or access to enumerate endpoints
- Python 3.10+ with `requests` library for scripted testing
- Autorize Burp extension installed for automated BOLA detection

## Workflow

1. **Reconnaissance** — Gather information about the target related to api. Identify attack surface.
2. **Vulnerability Identification** — Enumerate potential api weaknesses using automated and manual techniques.
3. **Exploit Development/Selection** — Use broken object level authorization to identify and test api vulnerabilities.
4. **Execution** — Execute the api test in a controlled manner with proper authorization.
5. **Post-Exploitation** — Document the impact and extent of successful exploitation.
6. **Reporting** — Write detailed findings with reproduction steps, impact assessment, and remediation guidance.

## Tools

- **broken object level authorization** — Primary tool for this skill
- **Vulnerability Scanner** — Automated weakness identification
- **Exploitation Framework** — Controlled exploitation testing
- **Reporting Tool** — Findings documentation and tracking

## Verification

- [ ] All api procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
