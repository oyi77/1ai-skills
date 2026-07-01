---
name: analyzing-persistence-mechanisms-in-linux
description: Detect and analyze Linux persistence mechanisms including crontab entries, systemd service units, LD_PRELOAD
  hijacking, bashrc modifications, and authorized_keys backdoors using auditd and file integrity monitoring
domain: cybersecurity
subdomain: threat-hunting
tags:
- linux-persistence
- crontab
- systemd
- ld-preload
- auditd
- threat-hunting
- incident-response
mitre_attack:
- T1053.003
- T1543.002
- T1574.006
- T1546.004
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- Executable Denylisting
- Execution Isolation
- File Metadata Consistency Validation
- Process Termination
- Content Format Conversion
nist_csf:
- DE.CM-01
- DE.AE-02
- DE.AE-07
- ID.RA-05
---

# Analyzing Persistence Mechanisms in Linux

## Overview

Adversaries establish persistence on Linux systems through crontab jobs, systemd service/timer units, LD_PRELOAD library injection, shell profile modifications (.bashrc, .profile), SSH authorized_keys backdoors, and init script manipulation. This skill scans for all known persistence vectors, checks file timestamps and integrity, and correlates findings with auditd logs to build a timeline of persistence installation.


## When to Use
**Trigger phrases:**
- "analyzing persistence mechanisms in linux"
- "Detect and analyze Linux persistence mechanisms including crontab entries, syste"


- When investigating security incidents that require analyzing persistence mechanisms in linux
- When building detection rules or threat hunting queries for this domain
- When SOC analysts need structured procedures for this analysis type
- When validating security monitoring coverage for related attack techniques

## Prerequisites

- Root or sudo access on target Linux system (or forensic image)
- auditd configured with file watch rules on persistence paths
- Python 3.8+ with standard library (os, subprocess, json)
- Optional: OSSEC/Wazuh agent for file integrity monitoring alerts

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

1. **Scan Crontab Entries** — Enumerate all user crontabs, /etc/cron.d/, /etc/cron.daily/, and anacron jobs for suspicious commands
2. **Audit Systemd Units** — Check /etc/systemd/system/ and ~/.config/systemd/user/ for non-package-managed service and timer units
3. **Detect LD_PRELOAD Hijacking** — Check /etc/ld.so.preload and LD_PRELOAD environment variable for injected shared libraries
4. **Inspect Shell Profiles** — Scan .bashrc, .bash_profile, .profile, /etc/profile.d/ for injected commands or reverse shells
5. **Check SSH Authorized Keys** — Audit all authorized_keys files for unauthorized public keys with command restrictions
6. **Correlate Auditd Logs** — Search auditd logs for file modification events on persistence paths to build an installation timeline
7. **Generate Persistence Report** — Produce a risk-scored report of all discovered persistence mechanisms

## Expected Output

- JSON report of all persistence mechanisms found with risk scores
- Timeline of persistence installation from auditd correlation
- MITRE ATT&CK technique mapping (T1053, T1543, T1574, T1546)
- Remediation commands for each detected persistence mechanism
## When NOT to Use

- You need to perform the attack, not analyze it (use performing-* skills)
- Task is about detection, not analysis (use detecting-* skills)
- You need to implement controls (use implementing-* skills)
- Task is about threat hunting, not post-incident analysis (use hunting-* skills)
- You don't have access to the artifacts/logs to analyze
- Task requires real-time monitoring (use SOC tools)


## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Sharing sensitive findings or credentials in unencrypted communications
- Failing to properly scope and contain the assessment before starting
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