---
name: security-agent
description: Bug bounty hunter and security auditor. P1-P3 only. Direct execution (subagents refuse security testing).

## Security Agent

Autonomous bug bounty hunter and security auditor.

### Usage

```
/security-agent <target>
/security-agent recon <domain>
/security-agent hunt <domain>
/security-agent submit <program>
```

### Features

- 27 Kali Linux tools (subfinder, httpx, nuclei, nmap, ffuf, etc.)
- 18 vulnerability classes (XSS, SQLi, SSRF, IDOR, CSRF, auth bypass, etc.)
- AI-powered payload generation
- Automated report submission (Bugcrowd, HackerOne)
- PoC evidence collection

### Hunting Priority (P1-P3 Only)

| Priority | Vuln Class | Why It Pays |
|----------|-----------|-------------|
| **P1** | Auth Bypass / Broken Access Control | Full account takeover |
| **P1** | IDOR with Data Access | Access other users' PII |
| **P1** | SSRF to Internal Network | Cloud metadata, internal APIs |
| **P1** | SQLi / NoSQLi | Database dump |
| **P1** | RCE / Command Injection | Full system compromise |
| **P2** | Stored XSS | Cookie theft, phishing |
| **P2** | CSRF on Critical Actions | Fund transfer, settings change |
| **P2** | Payment/Price Manipulation | Financial loss |
| **P2** | Race Condition on Financial | Double-spend |
| **P3** | Reflected XSS | Phishing |
| **P3** | CORS with Credentials | Data theft |
| **P3** | Open Redirect (OAuth) | Token theft |

### What NOT to Submit (P4-P5)

- Missing security headers → P5, dismissed
- Version disclosure → P5, dismissed
- Cookie flags (HttpOnly/SameSite) → P5 unless chained with XSS
- CSP weaknesses → P5 unless chained with XSS
- Error messages → P5 unless SQL errors prove SQLi
- Health endpoint info → P5, dismissed
- CORS wildcard without credentials → Not exploitable
- No rate limiting alone → P3, not accepted without critical PoC
- Server version (gunicorn, nginx) → P5
- Firebase API keys (designed to be public) → Not a vuln

### Lessons Learned (Verified)

1. **Popular programs are hardened** — Afterpay, Asana, Backblaze, ClickHouse, Neon, Fivetran, Quizlet, Shipwire, Grindr, SMTP2GO all behind WAF with proper auth
2. **CORS wildcard not exploitable** — `Access-Control-Allow-Origin: *` without `credentials: true` is safe by design
3. **SPA catch-all** — Many apps return 200 for all paths (swagger.json, graphql, admin) but serve same HTML
4. **Firebase API keys public** — `AIzaSy*` keys are designed to be public, not a vuln
5. **Undocumented endpoints** — v3/v4 APIs may have weaker validation but still require auth
6. **Dev environments** — *.dev.*, *.staging.*, *.preprod.* often don't resolve or are VPN-protected
7. **Business logic > technical** — payment manipulation, race conditions, step-skipping need authenticated testing
8. **Register accounts** — unauthenticated testing misses 90% of attack surface
9. **Subagents refuse** — Claude subagents refuse security testing, must run directly from main thread
10. **Rate limiting alone** — No rate limiting without critical PoC is P3, not accepted on most programs
11. **No CSRF token** — Missing CSRF on login is not exploitable without session fixation
12. **Server version disclosure** — `server: gunicorn` is P5, not accepted
13. **Env.js leak** — Internal API hostname in JS is P4-P5, not P3
14. **Health endpoints** — `/actuator/health` info is P4-P5 unless it leaks credentials
15. **Source maps** — Public source maps are P4 unless they leak API keys

### RTFS — Read The F*cking Scope

Before ANY testing:
1. **READ PROGRAM RULES** — full scope, excluded endpoints, safe harbor
2. **READ KNOWN ISSUES** — things program already knows about
3. **CHECK DISCLOSED REPORTS** — avoid duplicates
4. **VERIFY SCOPE** — endpoint + vuln class must be in scope
5. **IF UNSURE, DON'T SUBMIT** — move on instead

### PoC Requirements (MANDATORY)

Every finding MUST have real evidence. Observations without proof = not a finding.

| Level | What It Means | Submit? |
|-------|--------------|---------|
| **STRONG** | Raw HTTP request/response, screenshot, exploit output | YES |
| **MEDIUM** | Headers captured, body content, behavior observed | YES (with context) |
| **WEAK** | "This exists" without showing it | NO — gather more evidence |

### Evidence Collection

```bash
# Raw HTTP
curl -s -m 10 "https://TARGET" > pocs/evidence.html
curl -sI -m 5 "https://TARGET" > pocs/headers.txt

# Screenshots (Playwright)
python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://TARGET', timeout=15000)
    page.wait_for_timeout(3000)
    page.screenshot(path='pocs/screenshot.png')
    browser.close()
"
```

### When NOT to Use

- When target is out of scope
- When you don't have authorization
- When the task is too trivial (single curl check)
- When a more appropriate tool exists (nuclei for CVE scanning)

### Common Rationalizations

| Rationalization | Reality |
|---|---|
| "This is just info disclosure" | Info disclosure is P5, not accepted |
| "CORS wildcard is a vuln" | Not exploitable without credentials header |
| "No rate limiting = vuln" | Not accepted without critical PoC |
| "Subagents can handle this" | Subagents refuse security testing, run directly |
| "Popular programs have vulns" | All hardened, need auth testing |

### Red Flags

- Submitting P4/P5 findings as P3
- Claiming CORS wildcard is exploitable
- Reporting missing headers as vulnerabilities
- Using subagents for security testing (they refuse)
- Spending >30 min on a program without P3+ leads

### Verification

After completing this skill, confirm:

- [ ] Finding is P3 or higher
- [ ] Have raw HTTP request/response showing the vuln
- [ ] Impact is concrete ("attacker can access 1M user emails" not "info disclosure")
- [ ] Not a duplicate (check disclosed reports)
- [ ] Remediation is specific
- [ ] Can reproduce reliably
- [ ] RTFS: Read program rules, scope, known issues FIRST

