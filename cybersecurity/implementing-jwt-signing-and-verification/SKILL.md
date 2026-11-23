---
name: implementing-jwt-signing-and-verification
description: Use when JSON Web Tokens (JWT) defined in RFC 7519 are compact, URL-safe
  tokens used for authentication and authorization in web applications. This skill
  covers implementing secure JWT signing with HMAC-SHA256
domain: cybersecurity
subdomain: cryptography
tags:
- cryptography
- jwt
- authentication
- token-security
- digital-signatures
version: '1.0'
author: oyi77
license: Apache-2.0
nist_csf:
- PR.DS-01
- PR.DS-02
- PR.DS-10
category: cybersecurity
---

# Implementing JWT Signing and Verification

## Overview

JSON Web Tokens (JWT) defined in RFC 7519 are compact, URL-safe tokens used for authentication and authorization in web applications. This skill covers implementing secure JWT signing with HMAC-SHA256, RSA-PSS, and EdDSA algorithms, along with verification, token expiration, claims validation, and defense against common JWT attacks (algorithm confusion, none algorithm, key injection).


## When to Use
**Trigger phrases:**
- "implementing jwt signing and verification"
- "JSON Web Tokens (JWT) defined in RFC 7519 are compact, URL-safe tokens used for "


- When deploying or configuring implementing jwt signing and verification capabilities in your environment
- When establishing security controls aligned to compliance requirements
- When building or improving security architecture for this domain
- When conducting security assessments that require this implementation

## Prerequisites

- Familiarity with cryptography concepts and tools
- Access to a test or lab environment for safe execution
- Python 3.8+ with required dependencies installed
- Appropriate authorization for any testing activities

## Objectives

- Implement JWT signing with HS256, RS256, ES256, and EdDSA
- Verify JWT signatures and validate standard claims
- Implement token expiration, not-before, and audience validation
- Defend against algorithm confusion and none algorithm attacks
- Implement JWT key rotation with JWK Sets
- Build a complete authentication middleware

## Key Concepts

This section covers key concepts for implementing jwt signing and verification.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### JWT Algorithms

| Algorithm | Type | Key | Security Level |
|-----------|------|-----|---------------|
| HS256 | Symmetric (HMAC) | Shared secret | 128-bit |
| RS256 | Asymmetric (RSA) | RSA key pair | 112-bit |
| ES256 | Asymmetric (ECDSA) | P-256 key pair | 128-bit |
| EdDSA | Asymmetric (Ed25519) | Ed25519 pair | 128-bit |

### Common JWT Attacks

- **Algorithm confusion**: Switching from RS256 to HS256, using public key as HMAC secret
- **None algorithm**: Setting alg=none to bypass signature verification
- **Key injection**: Embedding key in JWK header
- **Weak secrets**: Brute-forcing short HMAC secrets
- **Token replay**: Reusing valid tokens without expiration

## Security Considerations

- Always validate the algorithm header against an allowlist
- Never accept alg=none in production
- Use asymmetric algorithms (RS256, ES256) for distributed systems
- Set short expiration times (15 min for access tokens)
- Implement token refresh mechanism
- Store secrets securely (not in source code)

## Validation Criteria

- [ ] JWT signing produces valid tokens for all algorithms
- [ ] Signature verification rejects tampered tokens
- [ ] Expired tokens are rejected
- [ ] Algorithm confusion attack is prevented
- [ ] None algorithm is rejected
- [ ] JWK key rotation works correctly
- [ ] Claims validation enforces all required claims
## When NOT to Use

- You need to test the implementation (use performing-* skills)
- Task is about configuring existing tools (use configuring-* skills)
- You need to analyze security events (use analyzing-* skills)
- Task is about building detection rules (use building-* skills)
- You don't have access to the target environment
- Task requires vendor-specific expertise (consult vendor docs)


## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Testing without rate limiting, potentially causing service degradation
- Storing sensitive test data (credentials, tokens) in plain text logs
- Using automated scanners blindly without reviewing results for false positives
## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Vulnerabilities reproduced with proof-of-concept and impact analysis
- False positives filtered out through manual verification
- Fix recommendations include code-level remediation guidance

## Workflow

1. **Choose the algorithm per trust boundary** — HS256 only when issuer and verifier share one secret store; RS256/ES256/EdDSA when multiple services verify. Never let the token's `alg` header select the algorithm.
2. **Generate and store keys** — `openssl genpkey -algorithm ed25519 -out jwt.key` (or RSA 2048+/P-256). Load from env/KMS/secret manager, never from source. Record key ID (`kid`) in the token header.
3. **Issue the token** — set `iss`, `aud`, `sub`, `exp` (≤15 min for access tokens), `nbf`, `iat`, `jti`. Keep claims minimal; no PII, no secrets, no roles that change faster than the token lifetime.
4. **Verify with a pinned algorithm and key** — decode with an explicit allowlist, resolve the key from your own JWKS or secret store by `kid`, and reject any `alg: none` or header-supplied key material (`jwk`, `jku`, `x5u`).
5. **Validate every claim you depend on** — signature first, then `exp`/`nbf` with small leeway, then `aud`/`iss` exact match, then `jti` against the replay/revocation store when you keep one.
6. **Handle refresh safely** — rotate refresh tokens on use, bind them to a device/client identifier, and keep refresh lifetimes short enough to be revocable.
7. **Rotate keys** — publish new key in JWKS alongside the old one, sign with the new `kid`, keep verifying the old until all outstanding tokens expire, then remove it.
8. **Test the attack cases** — tamper the payload, flip `alg` to `HS256` using the public key as secret, set `alg: none`, replay an expired token, and swap `aud`. Each must be rejected with a logged reason and no stack trace in the response.

```python
import jwt  # PyJWT
from jwt import InvalidTokenError

ALLOWED = {"EdDSA", "RS256"}

def verify(token: str, key, *, audience: str, issuer: str):
    # algorithms= is an allowlist; key is resolved from your store by kid, never from the header
    return jwt.decode(token, key, algorithms=sorted(ALLOWED),
                      audience=audience, issuer=issuer,
                      options={"require": ["exp", "iat", "aud", "iss"]})
try:
    claims = verify(token, key, audience="api://orders", issuer="https://auth.example.com")
except InvalidTokenError as e:
    raise AuthError("token rejected") from e  # log e, never return it to the client
```

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |