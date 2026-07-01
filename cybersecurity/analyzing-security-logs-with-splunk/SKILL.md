---
name: analyzing-security-logs-with-splunk
description: 'Leverages Splunk Enterprise Security and SPL (Search Processing Language) to investigate security incidents
  through log correlation, timeline reconstruction, and anomaly detection. Covers Windows event logs, firewall logs, proxy
  logs, and authentication data analysis. Activates for requests involving Splunk investigation, SPL queries, SIEM log analysis,
  security event correlation, or log-based incident investigation.

  '
domain: cybersecurity
tags:
- splunk
- SPL
- SIEM
- log-analysis
- security-monitoring
subdomain: incident-response
mitre_attack:
- T1070
- T1562
- T1059
version: 1.0.0
author: mahipal
license: Apache-2.0
atlas_techniques:
- AML.T0070
- AML.T0066
- AML.T0082
d3fend_techniques:
- Executable Denylisting
- Execution Isolation
- File Metadata Consistency Validation
- Content Format Conversion
- File Content Analysis
nist_ai_rmf:
- MEASURE-2.7
- MAP-5.1
- MANAGE-2.4
- MANAGE-3.1
- MEASURE-3.1
nist_csf:
- RS.MA-01
- RS.MA-02
- RS.AN-03
- RC.RP-01
---
# Analyzing Security Logs With Splunk

## Overview

Cybersecurity skill for analyzing security logs with splunk. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "analyzing security logs with splunk"
- "Leverages Splunk Enterprise Security and SPL (Search Processing Language) to inv"


- Investigating a security incident that requires correlation across multiple log sources
- Hunting for adversary activity using known TTPs and IOCs
- Building detection rules for specific attack patterns
- Reconstructing an incident timeline from disparate log sources
- Analyzing authentication anomalies, lateral movement, or data exfiltration patterns

**Do not use** for real-time packet-level analysis; use Wireshark or Zeek for full packet capture analysis.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Splunk Enterprise or Splunk Cloud with Enterprise Security (ES) app installed
- Log sources ingested: Windows Event Logs (via Splunk Universal Forwarder or WEF), firewall, proxy, DNS, EDR, email gateway
- Splunk CIM (Common Information Model) data models configured for normalized field names
- SPL proficiency at intermediate level or higher
- Role-based access with `search` and `accelerate_search` capabilities in Splunk

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

1. **Scope the Analysis** — Define what security logs artifacts or data sources to examine and the investigation timeline.
2. **Preserve Evidence** — Create forensic copies of relevant data. Maintain chain of custody documentation.
3. **Extract Key Indicators** — Use splunk to parse and extract relevant security logs data points from collected artifacts.
4. **Correlate Findings** — Cross-reference extracted data with other sources (threat intel, logs, timelines).
5. **Build Timeline** — Construct a chronological sequence of events related to security logs.
6. **Document Analysis** — Write findings report with evidence, conclusions, and recommendations.

## Tools

- **splunk** — Primary tool for this skill
- **Forensic Toolkit** — Evidence collection and analysis
- **Timeline Tools** — Chronological event reconstruction
- **Log Analysis Platform** — Centralized log parsing and search

## Verification

- [ ] All security logs procedures executed completely and documented
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