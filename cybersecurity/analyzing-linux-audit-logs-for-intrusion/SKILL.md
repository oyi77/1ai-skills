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

## Overview

Cybersecurity skill for analyzing linux audit logs for intrusion. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "analyzing linux audit logs for intrusion"
- "Uses the Linux Audit framework (auditd) with ausearch and aureport utilities to "


- Investigating suspected unauthorized access or privilege escalation on Linux hosts
- Hunting for evidence of exploitation, backdoor installation, or persistence mechanisms
- Auditing compliance with security baselines (CIS, STIG, PCI-DSS) that require system call monitoring
- Reconstructing a timeline of attacker actions during incident response
- Detecting file tampering on critical system files such as `/etc/passwd`, `/etc/shadow`, or SSH keys

**Do not use** for network-level intrusion detection; use Suricata or Zeek for network traffic analysis. Auditd operates at the kernel level on individual hosts.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Linux system with `auditd` package installed and the audit daemon running (`systemctl status auditd`)
- Root or sudo access to configure audit rules and query logs
- Audit rules deployed via `/etc/audit/rules.d/*.rules` or loaded with `auditctl`
- Recommended: Neo23x0/auditd ruleset from GitHub for comprehensive baseline coverage
- Familiarity with Linux syscalls (`execve`, `open`, `connect`, `ptrace`, etc.)
- Log storage with sufficient retention (default location: `/var/log/audit/audit.log`)

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

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |