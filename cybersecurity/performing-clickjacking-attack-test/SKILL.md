---
name: performing-clickjacking-attack-test
description: Testing web applications for clickjacking vulnerabilities by assessing frame embedding controls and crafting
  proof-of-concept overlay attacks during authorized security assessments.
domain: cybersecurity
tags:
- penetration-testing
- clickjacking
- ui-redressing
- web-security
- owasp
- x-frame-options
subdomain: web-application-security
version: '1.0'
author: mahipal
license: Apache-2.0
atlas_techniques:
- AML.T0024
- AML.T0035
nist_ai_rmf:
- MEASURE-2.8
- MAP-5.1
nist_csf:
- PR.PS-01
- ID.RA-01
- PR.DS-10
- DE.CM-01
---
# Performing Clickjacking Attack Test

## When to Use

- During authorized penetration tests when assessing UI redressing vulnerabilities
- When testing whether sensitive actions (delete account, transfer funds, change settings) can be performed via clickjacking
- For evaluating the effectiveness of X-Frame-Options and Content-Security-Policy frame-ancestors directives
- When assessing applications that process one-click actions without additional confirmation
- During security audits of applications handling financial transactions or account management

## Prerequisites

- **Authorization**: Written penetration testing agreement for the target
- **Web browser**: Modern browser for testing iframe embedding
- **Local web server**: Python `http.server` or similar for hosting PoC pages
- **Burp Suite**: For examining response headers
- **HTML/CSS knowledge**: For crafting clickjacking overlay pages
- **curl**: For checking framing headers on target pages


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## Workflow

1. **Plan Operations** — Define objectives, scope, and success criteria for clickjacking attack test operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for clickjacking attack test.
3. **Execute Core Workflow** — Perform the clickjacking attack test operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All clickjacking attack test procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
