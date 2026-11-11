---
name: red-team-credential-access-and-lateral-movement
description: Use when orchestrating credential dumping, LSASS extraction, DPAPI looting, and lateral movement operations using Mimikatz, nanodump, dploot, crackmapexec, and Coercer during authorized red team engagements.
domain: cybersecurity
subdomain: penetration-testing
category: cybersecurity
version: 1.0.0
author: oyi77
license: Apache-2.0
tags:
- red-team
- credential-access
- lateral-movement
- mimikatz
- hashcat
- ntlm
triggers:
- credential access
- lateral movement
- mimikatz
- password spraying
- hash cracking
- ntlm
---

# Red Team Credential Access and Lateral Movement

## Process
1. Scope by threat model.
2. Select tool category index.
3. Validate prerequisites.
4. Execute operational guidance.
5. Verify with checklist.

## Overview

Cybersecurity playbook for authorized offensive credential harvesting and lateral network progression. Follows minimum-privilege footprint principles, strictly scoped rules of engagement, and non-destructive proof-of-concept execution standards.

```bash
git clone https://github.com/cube0x0/nanodump && cd nanodump && make
./nanodump.x64.exe --write C:\Windows\Temp\lsass.dmp
crackmapexec smb <target-cidr> -u <user> -p '<pass>' --sam
crackmapexec winrm <target> -u <user> -H <ntlm-hash> -x "whoami /all"
```

## When to Use

**Trigger phrases:**
- "red team credential harvesting"
- "dump lsass with nanodump or mimikatz"
- "extract remote dpapi secrets using dploot"
- "lateral movement with crackmapexec or wmi"
- "coerce windows ntlm authentication with coercer"

- Harvesting cleartext credentials, NTLM hashes, and Kerberos tickets from memory or disk on authorized targets
- Evading endpoint detection while acquiring process dumps using minidump techniques (nanodump)
- Decrypting stored master keys and credentials across Windows workstations using DPAPI
- Progressing across Active Directory domain assets via SMB, WinRM, or WMI execution channels
- Forcing authentication loops against controlled listeners for hash relay and capture

## When NOT to Use

- When operating on production systems without explicit written rules of engagement
- When performing defensive credential rotation or account remediation (use `cybersecurity/role-security-engineer`)
- When exploiting systems with payloads capable of causing system crashes or data loss

## Prerequisites

- Written Rules of Engagement (RoE) defining target IP ranges and prohibited hosts
- Kali Linux or offensive Windows workstation with Impacket, crackmapexec, and Python 3.x
- High-integrity or SYSTEM shell on intermediate target for memory dumping operations

## Credential Extraction Techniques

### Memory Dumping & Mimikatz
- **nanodump:** Creates minidumps of the LSASS process using unhooked Native APIs (Syscalls) to evade EDR monitoring.
- **Mimikatz:** Parses offline minidumps or live process memory (`sekurlsa::logonpasswords`, `lsadump::sam`) to extract cleartext passwords and hashes.

### DPAPI & Local Secret Looting
- **dploot:** Python tool that connects via SMB/RPC, extracts DPAPI master keys, and loots Chrome, Edge, and Windows Vault credentials.
- **LaZagne:** Post-exploitation module recovering stored passwords from browsers, mail clients, and Wi-Fi networks.

### Cisco Configuration Parsing
- **SeeYouCM-Thief:** Automated discovery and extraction of VoIP phone configuration files and stored credentials across CUCM deployments.

## Lateral Movement Tradecraft

### Network Service Execution
- **crackmapexec / NetExec:** Rapid validation of captured credentials across SMB, WinRM, SSH, and MSSQL services.
- **LiquidSnake:** Fileless lateral movement technique that executes payloads directly in memory across remote systems without spawning suspicious processes.

### Authentication Coercion
- **Coercer:** Automates RPC methods (MS-RPRN, MS-EFSR) to force a remote Windows host to authenticate back to an attacker-controlled endpoint for NTLM relay attacks.

## Anti-Rationalization Table

| Excuse | Flawed Rationalization | Required Discipline |
|---|---|---|
| "Just run mimikatz directly from disk" | "It works faster." | Dropping known binaries triggers immediate EDR alerts; use in-memory execution or offline minidump extraction via nanodump. |
| "Spray the entire domain to find credentials" | "Higher volume means better results." | Fast spraying triggers lockout thresholds and blue team detection; use low-and-slow targeted spraying within RoE boundaries. |
| "Cracking passwords can be run with any wordlist" | "Brute-force everything." | Tailor wordlists to the target organization's naming patterns and season/year variations to minimize unnecessary computation. |

## Verification Checklist

- [ ] All target hosts confirmed within written RoE boundaries
- [ ] LSASS extraction executed using non-destructive memory dumping (nanodump)
- [ ] Captured hashes stored in encrypted, access-restricted containers
- [ ] Lateral movement executed with least-disruptive channel (WinRM preferred over PsExec)
- [ ] Proof of privilege documented with non-destructive canary commands
- [ ] Complete operational log recorded with exact execution timestamps
