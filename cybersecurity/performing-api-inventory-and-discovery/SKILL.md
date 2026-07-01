---
name: performing-api-inventory-and-discovery
description: Performs API inventory and discovery to identify all API endpoints in an organization's environment including
  documented, undocumented, shadow, zombie, and deprecated APIs. The tester uses passive traffic analysis, active scanning,
  DNS enumeration, JavaScript analysis, and cloud resource inventory to build a comprehensive API catalog. Maps to OWASP API9:2023
  Improper Inventory Management. Use when working with performing api inventory and discovery.
domain: cybersecurity
tags:
- api-security
- owasp
- api-discovery
- shadow-api
- inventory
- attack-surface
subdomain: api-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- ID.RA-01
- PR.DS-10
- DE.CM-01
---
# Performing Api Inventory And Discovery

## Overview

Cybersecurity skill for performing api inventory and discovery. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "performing api inventory and discovery"
- "Performs API inventory and discovery to identify all API endpoints in an organiz"


- Mapping the complete API attack surface of an organization before a security assessment
- Identifying shadow APIs deployed by development teams without security review
- Discovering deprecated or zombie API versions that remain accessible but unmaintained
- Finding undocumented API endpoints exposed through mobile applications, SPAs, or microservices
- Building an API inventory for compliance requirements (PCI-DSS, SOC2, GDPR)

**Do not use** without written authorization. API discovery involves scanning network infrastructure and analyzing traffic.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Written authorization specifying the target domains and network ranges
- Passive traffic capture capability (network tap, proxy, or cloud traffic mirroring)
- Active scanning tools: Amass, subfinder, httpx, and nuclei
- JavaScript analysis tools: LinkFinder, JS-Miner, or custom parsers
- Access to cloud console (AWS, Azure, GCP) for API gateway inventory
- Burp Suite Professional for passive API endpoint discovery

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

1. **Plan Operations** — Define objectives, scope, and success criteria for api inventory and discovery operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for api inventory and discovery.
3. **Execute Core Workflow** — Perform the api inventory and discovery operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Design** — Define interface, identify patterns, plan implementation
1. **Implement** — Write code following existing conventions, add tests
1. **Verify** — Run tests, check integration, validate behavior

## Verification

- [ ] All api inventory and discovery procedures executed completely and documented
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