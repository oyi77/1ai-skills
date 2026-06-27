---
name: collecting-volatile-evidence-from-compromised-host
description: Collect volatile forensic evidence from a compromised system following order of volatility, preserving memory,
  network connections, processes, and system state before they are lost.
domain: cybersecurity
tags:
- incident-response
- dfir
- forensics
- volatile-evidence
- memory-forensics
- chain-of-custody
subdomain: incident-response
mitre_attack:
- T1003
- T1055
- T1059
- T1547
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- RS.MA-01
- RS.MA-02
- RS.AN-03
- RC.RP-01
---
# Collecting Volatile Evidence From Compromised Host

## When to Use
- Security incident confirmed and compromised host identified
- Before system isolation, shutdown, or remediation begins
- Memory-resident malware suspected (fileless attacks)
- Need to capture network connections, running processes, and system state
- Legal proceedings may require forensic evidence preservation
- Incident requires root cause analysis with volatile data

## Prerequisites
- Forensic collection toolkit on USB or network share (trusted tools)
- WinPmem/LiME for memory acquisition
- Write-blocker or forensic workstation for disk imaging
- Chain of custody documentation forms
- Secure evidence storage with integrity verification
- Authorization to collect evidence (legal/HR approval for insider cases)

## Workflow

1. **Define Objectives** — Clarify the goals and scope for volatile evidence from compromised host.
2. **Gather Resources** — Collect tools, data, and access needed for volatile evidence from compromised host.
3. **Execute Process** — Carry out volatile evidence from compromised host operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All volatile evidence from compromised host procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
