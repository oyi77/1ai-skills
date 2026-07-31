---
name: continuous-hunter
description: Automated continuous bug hunting pipeline that runs 24/7 across multiple targets. Use when setting up persistent
  hunting, automating the find-report cycle, or scaling bug bounty income through automation.
domain: cybersecurity
author: oyi77
license: Apache-2.0
subdomain: general-cybersecurity
tags:
- continuous
- cybersecurity
- hunter
- pipeline
- security
- threat-defense
- money
version: 1.0.0
---
# Continuous Hunter

## Overview

24/7 automated vulnerability hunting pipeline. Deploy once, collect findings daily. Monitors targets across subdomain changes, port drift, new services, disclosed CVEs, and misconfiguration exposure — all without manual intervention.

## When to Use

**Trigger phrases:**
- "continuous hunter"
- "Scaling from manual hunting to automated pipeline"
- "Running overnight/weekend scans across target portfolio"
- "Monitoring targets for new vulnerabilities"

- Scaling from manual hunting to automated pipeline
- Running overnight/weekend scans across target portfolio
- Monitoring targets for new vulnerabilities
- Building passive income from bug bounties
- Maximizing findings per hour of effort

## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope

## Money-Making Overview

**Buyer Persona:** Mid-market CISOs at 50-500 employee tech companies; managed service providers who need to offer continuous security monitoring but lack in-house staff; startup CTOs who need compliance-ready vulnerability management without hiring a full-time security engineer.

**Pricing Tiers (Monthly Retainer):**

| Tier | Price | Scope | Deliverables |
|---|---|---|---|
| Starter | $1,000/mo | Up to 3 target domains, weekly scan cycle | Weekly report + Slack alerts |
| Growth | $2,500/mo | Up to 10 targets, daily scans, priority CVE monitoring | Weekly report + real-time Slack alerts + monthly trend analysis |
| Enterprise | $4,000/mo | Unlimited targets, 2x daily scans, custom integration | Everything above + SIEM feed + quarterly executive summary + on-call escalation |

**First-Dollar Timeline:** Deploy pipeline for first client in 2-3 hours. First weekly report goes out 7 days later. With 3 Starter clients at $1,000 each, that's $3,000/mo recurring in month one.

## First Action in 60 Minutes

Set up a cron-based daily scan pipeline for a target. This script discovers subdomains, probes live hosts, runs basic checks, and writes findings to a dated JSON report.

```bash
#!/bin/bash
# daily-hunt.sh — run this daily via cron: 0 6 * * * /opt/hunter/daily-hunt.sh
# Usage: ./daily-hunt.sh <target-domain> [output-dir]

TARGET="${1:-example.com}"
OUTDIR="${2:-./reports}"
DATE=$(date +%Y-%m-%d)
mkdir -p "$OUTDIR/$TARGET/$DATE"
REPORT="$OUTDIR/$TARGET/$DATE/findings.json"

echo "[+] Starting daily hunt for $TARGET — $(date)"

# 1. Subdomain enumeration (passive)
echo '{"target":"'"$TARGET"'","date":"'"$DATE"'","findings":[]}' > "$REPORT"

subdomains=$(curl -s "https://crt.sh/?q=%25.$TARGET&output=json" 2>/dev/null \
  | python3 -c "import sys,json; [print(d['name_value']) for d in json.load(sys.stdin)]" \
  | sort -u 2>/dev/null)

if [ -z "$subdomains" ]; then
  echo "  [!] No subdomains from crt.sh"
  subdomains="$TARGET"
fi

count=0
for sub in $subdomains; do
  # 2. Quick probe — is it alive?
  http_code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 --max-time 8 "https://$sub" 2>/dev/null)
  if [ "$http_code" != "000" ]; then
    # 3. Grab response headers for security assessment
    headers=$(curl -sI --connect-timeout 5 --max-time 8 "https://$sub" 2>/dev/null)
    missing=""
    echo "$headers" | grep -qi "Strict-Transport-Security" || missing="$missing hsts"
    echo "$headers" | grep -qi "Content-Security-Policy"  || missing="$missing csp"
    echo "$headers" | grep -qi "X-Content-Type-Options"  || missing="$missing xcto"
    echo "  [+] $sub (HTTP $http_code) missing:$missing"
    # Append finding
    python3 -c "
import json
with open('$REPORT') as f: r = json.load(f)
r['findings'].append({'subdomain':'$sub','status':$http_code,'missing_headers':'$missing'.strip()})
with open('$REPORT','w') as f: json.dump(r,f,indent=2)
" 2>/dev/null
    ((count++))
  fi
done

echo "[+] Done — $count live hosts checked. Report: $REPORT"
```

**Cron entry (run daily at 6 AM):**
```
0 6 * * * /opt/hunter/daily-hunt.sh clientcorp.com /var/reports/clientcorp
```

**Next iteration (add within 48 hours):**
- Port scan live hosts with `nmap -sV --top-ports 100`
- Check each live URL against known CVE signatures via `nuclei`
- Diff findings against yesterday's report and flag new/changed items
- Push new-finding alerts to Slack webhook

## Prerequisites

- `curl`, `python3`, `jq` installed
- `nmap`, `nuclei` (optional, for deeper scanning)
- Authorization from target owner (written scope document)
- Output directory with write permissions

## Workflow

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

1. **Define Objectives** — Clarify the goals and scope for hunter.
2. **Onboard Target** — Collect target domains, IP ranges, authorization scope; configure in pipeline config.
3. **Execute Scan Cycle** — Run passive recon → live host probe → service enumeration → vuln check → diff against baseline.
4. **Verify & Filter** — Auto-deduplicate; flag false positives for human review; promote confirmed findings.
5. **Deliver Report** — Generate weekly report; push critical alerts immediately via Slack/email.

## Deliverable Format

**Weekly Vulnerability Report (send as PDF to client every Monday 9 AM)**

```
┌─────────────────────────────────────────────────────┐
│ CONTINUOUS HUNTER — WEEKLY REPORT                    │
│ Client: [Company Name]                               │
│ Week: 2026-07-13 — 2026-07-19                       │
│ Status: 🔴 CRITICAL / 🟡 MEDIUM / 🟢 CLEAR          │
├─────────────────────────────────────────────────────┤
│                                                      │
│ 1. NEW FINDINGS THIS WEEK                           │
│ ┌──────┬──────────┬─────────┬──────────┬──────────┐ │
│ │  #   │ Severity │ Target  │   Type   │  Status  │ │
│ ├──────┼──────────┼─────────┼──────────┼──────────┤ │
│ │ CVE1 │  CRIT    │ api.xx  │ RCE      │ Unpatched│ │
│ │ CVE2 │  HIGH    │ app.xx  │ XSS      │ Mitigated│ │
│ │ I-42 │  MEDIUM  │ admin   │ Weak TLS │ New      │ │
│ └──────┴──────────┴─────────┴──────────┴──────────┘ │
│                                                      │
│ 2. ACTIVE FINDINGS (carried forward)                │
│   3 items from prior weeks, 1 past SLA              │
│                                                      │
│ 3. REMEDIATION TRACKER                              │
│   Avg time-to-fix this month: 4.2 days              │
│   SLA compliance: 89%                               │
│                                                      │
│ 4. SCOPE CHANGES                                    │
│   New subdomains detected: 2 (api-staging, dev-portal)│
│   Deprecated hosts: 1 (old-admin)                   │
│                                                      │
│ 5. RECOMMENDATIONS                                  │
│   • Patch api.example.com before next scan cycle    │
│   • Review CSP headers across all *.example.com     │
│   • Decommission dev-portal or add auth             │
├─────────────────────────────────────────────────────┤
│ Generated by Continuous Hunter Pipeline             │
│ Billing ID: [Invoice Line Item Reference]           │
└─────────────────────────────────────────────────────┘
```

Attach raw JSON/CSV findings as appendix. Include in the monthly invoice as a deliverable line item.

## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
2. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
3. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- [ ] All hunter procedures executed completely and documented
- [ ] New findings diffed against previous scan — only real changes flagged
- [ ] False positives identified and filtered before client delivery
- [ ] Results documented with evidence and timestamps
- [ ] Critical findings alerted immediately (not waiting for weekly report)
- [ ] Recommendations provided with risk-based prioritization

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll just run scans manually when I have time" | Manual means irregular. Irregular means you miss the window on zero-days and drift. Automation pays for itself in one missed CVE. |
| "Clients won't pay for a report of what they already have" | Clients don't have it — they have Nessus screenshots from last quarter. Fresh weekly data with change tracking IS the value. |
| "Open-source tools are free, why would they pay me $1K/mo?" | They pay for curation, triage, human judgment, and waking up when something critical appears — not for running nmap. |
| "I need expensive commercial scanners to be credible" | nucle + nmap + custom scripts catch 90% of surface-level vulns. The value add is your analysis, not the tool brand. |
| "What if nothing changes for 3 weeks?" | No news IS news — the clean report proves continuous coverage. Send it anyway; the absence of findings is itself a deliverable. |
