---
name: performing-web-cache-poisoning-attack
description: Exploiting web cache mechanisms to serve malicious content to other users by poisoning cached responses through
  unkeyed headers and parameters during authorized security tests.
domain: cybersecurity
tags:
- penetration-testing
- cache-poisoning
- web-security
- cdn
- burpsuite
- owasp
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
# Performing Web Cache Poisoning Attack

## When to Use

- During authorized penetration tests when the application uses CDN or reverse proxy caching (Cloudflare, Akamai, Varnish, Nginx)
- When assessing web applications for cache-based vulnerabilities that could affect all users
- For testing whether unkeyed HTTP headers are reflected in cached responses
- When evaluating cache key behavior and cache deception vulnerabilities
- During security assessments of applications with aggressive caching policies

## Prerequisites

- **Authorization**: Written penetration testing agreement explicitly covering cache poisoning testing
- **Burp Suite Professional**: With Param Miner extension for automated unkeyed header discovery
- **curl**: For manual cache testing with precise header control
- **Target knowledge**: Understanding of the caching layer (CDN provider, cache headers)
- **Cache buster**: Unique query parameter to isolate test requests from other users
- **Caution**: Cache poisoning affects all users; test with cache-busting parameters first


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## Workflow

1. **Plan Operations** — Define objectives, scope, and success criteria for web cache poisoning attack operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for web cache poisoning attack.
3. **Execute Core Workflow** — Perform the web cache poisoning attack operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All web cache poisoning attack procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
