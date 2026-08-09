---
name: src-hunter
description: >-
  Structured SRC bug bounty hunting for security response centers: intake
  scoped targets and payout rules, recon subdomains and perimeters, enumerate
  attack surface, hunt prioritized vulnerability classes with time-boxed
  discipline, and report with evidence discipline. Use when hunting on SRC
  platforms, running time-boxed bounty campaigns, or applying China-specific
  asset fingerprinting.
domain: cybersecurity
subdomain: web-application-security
tags:
  - bug-bounty
  - src
  - reconnaissance
  - web-application-security
  - pentesting
  - vulnerability-hunting
version: '1.0'
author: oyi77
license: Apache-2.0
nist_csf:
  - DE.AE-02
  - ID.RA-01
  - RS.AN-03
---

# SRC Bug Bounty Hunting

## Overview

Security Response Centers (SRCs, 安全应急响应中心) run scoped, rules-based
bug bounty programs with payout tables, explicit out-of-scope lists, and
strict compliance red lines. Hunting them productively is a staged campaign —
intake, recon, enumeration, hunt, report — where the highest-value failures
are scope violations and evidence gaps, not missed vulnerabilities.

This skill encodes that campaign structure plus China-specific asset
fingerprinting (OA/中间件 identification, ICP-style asset mapping) and the
compliance discipline SRC programs enforce. It complements general
bug-hunting skills with the scope/payout discipline and time-boxed
prioritization that SRC platforms demand.

Source: cherry-picked and translated from `zhaoxuya520/reverse-skill`
(`skills/pentest-tools/src-hunter`, MIT license). Reference payload
libraries are not bundled; this skill is the standalone workflow.

## When to Use

**Trigger phrases:**
- "hunt on this SRC program"
- "SRC bounty campaign"
- "scope-in/scope-out for a Chinese SRC"
- "time-boxed vulnerability hunt"
- "report a finding to an SRC"
- "China asset fingerprinting for bounty"

Use this skill when:

- You are working a scoped SRC/bug bounty target with published rules and
  payout tables.
- You need a repeatable, evidence-disciplined campaign rather than ad hoc
  probing.
- Out-of-scope boundaries and compliance red lines must be respected.

## Prerequisites

- Scope authorization for every asset tested (see red lines below).
- A recon toolset: subdomain enumeration, HTTP probing, directory/parameter
  fuzzing, and a vulnerability scanner for confirmation.
- The program's rules page: scope, out-of-scope, payout table, reporting
  format.

## Workflow

### Phase 1: Intake

- Record the scoped target list, the out-of-scope list, the rules, and the
  payout table in a campaign notes file.
- Note submission format and any "do not test" conditions (production
  hours, rate limits, WAF behavior).
- Define the campaign time box and the target classes in scope.

### Phase 2: Recon

- Subdomain discovery: passive (certificate transparency, DNS) then active
  (brute force) enumeration; validate resolvable, live hosts.
- Perimeter mapping: CDN/WAF identification (knowledge-pass these — see red
  lines), origin discovery, cloud asset inventory.
- File-browser and API discovery: exposed directories, JS bundle endpoints,
  API documentation endpoints, and versioned API surfaces.
- China-specific fingerprinting: OA (office automation) systems,
  中间件 (middleware: Weblogic, Tomcat, Nacos, Spring, etc.) version
  identification — these are frequent SRC fast wins.

### Phase 3: Enumeration

- Directory probing: dictionary + wordlist against live hosts; log status
  code, size, and tech stack.
- Parameter dimension: enumerate parameters on interesting endpoints
  (including hidden/undocumented params), record param types.
- Functional audit: walk each in-scope feature (auth, upload, search,
  export, password reset) and note trust boundaries.
- Aim-tagging: tag each finding candidate with the vulnerability class it
  most plausibly maps to — this drives Phase 4 priority.

### Phase 4: Hunt

Prioritize by payout × exploitability using the standard class table:

| Priority | Classes |
|---|---|
| High | XSS (stored/reflected), RCE, SSRF, IDOR/BOLA, SQLi |
| Medium | CSRF on sensitive actions, Path Traversal, File Upload, SSTI, XXE |
| Low | Race conditions, HTTP Smuggling, OAuth/JWT/SAML misconfig, GraphQL abuse, Mobile API issues, LLM prompt-level flaws, DoS (scope-checked) |

For each candidate:

- Confirm the class with a minimal proof (no destructive payloads).
- Capture evidence: request/response pair, time, affected asset, impact
  chain.
- Rule out false positives before moving on; a confirmed finding beats ten
  unconfirmed leads.

### Phase 5: Report

- Evidence discipline: every claim maps to a reproducible request/response
  or trace — no screenshots of "trust me".
- Classification: state severity, vulnerability class, and business impact
  (which data/function is affected).
- Relation to known issues: search the program's public duplicates before
  submitting.
- Timeline: submission date, expected triage SLA, follow-up cadence.

## Compliance Red Lines

- No production-damaging actions: no data destruction, no account takeover
  beyond the minimal proof, no load-generating tests without authorization.
- No privacy exfiltration: never download or exfiltrate real user data;
  use placeholders and minimal samples.
- No DoS: no volume/amplification testing.
- Authorization scope only: never test out-of-scope or third-party assets
  reachable from an in-scope host.
- CDN/WAF knowledge-pass: identify them in recon and route around rather
  than attacking the protection layer itself.
- Contact the SRC before testing anything unusual (origin discovery,
  production-adjacent assets, third-party integrations).

## Hands-On Example

Quick reachability probe of in-scope assets before active fingerprinting
(Phase 2 — Recon). With Python's httpx, installed via `pip install httpx`:

```python
import httpx
for url in ["https://example.com"]:
    r = httpx.get(url, timeout=10, headers={"User-Agent": "probe"})
    print(url, r.status_code, len(r.content), r.headers.get("server"))
# https://example.com 200 559 cloudflare
```

Output above verified live (example.com 200, 559 bytes). A 200 from a
CDN-backed asset is a probe result, not a finding: log it, fingerprint the
origin — Kali's `apt install nuclei` installs nuclei 3.8+ — and only assets
that survive scope + compliance red-line checks get active testing.

## Verification

Run this self-check before claiming completion:

- [ ] Campaign notes contain scope, out-of-scope, rules, and payout table.
- [ ] Recon artifacts (subdomain list, live hosts, CDN/WAF map) exist and
      are reproducible.
- [ ] Every finding has a request/response evidence pair and an affected
      asset.
- [ ] Priority ordering followed payout × exploitability, not convenience.
- [ ] No red line was crossed; scope checks are documented per tested asset.
- [ ] Report includes classification, business impact, and duplicate check.

## When NOT to Use

- Unscoped testing or assets without authorization — stop and get scope.
- Pure infrastructure/networking programs (no web surface) — use network
  pentest workflows.
- Long-horizon APT-style engagement — SRC hunting is time-boxed by design.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "It's in-scope-adjacent, so it's probably fine." | Adjacent is out-of-scope. Test only listed assets; document the scope check per asset. |
| "I'll grab a real user record to prove impact." | Privacy exfiltration is a red line and a program-ban offense. Use placeholders. |
| "One more payload pass on this low-priority class." | Time-box discipline beats volume: spend the next pass on the payout-weighted table. |
| "The screenshot proves it." | A screenshot without a request/response pair is not reproducible evidence; SRC triage will reject it. |
| "The WAF blocks me, so I'll attack the WAF." | Knowledge-pass the protection layer; route around it or report the bypass properly. |