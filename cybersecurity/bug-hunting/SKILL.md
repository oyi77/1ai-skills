---
name: bug-hunting
description: Automated bug bounty hunting workflow — recon, hunt, validate, report. Use when testing web applications for
  vulnerabilities, running security assessments, or preparing bug bounty submissions.
domain: cybersecurity
tags:
- bug
- cybersecurity
- hunting
- security
- testing
- threat-defense
- workflow
- money
---

# Bug Hunting Skill

## Overview

AI-orchestrated bug bounty workflow covering the full cycle from reconnaissance to report generation. Inspired by claude-bug-bounty (23 commands, 8 agents, 20 web2 + 10 web3 vuln classes, auth-aware hunting, persistent memory system). Designed for ethical security researchers operating within authorized bug bounty programs.

## When to Use

**Trigger phrases:**
- "bug hunting"
- "Hunting on bug bounty programs (HackerOne, Bugcrowd, Intigriti, Immunefi)"
- "Running security assessments against authorized web applications"
- "Discovering and validating vulnerabilities in web2 or web3 targets"


- Hunting on bug bounty programs (HackerOne, Bugcrowd, Intigriti, Immunefi)
- Running security assessments against authorized web applications
- Discovering and validating vulnerabilities in web2 or web3 targets
- Preparing submission-ready bug bounty reports
- Conducting penetration testing with explicit authorization

## The Process

1. **Scope the task** — define objectives, boundaries, and success criteria
2. **Gather information** — collect all necessary data and context before proceeding
3. **Execute the core workflow** — follow the domain-specific steps methodically
4. **Validate results** — verify outputs against expected outcomes or baselines
5. **Document findings** — record results, anomalies, and recommendations
### Step 1: Scope Validation

Verify the target is in-scope before any testing begins.

1. Fetch program rules from the platform (HackerOne, Bugcrowd, etc.)
2. Confirm the target domain/IP is explicitly listed as in-scope
3. Check for out-of-scope assets, excluded vulnerability types, and safe harbor provisions
4. Determine test type: web2, web3, mobile, or combined
5. Record scope details in `.private/target.json` for downstream tools

### Step 2: Reconnaissance

Map the attack surface before hunting.

1. **Subdomain enumeration** — subfinder, dnsReaper for subdomain takeover candidates
2. **Live host discovery** — httpx to probe which hosts respond on which ports
3. **URL crawling** — katana for spidering, historical URL extraction
4. **Technology fingerprinting** — identify frameworks, CMS, server versions, WAF
5. **Attack surface mapping** — enumerate endpoints, parameters, APIs, auth flows

### Step 3: Vulnerability Hunting

Test systematically across vulnerability classes.

**Web2 Classes (20):** IDOR, Auth Bypass, XSS (reflected/stored/DOM), SSRF, Business Logic, Race Conditions, SQL Injection, OAuth/OIDC flaws, File Upload abuse, GraphQL introspection/exploitation, LLM/AI bugs (prompt injection, data leakage), API Misconfiguration, Account Takeover, SSTI, Subdomain Takeover, Cloud/Infrastructure misconfig, HTTP Request Smuggling, Cache Poisoning, MFA Bypass, SAML/SSO flaws

**Web3 Classes (10):** Accounting Desync, Access Control, Incomplete Code Path, Off-By-One errors, Oracle Manipulation, ERC4626 Attacks, Reentrancy, Flash Loan exploits, Signature Replay, Proxy/Upgrade vulnerabilities

### Auth-Aware Hunting

Set authentication so all downstream tools carry the session:

- `--cookie "session=abc123"` for cookie-based auth
- `--bearer "eyJ..."` for token-based auth
- Environment variables (`AUTH_COOKIE`, `AUTH_BEARER`)
- `.private/target.json` with `cookie`, `bearer`, `headers` fields

This enables finding auth-gated bugs: IDOR, BOLA, mass assignment, SSRF behind login, privilege escalation.

### Step 4: Validation Gate

Every finding must pass this 7-question gate before reporting:

1. **Is it real?** — Can you reproduce it consistently?
2. **Is it exploitable?** — Does it have a working attack path?
3. **What's the impact?** — Data exposure, financial loss, account compromise?
4. **Is it in scope?** — Does the program accept this vuln class on this asset?
5. **Can it be reproduced?** — Are the steps clear enough for a triager to follow?
6. **What's the severity?** — CVSS or program-specific rating applied?
7. **Is the PoC clean?** — Non-destructive, no data exfiltration, screenshots redacted?

If any answer is "no" or "unclear," do not submit. Gather more evidence or discard.

### Step 5: Report Generation

Generate impact-first reports formatted for the target platform:

- **HackerOne** — Markdown with structured sections (Summary, Steps to Reproduce, Impact, Remediation)
- **Bugcrowd** — Similar structure with priority rating alignment
- **Intigriti** — Concise format with CVSS scoring
- **Immunefi** — Web3-focused with on-chain PoC details

Reports lead with impact (what an attacker can achieve), not with technical steps. Include clean PoC, affected endpoints, and suggested remediation.

## Memory System

Persistent JSONL-based learning across sessions:

- `audit.jsonl` — Session audit trail (targets tested, findings, timestamps)
- `patterns.jsonl` — Learned vulnerability patterns and signatures
- `journal.jsonl` — Strategy notes, what worked, what to try next

Auto-rotation at 10 MB with 3 backups. Cross-target pattern learning applies insights from prior hunts to new targets.

## External Tool Integration

Tools used at each phase (graceful degradation when missing):

| Phase | Tools |
|-------|-------|
| Recon | subfinder, httpx, katana, dnsReaper |
| Hunting | nuclei, dalfox, ffuf, arjun |
| Secrets | trufflehog, gitleaks, noseyparker |
| Validation | Manual verification, curl, browser |

If a tool is not installed, the workflow falls back to manual testing or alternative tools. Never skip a phase due to missing tooling.

## Autopilot Modes

Control the level of human oversight:

- **--paranoid** — Manual review at every step. Pause before each tool invocation, each finding validation, each report draft. Maximum control.
- **--normal** — Run autonomously through recon and hunting. Pause at the Validation Gate for human approval before reporting.
- **--yolo** — Full autonomous execution with safety checkpoints only. Fastest throughput, least oversight. Use only on low-risk targets with explicit authorization.

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- Testing out-of-scope assets (immediate disqualification from programs)
- Reporting findings without validation (creates noise, damages reputation)
- Generating false positives by not verifying exploitability
- Aggressive scanning without rate limiting (can cause outages, violates program rules)
- Ignoring program-specific rules (excluded vuln types, testing windows, disclosure policies)
- Testing without explicit written authorization (illegal in most jurisdictions)

## Verification

Before claiming any hunt is complete:

- Every finding passes the 7-question validation gate
- Reports are submission-ready for the target platform format
- All steps are reproducible by a third party
- PoC is clean and non-destructive (no data exfiltration, no persistence mechanisms)
- Scope compliance is documented (only tested in-scope assets)
- Rate limits were respected (no denial-of-service conditions created)

## Process

```python
# Example: IOC detection
import re

IOC_PATTERNS = {
    "ip": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "domain": r"\b[a-z0-9-]+\.[a-z]{2,}\b",
    "hash_md5": r"\b[a-f0-9]{32}\b",
    "hash_sha256": r"\b[a-f0-9]{64}\b",
}

def extract_iocs(text: str) -> dict:
    return {k: re.findall(v, text) for k, v in IOC_PATTERNS.items()}
```

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality


## Money-Making Overview

**Target Buyer:** Bug bounty hunters, penetration testers, and security researchers who need automation to scale their hunting or sell recon-as-a-service.

**How You Make Money:**

1. **Sell Recon-as-a-Service** — Run automated reconnaissance on client targets, deliver structured reports. No exploitation needed, no legal risk — pure information gathering.
2. **Win Bounties Faster** — Use the automation pipeline to find valid bugs before competitors. Speed is the edge in public programs.
3. **License Your Workflows** — Package your custom nuclei templates, auth-aware hunting scripts, and validation gates as a tool for other hunters.

### Service Tiers

| Tier | Price | What They Get |
|------|-------|---------------|
| **Basic** — Recon Report | $500 | Full subdomain + tech + URL mapping on 1 target, formatted markdown report, actionable takeaway list |
| **Pro** — Hunt Session | $1,500 | Recon + authenticated vulnerability hunting (20 web2 classes), validated findings only, CVSS-scored |
| **Enterprise** — Retainer | $4,000/mo | Weekly hunting on up to 5 targets, priority zero-day monitoring, custom nuclei templates, Slack integration |

**Expected First Dollar:** Week 1 (recon report), Week 2-3 (first bounty or Pro client).

## First Action in 60 Minutes

Run a complete recon-in-a-box on a target. This script enumerates subdomains, probes live hosts, fingerprints tech, and outputs a structured report you can sell or hunt from.

```bash
#!/bin/bash
# bug-recon-box.sh — run this on a fresh Kali/Ubuntu box
# Usage: ./bug-recon-box.sh example.com

set -euo pipefail
TARGET="${1:?Usage: $0 <domain>}"
OUTDIR="recon-$(date +%Y%m%d)-$TARGET"
mkdir -p "$OUTDIR"

echo "[*] Target: $TARGET"
echo "[*] Output: $OUTDIR"

# 1. Subdomain enumeration (60s)
echo "[1/4] Subdomain enumeration..."
subfinder -d "$TARGET" -silent | tee "$OUTDIR/subdomains.txt"

# 2. Live host probing (60s)
echo "[2/4] Live host probing..."
cat "$OUTDIR/subdomains.txt" | httpx -silent -status-code -tech-detect | tee "$OUTDIR/live-hosts.txt"

# 3. URL crawling (120s)
echo "[3/4] URL crawling..."
katana -list "$OUTDIR/subdomains.txt" -silent -o "$OUTDIR/urls.txt" 2>/dev/null || \
    echo "[!] katana not available — skipping URL crawl"

# 4. Generate report
echo "[4/4] Generating report..."
SUBS=$(wc -l < "$OUTDIR/subdomains.txt" 2>/dev/null || echo 0)
LIVE=$(wc -l < "$OUTDIR/live-hosts.txt" 2>/dev/null || echo 0)
URLS=$(wc -l < "$OUTDIR/urls.txt" 2>/dev/null || echo 0)

cat > "$OUTDIR/recon-report.md" << EOF
# Recon Report: $TARGET
**Date:** $(date)

## Summary
- Subdomains discovered: $SUBS
- Live hosts: $LIVE
- URLs crawled: $URLS

## Live Hosts
```
$(cat "$OUTDIR/live-hosts.txt" 2>/dev/null || echo "None found")
```

## All Subdomains
```
$(cat "$OUTDIR/subdomains.txt" 2>/dev/null || echo "None found")
```

## Next Steps
1. Run authenticated scanning with nuclei on live hosts
2. Test for IDOR, SSRF, XSS on discovered endpoints
3. Check subdomain takeover candidates with dnsReaper
EOF

echo "[+] Done. Report: $OUTDIR/recon-report.md"
echo "[+] Size: $(du -sh "$OUTDIR" | cut -f1)"
```

This script produces a sellable recon report in under 5 minutes. Sell it as-is for $500 or use it as your hunting starting point.

## Deliverable Format

Bug bounty reports must be submission-ready. Use this template:

```markdown
# Bug Bounty Report

**Title:** [Vulnerability Type] on [Target Endpoint]
**Severity:** [Critical/High/Medium/Low] (CVSS X.X)
**Program:** [HackerOne/Bugcrowd/Intigriti]

## Summary
One-paragraph impact statement. What can an attacker achieve?

## Affected Endpoint
```
URL: https://target.com/vulnerable-endpoint
Method: GET/POST/PUT
Auth: Required/Not Required
```

## Steps to Reproduce
1. [Step 1 — precise, copy-pasteable]
2. [Step 2]
3. [Step 3 — leads to proof]

## Proof of Concept
```
[curl command, HTTP request, or exploit script]
```

## Impact
- [Data exposure, account takeover, privilege escalation, etc.]
- [Business impact in financial or operational terms]

## Remediation
- [One-sentence fix recommendation]

## Supporting Evidence
- [Screenshot filename]
- [Request/response dump filename]

---

*Report generated by Bug Hunting Skill. Tested on in-scope assets only.*
```

**Invoice-ready description for recon-as-a-service clients:**

> **Service:** Automated Reconnaissance & Attack Surface Mapping
> **Target:** clientdomain.com
> **Deliverables:** Complete subdomain list, live host inventory, technology fingerprinting, URL map
> **Price:** $500
> **Payment:** Due on delivery via invoice.

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I need more certs before I can sell recon" | You need one paying client, not one more cert. Run the script above, deliver a report, collect $500. |
| "Bug bounty is too competitive to make money" | Most hunters skip recon automation. Speed is your moat — you find bugs while others are still setting up. |
| "I can't sell security services without a company" | Freelance recon-as-a-service is invoice-only, no LLC needed. $500-1500 per report is standard. |
| "I'll build the perfect toolchain first" | The perfect toolchain doesn't exist. Run bug-recon-box.sh today, improve it on paid gigs. |
| "Recon isn't valuable — anyone can run subfinder" | Clients pay $500 because they don't know which tools to run, how to interpret results, or how to present findings. |
| "I'm not fast enough for public programs" | Speed comes from automation, not skill. Your pipeline runs while competitors sleep. |
| "I'll wait until I find a critical bug" | Sell 10 recon reports ($5,000) while you hunt. Cash flow funds the grind. |