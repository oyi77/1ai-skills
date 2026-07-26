---
name: recon-automation
description: Automated reconnaissance and attack surface mapping. Use when mapping a target's infrastructure, discovering
  subdomains, or enumerating attack surface before security testing.
domain: cybersecurity
tags:
- cybersecurity
- recon
- security
- testing
- threat-defense
- money
version: 1.0.0
---

# Recon Automation Skill

## Overview

Systematic reconnaissance workflow for security assessments. Covers passive OSINT, active enumeration, secrets hunting, cloud asset discovery, and attack surface ranking. Integrates with industry-standard tools (subfinder, nmap, katana, trufflehog, cloud_enum, etc.) with graceful degradation when tools are missing. Results are persisted for reuse in subsequent hunting phases.

## Money-Making Overview

**Target buyer:** CISOs, security teams, pentest firms, and DevOps leads who need to understand their external attack surface before attackers find the holes.

**Service tiers:**

| Tier | Price | What They Get |
|------|-------|---------------|
| Basic — Attack Surface Scan | $500 | Automated subdomain enumeration, live host probing, tech stack detection, and secrets scan. One-time report for a single domain. Delivered in 48 hours. |
| Pro — Deep Recon Engagement | $1,500 | Everything in Basic plus full crawling (all URLs/params/endpoints), JS secrets extraction, cloud bucket discovery, origin IP bypass checks, and surface priority ranking. Includes 30-min call to walk through findings. |
| Enterprise — Continuous Attack Surface Monitoring | $4,000/mo | Weekly re-scans, change detection alerts, new subdomain/endpoint notifications, Slack integration, and quarterly executive briefings. Covers up to 5 domains. |

**First-dollar timeline:** First Basic report sold within 1 week of offering it to existing security contacts or local businesses. Pro deals close in 2-3 weeks. Enterprise contracts require a delivered Basic or Pro report as proof of work.

**Delivery:** Email PDF report or private Notion page. Payment via invoice (NET-15) or Stripe link.

## When to Use

**Trigger phrases:**
- "recon automation"
- "Pre-engagement reconnaissance for bug bounty or pentest"
- "Attack surface mapping for a target domain or organization"
- "Asset discovery: subdomains, live hosts, cloud buckets"


- Pre-engagement reconnaissance for bug bounty or pentest
- Attack surface mapping for a target domain or organization
- Asset discovery: subdomains, live hosts, cloud buckets
- Subdomain enumeration and validation
- Secrets leak detection across code repos, paste sites, and JS bundles
- Cloud bucket discovery (S3, Azure Blob, GCP Storage)
- Security audit preparation and scope inventory
- Re-running recon after discovering new root domains or acquisitions

## The Process

1. **Scope and authorize** — confirm written authorization and define target boundaries
2. **Reconnaissance** — enumerate targets, services, and potential attack surfaces
3. **Exploitation** — attempt exploitation of identified vulnerabilities within scope
4. **Post-exploitation** — document access level, lateral movement, and data exposure
5. **Report and remediate** — compile findings with reproduction steps and fix recommendations
### Step 1: Scope Validation

Verify the target is in-scope before any active or passive testing.

- Read program rules (bug bounty policy, ROE, pentest scope)
- Document authorization: who approved, what's in-scope, start/end dates
- Confirm target domains, IPs, CIDR ranges, and wildcards
- Identify explicit exclusions (e.g., `*.cdn.example.com`, production vs staging)
- Record scope in a local manifest file for reference during testing

**Output**: `scope-manifest.json` with authorized targets, exclusions, and authorization details.

### Step 2: Passive Recon

OSINT gathering without sending traffic to the target.

- **DNS records**: A, AAAA, MX, NS, TXT, CNAME, SOA via `dig` or `dnsx`
- **WHOIS**: domain registration, registrar, name servers, creation/expiry dates
- **Certificate Transparency**: crt.sh, CertSpotter for subdomains from TLS certs
- **Google Dorking**: `site:`, `inurl:`, `filetype:`, `intitle:` for exposed pages and files
- **Breach databases**: HaveIBeenPwned, DeHashed for associated email/password leaks
- **Code leaks**: GitHub search (`org:target`), GitLab, Pastebin, S3 bucket listings
- **Social media / metadata**: employee names, tech stack hints from job postings, LinkedIn

**Fallback**: If no OSINT tools available, use `curl` against public APIs (crt.sh, WHOIS).

### Step 3: Active Recon

Direct interaction with target infrastructure. Respect rate limits.

- **Subdomain enumeration**: `subfinder -d target.com`, `amass enum -passive -d target.com`, `chaos -d target.com`
- **DNS resolution**: `dnsx -l subdomains.txt -resp` to filter live resolvers
- **Port scanning**: `nmap -sV -sC -T3 -iL live_hosts.txt` (throttled), or `masscan` for fast sweep
- **Service fingerprinting**: `httpx -l subdomains.txt -title -tech-detect -status-code -follow-redirects`
- **Technology detection**: Wappalyzer CLI, httpx `-tech-detect` flag, WhatWeb

**Fallback**: Use `curl -I` for basic service fingerprinting if httpx unavailable. Use `nc -zv` for port checks if nmap unavailable.

### Step 4: Web Crawling

Discover URLs, parameters, and endpoints from live web services.

- **URL discovery**: `katana -u target.com -d 3 -jc` (with JS parsing), `gospider -s target.com`
- **Wayback Machine**: `waybackurls target.com` for historical URLs and parameters
- **Parameter extraction**: `arjun -u target.com` for hidden parameters, `x8` for parameter fuzzing
- **JavaScript analysis**: extract API endpoints, tokens, and secrets from JS bundles
- **robots.txt / sitemap.xml**: parse for hidden paths and disallowed directories
- **Endpoint mapping**: categorize URLs by type (API, admin, auth, upload, static)

**Fallback**: Use `curl` + manual regex for robots.txt/sitemap.xml parsing.

### Step 5: Secrets Hunting

Detect credential leaks and exposed sensitive data.

- **JS bundle analysis**: search for API keys, tokens, auth headers in minified JS
- **Exposed files**: `.env`, `.git/config`, `wp-config.php`, `.htaccess`, `config.json`
- **Git history**: `trufflehog git https://github.com/org/repo`, `gitleaks detect`, `noseyparker scan`
- **API key patterns**: regex for AWS keys (`AKIA...`), Google API keys, Stripe keys, JWT secrets
- **Hardcoded credentials**: search for `password=`, `secret=`, `token=`, `apikey=` in source
- **Paste sites**: search GitHub gists, Pastebin, Ghostbin for target-related leaks

**Fallback**: Use `grep -rE` with common secret regex patterns across downloaded files.

### Step 6: Cloud Recon

Discover cloud-hosted assets and potential misconfigurations.

- **S3 bucket discovery**: `cloud_enum -k target`, `S3Scanner --list`, brute-force bucket names
- **Azure Blob**: `cloud_enum -k target` with Azure module, check `<account>.blob.core.windows.net`
- **GCP Storage**: `cloud_enum -k target` with GCP module, check `<project>.storage.googleapis.com`
- **CloudFlare bypass**: find origin IPs via historical DNS (SecurityTrails), email headers, SSL certs
- **CDN identification**: identify CloudFlare, Fastly, Akamai, CloudFront from response headers
- **Metadata endpoints**: check `169.254.169.254` if SSRF is in-scope (only with authorization)

**Fallback**: Use `curl` to manually probe `<bucket>.s3.amazonaws.com` patterns.

### Step 7: Surface Ranking

Prioritize discovered assets by potential value for security testing.

| Priority | Asset Type | Why |
|----------|-----------|-----|
| P0 | Authentication endpoints | Login, signup, password reset, SSO, OAuth flows |
| P0 | API endpoints | REST/GraphQL with user-controlled input |
| P1 | File upload functionality | Potential for RCE, stored XSS, path traversal |
| P1 | Admin panels | Higher privilege, often less hardened |
| P1 | User-controlled input fields | Forms, search, comments, profile fields |
| P2 | Older/legacy endpoints | Likely less maintained, more vulns |
| P2 | Third-party integrations | Webhooks, OAuth callbacks, iframe embeds |
| P3 | Static assets | Low value unless serving user content |

**Output**: `surface-ranking.md` with categorized, prioritized asset inventory.

## External Tool Integration

Tools are optional. Each category has a fallback. Log missing tools and continue.

| Category | Tools | Fallback |
|----------|-------|----------|
| Subdomain | subfinder, amass, chaos, dnsx | crt.sh via `curl` |
| Probing | httpx, uncover | `curl -I` |
| Crawling | katana, gospider, waybackurls | `curl` + regex |
| Parameters | arjun, x8 | Manual parameter discovery |
| Secrets | trufflehog, gitleaks, noseyparker | `grep -rE` with regex patterns |
| DNS/Takeover | dnsReaper, subjack | Manual CNAME checks |
| Cloud | cloud_enum, S3Scanner | `curl` bucket probing |
| Scanning | nmap, masscan | `nc -zv` for port checks |

## Output Format

Structured asset inventory saved as markdown and JSON:

```
recon-output/
  scope-manifest.json       # Authorized scope
  passive/
    dns-records.md
    subdomains-ct.md
    whois.md
    osint-notes.md
  active/
    live-hosts.txt
    port-scan.md
    technologies.md
  crawling/
    urls-all.txt
    endpoints.md
    parameters.txt
    js-secrets.md
  secrets/
    leaked-credentials.md
    exposed-files.md
    git-leaks.md
  cloud/
    buckets.md
    origin-ips.md
    cdn-info.md
  surface-ranking.md         # Prioritized attack surface
  recon-summary.md           # Executive summary
```

## Session Persistence

- Save all recon output to `recon-output/` directory per target
- Each step appends to its respective file; re-runs update, not overwrite
- Load previous results before re-running to avoid duplicate work
- Share output with hunting phase: reference URLs, secrets, and ranked targets

## Incremental Recon

- Re-run specific steps as new information is discovered (e.g., new root domain from OSINT)
- New subdomains trigger re-run of Steps 3-4 (active + crawling)
- New live hosts trigger re-run of Steps 4-5 (crawling + secrets)
- Cloud findings trigger deeper cloud recon (Step 6)
- Track step completion timestamps in `recon-summary.md`

## First Action in 60 Minutes

Run this script against any target domain to produce a client-ready attack surface report. It enumerates subdomains, live hosts, technologies, and exposed secrets with zero config beyond a domain name.

```bash
#!/usr/bin/env python3
"""attack-surface-report.py — One-shot recon-as-service deliverable.
Usage: python3 attack-surface-report.py target.com client-name
"""
import json, subprocess, sys, os, urllib.request
from datetime import datetime
from pathlib import Path

domain = sys.argv[1]
client = sys.argv[2] if len(sys.argv) > 2 else domain
out = Path(f"recon-{domain.replace('.','-')}-{datetime.now().strftime('%Y%m%d')}")
(out / "evidence").mkdir(parents=True, exist_ok=True)

def run(cmd, timeout=60):
    try: return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    except Exception as e: return type("R",(),{"stdout":"","stderr":str(e)})()

# Step 1 — Subdomains via crt.sh (no API key needed)
print(f"[1/5] Enumerating subdomains for {domain}...")
resp = urllib.request.urlopen(
    f"https://crt.sh/?q=%25.{domain}&output=json", timeout=30
)
certs = json.loads(resp.read())
subdomains = sorted(set(e["name_value"] for e in certs if domain in e["name_value"]))
(out / "subdomains-all.txt").write_text("\n".join(subdomains))
print(f"       Found {len(subdomains)} subdomains")

# Step 2 — Live host probing
print(f"[2/5] Probing live hosts...")
live = []
for sd in subdomains[:200]:  # cap at 200
    r = run(f"curl -s -o /dev/null -w '%{{http_code}}' --connect-timeout 5 https://{sd}")
    if r.stdout.strip() not in ("", "000"):
        live.append(sd)
(out / "live-hosts.txt").write_text("\n".join(live))
print(f"       {len(live)} live hosts")

# Step 3 — Tech stack detection
print(f"[3/5] Detecting technologies...")
techs = {}
for h in live[:50]:  # cap at 50
    r = run(f"curl -sI --connect-timeout 5 https://{h}")
    headers = r.stdout.lower()
    detected = []
    if "cloudflare" in headers: detected.append("Cloudflare")
    if "nginx" in headers: detected.append("Nginx")
    if "apache" in headers: detected.append("Apache")
    if "server: gunicorn" in headers or "x-powered-by: python" in headers: detected.append("Python")
    if "x-powered-by: php" in headers: detected.append("PHP")
    if "x-powered-by: express" in headers: detected.append("Node.js/Express")
    if "x-amz-id" in headers or "x-amz-request-id" in headers: detected.append("AWS")
    if detected: techs[h] = detected
(out / "technologies.md").write_text(
    f"# Technology Stack — {domain}\n\n" +
    "\n".join(f"- **{h}**: {', '.join(t)}" for h, t in techs.items())
)

# Step 4 — Secrets scan in JS bundles
print(f"[4/5] Scanning for exposed secrets...")
secrets_found = []
patterns = {
    "AWS Key": r"AKIA[0-9A-Z]{16}",
    "Google API": r"AIza[0-9A-Za-z\-_]{35}",
    "Stripe Live": r"sk_live_[0-9a-zA-Z]{24,}",
    "Slack Token": r"xox[abp]-[0-9a-zA-Z\-]{10,}",
    "JWT": r"eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}",
}
import re
for h in live[:20]:
    r = run(f"curl -sL --connect-timeout 10 https://{h} 2>/dev/null | grep -oP 'src=[\"\\']([^\"\\']+\\.js)[\"\\']' | sed 's/src=[\"\\']//;s/[\"\\']//'")
    js_urls = r.stdout.strip().split("\n") if r.stdout.strip() else []
    for js in js_urls[:10]:
        js = js if js.startswith("http") else f"https://{h}{js}"
        r2 = run(f"curl -sL --connect-timeout 10 '{js}' 2>/dev/null")
        for name, pat in patterns.items():
            for m in re.finditer(pat, r2.stdout):
                secrets_found.append({"type": name, "match": m.group(), "url": js})
if secrets_found:
    (out / "secrets-found.json").write_text(json.dumps(secrets_found, indent=2))

# Step 5 — Attack Surface Report
print(f"[5/5] Generating report...")
total_endpoints = len(subdomains)
attack_surface_cats = {
    "Total Subdomains": total_endpoints,
    "Live Hosts": len(live),
    "Technologies Detected": sum(len(v) for v in techs.values()),
    "Secrets Found": len(secrets_found),
    "High-Value Targets": sum(1 for h in live if any(
        kw in h for kw in ["api", "admin", "login", "portal", "dashboard", "graphql"]
    )),
}

report = f"""# Attack Surface Report — {client}
**Domain:** {domain}  |  **Date:** {datetime.now().strftime('%Y-%m-%d')}

## Executive Summary
Automated external reconnaissance identified {total_endpoints} subdomains, {len(live)} live hosts,
{len(techs)} technology fingerprints, and {len(secrets_found)} potential credential leaks.

## Attack Surface Overview
| Category | Count |
|----------|-------|
"""
report += "\n".join(f"| {k} | {v} |" for k, v in attack_surface_cats.items())
report += """

## Live Hosts (Top 20)
""" + "\n".join(f"- {h}" for h in live[:20]) + """

## Technology Stack
""" + "\n".join(f"- **{h}**: {', '.join(t)}" for h, t in list(techs.items())[:20])

if secrets_found:
    report += "\n\n## Credential Leaks Detected\n"
    report += "\n".join(f"- `{s['type']}` at {s['url']}" for s in secrets_found)

report += "\n\n## Recommendations\n"
report += "1. Investigate all leaked credentials immediately\n"
report += "2. Review exposed admin/api subdomains for unauthorized access\n"
report += "3. Harden technology stack — update versions, remove fingerprinting headers\n"
report += "4. Enforce authentication on all discovered login/portal endpoints\n"
report += "5. Schedule quarterly attack surface reassessment\n"

(out / f"attack-surface-report-{domain}.md").write_text(report)
print(f"\n[DONE] Report saved to {out}/attack-surface-report-{domain}.md")

# Output summary for the invoice
summary = {
    "client": client, "domain": domain, "date": str(datetime.now().date()),
    "tier": "Basic", "price": "$500",
    "subdomains": total_endpoints, "live_hosts": len(live),
    "tech_fingerprints": len(techs), "secrets_found": len(secrets_found),
}
(out / "invoice-data.json").write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))
```

**Instructions:**
1. Save as `attack-surface-report.py`
2. Run: `python3 attack-surface-report.py example.com "Client Name Inc"`
3. Deliver the generated markdown report and invoice-data.json as your Basic tier deliverable
4. Takes ~10-30 minutes depending on target domain size

## Deliverable Format

Send the client a single PDF portfolio containing:

```
[CLIENT LOGO]

ATTACK SURFACE REPORT
[Client Name]
[Date]

Prepared by: [Your Name / Firm]
Engagement Type: External Reconnaissance (Basic / Pro / Enterprise)

---

SCOPE
- Domain(s): example.com, *.example.com
- Authorization: [Reference #]
- Date of scan: 2026-07-16

FINDINGS SUMMARY
- Subdomains discovered: 147
- Live hosts: 53
- Technologies identified: 8
- API/Admin endpoints: 12
- Credential leaks found: 3
- Open ports (average per host): 4

KEY RISKS
1. [Risk description — e.g., "3 exposed admin panels with no MFA"]
2. [Risk description — e.g., "AWS keys found in public JS bundle"]
3. [Risk description — e.g., "Legacy subdomain running EOL software"]

DETAILED FINDINGS
[Per-category breakdown with URLs, screenshots, evidence paths]

RECOMMENDATIONS
1. ...
2. ...
3. ...

---

INVOICE
Invoice #: INV-2026-XXXX
Amount: $500 (Basic) / $1,500 (Pro) / $4,000/mo (Enterprise)
Payment Terms: NET-15
Payment: [Stripe link or bank details]
```

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- Testing assets not explicitly listed in scope
- Aggressive scanning without throttling (`-T4`/`-T5` nmap, no rate limits)
- Ignoring `robots.txt` disallow rules during crawling
- Excessive request volume causing degradation or DoS
- Scanning without documented authorization
- Not respecting program-defined rate limits
- Running credential-stuffing or brute-force attacks without explicit permission
- Testing production systems when staging is in-scope

## Verification

- All discovered assets validated and categorized in output files
- Scope compliance verified: no out-of-scope hosts scanned or probed
- Tool outputs cross-referenced: subdomains from 2+ sources, live hosts confirmed
- Attack surface inventory complete with priority ranking
- Missing tools logged with fallback results documented
- Recon summary includes total counts per category and coverage gaps

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "They will just say no" | You are offering a paid service, not asking permission. Send the proposal. |
| "I need more certs to sell security work" | One delivered report is worth more than 10 certifications. Ship it. |
| "The market is saturated with recon tools" | Tools are a commodity. Delivered analysis with human judgment is not. |
| "Recon is just running tools, that is not billable" | The client is paying for interpretation, prioritization, and actionable insight — not curl output. |
| "Only big breaches need attack surface reports" | Every business with a website has an attack surface. Small companies need this most because nobody is looking. |
| "I will build the perfect toolchain first" | A single `curl` + `crt.sh` call already produces billable value. Start today. |
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |
