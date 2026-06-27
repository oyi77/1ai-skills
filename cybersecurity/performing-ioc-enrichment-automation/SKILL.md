---
name: performing-ioc-enrichment-automation
description: 'Automates Indicator of Compromise (IOC) enrichment by orchestrating lookups across VirusTotal, AbuseIPDB, Shodan,
  MISP, and other intelligence sources to provide contextual scoring and disposition recommendations. Use when SOC analysts
  need rapid multi-source enrichment of IPs, domains, URLs, and file hashes during alert triage or incident investigation.

  '
domain: cybersecurity
tags:
- soc
- ioc
- enrichment
- automation
- virustotal
- abuseipdb
- shodan
- threat-intelligence
subdomain: soc-operations
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- DE.CM-01
- DE.AE-02
- RS.MA-01
- DE.AE-06
---
# Performing Ioc Enrichment Automation

## Overview

Cybersecurity skill for performing ioc enrichment automation. Follows industry best practices and security standards.

## When to Use

Use this skill when:
- SOC analysts need to quickly enrich IOCs from multiple sources during alert triage
- High alert volumes require automated enrichment to reduce manual lookup time
- Incident investigations need comprehensive IOC context for scope assessment
- SOAR playbooks require enrichment actions as part of automated triage workflows

**Do not use** for bulk blocking decisions without analyst review — enrichment provides context, not definitive malicious/benign determination.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- API keys: VirusTotal (free or premium), AbuseIPDB, Shodan, URLScan.io, GreyNoise
- Python 3.8+ with `requests`, `vt-py`, `shodan` libraries
- MISP instance or TIP for cross-referencing organizational intelligence
- SOAR platform (optional) for workflow integration
- Rate limit awareness: VT free (4 req/min), AbuseIPDB (1000/day), Shodan (1 req/sec)

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

1. **Plan Operations** — Define objectives, scope, and success criteria for ioc enrichment automation operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for ioc enrichment automation.
3. **Execute Core Workflow** — Perform the ioc enrichment automation operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All ioc enrichment automation procedures executed completely and documented
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