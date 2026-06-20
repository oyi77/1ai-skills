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
---

# Bug Hunting Skill

## Overview

AI-orchestrated bug bounty workflow covering the full cycle from reconnaissance to report generation. Inspired by claude-bug-bounty (23 commands, 8 agents, 20 web2 + 10 web3 vuln classes, auth-aware hunting, persistent memory system). Designed for ethical security researchers operating within authorized bug bounty programs.

## When to Use

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
