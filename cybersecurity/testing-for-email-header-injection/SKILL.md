---
name: testing-for-email-header-injection
description: Test web application email functionality for SMTP header injection vulnerabilities that allow attackers to inject
  additional email headers, modify recipients, and abuse contact forms for spam relay.
domain: cybersecurity
tags:
- email-injection
- smtp-injection
- crlf-injection
- header-injection
- spam-relay
- contact-form
- email-security
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
# Testing For Email Header Injection

## When to Use
- When testing contact forms, feedback forms, or "email a friend" functionality
- During assessment of password reset email functionality
- When testing newsletter subscription or notification email systems
- During penetration testing of applications that send emails based on user input
- When auditing email-related API endpoints for header injection

## Prerequisites
- Burp Suite for intercepting and modifying HTTP requests
- Understanding of SMTP protocol and email header structure
- Knowledge of CRLF injection techniques (\r\n sequences)
- Test email accounts for receiving injected emails
- Access to application features that trigger email sending
- SMTP server logs access for monitoring injection attempts

## Workflow

1. **Reconnaissance** — Gather information about the target related to . Identify attack surface.
2. **Vulnerability Identification** — Enumerate potential  weaknesses using automated and manual techniques.
3. **Exploit Development/Selection** — Use email header injection to identify and test  vulnerabilities.
4. **Execution** — Execute the  test in a controlled manner with proper authorization.
5. **Post-Exploitation** — Document the impact and extent of successful exploitation.
6. **Reporting** — Write detailed findings with reproduction steps, impact assessment, and remediation guidance.

## Tools

- **email header injection** — Primary tool for this skill
- **Vulnerability Scanner** — Automated weakness identification
- **Exploitation Framework** — Controlled exploitation testing
- **Reporting Tool** — Findings documentation and tracking

## Verification

- [ ] All  procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
