---
name: hunting-for-data-staging-before-exfiltration
description: Detect data staging activity before exfiltration by monitoring for archive creation with 7-Zip/RAR, unusual temp
  folder access, large file consolidation, and staging directory patterns via EDR and process telemetry
domain: cybersecurity
subdomain: threat-hunting
tags:
- data-staging
- exfiltration
- t1074
- archive-detection
- edr
- threat-hunting
- dlp
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- File Metadata Consistency Validation
- Content Format Conversion
- File Content Analysis
- Platform Hardening
- File Format Verification
nist_csf:
- DE.CM-01
- DE.AE-02
- DE.AE-07
- ID.RA-05
---

# Hunting for Data Staging Before Exfiltration

## Overview

Before exfiltrating data, adversaries typically stage collected files in a central location (MITRE ATT&CK T1074). This involves creating archives with tools like 7-Zip, RAR, or tar, consolidating files from multiple directories, and using temporary or hidden staging directories. This skill detects staging behavior by analyzing process creation logs for archiver activity, monitoring file system events in common staging paths, and identifying anomalous file consolidation patterns.


## When to Use

- When investigating security incidents that require hunting for data staging before exfiltration
- When building detection rules or threat hunting queries for this domain
- When SOC analysts need structured procedures for this analysis type
- When validating security monitoring coverage for related attack techniques

## Prerequisites

- EDR or Sysmon telemetry with process creation and file system events
- Windows Event Logs (Event ID 4688) or Sysmon Event ID 1, 11
- Python 3.8+ with standard library
- Access to process creation logs in JSON/CSV format

## Steps

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

1. **Detect Archive Tool Execution** — Monitor for 7z.exe, rar.exe, tar, zip, and WinRAR process creation with compression arguments
2. **Identify Staging Directories** — Flag file writes to common staging locations (Recycle Bin, %TEMP%, ProgramData, hidden directories)
3. **Detect Large File Consolidation** — Identify patterns of multiple file reads followed by writes to a single directory
4. **Monitor Sensitive Path Access** — Track bulk reads from document directories, database paths, and network shares
5. **Analyze Archive Metadata** — Extract and analyze archive file sizes, creation times, and source paths
6. **Score Staging Risk** — Apply heuristic scoring based on archive size, source diversity, staging path suspicion, and timing
7. **Generate Hunt Report** — Produce a structured report with staging event timeline and MITRE ATT&CK mapping

## Expected Output

- JSON report of detected staging events with risk scores
- Archive creation timeline with source file analysis
- MITRE ATT&CK mapping (T1074.001, T1074.002, T1560)
- Staging directory heat map showing suspicious write activity
## When NOT to Use

- You're responding to a known incident (use IR skills)
- Task is about analyzing confirmed malware (use analyzing-* skills)
- You need to implement detection rules (use implementing-* skills)
- Task is about vulnerability scanning (use scanning tools)
- You don't have access to endpoint/network data
- Task requires compliance auditing (use auditing-* skills)


## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Acting on threat intelligence without validating source reliability
- Sharing classified or sensitive indicators without proper handling procedures
- Alerting threat actors to detection capabilities through visible response actions
## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Results validated against known-good baselines or reference implementations
- Documentation complete enough for another analyst to reproduce findings

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |