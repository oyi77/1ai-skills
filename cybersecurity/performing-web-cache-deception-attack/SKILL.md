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

## Overview

Cybersecurity skill for performing web cache deception attack. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "performing web cache deception attack"
- "Execute web cache deception attacks by exploiting path normalization discrepanci"

- When testing applications behind CDNs or reverse proxies (Cloudflare, Akamai, Varnish, Nginx)
- During assessment of authenticated page caching behavior
- When evaluating path normalization differences between caching and origin layers
- During bug bounty hunting on applications with aggressive caching policies
- When testing for sensitive data exposure through cache layer misconfiguration


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites
- Understanding of HTTP caching mechanisms (Cache-Control, Vary, Age headers)
- Knowledge of CDN path normalization and cache key construction
- Burp Suite for intercepting and crafting requests
- Two browser sessions (authenticated victim and unauthenticated attacker)
- Understanding of URL path parsing differences across technologies
- Familiarity with common CDN platforms (Cloudflare, Akamai, Fastly, AWS CloudFront)


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

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

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |