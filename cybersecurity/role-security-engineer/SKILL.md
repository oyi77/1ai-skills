---
name: role-security-engineer
description: Use when orchestrating application security defenses, threat modeling,
  API vulnerability mitigation, access control enforcement, security headers, and
  cloud compliance.
domain: cybersecurity
author: oyi77
version: 1.0.0
category: cybersecurity
tags:
- security
- appsec
- cybersecurity
- threat-modeling
- access-control
- owasp
- cis-benchmarks
- hardening
license: MIT
subdomain: security-engineering
---

## Overview

The `role-security-engineer` skill directs defensive application security, cloud security posture management, and vulnerability mitigation. Rather than relying on sporadic, passive scanning or surface-level checkbox compliance, this role coordinates proactive threat modeling, automated API security defense, fine-grained access control (BOLA/IDOR) enforcement, strict HTTP security header hardening, and continuous CIS compliance benchmarking across cloud infrastructure.

```
[Phase 1: Threat Modeling & Surface Recon] ──► [Phase 2: Access & Auth Gate Audit] ──► [Phase 3: Vulnerability Remediation]
                                                                                                    │
                     [Phase 5: Continuous Defense & CIS] ◄── [Phase 4: Defensive Hardening] ◄──────┘
```

The security engineer operates on the principle of defense-in-depth, enforcing least privilege, zero trust boundaries, and parameter validation across all internal and public attack surfaces.

## When to Use

- When conducting end-to-end application security reviews and defensive threat modeling.
- When evaluating and mitigating OWASP Top 10 vulnerabilities (SQLi, XSS, SSRF, BOLA/IDOR).
- When implementing or auditing RBAC/ABAC authorization barriers across API endpoints.
- When hardening web applications with strict Content Security Policy (CSP), HSTS, and CORS rules.
- When assessing AWS, GCP, or Azure environments against CIS Security Benchmarks.
- When reviewing third-party dependency vulnerabilities and automated SAST/DAST scanner outputs.

## When NOT to Use

- When conducting external offensive penetration tests or red team exploits (use `cybersecurity/role-penetration-tester`).
- When fixing general application logic bugs unrelated to security or auth (use `development/role-software-engineer`).
- When managing general CI/CD deployment pipelines or Docker build caches (use `devops/role-devops-sre-engineer`).
- When performing financial risk modeling or quantitative trading (use `trading/role-quantitative-trader`).

## Deterministic Dispatch Matrix

| Security Challenge / Attack Vector | Delegated Child Skill | Primary Defensive Artifact |
|---|---|---|
| Comprehensive cybersecurity routing and triage across 790+ playbooks | `cybersecurity/cybersecurity-router` | Triage classification and specialized playbook assignment |
| Aggressive API vulnerability fuzzing, rate limit evasion, and injection defense | `cybersecurity/api-destroyer` | API threat report, rate limiting rules, and parameter sanitization |
| Insecure direct object references, cross-tenant data leaks, BOLA/BFLA | `cybersecurity/testing-for-broken-access-control` | Object-level auth matrix and tenant isolation unit tests |
| Automated vulnerability assessment, CVE triage, and patch prioritization | `cybersecurity/vulnerability-scanner` | Vulnerability assessment ledger with verified EPSS/CVSS ranking |
| Missing CSP, clickjacking, MIME sniffing, and insecure cookie attributes | `development/security-headers` | Hardened reverse proxy / web framework security header config |
| Cloud misconfigurations, over-permissive IAM, and public storage exposure | `cybersecurity/auditing-cloud-with-cis-benchmarks` | CIS compliance report and automated terraform remediation |

## Workflow

### Phase 1: Attack Surface Reconnaissance & Threat Modeling

1. Map exposed ingress routes, unauthenticated endpoints, and external webhook receivers.
2. For broad, multi-vector investigations, dispatch to `cybersecurity/cybersecurity-router` to assign specialized domain sub-playbooks.
3. Classify sensitive assets (PII, tokens, payment data, cryptographic secrets).

### Phase 2: Authentication & Authorization Gate Audit

1. Audit session lifetimes, token signatures, and role-based permissions.
2. Dispatch to `cybersecurity/testing-for-broken-access-control` to verify tenant scoping and prevent cross-account IDOR vulnerabilities.
3. Validate that every database mutation explicitly checks `where userId = currentUser.id`.

### Phase 3: Vulnerability Scanning & Exploit Mitigation

1. Execute automated SAST/DAST sweeps using `cybersecurity/vulnerability-scanner`.
2. Subject external endpoints to stress and parameter tampering tests via `cybersecurity/api-destroyer`.
3. Eliminate injection paths by requiring parameterized SQL queries and typed ORM bindings.
4. Block SSRF vectors by enforcing IP allowlists and disabling loopback/private subnet requests (127.0.0.1, 10.0.0.0/8, 169.254.169.254).

### Phase 4: Defensive Boundary Hardening

1. Implement hardened HTTP security headers using `development/security-headers` (strict CSP, HSTS, X-Frame-Options: DENY, X-Content-Type-Options: nosniff).
2. Enforce `HttpOnly`, `SameSite=Strict`, and `Secure` attributes on all session cookies.
3. Configure API Gateway rate limiting and burst throttling.

### Phase 5: Cloud Posture & Compliance Benchmarking

1. Run infrastructure posture audits via `cybersecurity/auditing-cloud-with-cis-benchmarks`.
2. Verify zero public S3/Blob storage buckets, enforce KMS encryption at rest, and rotate stale access keys.
3. Generate signed security compliance audit receipt with zero high/critical unmitigated findings.

## Anti-Rationalization

| Security Excuse | Flawed Rationalization | Required AppSec Discipline |
|---|---|---|
| "The endpoint is hidden; nobody will guess the URL" | "Security through obscurity is sufficient for internal tools." | Obscurity is zero protection. Implement explicit authentication and authorization on every route. |
| "We trust our internal network and microservices" | "Requests behind the firewall do not need authentication." | Zero Trust architecture requires mutual authentication (mTLS/JWT) at every service boundary. |
| "A WAF will block any SQL injections" | "We don't need to rewrite legacy queries if Cloudflare is on." | WAFs can be bypassed via encoding tricks. Parameterize queries at the application level. |
| "CORS with `*` is fine for quick frontend dev" | "It prevents frontend connection errors." | Wildcard CORS exposes authenticated user data to malicious origins. Explicitly whitelist exact origins. |
| "Fixing low/medium CVEs can wait for next quarter" | "Only critical CVEs are actively exploited." | Attackers chain low-severity info disclosures and misconfigurations into critical RCEs. Remediate systematically. |

## Implementation Examples

### Automated Security Headers Auditor (Python)

```python
import urllib.request
import sys
from typing import Dict, List

REQUIRED_HEADERS: Dict[str, str] = {
    "X-Frame-Options": "DENY",
    "X-Content-Type-Options": "nosniff",
    "Strict-Transport-Security": "max-age=",
    "Content-Security-Policy": "default-src",
    "Referrer-Policy": "strict-origin-when-cross-origin",
}

def audit_security_headers(target_url: str) -> List[str]:
    """Audits a live HTTP endpoint for mandatory security headers."""
    print(f"Auditing security headers for: {target_url}")
    req = urllib.request.Request(target_url, headers={"User-Agent": "SecurityAuditor/1.0"})
    
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            headers = {k.title(): v for k, v in resp.headers.items()}
    except Exception as e:
        print(f"Connection failed: {e}")
        return ["Target unreachable"]

    violations: List[str] = []
    for header, expected_snippet in REQUIRED_HEADERS.items():
        val = headers.get(header.title())
        if not val:
            violations.append(f"MISSING: Header '{header}' not present in response.")
        elif expected_snippet not in val:
            violations.append(f"WEAK: Header '{header}: {val}' lacks required '{expected_snippet}'.")

    return violations

if __name__ == "__main__":
    print("Security header auditing framework initialized.")
```

### Automated CIS Bucket Permission Audit (Bash)

```bash
#!/usr/bin/env bash
set -euo pipefail

BUCKET_NAME="${1:-production-assets-bucket}"

echo "=== Auditing S3 Bucket Public Access Block: $BUCKET_NAME ==="
PUBLIC_BLOCK=$(aws s3api get-public-access-block --bucket "$BUCKET_NAME" --query "PublicAccessBlockConfiguration" --output json)

BLOCK_PUBLIC_ACLS=$(echo "$PUBLIC_BLOCK" | grep -o '"BlockPublicAcls": true' || true)
IGNORE_PUBLIC_ACLS=$(echo "$PUBLIC_BLOCK" | grep -o '"IgnorePublicAcls": true' || true)
BLOCK_PUBLIC_POLICY=$(echo "$PUBLIC_BLOCK" | grep -o '"BlockPublicPolicy": true' || true)
RESTRICT_PUBLIC_BUCKETS=$(echo "$PUBLIC_BLOCK" | grep -o '"RestrictPublicBuckets": true' || true)

if [ -n "$BLOCK_PUBLIC_ACLS" ] && [ -n "$IGNORE_PUBLIC_ACLS" ] && [ -n "$BLOCK_PUBLIC_POLICY" ] && [ -n "$RESTRICT_PUBLIC_BUCKETS" ]; then
    echo "SUCCESS: Bucket $BUCKET_NAME complies with CIS public access block benchmark."
else
    echo "ERROR: Bucket $BUCKET_NAME has exposed public access settings!"
    exit 1
fi
```

## Verification Checklist

- [ ] All public endpoints protected by authenticated session and object-level authorization (IDOR/BOLA free).
- [ ] Database queries parameterized with zero dynamic SQL string concatenations.
- [ ] SSRF defense blocks local loopbacks and internal cloud metadata endpoints.
- [ ] HTTP responses enforce strict CSP, HSTS, X-Frame-Options, and secure cookie attributes.
- [ ] Cloud storage and compute resources comply with CIS Benchmark hardening baselines.
- [ ] Formal security audit report emitted with zero unmitigated high/critical vulnerabilities.
