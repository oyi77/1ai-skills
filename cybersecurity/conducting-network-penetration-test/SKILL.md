---
name: conducting-network-penetration-test
description: "Conducts comprehensive network penetration tests against authorized target environments by performing host discovery, port scanning, service enumeration, vulnerability identification, and controlled exploitation to assess the security posture of network infrastructure. The tester follows PTES methodology from reconnaissance through post-exploitation and reporting. Use when working with conducting network penetration test."
domain: cybersecurity
tags:
- network-pentest
- Nmap
- Metasploit
- vulnerability-exploitation
- infrastructure-security
- penetration-testing
- PTES
- Kali-Linux
- money
subdomain: penetration-testing
version: 2.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- ID.RA-01
- ID.RA-06
- GV.OV-02
- DE.AE-07
- PR.IP-12
- RS.MI-01
price:
  basic: 2000
  pro: 5000
  enterprise: 8000
---

# Conducting Network Penetration Test

## Overview

Internal and external network penetration test following PTES methodology. You enumerate hosts, discover services, identify vulnerabilities, and demonstrate impact through controlled exploitation — then deliver a compliance-grade report that satisfies PCI-DSS ASV scanning requirements, SOC 2 Type II controls, HIPAA Security Rule risk assessments, and ISO 27001 Annex A.12.6.

This is **the** baseline security service every compliance framework mandates. No org that answers to a board or auditor skips it.

## When to Use

**Trigger phrases:**
- "conduct network pentest" / "network penetration test"
- "internal network assessment" / "external network assessment"
- "assess network security posture" / "infrastructure security review"
- "PCI ASV scan" / "compliance pentest" / "SOC 2 network test"
- "Kali network audit" / "Nmap vulnerability assessment"

**Appropriate contexts:**
- Pre-deployment infrastructure audit before prod cutover
- Annual compliance testing (PCI-DSS 11.3, SOC 2 CC7.1, HIPAA 164.308)
- Post-breach network reassessment to validate containment
- M&A network security due diligence
- Insurance-mandated penetration test for cyber policy qualification
- Firewall rule and segmentation validation

**Do not use** without signed Rules of Engagement. Never test production systems outside an approved change window. Not for DoS/DDoS testing unless explicitly scoped. Not a replacement for a web application pentest — network and app tests are separate deliverables.

## Prerequisites

- Signed Rules of Engagement (RoE): target IP ranges, excluded hosts, maintenance window, escalation contacts
- Written authorization letter (get-out-of-jail) from asset owner with client legal sign-off
- Kali Linux workstation with Nessus (or alternative) license, Metasploit Pro (or community), and current tool updates
- VPN or direct L2/L3 access for internal; public IP for external scope
- Out-of-band chat channel with client SOC/IR team (Slack, Teams, phone)
- Scope document: explicit in-scope CIDRs, out-of-scope systems (medical devices, SCADA, OT, management networks)

## Money-Making Overview

### Target Buyer

**Compliance-driven CISOs, IT Directors, and MSP/MSSP procurement** at companies that need audit evidence:
- Mid-market ($50-500M rev) — annual PCI/SOC 2 requirement, no internal pentest team
- Regulated startups (fintech, healthtech, legal tech) — SOC 2 Type I/II in progress
- MSPs reselling security assessments to their SMB client base
- Insurance carriers underwriting cyber policies that require pentest evidence

You sell **evidence**, not hacking. The deliverable is the report that goes in the auditor's binder.

### Service Tiers

| Tier | Price (USD) | Scope | Deliverables | Timeline |
|------|-------------|-------|-------------|----------|
| **Basic** | $2,000 | Single external range (/24), unauthenticated scan + 5 vuln validations | Executive summary, findings table, CVSS-scored, PDF report | 1 week |
| **Pro** | $5,000 | Internal + external (/23 each), authenticated scanning (AD creds), 15 validated exploits, persistence attempt | Tier 1 + replay PoCs, network topology map, MITRE ATT&CK mapping, remediation workshop (1h) | 2 weeks |
| **Enterprise** | $8,000 | Full-scope internal/external (/22 or 10 /24s), segmentation testing, wireless assessment, AD attack path validation, purple-team handoff | Tier 2 + ROE packet, segmentation test results, retest validation, exec presentation, 90-day remediation tracking | 3-4 weeks |

**Pricing notes:** Adjust $500-1000 for same-region compliance (PCI APAC, GDPR EU). Add $1500 for rush (72h window). Wireless add-on: +$1500. AD attack path: +$2000. Retest (validation scan): 50% of tier price.

### First-Dollar Timeline

- **Day 1-2:** Deliver signed ROE + schedule kickoff call
- **Day 3:** Run First Action script below → initial findings
- **Day 5:** Manual exploitation + validation of top-10 findings
- **Day 7:** Basic deliverable complete — invoice sent
- **Pro/Enterprise** adds 5-10 days for authenticated testing, topology mapping, and remediation workshop

## First Action in 60 Minutes

Run this script from your Kali workstation after receiving the signed scope. It performs host discovery, port scanning, service enumeration, and vulnerability scanning — then packages everything into a structured findings directory.

```bash
#!/bin/bash
# =============================================================================
# network-pentest-scout.sh — Automated Network Pentest Initial Scan
# =============================================================================
# Usage: ./network-pentest-scout.sh <target_cidr> <engagement_name>
#   Example: ./network-pentest-scout.sh 192.168.1.0/24 acme-corp-Q1-2026
#
# Output: ./<engagement_name>/
#   ├── 01-recon/          — Nmap host discovery + port scans
#   ├── 02-vuln/           — Vuln scan results (NSE + optional Nessus)
#   ├── 03-evidence/       — Raw PCAPs, screenshots, proofs
#   ├── findings.csv       — Consolidated finding list (CVSS 4.0)
#   └── report.md          — Draft executive report
# =============================================================================

set -euo pipefail

TARGET="${1:?Usage: $0 <target_cidr> <engagement_name>}"
ENGAGEMENT="${2:-network-pentest-$(date +%Y%m%d)}"
BASE="$PWD/$ENGAGEMENT"

mkdir -p "$BASE"/{01-recon,02-vuln,03-evidence}

echo "[+] Starting reconnaissance against $TARGET"

# --- Phase 1: Host Discovery ---
echo "[1/5] Host discovery (ping sweep)..."
nmap -sn -T4 "$TARGET" -oA "$BASE/01-recon/host-discovery" 2>/dev/null
grep -oP 'Nmap scan report for \K\S+' "$BASE/01-recon/host-discovery.nmap" \
  > "$BASE/01-recon/live-hosts.txt"

LIVE_COUNT=$(wc -l < "$BASE/01-recon/live-hosts.txt")
echo "  -> $LIVE_COUNT live hosts found"

# --- Phase 2: Port & Service Scan ---
echo "[2/5] Port scanning all TCP ports on live hosts..."
nmap -Pn -sV -sC -p- --min-rate=1000 \
  -iL "$BASE/01-recon/live-hosts.txt" \
  -oA "$BASE/01-recon/full-tcp-scan" 2>/dev/null

# --- Phase 3: Quick Vulnerability Scan (NSE) ---
echo "[3/5] Running NSE vulnerability scripts..."
nmap -Pn -sV --script vuln \
  -iL "$BASE/01-recon/live-hosts.txt" \
  -oA "$BASE/02-vuln/nse-vuln-scan" 2>/dev/null

# --- Phase 4: Extract Findings ---
echo "[4/5] Extracting findings and building CSV..."
echo "host,port,service,severity,description" > "$BASE/findings.csv"

awk '/^Nmap scan report/{h=$NF} /vuln/{for(i=2;i<=NF;i++){if($i~"^[0-9]"&&$(i+1)~"/tcp"){p=$i;sv=$(i+2)}}
  /VULNERABLE/{sev=$NF; desc=$0; printf "%s,%s,%s,%s,\"%s\"\n",h,p,sv,sev,desc >> "'"$BASE"'/findings.csv"}' \
  "$BASE/02-vuln/nse-vuln-scan.nmap" 2>/dev/null || true

# --- Phase 5: Generate Report Draft ---
echo "[5/5] Generating draft report..."
cat > "$BASE/report.md" << REPORT
# Network Penetration Test Report — $ENGAGEMENT

**Date:** $(date -I)
**Tester:** $(whoami)
**Target Scope:** $TARGET

---

## Executive Summary

A network penetration test was conducted against the defined scope. 
$LIVE_COUNT hosts were discovered on the target network.

## Key Findings

$(python3 -c "
import csv
with open('$BASE/findings.csv') as f:
    r = csv.reader(f); next(r)
    vulns = list(r)
print(f'- Total potential findings: {len(vulns)}')
ips = set(v[0] for v in vulns if v)
print(f'- Affected hosts: {len(ips)}')
print()
for v in vulns[:10]:
    print(f'- {v[0]}:{v[1]} {v[2]} — {v[3]} — {v[4]}')
" 2>/dev/null || echo "  (Findings incomplete — continue manual validation)")

## Scope

- **Target CIDR:** $TARGET
- **Methodology:** PTES (Penetration Testing Execution Standard)
- **Classification:** Confidential — for authorized recipients only

## Next Steps

1. Manually validate each finding (confirm false positives vs. true positives)
2. Attempt controlled exploitation of confirmed vulnerabilities
3. Perform post-exploitation / lateral movement assessment (if in scope)
4. Produce final report with remediation guidance

REPORT

echo "[+] Done. Engagement directory: $BASE"
echo "    Report draft: $BASE/report.md"
echo "    Findings CSV: $BASE/findings.csv"
echo "    Scan results: $BASE/01-recon/ $BASE/02-vuln/"
```

Run this after the ROE is signed. It produces a structured directory you can immediately use to start the manual validation phase.

## Workflow (PTES Methodology)

### Phase 1: Pre-Engagement
1. Sign ROE with client — target ranges, exclusions, hours, emergency contact
2. Set up isolated Kali VM or dedicated testing workstation
3. Establish IR communication channel (client's SOC watch desk)
4. Configure Nessus/OpenVAS credentials if authenticated scanning is in scope

### Phase 2: Intelligence Gathering
1. Passive recon: DNS enumeration (dnsrecon, fierce, dig), WHOIS, Shodan for external
2. Active recon: Nmap ping sweep (-sn) to discover live hosts
3. Identify network topology, VLAN segmentation, firewall rules through TTL analysis and traceroute

### Phase 3: Vulnerability Identification
1. **Port scanning:** Nmap full TCP (-p-) + top 1000 UDP (-sU --top-ports 1000)
2. **Service enumeration:** Nmap -sV with version detection, banner grabbing (nc, telnet)
3. **Vulnerability scanning:** NSE vuln scripts, Nessus/OpenVAS authenticated scan
4. **Manual fingerprinting:** Web server headers, SNMP enumeration, SMB version detection
5. **Credential testing:** Weak/default password checks, null session tests, default SNMP community strings

### Phase 4: Controlled Exploitation
1. Validate top findings — eliminate false positives manually
2. Exploit confirmed vulns with minimum necessary impact:
   - Metasploit module for known CVEs (EternalBlue, BlueKeep, SMBGhost, Log4Shell)
   - Manual exploitation (unauthenticated RCE via vulnerable web services, default creds on appliances)
   - Credential replay (pass-the-hash, Kerberoasting for AD environments)
3. Demonstrate business impact — show what an attacker could access (financial data, PII, domain admin)
4. Screenshot every successful exploitation step (evidence package)

### Phase 5: Post-Exploitation / Lateral Movement (if scoped)
1. Enumerate AD attack paths with BloodHound
2. Attempt lateral movement via PSExec, WMI, WinRM, SMB
3. Test segmentation controls — can you reach the PCI CDE or HR database from a compromised workstation?
4. Escalate privileges — local admin on workstation → domain admin?

### Phase 6: Reporting
1. Compile findings with CVSS 4.0 scores, evidence screenshots, and remediation guidance
2. Executive summary (non-technical) + technical appendix
3. Remediation workshop (Pro tier+) — walk through each finding with the client's IT team
4. Deliver final PDF + editable format (DOCX)
5. Offer retest (validation scan) after client remediates — bill at 50% of tier

## Deliverable Format

The final report follows this structure. Every client receives a branded PDF; Pro+ includes an editable DOCX.

```markdown
# Network Penetration Test Report
## [Client Name] — [Engagement Date]

**Tester:** [Name / Company]
**Classification:** Confidential

---

### 1. Executive Summary (1 page max)
- Engagement objective and scope
- Overall risk rating (Critical / High / Moderate / Low)
- Key finding: "X critical, Y high, Z moderate vulnerabilities identified"
- One-sentence business impact
- Top 3 recommended actions

### 2. Engagement Overview
- **Methodology:** PTES
- **Scope:** [CIDR ranges, domains]
- **Testing Dates:** [start] — [end]
- **Tools:** Nmap, Nessus, Metasploit, CrackMapExec, BloodHound, Impacket
- **Exclusions:** [out-of-scope hosts, reasons]

### 3. Findings Summary
| ID | Host | Port/Service | Vulnerability | CVSS 4.0 | Risk | Status |
|----|------|-------------|--------------|----------|------|--------|
| NET-001 | 10.0.1.45 | 445/SMB | MS17-010 RCE | 9.8 | Critical | Confirmed |
| NET-002 | 10.0.1.22 | 3389/RDP | CVE-2019-0708 BlueKeep | 9.8 | Critical | Confirmed |

### 4. Detailed Findings
For each finding:
- **Host:** IP and hostname
- **Service:** Port, protocol, service name, version
- **Vulnerability:** CVE ID, CVSS 4.0 vector string
- **Evidence:** Nmap output, exploitation PoC screenshot, Metasploit console output
- **Risk:** Likelihood + Business Impact assessment
- **Remediation:** Step-by-step fix (patch version, config change, firewall rule)
- **References:** CVE link, vendor advisory, MITRE ATT&CK technique

### 5. Methodology Details
- Reconnaissance results (live hosts, OS fingerprinting)
- Network topology diagram (Visio/Draw.io export)
- Vulnerabilities discovered per host
- Exploitation chain walkthrough (critical findings only)

### 6. Remediation Roadmap
| Priority | Action | Owner | Timeline |
|----------|--------|-------|----------|
| Critical | Patch SMB on all Windows servers | IT Ops | 7 days |
| High | Disable RDP on non-admin workstations | IT Ops | 14 days |
| Moderate | Update SNMP community strings | Network | 30 days |

### 7. Raw Artifacts (Appendix)
- Full Nmap scan results
- Nessus/OpenVAS export
- PCAP files from exploitation
- Screenshot evidence log
```

**Invoice-ready line items:**
```
Line Item                                                  Qty     Rate     Total
─────────────────────────────────────────────────────────────────────────────
Basic Network Penetration Test (external /24)               1    $2,000   $2,000
Vulnerability validation (5 findings)                       1    incl.    incl.
Executive summary + Findings report (PDF)                   1    incl.    incl.
─────────────────────────────────────────────────────────────────────────────
Total                                                                  $2,000
```

**Email template for proposal delivery:**
```
Subject: Network Penetration Test Proposal — [Client Name]

[Client],

Following our discussion, here is the proposal for your annual
network penetration test required for [compliance framework].

Scope:     [CIDR ranges]
Timeline:  [start] — [end]
Deliverable: Compliance-grade PDF report + retest option
Cost:      $[amount]
Quote ref: [number]

The deliverable includes the executive summary, CVSS-scored findings,
evidence screenshots, and step-by-step remediation guidance.

Ready to book the maintenance window?

Best,
[Your Name]
```

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We already run Nessus internally" | Nessus finds symptoms. A pentester chains them into an attack path that demonstrates real business impact — something no scanner can do. |
| "We passed our PCI ASV scan, we're fine" | ASV scans are external and unauthenticated. An internal authenticated pentest finds 10x more critical vulnerabilities. PCI requires BOTH. |
| "Our network is fully patched" | Every field engagement finds default creds, exposed management interfaces, and misconfigured ACLs on "fully patched" networks. Patch level ≠ security posture. |
| "We'll do it ourselves with the internal team" | Independence requirement: auditors will not accept self-performed tests. You need an external party. |
| "A pentest is too expensive for our budget" | The average ransomware demand covers 20 pentests. One finding prevented = entire engagement paid for. |
| "We just did one last year" | Attack surface changes every quarter — new devices, config changes, personnel turnover. Annual testing is the minimum, not the gold standard. |
| "I need more certs before I can sell this" | You need one paying client, not one more cert. OSCP helps, but 10 clean report deliveries matter more to buyers. Start with a friend's company. |
| "There are no vulnerabilities — our firewall is enterprise-grade" | Firewalls don't prevent credential reuse, SMB relay, or misconfigured services behind them. We test what the firewall protects, not the firewall itself. |

## Tools

- **Nmap** — Host discovery, port scanning, service detection, NSE vuln scripts
- **Nessus / OpenVAS** — Authenticated vulnerability scanning
- **Metasploit (Pro or Community)** — Exploitation framework for validated CVEs
- **CrackMapExec** — SMB enumeration, credential spraying, lateral movement
- **BloodHound / SharpHound** — Active Directory attack path mapping
- **Impacket** — psexec, wmiexec, smbexec, secretsdump for post-exploitation
- **Responder** — LLMNR/NBT-NS poisoning for credential capture
- **Hashcat** — Offline password hash cracking
- **Wireshark / tcpdump** — Packet capture for evidence and protocol analysis
- **Burp Suite** — Web service testing within scope (manager interfaces, API endpoints)
- **Draw.io / Excalidraw** — Network topology documentation
- **Jira / Notion** — Finding tracking and client communication

## Verification

- [ ] ROE signed and stored before any scan runs
- [ ] Host discovery complete — live hosts enumerated against scope
- [ ] Full TCP port scan on all live hosts; top UDP scan completed
- [ ] Service version detection on all open ports
- [ ] Vulnerability scan (NSE + Nessus/OpenVAS) completed and parsed
- [ ] Top-5 critical/high findings manually validated (not scanner-only)
- [ ] Controlled exploitation of at least 2 validated findings with evidence (screenshots, console output)
- [ ] False positives documented and excluded from final count
- [ ] Report drafted with executive summary, findings, and remediation roadmap
- [ ] Client remediation workshop delivered (Pro+ tier)
- [ ] Retest scheduled (if applicable) — bill at 50% of engagement
- [ ] Invoice submitted within 48h of report delivery
