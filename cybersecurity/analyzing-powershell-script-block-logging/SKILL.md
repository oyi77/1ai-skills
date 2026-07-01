---
name: analyzing-powershell-script-block-logging
description: Parse Windows PowerShell Script Block Logs (Event ID 4104) from EVTX files to detect obfuscated commands, encoded
  payloads, and living-off-the-land techniques. Uses python-evtx to extract and reconstruct multi-block scripts, applies entropy
  analysis and pattern matching for Base64-encoded commands, Invoke-Expression abuse, download cradles, and AMSI bypass attempts. Use when working with analyzing powershell script block logging.
domain: cybersecurity
tags:
- powershell
- script-block-logging
- event-id-4104
- obfuscation-detection
- windows-forensics
- endpoint-security
subdomain: security-operations
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- DE.CM-01
- RS.MA-01
- GV.OV-01
- DE.AE-02
---
# Analyzing Powershell Script Block Logging

## Overview

Cybersecurity skill for analyzing powershell script block logging. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "analyzing powershell script block logging"
- "Parse Windows PowerShell Script Block Logs (Event ID 4104) from EVTX files to de"


- When investigating security incidents that require analyzing powershell script block logging
- When building detection rules or threat hunting queries for this domain
- When SOC analysts need structured procedures for this analysis type
- When validating security monitoring coverage for related attack techniques


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Familiarity with security operations concepts and tools
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

1. **Scope the Analysis** — Define what powershell script block logging artifacts or data sources to examine and the investigation timeline.
2. **Preserve Evidence** — Create forensic copies of relevant data. Maintain chain of custody documentation.
3. **Extract Key Indicators** — Parse and extract relevant powershell script block logging data points from collected artifacts.
4. **Correlate Findings** — Cross-reference extracted data with other sources (threat intel, logs, timelines).
5. **Build Timeline** — Construct a chronological sequence of events related to powershell script block logging.
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

- [ ] All powershell script block logging procedures executed completely and documented
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