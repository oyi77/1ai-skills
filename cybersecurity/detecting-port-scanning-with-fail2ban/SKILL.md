---
name: detecting-port-scanning-with-fail2ban
description: 'Configures Fail2ban with custom filters and actions to detect port scanning activity, SSH brute force attempts,
  and network reconnaissance, automatically banning offending IP addresses and alerting security teams to suspicious network
  probing.

  '
domain: cybersecurity
tags:
- network-security
- fail2ban
- port-scanning
- intrusion-prevention
- automated-defense
subdomain: network-security
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- DE.CM-01
- ID.AM-03
- PR.DS-02
---
# Detecting Port Scanning With Fail2Ban

## Overview

Cybersecurity skill for detecting port scanning with fail2ban. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "detecting port scanning with fail2ban"
- "Configures Fail2ban with custom filters and actions to detect port scanning acti"


- Automatically blocking IP addresses that perform port scans against internet-facing servers
- Defending SSH, HTTP, FTP, and other services against brute force attacks with automated IP banning
- Creating custom detection filters for organization-specific attack patterns in log files
- Reducing noise from automated scanning bots before traffic reaches IDS/IPS for deeper analysis
- Implementing defense-in-depth by adding host-based automated response to network monitoring

**Do not use** as the sole network security control, for protecting against distributed attacks from many source IPs, or as a replacement for proper firewall rules and network segmentation.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Fail2ban 0.11+ installed (`fail2ban-client --version`)
- Root/sudo access for iptables/nftables manipulation
- Services logging connection attempts to parseable log files (syslog, auth.log, access.log)
- iptables or nftables installed and operational as the host firewall
- Optional: SMTP server for email notifications on ban events

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

1. **Define Detection Scope** — Identify the specific port scanning techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for port scanning.
3. **Build Detection Queries** — Write fail2ban queries targeting port scanning indicators. Use platform-specific query language for optimal performance.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **fail2ban** — Primary tool for this skill
- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All port scanning procedures executed completely and documented
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