---
name: blue-team-tools-catalog
description: Use when querying, evaluating, or orchestrating 70+ defensive security tools from the A-poc/BlueTeam-Tools index across threat hunting, network discovery, vulnerability management, security monitoring, and forensics.
domain: cybersecurity
subdomain: threat-hunting
category: cybersecurity
version: 1.0.0
author: oyi77
license: Apache-2.0
tags:
- blue-team
- defense
- threat-hunting
- incident-response
- soc
triggers:
- blue team tools
- defensive security tools
- threat hunting toolkit
- blue team tips
- security monitoring tools
---

# Blue Team Tools Catalog

## Process
1. Scope by threat model.
2. Select tool category index.
3. Validate prerequisites.
4. Execute operational guidance.
5. Verify with checklist.

## Overview

Comprehensive reference index cataloging 70+ tools and practical techniques from the curated A-poc/BlueTeam-Tools repository. Provides operational guidance across threat hunting, vulnerability scanning, security monitoring, forensics, and incident response.

```bash
exiftool -PDF-update:all= suspicious.pdf > recovered_metadata.txt
grep -Ei '(xmr\.|pool\.com|pool\.org)' /var/log/squid/access.log | sort | uniq -c | sort -rn | head
```
## When to Use

**Trigger phrases:**
- "blue team tools catalog"
- "lookup defensive security tooling"
- "find security monitoring and detection tools"
- "blue team tips and mitigation playbooks"

- Identifying specialized defensive software for SOC and blue team operational requirements
- Evaluating open-source and commercial threat hunting, network mapping, and log analysis solutions
- Implementing practical blue team hardening tips (e.g., GPO script execution prevention, proxy cryptojacking detection)
- Cross-referencing tooling for ISO 27001, NIST CSF, and CIS benchmark operational alignment

## When NOT to Use

- When conducting red team exercises or active exploitation (use `cybersecurity/role-penetration-tester`)
- When seeking deep automated implementation instructions for a single tool (use specialized individual skills)

## Prerequisites

- Standard Linux/Windows administrative environment
- Knowledge of network defense architectures and log forwarding concepts

## Core Blue Team Tips

- **Payload Extraction via Process Hacker:** Monitor memory for newly spawned processes loading .NET assemblies; dump assemblies directly without manual de-obfuscation.
- **Prevent Script Execution via Double-Click:** Reassign default application for `.vbs`, `.js`, `.vba`, and `.hta` to `notepad.exe` via Group Policy.
- **Detect Cryptojacking via Proxy Logs:** Filter egress logs for mining pool connections matching `*xmr.*`, `*pool.com`, or `*pool.org`.
- **Remove Null Bytes in CyberChef:** Use the "Remove null bytes" operation after base64 decoding Unicode strings to restore legible script bodies.
- **Recover Scrubbed PDF Metadata:** Extract incremental metadata history using `exiftool -PDF-update:all= file.pdf`.

## Tool Category Index

| Category | Primary Tools | Operational Function |
|---|---|---|
| Threat Hunting | `hunt.io`, `threathunt.app`, `Validin` | Adversary infrastructure tracking, passive DNS, hunting maturity |
| Network Discovery | `Nmap`, `Nuclei`, `Masscan`, `ZMap`, `Shodan` | Port discovery, vulnerability template scanning, internet-wide mapping |
| Vulnerability Management | `OpenVAS`, `Nessus`, `Nexpose`, `Lynis` | Host/service auditing, CIS compliance scanning, patch prioritization |
| Security Monitoring | `Sysmon`, `Logstash`, `Kibana`, `maltrail`, `procfilter` | Endpoint telemetry, log pipeline ETL, malicious traffic interception |
| DFIR & Recovery | `Autopsy`, `The Sleuth Kit`, `TestDisk`, `Extundelete` | Bit-stream disk analysis, timeline reconstruction, partition salvage |

## Anti-Rationalization Table

| Excuse | Flawed Rationalization | Required Discipline |
|---|---|---|
| "We already have an AV, we don't need dedicated hunting tools" | "Endpoint AV catches all attacks." | Modern threats use living-off-the-land techniques; proactive hunting via threat platforms and Sysmon is essential. |
| "Default Windows associations are safe enough" | "Users won't click untrusted files." | Double-click script execution remains a top initial access vector; enforce notepad association via GPO. |

## Verification Checklist

- [ ] Defensive tool capabilities matched against threat model
- [ ] GPO hardening tips verified in test Active Directory OU
- [ ] Tool prerequisites and operational licensing reviewed
- [ ] Integration with centralized SIEM/Syslog confirmed
