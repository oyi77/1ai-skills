---
name: bug-chain-builder
description: Chain multiple low-severity bugs into critical impact for maximum bounty payouts. Use when combining vulnerabilities,
  escalating impact, or when a single bug isn't enough for a high-severity report.
domain: cybersecurity
tags:
- bug
- builder
- chain
- cybersecurity
- security
- threat-defense
---

# Bug Chain Builder

The real money in bug bounty isn't finding one bug — it's chaining 3-4 "low" bugs into account takeover or RCE. A $250 info disclosure + $500 open redirect + missing rate limit = $10,000 critical chain.

## When to Use

- Found a low-severity bug that feels "not impactful enough"
- Need to escalate impact for a higher bounty
- Multiple findings on the same target that could combine
- Report marked as "informative" — chain it to critical
- Want to maximize payout from a single target

## The Process

1. **Scope the task** — define objectives, boundaries, and success criteria
2. **Gather information** — collect all necessary data and context before proceeding
3. **Execute the core workflow** — follow the domain-specific steps methodically
4. **Validate results** — verify outputs against expected outcomes or baselines
5. **Document findings** — record results, anomalies, and recommendations
### 1. Impact Escalation Matrix

| Low Bug A | + Low Bug B | = Critical Chain |
|-----------|-------------|-----------------|
| Username enumeration | Weak password policy | Mass account takeover |
| Open redirect | OAuth implicit flow | Token theft → ATO |
| CORS misconfig | API returning PII | Cross-origin data leak |
| IDOR (read) | IDOR (write) | Full account control |
| Info disclosure (internal URLs) | SSRF | Internal network access |
| Missing rate limit | Password reset | Account takeover |
| XSS (self) | Cookie without Secure | Session hijacking |
| Subdomain takeover | CNAME to auth service | Full auth bypass |
| JS source leak | Hardcoded API keys | Backend access |
| Clickjacking | CSRF | Forced actions on behalf of user |

### 2. Chain Patterns

#### The Account Takeover Chain
```
1. Username enumeration via login error messages ($0 → informative)
2. Password reset token not invalidated after use ($250 → low)
3. Token exposed in URL parameters ($250 → low)
4. Missing rate limit on reset endpoint ($500 → medium)
   → CHAIN: Enumerate users → brute force reset → steal tokens → mass ATO
   → RESULT: $5000-$10000 (critical)
```

#### The Data Exfiltration Chain
```
1. GraphQL introspection enabled (info disclosure → $250)
2. IDOR on user query by sequential ID ($500 → medium)
3. No rate limit on API ($250 → low)
   → CHAIN: Discover schema → enumerate all users → dump database
   → RESULT: $10000+ (critical - mass data breach)
```

#### The Internal Network Pivot Chain
```
1. XSS in markdown renderer (self-XSS → $0)
2. CORS misconfiguration reflects Origin ($500 → medium)
3. Internal API accessible via SSRF ($1000 → high)
   → CHAIN: Inject XSS via CORS → SSRF to internal API → internal network access
   → RESULT: $5000-$15000 (critical)
```

#### The OAuth Kill Chain
```
1. Open redirect via path traversal ($500 → medium)
2. OAuth redirect_uri not validated ($1000 → high)
3. Token stored in localStorage ($250 → low)
   → CHAIN: Redirect OAuth flow → steal token → persistent access
   → RESULT: $5000-$10000 (critical - full account takeover)
```

#### The Supply Chain Chain
```
1. Dependency confusion in private package ($1000 → high)
2. CI/CD pipeline runs on PR without approval ($500 → medium)
3. Secrets in CI environment variables ($500 → medium)
   → CHAIN: Poison dependency → execute in CI → steal secrets → prod access
   → RESULT: $10000-$50000 (critical)
```

### 3. Chain Discovery Techniques

#### Graph-Based Analysis
Map all findings as nodes, look for paths:
```
[User Input] → [Processing] → [Internal Service] → [Data Store]
     ↑               ↑              ↑                ↑
  XSS/SQLi       SSRF/RCE      IDOR/AuthZ       Data Exfil
```

#### Time-Based Correlation
Findings that seem unrelated may chain when:
- Same authentication context
- Same API version
- Same backend service
- Same developer's code

#### Cross-Feature Correlation
Bugs in different features that share:
- Same user session handling
- Same authorization middleware
- Same data access layer
- Same error handling

### 4. Report Writing for Chains

```
Title: Account Takeover via Chained Vulnerabilities

Summary:
By combining [Bug A], [Bug B], and [Bug C], an attacker can
take over any user account without interaction.

Step 1: [Low bug - enumerate users]
Step 2: [Medium bug - extract token]
Step 3: [Low bug - no rate limit on reset]
Step 4: [Chain - mass exploitation]

Impact: Full account takeover for all users.
Severity: Critical (CVSS 9.1)
```

**Key rule**: The chain's severity is determined by the HIGHEST impact achievable, not the average of individual bugs.

### 5. Common Chain Recipes

| Recipe | Components | Result |
|--------|-----------|--------|
| Mass ATO | Enum + weak reset + no rate limit | Critical |
| Data Dump | Introspection + IDOR + no rate limit | Critical |
| RCE via Upload | Unrestricted upload + path traversal + executable dir | Critical |
| Full Account Control | XSS + missing HttpOnly + session fixation | Critical |
| Internal Access | SSRF + internal service + default creds | Critical |
| Financial Theft | Race condition + decimal precision + no balance check | Critical |

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- Submitting chain that requires unrealistic prerequisites
- Each individual bug must be real — don't fabricate components
- Chain must be reproducible end-to-end
- Don't overstate impact — prove the chain works
- Clean up all artifacts from testing

## Verification

- Each component bug is independently verified
- Chain works end-to-end from clean state
- Impact is demonstrated, not theoretical
- CVSS score reflects combined impact
- PoC demonstrates full chain execution

## Revenue Impact

| Single Bug | With Chaining | Increase |
|-----------|---------------|----------|
| $250 (info disclosure) | $5000 (data breach) | 20x |
| $500 (open redirect) | $10000 (ATO) | 20x |
| $0 (self-XSS) | $5000 (session hijack) | ∞ |
| $250 (subdomain takeover) | $15000 (auth bypass) | 60x |

## Overview

> Section content — see SKILL.md body for full details.
