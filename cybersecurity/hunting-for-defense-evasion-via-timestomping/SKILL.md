---
name: hunting-for-defense-evasion-via-timestomping
description: 'Detect NTFS timestamp manipulation (MITRE T1070.006) by comparing $STANDARD_INFORMATION vs $FILE_NAME timestamps
  in the MFT. Uses analyzeMFT and Python to identify files with anomalous temporal patterns indicating anti-forensic timestomping
  activity.

  '
domain: cybersecurity
tags:
- timestomping
- ntfs-forensics
- mft-analysis
- defense-evasion
subdomain: threat-hunting
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
# Hunting For Defense Evasion Via Timestomping

## Overview

Cybersecurity skill for hunting for defense evasion via timestomping. Follows industry best practices and security standards.

## When to Use

- Investigating suspected anti-forensic activity where an adversary may have altered file timestamps to blend malware into legitimate directories
- Threat hunting for defense evasion (MITRE ATT&CK T1070.006) across compromised Windows systems
- Validating timeline integrity during forensic examinations of disk images or live acquisitions
- Triaging suspicious files that appear to have creation dates older than the OS installation or inconsistent with known deployment timelines
- Detecting tools like Timestomp (Metasploit), NTimeStomp, SetMACE, or PowerShell Set-ItemProperty used to alter timestamps
- Building automated detection pipelines that flag temporal anomalies in MFT data for SOC analysts

**Do not use** as the sole detection method; advanced adversaries can manipulate both $STANDARD_INFORMATION and $FILE_NAME timestamps (though the latter requires raw disk access and is much harder). Combine with USN Journal, $LogFile, and ShimCache/Amcache analysis for corroboration.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Raw $MFT file extracted from a Windows system (via FTK Imager, KAPE, or live extraction)
- `MFTECmd` (Eric Zimmerman tool) or `analyzeMFT` for MFT parsing
- Python 3.8+ with `pandas` for analysis
- Optional: `mft` Python library (`pip install mft`) for programmatic MFT parsing
- Optional: KAPE (Kroll Artifact Parser and Extractor) for automated artifact collection
- Timeline Explorer or Excel for visual analysis of parsed MFT output

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

1. **Define Detection Scope** — Identify the specific  techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for .
3. **Build Detection Queries** — Write defense evasion via timestomping queries targeting  indicators. Use platform-specific query language for optimal performance.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **defense evasion via timestomping** — Primary tool for this skill
- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All  procedures executed completely and documented
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