---
name: testing-for-broken-access-control
description: Systematically testing web applications for broken access control vulnerabilities including privilege escalation,
  missing function-level checks, and insecure direct object references.
domain: cybersecurity
tags:
- penetration-testing
- access-control
- authorization
- owasp
- privilege-escalation
- web-security
subdomain: web-application-security
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- ID.RA-01
- PR.DS-10
- DE.CM-01
---
# Testing For Broken Access Control

## When to Use

- During authorized penetration tests as the primary assessment for OWASP A01:2021 - Broken Access Control
- When evaluating role-based access control (RBAC) implementations across all application endpoints
- For testing multi-tenant applications where users in one organization should not access another's data
- When assessing API endpoints for missing or inconsistent authorization checks
- During security audits where privilege escalation and unauthorized access are primary concerns

## Prerequisites

- **Authorization**: Written penetration testing agreement for the target
- **Burp Suite Professional**: With Authorize extension for automated access control testing
- **Multiple test accounts**: Accounts at each role level (admin, manager, user, guest)
- **Application role matrix**: Documentation of what each role should and should not access
- **curl/httpie**: For manual endpoint testing with different authentication contexts
- **ffuf**: For discovering hidden endpoints that may lack access controls

## Workflow

1. **Reconnaissance** — Gather information about the target related to . Identify attack surface.
2. **Vulnerability Identification** — Enumerate potential  weaknesses using automated and manual techniques.
3. **Exploit Development/Selection** — Use broken access control to identify and test  vulnerabilities.
4. **Execution** — Execute the  test in a controlled manner with proper authorization.
5. **Post-Exploitation** — Document the impact and extent of successful exploitation.
6. **Reporting** — Write detailed findings with reproduction steps, impact assessment, and remediation guidance.

## Tools

- **broken access control** — Primary tool for this skill
- **Vulnerability Scanner** — Automated weakness identification
- **Exploitation Framework** — Controlled exploitation testing
- **Reporting Tool** — Findings documentation and tracking

## Verification

- [ ] All  procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
