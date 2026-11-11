---
name: red-team-tools-catalog
description: Use when querying, evaluating, or orchestrating 150+ offensive security tools from the A-poc/RedTeam-Tools index across reconnaissance, resource development, initial access, execution, persistence, and evasion.
domain: cybersecurity
subdomain: penetration-testing
category: cybersecurity
version: 1.0.0
author: oyi77
license: Apache-2.0
tags:
- red-team
- offensive-security
- pentesting
- cyber
- attack
triggers:
- red team tools
- offensive tools
- red team tips
- adversary toolkits
- red teaming resources
---

# Red Team Tools Catalog

## Process
1. Scope by threat model.
2. Select tool category index.
3. Validate prerequisites.
4. Execute operational guidance.
5. Verify with checklist.

## Overview

Comprehensive reference index cataloging 150+ specialized tools and offensive techniques from the curated A-poc/RedTeam-Tools repository. Provides structured operational guidance across all phases of the MITRE ATT&CK enterprise matrix for authorized red team engagements.

## When to Use

**Trigger phrases:**
- "red team tools catalog"
- "lookup offensive security tooling"
- "find red team exploitation and persistence tools"
- "red team tips and evasion techniques"

- Selecting appropriate offensive tooling for authorized penetration tests and red team operations
- Reviewing adversary techniques and command syntaxes across the attack lifecycle
- Implementing practical red team tradecraft tips (e.g., LOLBas port scanning, registry account hiding, AppLocker enumeration)
- Cross-referencing adversary emulation tooling against threat actor profiles (TTPs)

## When NOT to Use

- When operating without explicit, signed authorization and rules of engagement
- When performing defensive threat monitoring or incident containment (use `cybersecurity/role-security-engineer`)

## Prerequisites

- Written Rules of Engagement and operational boundary definitions
- Dedicated offensive infrastructure and lab validation environments

## Core Red Team Tips

- **Hiding Local Admin Account:** Hide a created backdoor account from the Windows logon UI via registry: `reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\SpecialAccounts\UserList" /t REG_DWORD /v <account> /d 0 /f`
- **Neuter Windows Defender Signatures:** Remove loaded signature definitions without triggering full service alerts: `"%Program Files%\Windows Defender\MpCmdRun.exe" -RemoveDefinitions -All`
- **Enable Multi-Session RDP:** Allow multiple concurrent RDP sessions per user account: `reg add HKLM\System\CurrentControlSet\Control\TerminalServer /v fSingleSessionPerUser /d 0 /f`
- **Live-off-the-Land Port Scanner:** Scan ports using native PowerShell sockets without uploading scanner binaries: `0..1024 | % {echo ((new-object Net.Sockets.TcpClient).Connect("<target>",$_)) "Port $_ open"} 2>$null`
- **Bypass Disabled Command Prompt:** Circumvent UI policy command prompt blocks using the run dialog: `cmd.exe /k "whoami"`
- **Disable AV via Sysinternals PsSuspend:** Suspend target anti-virus service processes via native signed binary calls: `PsSuspend.exe <service_pid>`

```powershell
# Native PowerShell port scanner (LOLBas, no scanner binary on disk)
0..1024 | % { echo ((New-Object Net.Sockets.TcpClient).Connect("<target>",$_)) "Port $_ open" } 2>$null
# Multi-session RDP + hide local admin from logon UI
reg add HKLM\System\CurrentControlSet\Control\TerminalServer /v fSingleSessionPerUser /d 0 /f
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\SpecialAccounts\UserList" /t REG_DWORD /v <account> /d 0 /f
```

## Tool Category Index

| Category | Primary Tools | Operational Function |
|---|---|---|
| Reconnaissance | `SpiderFoot`, `reconFTW`, `subzy`, `CloudBrute`, `certSniff` | Asset enumeration, takeover detection, cloud storage discovery |
| Resource Development | `Freeze`, `ScareCrow`, `Shellter`, `remoteinjector`, `Chimera` | Payload compilation, EDR hook evasion, macro weaponization |
| Initial Access | `CredMaster`, `TREVORspray`, `King Phisher`, `EvilGoPhish` | Password spraying, OAuth phishing, credential harvesting |
| Execution | `Responder`, `Donut`, `evil-winrm`, `SQLRecon`, `PowerZure` | In-memory .NET execution, remote WinRM shell, MSSQL abuse |
| Privilege Escalation | `LinPEAS`, `WinPEAS`, `BeRoot`, `Certify`, `ImpulsiveDLLHijack` | Host auditing, ADCS abuse paths, DLL search order hijacking |
| Defense Evasion | `Invoke-Obfuscation`, `Alcatraz`, `SharpBlock`, `Mangle` | Script obfuscation, binary structure alteration, DLL hook prevention |
| Credential Access | `Mimikatz`, `nanodump`, `dploot`, `hashcat`, `SeeYouCM-Thief` | Process minidumping, DPAPI extraction, offline hash cracking |
| Lateral Movement | `crackmapexec`, `LiquidSnake`, `Coercer`, `ADFSpoof` | Network execution, NTLM coercion, AD FS token forgery |
| C2 & Exfiltration | `Havoc`, `Covenant`, `Merlin`, `Dnscat2`, `Cloakify`, `PyExfil` | Post-exploitation management, DNS tunneling, DLP evasion |

## Anti-Rationalization Table

| Excuse | Flawed Rationalization | Required Discipline |
|---|---|---|
| "Any tool in the catalog is safe to run" | "It's listed in the catalog, so it's fine." | Every tool carries operational risk; verify tool stability and noisy signatures in a lab environment before running against target infrastructure. |
| "Tips work identically across all Windows builds" | "Tricks are universal." | Windows security baselines change; test registry modifications and LOLBas commands on exact target OS versions. |

## Verification Checklist

- [ ] All tool usage scoped to authorized target IP ranges and accounts
- [ ] Tool prerequisites and runtime requirements validated in staging
- [ ] Operational tradecraft tips verified against target operating system version
- [ ] Red team action logs timestamped and aligned with engagement timeline
