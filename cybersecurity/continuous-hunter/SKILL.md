---
name: continuous-hunter
description: Automated continuous bug hunting pipeline that runs 24/7 across multiple targets. Use when setting up persistent
  hunting, automating the find-report cycle, or scaling bug bounty income through automation.
domain: cybersecurity
tags:
- continuous
- cybersecurity
- hunter
- pipeline
- security
- threat-defense
---

# Continuous Hunter

Runs an automated hunting pipeline that discovers, tests, validates, and reports vulnerabilities across multiple targets continuously. Turns bug bounty from manual hunting into a money machine.

## When to Use

- Scaling from manual hunting to automated pipeline
- Running overnight/weekend scans across target portfolio
- Monitoring targets for new vulnerabilities
- Building passive income from bug bounties
- Maximizing findings per hour of effort

## The Process

1. **Scope the task** — define objectives, boundaries, and success criteria
2. **Gather information** — collect all necessary data and context before proceeding
3. **Execute the core workflow** — follow the domain-specific steps methodically
4. **Validate results** — verify outputs against expected outcomes or baselines
5. **Document findings** — record results, anomalies, and recommendations
### 1. Pipeline Architecture

```
[Target Pool] → [Recon Engine] → [Vuln Scanner] → [Validator] → [Reporter] → [Submit]
     ↑                                    ↓
[Monitor] ← [New Assets] ← [Scope Watcher] ← [Feedback Loop]
```

### 2. Recon Engine (Always Running)

Continuous asset discovery:

| Task | Frequency | Tool |
|------|-----------|------|
| Subdomain enumeration | Daily | subfinder, amass |
| Live host probing | Every 6h | httpx |
| URL discovery | Daily | katana, gau, waybackurls |
| Parameter discovery | On new URLs | arjun |
| Technology fingerprinting | On new hosts | Wappalyzer |
| Secret scanning | On new JS/files | trufflehog, gitleaks |
| Port scanning | Weekly | nmap (top 1000) |

**Output**: Structured asset database with timestamps, diffed against previous run.

### 3. Vuln Scanner (Targeted)

For each new/changed asset, run targeted checks:

```
For each new_subdomain:
  → Check for subdomain takeover (CNAME → dangling cloud resource)
  → Check for exposed services (.git, .env, .svn, backup files)
  → Check for default credentials on admin panels
  → Check for missing security headers

For each new_endpoint:
  → IDOR check (manipulate IDs, test authorization)
  → SSRF check (inject internal URLs in parameters)
  → XSS check (reflected input in response)
  → SQLi check (error-based probing)
  → Open redirect check (redirect parameter manipulation)
  → CORS check (origin reflection)

For each api_endpoint:
  → GraphQL introspection
  → Missing authentication
  → Rate limiting bypass
  → Parameter pollution
  → Mass assignment
```

### 4. Validator (7-Question Gate)

Before any finding becomes a report:

1. **Is it real?** — Reproduce from scratch, clean environment
2. **Is it exploitable?** — Demonstrate actual impact, not theoretical
3. **What's the impact?** — Quantify: data exposure, financial loss, account takeover
4. **Is it in scope?** — Check program rules, verify asset is covered
5. **Can it be reproduced?** — Write steps that anyone can follow
6. **What's the severity?** — CVSS v3.1 calculated, not guessed
7. **Is the PoC clean?** — Non-destructive, no real user data, cleanup included

**Auto-reject signals:**
- Cannot reproduce from clean state
- Impact is purely theoretical
- Asset is out of scope
- Finding is a duplicate of existing report
- PoC requires user interaction that won't happen naturally

### 5. Reporter (Auto-Generate)

Generate platform-specific reports:

- **HackerOne**: Title, Severity, Weakness, Summary, Steps, Impact, Supporting Material
- **Bugcrowd**: Title, Description, Steps, Impact, Remediation
- **Intigriti**: Title, Type, Severity, Description, Steps, Impact, Fix
- **Immunefi**: Title, Severity, Target, Vuln Type, Impact, PoC, Fix

Each report includes:
- Clear, concise title (e.g., "IDOR in /api/v2/users/{id}/orders allows reading any user's orders")
- CVSS score with vector string
- Step-by-step reproduction with curl/HTTP requests
- Screenshots or video proof
- Remediation recommendations

### 6. Feedback Loop

After submission:
- Track report status (triaged, validated, paid, duplicate, informative)
- Learn from rejections (what was wrong? better validation needed?)
- Update scanning rules based on accepted findings
- Add successful patterns to automated checks
- Track payout history per target per vuln type

## Automation Scheduling

```bash
# Cron schedule for continuous hunting
# Daily recon at 2 AM
0 2 * * * /path/to/recon-engine.sh

# Vuln scan every 6 hours
0 */6 * * * /path/to/vuln-scanner.sh

# Full pipeline on weekends (deeper scans)
0 0 * * 6 /path/to/deep-scan.sh

# Scope monitoring every hour
0 * * * * /path/to/scope-watcher.sh
```

## Income Optimization

This section covers income optimization for continuous hunter.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### Volume Strategy
- Run automated checks on 20+ targets simultaneously
- Focus on high-frequency, moderate-payout vulns (IDOR, missing auth, CORS)
- Automated report generation saves 30-60 min per finding
- Target: 5-10 validated findings per week

### Quality Strategy
- Deep manual testing on 2-3 primary targets
- Focus on critical/high severity ($1000+ per finding)
- Build expertise in specific domains (fintech, healthcare, e-commerce)
- Target: 1-3 high-value findings per week

### Hybrid (Recommended)
- Automated pipeline catches low-hanging fruit (volume)
- Manual deep dives on promising leads from automation (quality)
- Target: 3-7 findings per week, mix of $250-$5000 each

## Revenue Targets

| Level | Monthly Income | Effort | Strategy |
|-------|---------------|--------|----------|
| Beginner | $500-$2000 | 10h/week | Manual, 3-5 targets, common vulns |
| Intermediate | $2000-$10000 | 20h/week | Semi-automated, 10+ targets |
| Advanced | $10000-$50000 | 30h/week | Full pipeline, 20+ targets, deep expertise |
| Elite | $50000+ | Full-time | Automated pipeline + web3 + private programs |

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- Running scans without authorization
- Submitting findings without validation (wastes everyone's time)
- Not respecting rate limits (gets you banned)
- Submitting duplicate findings (check existing reports first)
- Aggressive scanning that causes service disruption
- Not cleaning up test data

## Verification

- Pipeline runs without errors for 24h
- All findings pass 7-question validation gate
- Reports are submission-ready
- No false positives submitted
- Revenue tracking shows positive ROI on time invested
- Target portfolio is diverse and well-managed

## Tools Required

| Category | Tools |
|----------|-------|
| Recon | subfinder, httpx, katana, gau, amass |
| Scanning | nuclei, dalfox, ffuf, feroxbuster |
| Validation | curl, Burp Suite, custom scripts |
| Reporting | Templates + automation scripts |
| Monitoring | Custom watchers, cron, notifications |
| Storage | SQLite/JSON for asset database |

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
