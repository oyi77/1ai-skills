---
name: analyzing-network-flow-data-with-netflow
description: Parse NetFlow v9 and IPFIX records to detect volumetric anomalies, port scanning, data exfiltration, and C2 beaconing
  patterns. Uses the Python netflow library to decode flow records, builds traffic baselines, and applies statistical analysis
  to identify flows with abnormal byte counts, connection durations, and periodic timing patterns.
domain: cybersecurity
tags:
- analyzing
- network
- flow
- data
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
# Analyzing Network Flow Data With Netflow

## Overview

Cybersecurity skill for analyzing network flow data with netflow. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "analyzing network flow data with netflow"
- "Parse NetFlow v9 and IPFIX records to detect volumetric anomalies, port scanning"


- When investigating security incidents that require analyzing network flow data with netflow
- When building detection rules or threat hunting queries for this domain
- When SOC analysts need structured procedures for this analysis type
- When validating security monitoring coverage for related attack techniques


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Familiarity with network security concepts and tools
- Access to a test or lab environment for safe execution
- Python 3.8+ with required dependencies installed
- Appropriate authorization for any testing activities

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

1. **Scope the Analysis** — Define what network flow data artifacts or data sources to examine and the investigation timeline.
2. **Preserve Evidence** — Create forensic copies of relevant data. Maintain chain of custody documentation.
3. **Extract Key Indicators** — Use netflow to parse and extract relevant network flow data data points from collected artifacts.
4. **Correlate Findings** — Cross-reference extracted data with other sources (threat intel, logs, timelines).
5. **Build Timeline** — Construct a chronological sequence of events related to network flow data.
6. **Document Analysis** — Write findings report with evidence, conclusions, and recommendations.

## Tools

- **netflow** — Primary tool for this skill
- **Forensic Toolkit** — Evidence collection and analysis
- **Timeline Tools** — Chronological event reconstruction
- **Log Analysis Platform** — Centralized log parsing and search

## Verification

- [ ] All network flow data procedures executed completely and documented
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