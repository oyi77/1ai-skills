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
---

# Recon Automation Skill

## Overview

Systematic reconnaissance workflow for security assessments. Covers passive OSINT, active enumeration, secrets hunting, cloud asset discovery, and attack surface ranking. Integrates with industry-standard tools (subfinder, nmap, katana, trufflehog, cloud_enum, etc.) with graceful degradation when tools are missing. Results are persisted for reuse in subsequent hunting phases.

## When to Use

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
