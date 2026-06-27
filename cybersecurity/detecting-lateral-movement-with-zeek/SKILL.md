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

## When to Use

- Hunting for lateral movement after an initial compromise indicator is found on one endpoint
- Investigating suspected NTLM account spray or Pass-the-Ticket attacks across the internal network
- Monitoring SMB traffic for unauthorized file transfers to admin shares (C$, ADMIN$, IPC$)
- Detecting remote service execution via DCE/RPC (PsExec, schtasks, WMI lateral patterns)
- Building alerting rules for internal network anomalies in a Zeek-based NSMP deployment
- Performing post-incident timeline reconstruction using Zeek logs as a network-level evidence source

**Do not use** as a standalone detection mechanism. Zeek sees network traffic only; combine with endpoint telemetry (Sysmon, EDR) for full visibility. Encrypted SMB3 traffic may limit Zeek's visibility into file-level details.

## Prerequisites

- Zeek 6.0+ deployed on a network tap or SPAN port monitoring internal VLAN traffic
- Zeek SMB analyzer enabled (loaded by default: `@load base/protocols/smb`)
- Zeek DCE/RPC analyzer enabled (`@load base/protocols/dce-rpc`)
- Zeek Kerberos analyzer enabled (`@load base/protocols/krb`)
- Python 3.8+ (standard library only)
- Access to Zeek log directory (default: `/opt/zeek/logs/current/`)
- Familiarity with Zeek TSV log format (fields separated by `\t`, header lines prefixed with `#`)

## Workflow

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
