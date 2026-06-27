---
name: performing-mobile-app-certificate-pinning-bypass
description: 'Bypasses SSL/TLS certificate pinning implementations in Android and iOS applications to enable traffic interception
  during authorized security assessments. Covers OkHttp, TrustManager, NSURLSession, and third-party pinning library bypass
  techniques using Frida, Objection, and custom scripts. Activates for requests involving certificate pinning bypass, SSL
  pinning defeat, mobile TLS interception, or proxy-resistant app testing.

  '
domain: cybersecurity
tags:
- mobile-security
- android
- ios
- certificate-pinning
- frida
- penetration-testing
subdomain: mobile-security
author: mahipal
version: 1.0.0
license: Apache-2.0
nist_csf:
- PR.PS-01
- PR.AA-05
- ID.RA-01
- DE.CM-09
---
# Performing Mobile App Certificate Pinning Bypass

## Overview

Cybersecurity skill for performing mobile app certificate pinning bypass. Follows industry best practices and security standards.

## When to Use

Use this skill when:
- Mobile app refuses connections through a proxy due to certificate pinning
- Performing authorized security testing requiring HTTPS traffic interception
- Assessing the strength and bypass difficulty of pinning implementations
- Evaluating defense-in-depth of mobile app network security

**Do not use** to bypass pinning on apps without explicit testing authorization.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Burp Suite configured as proxy with listener on all interfaces
- Rooted Android device or jailbroken iOS device
- Frida server running on target device
- Objection installed (`pip install objection`)
- Target app installed and reproducing the pinning behavior

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

1. **Plan Operations** — Define objectives, scope, and success criteria for mobile app certificate pinning bypass operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for mobile app certificate pinning bypass.
3. **Execute Core Workflow** — Perform the mobile app certificate pinning bypass operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All mobile app certificate pinning bypass procedures executed completely and documented
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