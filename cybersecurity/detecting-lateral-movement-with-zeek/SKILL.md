---
name: detecting-lateral-movement-with-zeek
description: 'Detect lateral movement in network traffic using Zeek (formerly Bro) log analysis. Parses conn.log, smb_mapping.log,
  smb_files.log, dce_rpc.log, kerberos.log, and ntlm.log to identify SMB file transfers, NTLM account spray activity, remote
  service execution, and anomalous internal connections.

  '
domain: cybersecurity
tags:
- zeek
- lateral-movement
- smb
- dce-rpc
- ntlm-spray
- network-forensics
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
# Detecting Lateral Movement With Zeek

## Overview

Cybersecurity skill for detecting lateral movement with zeek. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "detecting lateral movement with zeek"
- "Detect lateral movement in network traffic using Zeek (formerly Bro) log analysi"


- Hunting for lateral movement after an initial compromise indicator is found on one endpoint
- Investigating suspected NTLM account spray or Pass-the-Ticket attacks across the internal network
- Monitoring SMB traffic for unauthorized file transfers to admin shares (C$, ADMIN$, IPC$)
- Detecting remote service execution via DCE/RPC (PsExec, schtasks, WMI lateral patterns)
- Building alerting rules for internal network anomalies in a Zeek-based NSMP deployment
- Performing post-incident timeline reconstruction using Zeek logs as a network-level evidence source

**Do not use** as a standalone detection mechanism. Zeek sees network traffic only; combine with endpoint telemetry (Sysmon, EDR) for full visibility. Encrypted SMB3 traffic may limit Zeek's visibility into file-level details.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Zeek 6.0+ deployed on a network tap or SPAN port monitoring internal VLAN traffic
- Zeek SMB analyzer enabled (loaded by default: `@load base/protocols/smb`)
- Zeek DCE/RPC analyzer enabled (`@load base/protocols/dce-rpc`)
- Zeek Kerberos analyzer enabled (`@load base/protocols/krb`)
- Python 3.8+ (standard library only)
- Access to Zeek log directory (default: `/opt/zeek/logs/current/`)
- Familiarity with Zeek TSV log format (fields separated by `\t`, header lines prefixed with `#`)

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

1. **Define Detection Scope** — Identify the specific lateral movement techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for lateral movement.
3. **Build Detection Queries** — Write zeek queries targeting lateral movement indicators. Use platform-specific query language for optimal performance.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **zeek** — Primary tool for this skill
- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All lateral movement procedures executed completely and documented
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