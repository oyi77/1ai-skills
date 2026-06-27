---
name: detecting-dcsync-attack-in-active-directory
description: Detect DCSync attacks where adversaries abuse Active Directory replication privileges to extract password hashes
  by monitoring for non-domain-controller accounts requesting directory replication via DsGetNCChanges.
domain: cybersecurity
tags:
- threat-hunting
- active-directory
- dcsync
- credential-theft
- mitre-t1003-006
- mimikatz
- kerberos
subdomain: threat-hunting
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- Application Protocol Command Analysis
- Network Isolation
- Network Traffic Analysis
- Client-server Payload Profiling
- Platform Monitoring
nist_csf:
- DE.CM-01
- DE.AE-02
- DE.AE-07
- ID.RA-05
---
# Detecting Dcsync Attack In Active Directory

## When to Use

- When hunting for credential theft in Active Directory environments
- After compromise of accounts with Replicating Directory Changes permissions
- When investigating suspected use of Mimikatz or Impacket secretsdump
- During incident response involving lateral movement with domain admin credentials
- When auditing AD replication permissions as part of security hardening

## Prerequisites

- Windows Security Event Logs with Event ID 4662 (Object Access) enabled
- Advanced Audit Policy: Audit Directory Service Access enabled
- Domain Controller event forwarding to SIEM
- Knowledge of legitimate domain controller hostnames and IPs
- Directory Service Access auditing with SACL on domain object

## Workflow

1. **Define Detection Scope** — Identify the specific dcsync attack in active directory techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for dcsync attack in active directory.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting dcsync attack in active directory indicators.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All dcsync attack in active directory procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
