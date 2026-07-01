---
name: analyzing-indicators-of-compromise
description: 'Analyzes indicators of compromise (IOCs) including IP addresses, domains, file hashes, URLs, and email artifacts
  to determine maliciousness confidence, campaign attribution, and blocking priority. Use when triaging IOCs from phishing
  emails, security alerts, or external threat feeds; enriching raw IOCs with multi-source intelligence; or making block/monitor/whitelist
  decisions. Activates for requests involving VirusTotal, AbuseIPDB, MalwareBazaar, MISP, or IOC enrichment pipelines.

  '
domain: cybersecurity
tags:
- IOC
- VirusTotal
- AbuseIPDB
- MalwareBazaar
- MISP
- threat-intelligence
- STIX
- NIST-CSF
subdomain: threat-intelligence
version: 1.0.0
author: mahipal
license: Apache-2.0
atlas_techniques:
- AML.T0052
nist_csf:
- ID.RA-01
- ID.RA-05
- DE.CM-01
- DE.AE-02
---
# Analyzing Indicators Of Compromise

## Overview

Cybersecurity skill for analyzing indicators of compromise. Follows industry best practices and security standards.

## When to Use

Use this skill when:
- A phishing email or alert generates IOCs (URLs, IP addresses, file hashes) requiring rapid triage
- Automated feeds deliver bulk IOCs that need confidence scoring before ingestion into blocking controls
- An incident investigation requires contextual enrichment of observed network artifacts

**Do not use** this skill in isolation for high-stakes blocking decisions — always combine automated enrichment with analyst judgment, especially for shared infrastructure (CDNs, cloud providers).


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- VirusTotal API key (free or Enterprise) for multi-AV and sandbox lookup
- AbuseIPDB API key for IP reputation checks
- MISP instance or TIP for cross-referencing against known campaigns
- Python with `requests` and `vt-py` libraries, or SOAR platform with pre-built connectors

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

1. **Scope the Analysis** — Define what indicators of compromise artifacts or data sources to examine and the investigation timeline.
2. **Preserve Evidence** — Create forensic copies of relevant data. Maintain chain of custody documentation.
3. **Extract Key Indicators** — Parse and extract relevant indicators of compromise data points from collected artifacts.
4. **Correlate Findings** — Cross-reference extracted data with other sources (threat intel, logs, timelines).
5. **Build Timeline** — Construct a chronological sequence of events related to indicators of compromise.
6. **Document Analysis** — Write findings report with evidence, conclusions, and recommendations.

## Tools

- **Forensic Toolkit** — Evidence collection and analysis
- **Timeline Tools** — Chronological event reconstruction
- **Log Analysis Platform** — Centralized log parsing and search


## Process

1. **Scope** — Define research questions, identify data sources, set time boundaries
1. **Gather** — Collect data from primary sources, APIs, and public records
1. **Synthesize** — Analyze findings, identify patterns, produce actionable report

## Verification

- [ ] All indicators of compromise procedures executed completely and documented
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