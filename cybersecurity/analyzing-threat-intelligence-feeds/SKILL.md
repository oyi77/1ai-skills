---
name: analyzing-threat-intelligence-feeds
description: 'Analyzes structured and unstructured threat intelligence feeds to extract actionable indicators, adversary tactics,
  and campaign context. Use when ingesting commercial or open-source CTI feeds, evaluating feed quality, normalizing data
  into STIX 2.1 format, or enriching existing IOCs with campaign attribution. Activates for requests involving ThreatConnect,
  Recorded Future, Mandiant Advantage, MISP, AlienVault OTX, or automated feed aggregation pipelines.

  '
domain: cybersecurity
tags:
- STIX
- TAXII
- MITRE-ATT&CK
- IOC
- ThreatConnect
- Recorded-Future
- MISP
- CTI
- NIST-CSF
subdomain: threat-intelligence
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- ID.RA-01
- ID.RA-05
- DE.CM-01
- DE.AE-02
---
# Analyzing Threat Intelligence Feeds

## Overview

Cybersecurity skill for analyzing threat intelligence feeds. Follows industry best practices and security standards.

## When to Use

Use this skill when:
- Ingesting new commercial or OSINT threat feeds and assessing their signal-to-noise ratio
- Normalizing heterogeneous IOC formats (STIX 2.1, OpenIOC, YARA, Sigma) into a unified schema
- Evaluating feed freshness, fidelity, and relevance to the organization's threat profile
- Building automated enrichment pipelines that correlate IOCs against SIEM events

**Do not use** this skill for raw packet capture analysis or live incident triage without first establishing a CTI baseline.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Access to a Threat Intelligence Platform (TIP) such as ThreatConnect, MISP, or OpenCTI
- API keys for at least one commercial feed (Recorded Future, Mandiant Advantage, or VirusTotal Enterprise)
- TAXII 2.1 client library (taxii2-client Python package or equivalent)
- Role with read/write permissions to the TIP's indicator database

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

1. **Scope the Analysis** — Define what threat intelligence feeds artifacts or data sources to examine and the investigation timeline.
2. **Preserve Evidence** — Create forensic copies of relevant data. Maintain chain of custody documentation.
3. **Extract Key Indicators** — Parse and extract relevant threat intelligence feeds data points from collected artifacts.
4. **Correlate Findings** — Cross-reference extracted data with other sources (threat intel, logs, timelines).
5. **Build Timeline** — Construct a chronological sequence of events related to threat intelligence feeds.
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

- [ ] All threat intelligence feeds procedures executed completely and documented
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