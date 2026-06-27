---
name: performing-second-order-sql-injection
description: Detect and exploit second-order SQL injection vulnerabilities where malicious input is stored in a database and
  later executed in an unsafe SQL query during a different application operation.
domain: cybersecurity
tags:
- second-order-sqli
- stored-sql-injection
- sql-injection
- database-security
- web-security
- blind-injection
- persistent-sqli
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
# Performing Second Order Sql Injection

## When to Use
- When first-order SQL injection testing reveals proper input sanitization at storage time
- During penetration testing of applications with user-generated content stored in databases
- When testing multi-step workflows where stored data feeds subsequent database queries
- During assessment of admin panels that display or process user-submitted data
- When evaluating stored procedure execution paths that use previously stored data

## Prerequisites
- Burp Suite Professional for request tracking across application flows
- SQLMap with second-order injection support (--second-url flag)
- Understanding of SQL injection fundamentals and blind extraction techniques
- Two or more application functions (one for storing data, another for triggering execution)
- Database error message monitoring or blind technique knowledge
- Multiple user accounts for testing stored data across different contexts

## Workflow

1. **Plan Operations** — Define objectives, scope, and success criteria for second order sql injection operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for second order sql injection.
3. **Execute Core Workflow** — Perform the second order sql injection operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All second order sql injection procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
