---
name: auth-patterns
description: Authentication patterns — OAuth 2.0, JWT, session management, MFA, RBAC, API key management. Use when working with auth patterns.
domain: operations
tags:
- api
- auth
- business-ops
- management
- operations
- patterns
---

## Overview

Implement production authentication — OAuth 2.0 flows, JWT tokens, session storage, multi-factor auth, role-based access control, and API key management.

## Capabilities

- OAuth 2.0 (authorization code, client credentials, PKCE)
- JWT token generation and validation
- Session-based authentication
- MFA/TOTP implementation
- RBAC (Role-Based Access Control)
- API key management and rotation
- Password hashing (bcrypt, argon2)

## When to Use
**Trigger phrases:**
- "auth patterns"
- "Authentication patterns — OAuth 2"


- Building user authentication systems
- Implementing SSO with third-party providers
- Designing API authentication (JWT vs API keys)
- Adding multi-factor authentication
- Implementing role-based permissions

## When NOT to Use

- Implementing authorization logic (auth patterns are about authentication)
- Building user registration flows (use user management patterns)
- Implementing OAuth provider (that's server-side OAuth, not client)
- Task is about session management only (use session patterns)
- You need to audit existing auth (use security review)
- Auth is handled by a third-party service (just integrate)

## Pseudo Code

Implementation patterns for common use cases with this skill.


### OAuth 2.0 Authorization Code Flow

```javascript
// Step 1: Redirect to provider
app.get('/auth/google', (req, res) => {
  const url = new URL('https://accounts.google.com/o/oauth2/v2/auth')
  url.searchParams.set('client_id', process.env.GOOGLE_CLIENT_ID)
  url.searchParams.set('redirect_uri', 'https://app.com/auth/callback')
  url.searchParams.set('response_type', 'code')
  url.searchParams.set('scope', 'openid email profile')
  url.searchParams.set('state', generateState())
  res.redirect(url.toString())
})

// Step 2: Handle callback
app.get('/auth/callback', async (req, res) => {
  const { code, state } = req.query
  if (state !== req.session.state) return res.status(400).send('Invalid state')

  const tokenRes = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    body: new URLSearchParams({
      code,
      client_id: process.env.GOOGLE_CLIENT_ID,
      client_secret: process.env.GOOGLE_CLIENT_SECRET,
      redirect_uri: 'https://app.com/auth/callback',
      grant_type: 'authorization_code',
    }),
  })
  const { access_token } = await tokenRes.json()
  const user = await fetchGoogleUser(access_token)
  req.session.userId = user.id
  res.redirect('/dashboard')
})
```

### JWT Token

```javascript
import jwt from 'jsonwebtoken'

// Generate
const token = jwt.sign(
  { sub: user.id, role: user.role, exp: Math.floor(Date.now() / 1000) + 3600 },
  process.env.JWT_SECRET,
  { algorithm: 'RS256' }
)

// Verify middleware
function authMiddleware(req, res, next) {
  const token = req.headers.authorization?.replace('Bearer ', '')
  if (!token) return res.status(401).json({ error: 'No token' })

  try {
    req.user = jwt.verify(token, process.env.JWT_PUBLIC_KEY)
    next()
  } catch (err) {
    res.status(401).json({ error: 'Invalid token' })
  }
}
```

### RBAC Middleware

```javascript
const permissions = {
  admin: ['users:read', 'users:write', 'billing:read', 'billing:write'],
  editor: ['users:read', 'content:read', 'content:write'],
  viewer: ['users:read', 'content:read'],
}

function requirePermission(permission) {
  return (req, res, next) => {
    const role = req.user.role
    if (!permissions[role]?.includes(permission)) {
      return res.status(403).json({ error: 'Forbidden' })
    }
    next()
  }
}

app.delete('/api/users/:id', authMiddleware, requirePermission('users:write'), deleteUser)
```

### MFA/TOTP

```javascript
import { authenticator } from 'otplib'

// Generate secret
const secret = authenticator.generateSecret()
const qrCode = await qrcode.toDataURL(authenticator.keyuri(user.email, 'MyApp', secret))

// Verify token
const isValid = authenticator.verify({ token: req.body.totpCode, secret: user.mfaSecret })
```

### API Key Management

```javascript
import crypto from 'crypto'

// Generate API key
const rawKey = crypto.randomBytes(32).toString('hex')
const hashedKey = crypto.createHash('sha256').update(rawKey).digest('hex')
await db.apiKeys.create({ userId, hashedKey, prefix: rawKey.slice(0, 8) })

// Verify API key
function apiKeyAuth(req, res, next) {
  const key = req.headers['x-api-key']
  if (!key) return res.status(401).json({ error: 'No API key' })

  const hashed = crypto.createHash('sha256').update(key).digest('hex')
  const apiKey = await db.apiKeys.findOne({ hashedKey: hashed })
  if (!apiKey) return res.status(401).json({ error: 'Invalid API key' })

  req.user = await db.users.findById(apiKey.userId)
  next()
}
```

## Common Patterns

- **PKCE for SPAs**: Use PKCE flow for single-page apps (no client secret)
- **Short-lived JWTs**: 15min access tokens + 7-day refresh tokens
- **Token rotation**: Rotate refresh tokens on each use
- **Password hashing**: Use argon2id (preferred) or bcrypt with cost 12+
- **API key prefix**: Show first 8 chars for identification, store only hash

## Red Flags

- Storing passwords in plain text
- Not using HTTPS for authentication
- Missing rate limiting on auth endpoints
- Not validating input properly
- Ignoring OWASP auth guidelines

## Verification

- [ ] Passwords are hashed securely
- [ ] HTTPS is used for all auth
- [ ] Rate limiting is in place
- [ ] Input is validated properly
- [ ] OWASP guidelines are followed

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We do not need SOPs" | Without SOPs, quality depends on memory. Document everything. |
| "Manual processes work fine" | Manual processes do not scale and are error-prone. Automate. |
| "Compliance is optional" | Compliance protects you legally. Build it in from the start. |