---
name: performing-web-cache-deception-attack
description: Execute web cache deception attacks by exploiting path normalization discrepancies between CDN caching layers
  and origin servers to cache and retrieve sensitive authenticated content.
domain: cybersecurity
tags:
- web-cache-deception
- cdn-attack
- cache-poisoning
- path-normalization
- cloudflare
- cache-key
- static-resource
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
# Performing Web Cache Deception Attack

## When to Use
- When testing applications behind CDNs or reverse proxies (Cloudflare, Akamai, Varnish, Nginx)
- During assessment of authenticated page caching behavior
- When evaluating path normalization differences between caching and origin layers
- During bug bounty hunting on applications with aggressive caching policies
- When testing for sensitive data exposure through cache layer misconfiguration

## Prerequisites
- Understanding of HTTP caching mechanisms (Cache-Control, Vary, Age headers)
- Knowledge of CDN path normalization and cache key construction
- Burp Suite for intercepting and crafting requests
- Two browser sessions (authenticated victim and unauthenticated attacker)
- Understanding of URL path parsing differences across technologies
- Familiarity with common CDN platforms (Cloudflare, Akamai, Fastly, AWS CloudFront)


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## Workflow

1. **Plan Operations** — Define objectives, scope, and success criteria for web cache deception attack operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for web cache deception attack.
3. **Execute Core Workflow** — Perform the web cache deception attack operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All web cache deception attack procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
