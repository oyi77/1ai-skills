---
name: analyzing-linux-audit-logs-for-intrusion
description: 'Uses the Linux Audit framework (auditd) with ausearch and aureport utilities to detect intrusion attempts, unauthorized
  access, privilege escalation, and suspicious system activity. Covers audit rule configuration, log querying, timeline reconstruction,
  and integration with SIEM platforms. Activates for requests involving auditd analysis, Linux audit log investigation, ausearch
  queries, aureport summaries, or host-based intrusion detection on Linux.

  '
domain: cybersecurity
tags:
- auditd
- ausearch
- aureport
- linux-security
- intrusion-detection
- HIDS
- forensics
subdomain: incident-response
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- RS.MA-01
- RS.MA-02
- RS.AN-03
- RC.RP-01
---
# Analyzing Linux Audit Logs For Intrusion

## When to Use

- Investigating suspected unauthorized access or privilege escalation on Linux hosts
- Hunting for evidence of exploitation, backdoor installation, or persistence mechanisms
- Auditing compliance with security baselines (CIS, STIG, PCI-DSS) that require system call monitoring
- Reconstructing a timeline of attacker actions during incident response
- Detecting file tampering on critical system files such as `/etc/passwd`, `/etc/shadow`, or SSH keys

**Do not use** for network-level intrusion detection; use Suricata or Zeek for network traffic analysis. Auditd operates at the kernel level on individual hosts.

## Prerequisites

- Linux system with `auditd` package installed and the audit daemon running (`systemctl status auditd`)
- Root or sudo access to configure audit rules and query logs
- Audit rules deployed via `/etc/audit/rules.d/*.rules` or loaded with `auditctl`
- Recommended: Neo23x0/auditd ruleset from GitHub for comprehensive baseline coverage
- Familiarity with Linux syscalls (`execve`, `open`, `connect`, `ptrace`, etc.)
- Log storage with sufficient retention (default location: `/var/log/audit/audit.log`)

## Workflow

1. **Scope the Analysis** — Define what linux audit logs artifacts or data sources to examine and the investigation timeline.
2. **Preserve Evidence** — Create forensic copies of relevant data. Maintain chain of custody documentation.
3. **Extract Key Indicators** — Use intrusion to parse and extract relevant linux audit logs data points from collected artifacts.
4. **Correlate Findings** — Cross-reference extracted data with other sources (threat intel, logs, timelines).
5. **Build Timeline** — Construct a chronological sequence of events related to linux audit logs.
6. **Document Analysis** — Write findings report with evidence, conclusions, and recommendations.

## Tools

- **intrusion** — Primary tool for this skill
- **Forensic Toolkit** — Evidence collection and analysis
- **Timeline Tools** — Chronological event reconstruction
- **Log Analysis Platform** — Centralized log parsing and search

## Verification

- [ ] All linux audit logs procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
