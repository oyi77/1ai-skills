---
name: detecting-rootkit-activity
description: 'Detects rootkit presence on compromised systems by identifying hidden processes, hooked system calls, modified
  kernel structures, hidden files, and covert network connections using memory forensics, cross-view detection, and integrity
  checking techniques. Activates for requests involving rootkit detection, hidden process discovery, kernel integrity checking,
  or system call hook analysis.

  '. Use when working with detecting rootkit activity.
domain: cybersecurity
tags:
- malware
- rootkit
- detection
- kernel-analysis
- memory-forensics
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
# Detecting Rootkit Activity

## Overview

Cybersecurity skill for detecting rootkit activity. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "detecting rootkit activity"
- "Detects rootkit presence on compromised systems by identifying hidden processes,"


- System shows signs of compromise but standard tools (Task Manager, netstat) show nothing abnormal
- Antivirus/EDR detects rootkit signatures but cannot identify the specific hiding mechanism
- Memory forensics reveals discrepancies between kernel data structures and user-mode tool output
- Investigating a persistent threat that survives remediation attempts and system reboots
- Validating system integrity after a suspected kernel-level compromise

**Do not use** as a first-line detection method; start with standard malware triage and escalate to rootkit analysis when hiding behavior is suspected.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Volatility 3 for memory forensics and kernel structure analysis
- GMER or Rootkit Revealer (Windows) for live system scanning
- rkhunter and chkrootkit (Linux) for filesystem and process integrity checks
- Sysinternals tools (Process Explorer, Autoruns, RootkitRevealer) for Windows analysis
- Memory dump from the suspected system (WinPmem, LiME)
- Clean baseline of the OS for comparison (known-good kernel module hashes)

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

1. **Define Detection Scope** — Identify the specific rootkit activity techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for rootkit activity.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting rootkit activity indicators.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis


## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- [ ] All rootkit activity procedures executed completely and documented
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