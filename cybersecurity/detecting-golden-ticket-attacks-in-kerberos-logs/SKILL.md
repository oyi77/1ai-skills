---
name: detecting-golden-ticket-attacks-in-kerberos-logs
description: Detect Golden Ticket attacks in Active Directory by analyzing Kerberos TGT anomalies including mismatched encryption
  types, impossible ticket lifetimes, non-existent accounts, and forged PAC signatures in domain controller event logs.
domain: cybersecurity
tags:
- threat-hunting
- golden-ticket
- kerberos
- active-directory
- mitre-t1558-001
- credential-abuse
subdomain: threat-hunting
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- DE.CM-01
- DE.AE-02
- DE.AE-07
- ID.RA-05
---
# Detecting Golden Ticket Attacks In Kerberos Logs

## When to Use

- When KRBTGT account hash may have been compromised via DCSync or NTDS.dit extraction
- When hunting for forged Kerberos tickets used for persistent domain access
- After incident response reveals credential theft at the domain level
- When investigating impossible logon patterns (users logging in from multiple locations simultaneously)
- During post-breach assessment to determine if Golden Tickets are in use

## Prerequisites

- Windows Security Event IDs 4768, 4769, 4771 on domain controllers
- Kerberos policy configuration knowledge (max ticket lifetime, encryption types)
- Domain controller audit policy enabling Kerberos Service Ticket Operations
- SIEM with ability to correlate Kerberos events across multiple DCs

## Workflow

1. **Define Detection Scope** — Identify the specific golden ticket attacks in kerberos logs techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for golden ticket attacks in kerberos logs.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting golden ticket attacks in kerberos logs indicators.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All golden ticket attacks in kerberos logs procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
