---
name: role-penetration-tester
description: Use when orchestrating offensive security testing, ethical red teaming,
  web vulnerability discovery, API fuzzing, reverse engineering, exploit chaining,
  and bug bounty reporting.
domain: cybersecurity
author: oyi77
version: 1.0.0
category: cybersecurity
tags:
- security
- pentest
- red-team
- offensive-security
- bug-bounty
- fuzzing
- exploit-chaining
- reporting
license: MIT
subdomain: penetration-testing
---

## Overview

The `role-penetration-tester` skill directs authorized offensive security assessments, red team exercises, bug bounty investigations, and exploit chaining. Rather than executing disjointed vulnerability scans or producing unverified theoretical findings, this role coordinates multi-phase penetration testing spanning passive/active reconnaissance, target surface mapping, API protocol fuzzing, binary and script reverse engineering, multi-vulnerability exploit chaining, and professional executive/technical reporting.

```
[Phase 1: Scope & Reconnaissance] ──► [Phase 2: Vulnerability Hunting & Fuzzing] ──► [Phase 3: Reverse Engineering]
                                                                                                  │
              [Phase 5: Proof & Report Delivery] ◄── [Phase 4: Exploit Chaining] ◄────────────────┘
```

The penetration tester operates strictly within authorized rules of engagement, validates proof-of-concept exploits without causing Denial of Service or data loss, and chains low-severity findings into demonstrable business impact.

## When to Use

- When conducting authorized penetration tests against web applications, APIs, or cloud platforms.
- When executing time-boxed bug bounty hunts on HackerOne, Bugcrowd, or private programs.
- When performing advanced protocol, parameter, or grammar fuzzing on proprietary binaries and network endpoints.
- When decompiling and reverse engineering compiled binaries, Android APKs, or obfuscated frontend JavaScript bundles.
- When chaining multiple low/medium severity vulnerabilities (e.g. CSRF + CORS + IDOR) into account takeover or RCE.
- When drafting professional penetration test reports with executive summaries, CVSS 3.1 scoring, and remediation steps.

## When NOT to Use

- When implementing defensive application code patches or writing production fixes (use `cybersecurity/role-security-engineer`).
- When managing CI/CD deployment pipelines or infrastructure orchestration (use `devops/role-devops-sre-engineer`).
- When conducting unit or integration regression testing of normal software features (use `development/role-qa-automation-engineer`).
- When unauthorized by explicit written rules of engagement or program scope.

## Deterministic Dispatch Matrix

| Offensive Engagement Phase / Technique | Delegated Child Skill | Primary Offensive Artifact |
|---|---|---|
| Autonomous multi-tool pentesting orchestration & MCP security tools | `cybersecurity/hexstrike-ai-pentest` | Coordinated scan outputs, target maps, tool logs |
| Systematic web app vulnerability hunting (OWASP Top 10, logic flaws) | `cybersecurity/bug-hunting` | Validated vulnerability PoCs with reproduction steps |
| Advanced parameter, grammar, and memory fuzzing for zero-days | `cybersecurity/fuzz-master` | Fuzzing crash dumps, mutated testcases, exception traces |
| Decompiling binaries, APKs, WASM, and deobfuscating JS bundles | `cybersecurity/reverse-engineering-router` | Reconstructed source models, API endpoints, protocol specs |
| Combining isolated vulnerabilities into high-impact exploit chains | `cybersecurity/bug-chain-builder` | Multi-step exploit chain proof (e.g. Info Leak -> Auth Bypass -> RCE) |
| Generating professional bug bounty & audit vulnerability reports | `cybersecurity/report-generator` | Structured Markdown/PDF security assessment report |

## Workflow

### Phase 1: Scoping & Reconnaissance

1. Verify authorization, target scope, excluded assets, and safe testing boundaries.
2. Coordinate reconnaissance tooling via `cybersecurity/hexstrike-ai-pentest` (subdomain discovery, port mapping, technology stack fingerprinting).
3. Map authenticated and unauthenticated attack surfaces.

### Phase 2: Vulnerability Hunting & Protocol Fuzzing

1. Dispatch to `cybersecurity/bug-hunting` for systematic testing of business logic, access control, and injection vectors.
2. For binary parsers or custom RPC protocols, dispatch to `cybersecurity/fuzz-master` to deliver mutated inputs and detect crashes.
3. Record all anomalous responses, timing variations, and verbose error envelopes.

### Phase 3: Deep Reverse Engineering & Protocol Dissection

1. When analyzing client-side binaries, mobile applications, or obfuscated SPA bundles, dispatch to `cybersecurity/reverse-engineering-router`.
2. Extract hidden API endpoints, cryptographic keys, request signing routines, and undocumented parameters.
3. Validate client-side restrictions and identify missing server-side authorization checks.

### Phase 4: Exploit Chaining & Impact Demonstration

1. Dispatch to `cybersecurity/bug-chain-builder` to correlate isolated low/medium severity defects.
2. Construct deterministic multi-stage exploit chains demonstrating tangible business impact (e.g. Account Takeover, Privilege Escalation, Remote Code Execution).
3. Verify that exploit payloads are benign and non-destructive (e.g. reading harmless canary files or demonstrating state modification safely).

### Phase 5: Evidence Packaging & Report Delivery

1. Compile reproduction steps, raw HTTP requests/responses, and environmental prerequisites.
2. Dispatch to `cybersecurity/report-generator` to draft the executive summary, calculate CVSS 3.1 scores, and document precise remediation guidance.
3. Deliver the final assessment package adhering to enterprise bug bounty and pentest standards.

## Anti-Rationalization

| Pentest Excuse | Flawed Rationalization | Required Offensive Discipline |
|---|---|---|
| "Scanner says clean, so target is secure" | "Automated tools tested all known CVEs." | Scanners cannot understand custom business logic. Manually probe workflows, race conditions, and role transitions. |
| "This bug is only low severity, ignore it" | "Self-XSS or info disclosure isn't worth reporting." | Chain low-severity vulnerabilities together via `cybersecurity/bug-chain-builder` to prove critical impact. |
| "Run intrusive payloads on production" | "Testing with destructive drops proves RCE faster." | Destructive payloads violate ethical boundaries. Always use harmless canaries (`whoami`, `id`, touch canary). |
| "Screenshot of the error page is enough PoC" | "The client can see the stack trace in the image." | Screenshots without repeatable curl or script reproduction are rejected. Provide deterministic CLI proof. |
| "Skip documenting remediation" | "The developers should know how to fix their own code." | Incomplete reports provide zero defensive value. Provide concrete code diffs and architectural fixes. |

## Implementation Examples

### Reproducible Proof-of-Concept Exploit Harness (Python)

```python
import urllib.request
import urllib.parse
import json
import sys

def verify_idor_vulnerability(target_api: str, attacker_token: str, victim_resource_id: str) -> bool:
    """Demonstrates authorization bypass (IDOR) without data destruction."""
    url = f"{target_api}/api/v1/documents/{victim_resource_id}"
    headers = {
        "Authorization": f"Bearer {attacker_token}",
        "User-Agent": "EthicalSecurityTester/1.0",
        "Accept": "application/json"
    }
    
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                body = json.loads(resp.read().decode())
                # Verify that resource belongs to another tenant without leaking PII
                if "owner_id" in body and body["owner_id"] != "attacker_user":
                    print(f"CONFIRMED: IDOR vulnerability detected on resource {victim_resource_id}!")
                    print(f"Status: {resp.status} OK | Leaked Metadata: {list(body.keys())}")
                    return True
    except Exception as e:
        print(f"Test safely rejected or target unreachable: {e}")
        
    return False

if __name__ == "__main__":
    print("Penetration testing PoC harness initialized.")
```

### Exploit Reproduction Verification Script (Bash)

```bash
#!/usr/bin/env bash
set -euo pipefail

TARGET_HOST="https://api.target.internal"
ATTACKER_JWT="eyJhbGciOi..."
RESOURCE_ID="10928"

echo "=== Testing BOLA/IDOR on Target Resource: $RESOURCE_ID ==="
HTTP_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$TARGET_HOST/api/v1/records/$RESOURCE_ID" \
  -H "Authorization: Bearer $ATTACKER_JWT" \
  -H "Content-Type: application/json")

HTTP_STATUS=$(echo "$HTTP_RESPONSE" | tail -n1)
BODY=$(echo "$HTTP_RESPONSE" | head -n -1)

if [ "$HTTP_STATUS" -eq 200 ]; then
  echo "CRITICAL: Authorization barrier failed! HTTP 200 received for cross-tenant resource."
  echo "Evidence snippet: ${BODY:0:120}..."
  exit 0
elif [ "$HTTP_STATUS" -eq 403 ] || [ "$HTTP_STATUS" -eq 404 ]; then
  echo "SAFE: Endpoint properly restricted with HTTP $HTTP_STATUS."
  exit 1
fi
```

## Verification Checklist

- [ ] Written authorization and scope boundaries confirmed before testing.
- [ ] Automated and manual vulnerability hunting executed without service disruption.
- [ ] Binary, mobile, or web assets reverse-engineered to identify undocumented API surfaces.
- [ ] Isolated vulnerabilities chained to demonstrate tangible business risk.
- [ ] Proof of concept adheres to safe, non-destructive validation principles.
- [ ] Comprehensive penetration test report compiled with CVSS metrics and remediation diffs.
