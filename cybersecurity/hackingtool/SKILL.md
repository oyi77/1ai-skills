---
name: hackingtool
description: All-in-one terminal hacking toolkit — 185+ security tools across 20 categories with unified menu, search, and batch install. Use when setting up a pentest environment, launching security tools, or managing a hacking toolkit.
---

## Overview

Z4nzu/hackingtool is a Python-based terminal aggregator that provides a unified menu interface to 185+ open-source security tools. It doesn't implement exploits itself — it installs, updates, and launches well-known tools organized by attack category.

**GitHub:** https://github.com/Z4nzu/hackingtool (75K+ stars)
**Version:** v2.0.0 | **License:** MIT | **Platform:** Linux, macOS

## Capabilities

- Unified interactive menu for 185+ security tools
- 20 attack categories from recon to post-exploitation
- Search tools by keyword (`/query`) or tag filter (`t`)
- Recommendation engine — describe what you want, get tool suggestions
- Install status tracking — shows which tools are locally installed
- Batch install all tools in a category (option 97)
- Smart update per tool (auto-detects git/pip/go)
- Docker support for isolated environments
- OS-aware — hides Linux-only tools on macOS

## When to Use

- Setting up a new pentest environment from scratch
- Need a quick launcher for security tools across categories
- Want to discover tools for a specific attack type
- Managing tool installation and updates across a toolkit
- Building a bug bounty hunting workstation

## Installation

```bash
# One-liner installer
curl -sSL https://raw.githubusercontent.com/Z4nzu/hackingtool/master/install.sh | sudo bash

# Or manual install
git clone https://github.com/Z4nzu/hackingtool.git
cd hackingtool
pip install -r requirements.txt
python3 hackingtool.py

# Docker
docker-compose up -d
```

## Tool Categories (20)

| Tool | Purpose |
|------|---------|
| Burp Suite | Web application security testing proxy |
| Metasploit | Exploitation framework for penetration testing |
| Nmap | Network discovery and security auditing |
| Impacket | Python library for network protocol interaction |
### 1. Anonymously Hiding (2 tools)
AnonSurf, Multitor — traffic anonymization and multi-Tor routing

### 2. Information Gathering (26 tools)
nmap, Amass, theHarvester, RustScan, SpiderFoot, Subfinder, TruffleHog, Gitleaks, Shodan, Censys, Recon-ng, Photon, OSINT-SPY

### 3. Wordlist Generator (7 tools)
Cupp, Hashcat, John the Ripper, CeWL, kwprocessor, Mentalist

### 4. Wireless Attack (13 tools)
Wifite, Fluxion, Airgeddon, Bettercap, hcxdumptool, EAPHammer, wifiphisher

### 5. SQL Injection (7 tools)
Sqlmap, NoSqlMap, DSSS, JSInjection, SQLiScanner

### 6. Phishing Attack (17 tools)
SET, Evilginx3, ShellPhish, PyPhisher, HiddenEye, Gophish, Zphisher, SocialFish

### 7. Web Attack (20 tools)
Nuclei, ffuf, Feroxbuster, Nikto, OWASP ZAP, mitmproxy, Dirsearch, httpx, Katana, Arjun

### 8. Post Exploitation (10 tools)
Sliver, Havoc, Mythic, PEASS-ng, Ligolo-ng, Chisel, Evil-WinRM, Pwncat

### 9. Forensics (8 tools)
Autopsy, Wireshark, Volatility 3, Binwalk, pspy, Bulk Extractor

### 10. Payload Creation (8 tools)
TheFatRat, MSFvenom Payload Creator, Enigma, Venom

### 11. Exploit Framework (4 tools)
RouterSploit, WebSploit, Commix, Faraday

### 12. Reverse Engineering (5 tools)
Ghidra, Radare2, JadX, Androguard, Capstone

### 13. DDOS Attack (5 tools)
SlowLoris, GoldenEye, UFOnet, HOIC, LOIC

### 14. RAT (Remote Admin) (1 tool)
Pyshell

### 15. XSS Attack (9 tools)
DalFox, XSStrike, XSpear, XSSer, BruteXSS

### 16. Steganography (4 tools)
StegoCracker, SteganoHide, OpenStego, Steghide

### 17. Active Directory (6 tools)
BloodHound, NetExec, Impacket, Responder, Certipy-ad, Kerbrute

### 18. Cloud Security (4 tools)
Prowler, ScoutSuite, Pacu, Trivy

### 19. Mobile Security (3 tools)
MobSF, Frida, Objection

### 20. Other Tools (24 tools)
Sherlock, SocialMapper, Hash Buster, Gospider, Photon, Holehe

## Pseudo Code

This section covers pseudo code for hackingtool.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### Launch the toolkit
```bash
cd hackingtool
python3 hackingtool.py
```

### Search for a specific tool
```
# From the main menu, type:
/nuclei        # Search for nuclei
/sqlmap        # Search for sqlmap
```

### Filter by tag
```
# Press 't' then select tag:
# osint, web, c2, cloud, mobile, wireless, phishing, exploit, forensics
```

### Use the recommendation engine
```
# Press 'r' then describe your goal:
"I want to find subdomains of a target"
# → Suggests: Amass, Subfinder, Sublist3r
```

### Batch install a category
```
# Select a category, then choose option 97 to install all tools
```

### Integration with existing security skills
```bash
# After installing hackingtool, use it alongside your security skills:

# 1. Use recon-automation skill to plan recon
# 2. Launch hackingtool for tool execution
# 3. Use report-generator skill to document findings

# Example workflow:
python3 hackingtool.py                    # Launch toolkit
# Select: Information Gathering → Amass
# Run recon, then use report-generator for documentation
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: rich` | Missing Python dependency | `pip install rich` |
| `Python 3.10+ required` | Old Python version | `python3 --version`, upgrade if needed |
| `Permission denied` | Need sudo for installs | `sudo python3 hackingtool.py` |
| `Tool not found` | Not installed yet | Select tool → Install option |
| `Linux-only tool` | Running on macOS | Use Docker or Linux VM |

## Common Patterns

- **Follow the principle of least privilege** — use the minimum permissions needed for each task
- **Document everything** — maintain logs of all actions, configurations, and findings
- **Verify before acting** — confirm assumptions about the environment before making changes
- **Automate repetitive steps** — script common workflows to reduce human error
### Pentest Setup Workflow
```
1. Install hackingtool (one-liner or Docker)
2. Launch: python3 hackingtool.py
3. Information Gathering → Install all (option 97)
4. Web Attack → Install nuclei, ffuf, nikto
5. Post Exploitation → Install sliver, ligolo-ng
6. Use recon-automation skill for structured recon
7. Use vulnerability-scanner skill for scanning
8. Use report-generator skill for documentation
```

### Bug Bounty Workflow
```
1. recon-automation → subdomain enumeration
2. hackingtool → Information Gathering → Amass/Subfinder
3. hackingtool → Web Attack → nuclei/ffuf for scanning
4. vulnerability-scanner → targeted testing
5. report-generator → write findings
```

### Red Team Setup
```
1. hackingtool → Post Exploitation → Sliver/Havoc (C2)
2. hackingtool → Phishing → Evilginx3/SET
3. hackingtool → Payload Creation → MSFvenom
4. hackingtool → Active Directory → BloodHound/Impacket
```
## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Exceeding the authorized scope of the engagement
- Leaving persistent access mechanisms without explicit approval
- Causing denial-of-service on production systems during testing
## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- All exploited vulnerabilities documented with reproduction steps
- Scope boundaries confirmed — only authorized targets were tested
- Remediation recommendations included for every finding
