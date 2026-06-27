---
name: testing-for-sensitive-data-exposure
description: Identifying sensitive data exposure vulnerabilities including API key leakage, PII in responses, insecure storage,
  and unprotected data transmission during security assessments.
domain: cybersecurity
tags:
- penetration-testing
- data-exposure
- pii
- owasp
- web-security
- api-keys
- secrets
subdomain: web-application-security
version: '1.0'
author: mahipal
license: Apache-2.0
nist_ai_rmf:
- MEASURE-2.7
- MAP-5.1
- MANAGE-2.4
atlas_techniques:
- AML.T0070
- AML.T0066
- AML.T0082
nist_csf:
- PR.PS-01
- ID.RA-01
- PR.DS-10
- DE.CM-01
---
# Testing For Sensitive Data Exposure

## When to Use

- During authorized penetration tests when assessing data protection controls
- When evaluating applications for GDPR, PCI DSS, HIPAA, or other data protection compliance
- For identifying leaked API keys, credentials, tokens, and secrets in application responses
- When testing whether sensitive data is properly encrypted in transit and at rest
- During security assessments of APIs that handle PII, financial data, or health records

## Prerequisites

- **Authorization**: Written penetration testing agreement with data handling scope
- **Burp Suite Professional**: For intercepting and analyzing responses for sensitive data
- **trufflehog**: Secret scanning tool (`pip install trufflehog`)
- **gitleaks**: Git repository secret scanner (`go install github.com/gitleaks/gitleaks/v8@latest`)
- **curl/httpie**: For manual endpoint testing
- **Browser DevTools**: For examining local storage, session storage, and cached data
- **testssl.sh**: TLS configuration testing tool

## Workflow

1. **Reconnaissance** — Gather information about the target related to . Identify attack surface.
2. **Vulnerability Identification** — Enumerate potential  weaknesses using automated and manual techniques.
3. **Exploit Development/Selection** — Use sensitive data exposure to identify and test  vulnerabilities.
4. **Execution** — Execute the  test in a controlled manner with proper authorization.
5. **Post-Exploitation** — Document the impact and extent of successful exploitation.
6. **Reporting** — Write detailed findings with reproduction steps, impact assessment, and remediation guidance.

## Tools

- **sensitive data exposure** — Primary tool for this skill
- **Vulnerability Scanner** — Automated weakness identification
- **Exploitation Framework** — Controlled exploitation testing
- **Reporting Tool** — Findings documentation and tracking

## Verification

- [ ] All  procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
