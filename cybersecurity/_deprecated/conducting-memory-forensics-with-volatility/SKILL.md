---
name: conducting-memory-forensics-with-volatility
description: 'Performs memory forensics analysis using Volatility 3 to extract evidence of malware execution, process injection,
  network connections, and credential theft from RAM dumps captured during incident response. Covers memory acquisition, process
  analysis, DLL inspection, and malware detection. Activates for requests involving memory forensics, RAM analysis, Volatility
  framework, memory dump investigation, volatile evidence analysis, or live memory acquisition.

  '
domain: cybersecurity
tags:
- memory-forensics
- volatility
- RAM-analysis
- process-injection
- DFIR
subdomain: incident-response
mitre_attack:
- T1003
- T1055
- T1620
- T1574
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- RS.MA-01
- RS.MA-02
- RS.AN-03
- RC.RP-01
---
# Conducting Memory Forensics With Volatility

## Overview

Cybersecurity skill for conducting memory forensics with volatility. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "conducting memory forensics with volatility"
- "Performs memory forensics analysis using Volatility 3 to extract evidence of mal"


- An endpoint has been contained during an active incident and volatile evidence must be preserved
- EDR alerts suggest process injection or fileless malware that only exists in memory
- Encryption keys need to be recovered from a ransomware-infected system before shutdown
- Credential theft (Mimikatz, LSASS dumping) is suspected and evidence must be confirmed
- A rootkit or kernel-level compromise is suspected and disk-based analysis is insufficient

**Do not use** for analyzing disk images or file system artifacts; use disk forensics tools (Autopsy, FTK) for those tasks.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Memory acquisition tool deployed or available: WinPmem, Magnet RAM Capture, DumpIt, or AVML (Linux)
- Volatility 3 installed with Python 3.8+ and required symbol tables
- Sufficient storage for memory dumps (equal to system RAM size, typically 8-64 GB)
- YARA rules for malware detection in memory (Florian Roth's signature-base, custom rules)
- Reference baseline of normal processes and DLLs for the OS version being analyzed
- Chain of custody documentation for evidence handling

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

1. **Scope the Analysis** — Define what memory forensics artifacts or data sources to examine and the investigation timeline.
2. **Preserve Evidence** — Create forensic copies of relevant data. Maintain chain of custody documentation.
3. **Extract Key Indicators** — Use volatility to parse and extract relevant memory forensics data points from collected artifacts.
4. **Correlate Findings** — Cross-reference extracted data with other sources (threat intel, logs, timelines).
5. **Build Timeline** — Construct a chronological sequence of events related to memory forensics.
6. **Document Analysis** — Write findings report with evidence, conclusions, and recommendations.

## Tools

- **volatility** — Primary tool for this skill
- **Forensic Toolkit** — Evidence collection and analysis
- **Timeline Tools** — Chronological event reconstruction
- **Log Analysis Platform** — Centralized log parsing and search

## Verification

- [ ] All memory forensics procedures executed completely and documented
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