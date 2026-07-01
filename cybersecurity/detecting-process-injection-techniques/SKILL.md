---
name: detecting-process-injection-techniques
description: 'Detects and analyzes process injection techniques used by malware including classic DLL injection, process hollowing,
  APC injection, thread hijacking, and reflective loading. Uses memory forensics, API monitoring, and behavioral analysis
  to identify injection artifacts. Activates for requests involving process injection detection, code injection analysis,
  hollowed process investigation, or in-memory threat detection.

  '
domain: cybersecurity
tags:
- malware
- process-injection
- detection
- memory-forensics
- defense-evasion
subdomain: malware-analysis
version: 1.0.0
author: mahipal
license: Apache-2.0
d3fend_techniques:
- Executable Denylisting
- Execution Isolation
- File Metadata Consistency Validation
- Content Format Conversion
- File Content Analysis
nist_csf:
- DE.AE-02
- RS.AN-03
- ID.RA-01
- DE.CM-01
---
# Detecting Process Injection Techniques

## Overview

Cybersecurity skill for detecting process injection techniques. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "detecting process injection techniques"
- "Detects and analyzes process injection techniques used by malware including clas"


- EDR alerts on suspicious API call sequences (VirtualAllocEx + WriteProcessMemory + CreateRemoteThread)
- A legitimate process (explorer.exe, svchost.exe) exhibits unexpected network connections or file operations
- Memory forensics reveals executable code in memory regions that should not contain it
- Investigating living-off-the-land attacks where malware hides inside trusted processes
- Building detection logic for specific injection techniques in EDR or SIEM rules

**Do not use** for standard DLL loading analysis; injection implies unauthorized code placement in a process without that process's cooperation.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Volatility 3 for memory forensics analysis of injection artifacts
- Sysmon configured with Event IDs 8 (CreateRemoteThread) and 10 (ProcessAccess)
- API Monitor or x64dbg for observing injection API calls in real-time
- Process Hacker or Process Explorer for inspecting process memory regions
- Understanding of Windows memory management (VirtualAlloc, VAD, page protections)
- Isolated analysis environment for safe malware execution and monitoring

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

1. **Define Detection Scope** — Identify the specific process injection techniques techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for process injection techniques.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting process injection techniques indicators.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All process injection techniques procedures executed completely and documented
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