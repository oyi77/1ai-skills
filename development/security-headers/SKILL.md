---
name: security-headers
description: Web security headers — CSP, CORS, HSTS, X-Frame-Options. Configure, audit, and harden HTTP security headers. Use when working with security headers.
domain: development
tags:
- coding
- headers
- security
- software-engineering
- testing
---


## Overview

HTTP security headers protect web applications from XSS, clickjacking, MIME sniffing, and other attacks. This skill covers configuring Content Security Policy (CSP), CORS, HSTS, and other headers, plus auditing tools to verify proper setup.

## Capabilities

- Configure Content Security Policy (CSP) directives
- Set up Cross-Origin Resource Sharing (CORS) policies
- Enable HTTP Strict Transport Security (HSTS)
- Audit existing headers with security scanners
- Implement Permissions-Policy for feature restriction
- Generate headers for Express, Nginx, Apache, Cloudflare

## When to Use
**Trigger phrases:**
- "security headers"
- "Web security headers — CSP, CORS, HSTS, X-Frame-Options"


- Hardening a web application before production
- Fixing CSP or CORS issues in security audits
- Configuring headers for API servers
- Meeting compliance requirements (PCI-DSS, SOC2)
- Preventing XSS, clickjacking, or data leakage

## Pseudo Content

- Configure audit, configure, cors, frame, harden settings before first use


### Content Security Policy (CSP)
```javascript
// Express.js
app.use((req, res, next) => {
  res.setHeader('Content-Security-Policy', [
    "default-src 'self'",
    "script-src 'self' 'nonce-{random}' https://cdn.jsdelivr.net",
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
    "img-src 'self' data: https:",
    "font-src 'self' https://fonts.gstatic.com",
    "connect-src 'self' https://api.example.com",
    "frame-ancestors 'none'",
    "base-uri 'self'",
    "form-action 'self'",
  ].join('; '));
  next();
});
```

### CORS Configuration
```javascript
// Express.js with cors middleware
const cors = require('cors');

app.use(cors({
  origin: ['https://app.example.com', 'https://admin.example.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
  maxAge: 86400,              // Preflight cache 24h
}));

// Nginx
# add_header Access-Control-Allow-Origin "https://app.example.com";
# add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE";
# add_header Access-Control-Allow-Headers "Content-Type, Authorization";
# add_header Access-Control-Allow-Credentials "true";
# add_header Access-Control-Max-Age "86400";
```

### HSTS (HTTP Strict Transport Security)
```nginx
# Nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

# Express.js
app.use((req, res, next) => {
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains; preload');
  next();
});
```

### Full Security Headers Stack
```javascript
// Express.js middleware
app.use((req, res, next) => {
  // Prevent MIME sniffing
  res.setHeader('X-Content-Type-Options', 'nosniff');

  // Clickjacking protection
  res.setHeader('X-Frame-Options', 'DENY');

  // XSS protection (legacy)
  res.setHeader('X-XSS-Protection', '1; mode=block');

  // Referrer policy
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');

  // Permissions policy
  res.setHeader('Permissions-Policy', 'camera=(), microphone=(), geolocation=()');

  // Remove server header
  res.removeHeader('X-Powered-By');

  next();
});
```

### Audit with CLI
```bash
# Security Headers check
curl -sI https://example.com | grep -iE "strict-transport|content-security|x-frame|x-content-type|referrer-policy|permissions-policy"

# Using securityheaders.com API
curl "https://securityheaders.com/?q=https://example.com&followRedirects=on"

# Mozilla Observatory
curl "https://http-observatory.security.mozilla.org/api/v1/analyze?host=example.com"

# Using npx
npx security-headers check https://example.com
```

### Nginx Full Config
```nginx
server {
    listen 443 ssl http2;

    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # CSP
    add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';" always;

    # Anti-clickjacking
    add_header X-Frame-Options "DENY" always;

    # MIME sniffing
    add_header X-Content-Type-Options "nosniff" always;

    # Referrer
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Permissions
    add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;

    # Remove server version
    server_tokens off;
}
```

## Common Patterns

| Header | Protection | Value |
|--------|-----------|-------|
| `Content-Security-Policy` | XSS, injection | `default-src 'self'` |
| `Strict-Transport-Security` | SSL stripping | `max-age=31536000; includeSubDomains` |
| `X-Frame-Options` | Clickjacking | `DENY` or `SAMEORIGIN` |
| `X-Content-Type-Options` | MIME sniffing | `nosniff` |
| `Referrer-Policy` | Data leakage | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | Feature abuse | `camera=(), microphone=()` |

## How to Use

1. Understand the requirement and existing codebase patterns
2. Design the solution with error handling and testability in mind
3. Implement incrementally with tests for each change
4. Verify against expected outcomes (manual and automated)
5. Document usage, edge cases, and integration points
6. Review with team before merging to shared branches

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Red Flags

- **Skipping tests to ship faster**: Untested code breaks in production when you least expect it
- **No error handling in production code**: Unhandled errors crash services and lose user data
- **Hardcoded configuration values**: Hardcoded values prevent environment switching and leak secrets
- **Ignoring security implications**: Missing input validation, auth bypasses, and injection vulnerabilities
- **Over-engineering simple solutions**: Premature abstraction adds complexity without proportional benefit

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Tests slow me down" | Bugs slow you down 10x more. Tests are speed, not overhead. |
| "I will refactor later" | Technical debt compounds. Refactor as you go. |
| "It works on my machine" | If it is not in CI, it does not work. Ship proof, not claims. |