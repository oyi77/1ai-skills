---
name: analyzing-bootkit-and-rootkit-samples
description: 'Analyzes bootkit and advanced rootkit malware that infects the Master Boot Record (MBR), Volume Boot Record
  (VBR), or UEFI firmware to gain persistence below the operating system. Covers boot sector analysis, UEFI module inspection,
  and anti-rootkit detection techniques. Activates for requests involving bootkit analysis, MBR malware investigation, UEFI
  persistence analysis, or pre-OS malware detection.

  '
domain: cybersecurity
tags:
- malware
- bootkit
- rootkit
- UEFI
- MBR-analysis
subdomain: malware-analysis
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- DE.AE-02
- RS.AN-03
- ID.RA-01
- DE.CM-01
---
# Analyzing Bootkit And Rootkit Samples

## Overview

Cybersecurity skill for analyzing bootkit and rootkit samples. Follows industry best practices and security standards.

## When to Use

- A system shows signs of compromise that persist through OS reinstallation
- Antivirus and EDR are unable to detect malware despite clear evidence of compromise
- UEFI Secure Boot has been disabled or shows integrity violations
- Memory forensics reveals rootkit behavior (hidden processes, hooked system calls)
- Investigating nation-state level threats known to deploy bootkits (APT28, APT41, Equation Group)

**Do not use** for standard user-mode malware; bootkits and rootkits operate at a fundamentally different level requiring specialized analysis techniques.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Disk imaging tools (dd, FTK Imager) for acquiring MBR/VBR sectors
- UEFITool for UEFI firmware volume analysis and module extraction
- chipsec for hardware-level firmware security assessment
- Ghidra with x86 real-mode and 16-bit support for MBR code analysis
- Volatility 3 for kernel-level rootkit artifact detection
- Bootable Linux live USB for offline system analysis

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

1. **Scope the Analysis** — Define what bootkit and rootkit samples artifacts or data sources to examine and the investigation timeline.
2. **Preserve Evidence** — Create forensic copies of relevant data. Maintain chain of custody documentation.
3. **Extract Key Indicators** — Parse and extract relevant bootkit and rootkit samples data points from collected artifacts.
4. **Correlate Findings** — Cross-reference extracted data with other sources (threat intel, logs, timelines).
5. **Build Timeline** — Construct a chronological sequence of events related to bootkit and rootkit samples.
6. **Document Analysis** — Write findings report with evidence, conclusions, and recommendations.

## Tools

- **Forensic Toolkit** — Evidence collection and analysis
- **Timeline Tools** — Chronological event reconstruction
- **Log Analysis Platform** — Centralized log parsing and search

## Verification

- [ ] All bootkit and rootkit samples procedures executed completely and documented
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