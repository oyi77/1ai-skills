---
name: detecting-rootkit-activity
description: 'Detects rootkit presence on compromised systems by identifying hidden processes, hooked system calls, modified
  kernel structures, hidden files, and covert network connections using memory forensics, cross-view detection, and integrity
  checking techniques. Activates for requests involving rootkit detection, hidden process discovery, kernel integrity checking,
  or system call hook analysis.

  '
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

## When to Use

- System shows signs of compromise but standard tools (Task Manager, netstat) show nothing abnormal
- Antivirus/EDR detects rootkit signatures but cannot identify the specific hiding mechanism
- Memory forensics reveals discrepancies between kernel data structures and user-mode tool output
- Investigating a persistent threat that survives remediation attempts and system reboots
- Validating system integrity after a suspected kernel-level compromise

**Do not use** as a first-line detection method; start with standard malware triage and escalate to rootkit analysis when hiding behavior is suspected.

## Prerequisites

- Volatility 3 for memory forensics and kernel structure analysis
- GMER or Rootkit Revealer (Windows) for live system scanning
- rkhunter and chkrootkit (Linux) for filesystem and process integrity checks
- Sysinternals tools (Process Explorer, Autoruns, RootkitRevealer) for Windows analysis
- Memory dump from the suspected system (WinPmem, LiME)
- Clean baseline of the OS for comparison (known-good kernel module hashes)

## Workflow

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

## Verification

- [ ] All rootkit activity procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
