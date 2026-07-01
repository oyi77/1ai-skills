---
name: performing-ssl-stripping-attack
description: 'Simulates SSL stripping attacks using sslstrip, Bettercap, and mitmproxy in authorized environments to test
  HSTS enforcement, certificate validation, and HTTPS upgrade mechanisms that protect users from downgrade attacks on encrypted
  connections.

  '
domain: cybersecurity
tags:
- network-security
- ssl-stripping
- https
- hsts
- tls-security
subdomain: network-security
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- DE.CM-01
- ID.AM-03
- PR.DS-02
---
# Performing Ssl Stripping Attack

## Overview

Cybersecurity skill for performing ssl stripping attack. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "performing ssl stripping attack"
- "Simulates SSL stripping attacks using sslstrip, Bettercap, and mitmproxy in auth"


- Testing whether web applications properly enforce HTTPS through HSTS headers and redirect chains
- Validating that HSTS preloading is correctly configured and registered in browser preload lists
- Demonstrating the risk of cleartext HTTP to stakeholders during authorized security assessments
- Assessing whether internal applications and thick clients validate TLS certificates and reject downgrades
- Training SOC teams to detect SSL stripping indicators in network traffic

**Do not use** against networks or applications without explicit written authorization, to intercept real user credentials, or against production systems during business hours without change management approval.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Written authorization specifying in-scope applications and approved attack techniques
- Bettercap 2.x or sslstrip2 installed on the attacker machine
- ARP spoofing or other MITM positioning established (see ARP spoofing skill)
- IP forwarding enabled on the attacker machine
- Wireshark for verifying attack success and capturing evidence
- Test accounts (not real user credentials) for demonstrating credential interception


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

1. **Plan Operations** — Define objectives, scope, and success criteria for ssl stripping attack operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for ssl stripping attack.
3. **Execute Core Workflow** — Perform the ssl stripping attack operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All ssl stripping attack procedures executed completely and documented
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