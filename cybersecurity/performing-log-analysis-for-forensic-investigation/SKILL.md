---
name: performing-log-analysis-for-forensic-investigation
description: Collect, parse, and correlate system, application, and security logs to reconstruct events and establish timelines
  during forensic investigations. Use when working with performing log analysis for forensic investigation.
domain: cybersecurity
tags:
- forensics
- log-analysis
- siem
- event-correlation
- timeline-analysis
- evidence-collection
subdomain: digital-forensics
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- RS.AN-01
- RS.AN-03
- DE.AE-02
- RS.MA-01
---
# Performing Log Analysis For Forensic Investigation

## Overview

Cybersecurity skill for performing log analysis for forensic investigation. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "performing log analysis for forensic investigation"
- "Collect, parse, and correlate system, application, and security logs to reconstr"

- When reconstructing the timeline of a security incident from available log sources
- During post-breach investigation to identify initial access, lateral movement, and exfiltration
- When correlating events across multiple systems and log sources
- For establishing evidence of unauthorized access or policy violations
- When preparing forensic reports requiring detailed event chronology


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites
- Access to collected log files (Windows Event Logs, syslog, application logs)
- Log parsing tools (LogParser, jq, awk, or ELK stack)
- Understanding of log formats (EVTX, syslog, JSON, CSV)
- NTP-synchronized timestamps across all log sources for correlation
- Sufficient storage for log aggregation and indexing
- Timeline analysis tools (log2timeline, Plaso)

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

1. **Plan Operations** — Define objectives, scope, and success criteria for log analysis operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for log analysis.
3. **Execute Core Workflow** — Use forensic investigation to perform log analysis operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **forensic investigation** — Primary tool for this skill
- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- [ ] All log analysis procedures executed completely and documented
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