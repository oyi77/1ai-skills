---
name: hunting-for-persistence-mechanisms-in-windows
description: Use when systematically hunt for adversary persistence mechanisms across
  Windows endpoints including registry, services, startup folders, and WMI subscriptions.
  Use when working with hunting for persistence mechanisms in windows.
domain: cybersecurity
tags:
- threat-hunting
- mitre-attack
- persistence
- windows
- registry
- siem
- proactive-detection
subdomain: threat-hunting
version: '1.0'
author: oyi77
license: Apache-2.0
d3fend_techniques:
- Executable Denylisting
- Execution Isolation
- File Metadata Consistency Validation
- Content Format Conversion
- File Content Analysis
nist_csf:
- DE.CM-01
- DE.AE-02
- DE.AE-07
- ID.RA-05
category: cybersecurity
---

# Hunting For Persistence Mechanisms In Windows

## Overview

Cybersecurity skill for hunting for persistence mechanisms in windows. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "hunting for persistence mechanisms in windows"
- "Systematically hunt for adversary persistence mechanisms across Windows endpoint"


- During periodic proactive threat hunts for dormant backdoors
- After an incident to identify all persistence mechanisms an attacker planted
- When investigating unusual services, scheduled tasks, or startup entries
- When threat intel reports describe new persistence techniques in the wild
- During security posture assessments to identify unauthorized persistent software


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Sysmon deployed with Event IDs 12/13/14 (Registry), 19/20/21 (WMI), 1 (Process Creation)
- Windows Security Event forwarding for 4697 (Service Install), 4698 (Scheduled Task)
- EDR with registry and file monitoring capabilities
- PowerShell script block logging enabled (Event ID 4104)
- Autoruns or equivalent baseline of legitimate persistent entries

## Workflow

1. **Define scope and authorization** — identify hosts, accounts, and registry/run locations in scope; obtain written authorization and change-management approval before touching any host; document evidence-handling rules.
2. **Establish a baseline** — collect clean persistence state from known-good systems (Run keys, RunOnce, scheduled tasks, WMI subscriptions, services, browser helper objects, browser extensions, shell extensions, boot execute, and common startup folders).
3. **Collect persistence evidence per host** — query registry keys (HKLM/HKCU \Software\Microsoft\Windows\CurrentVersion\Run/RunOnce/RunOnceEx, AppInit_DLLs, LSA, Image File Execution Options), Scheduled Tasks, WMI event consumers (Win32_ProcessorCommandLineEvent, __FilterToConsumerBinding), services (sc query state), startup folders (%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup and %ProgramData%\Microsoft\Windows\Start Menu\Programs\Startup), and scheduled tasks (schtasks /query /fo CSV /v).
4. **Baseline comparison** — diff current persistence state against the known-good baseline; flag new entries, changed hashes, suspicious parent processes, suspicious service accounts, and binaries in temp/user temp paths.
5. **Enrich and correlate** — resolve file hashes against threat-intel feeds, check file creation/modification timestamps against first-seen execution timestamps, correlate parent processes and scheduled-task owners with authorized admins/service accounts.
6. **Triage and document** — assign each hit one of: known-good/expected, false positive, suspicious-unconfirmed, confirmed-malicious; record artifact, hash, timestamp, source, and remediation action.
7. **Remediate and document** — remove unauthorized persistence only with owner approval; document each removal (what, where, how, who approved); preserve evidence of removed artifacts for forensic review.

## Tools

- **persistence mechanisms in windows** — Primary tool for this skill
- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis


## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- [ ] All  procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |