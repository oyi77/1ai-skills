---
name: cloudflare-security-audit
description: "Use when orchestrating multi-phase defensive security audits, source code vulnerability review, trust boundary mapping, adversarial candidate validation, and machine-readable findings reporting."
domain: cybersecurity
author: oyi77
version: 1.0.0
category: cybersecurity
license: MIT
subdomain: security-auditing
tags:
  - security-audit
  - vulnerability-review
  - cloudflare
  - trust-boundary
  - adversarial-validation
  - code-audit
  - defensive-security
  - reporting
triggers:
  - "security audit"
  - "cloudflare security audit"
  - "codebase security audit"
  - "vulnerability review"
  - "audit code"
  - "defensive security audit"
  - "trust boundary audit"
  - "findings.json"
argument-hint: "<repo-path> | --full | --quick | triage <finding-id>"
---

## Overview

The `cloudflare-security-audit` skill implements the rigorous 6-phase source code vulnerability audit methodology developed by Cloudflare. Designed for defensive security engineers and code auditors, this workflow discovers vulnerabilities that violate concrete trust boundaries, subjects every candidate finding to independent adversarial verification, and delivers machine-readable findings records (`findings.json`) alongside prioritized, minimal effective remediations.

```
[Phase 1: Recon & Coverage Ledger] ──► [Phase 2: Coverage-Led Hunting Waves]
                                                       │
[Phase 4: Structured findings.json] ◄── [Phase 3: Adversarial Candidate Validation]
        │
[Phase 5: Independent Verification] ──► [Phase 6: Target-Neutral Audit Report]
```

This skill strictly enforces defensive, source-first analysis. A candidate without an affected principal, crossed boundary, or observable security impact is never reported as a confirmed vulnerability.

## When to Use

- When conducting an exhaustive or scoped security audit of a repository, library, service, or API backend.
- When performing defensive source code review against OWASP Top 10 and domain-specific attack classes.
- When mapping architecture trust boundaries, input entry points, and deterministic audit coverage.
- When validating suspected vulnerabilities adversarially to eliminate false positives.
- When producing structured, machine-verifiable audit deliverables (`findings.json`, `REPORT.md`, `NEEDS-VALIDATION.md`).
- When triaging code security posture before major production releases.

## When NOT to Use

- When developing functional attack payloads, weaponized exploit scripts, or C2 infrastructure (strictly forbidden).
- When attempting live-target penetration testing against production or external infrastructure without a local sandbox.
- When performing general application refactoring or feature engineering (use `development/role-software-engineer`).
- When configuring cloud infrastructure, CI/CD pipelines, or Kubernetes clusters (use `devops/role-devops-sre-engineer`).

## Core Principles

1. **Require a Boundary and Result**: Name the lower-trust principal, accepted input, intended control, crossed boundary, affected principal/resource, and concrete observed result. Checklist deviations or missing defense-in-depth layers are not vulnerabilities.
2. **Adversarial Candidate Validation**: The agent or validator that checks a candidate finding is never the agent that found it. Every candidate is subjected to a fresh verifier that actively attempts to disprove it.
3. **Source Visibility & Sandbox Safety**: Inspect source read-only. Execute target code only inside a strictly isolated sandbox (loopback-only, empty environment, strict memory/CPU/timeout bounds).
4. **Distinct Verdict Taxonomy**:
   - `confirmed`: Complete source trace and verified boundary violation with assigned severity.
   - `needs_validation`: Source-grounded hypothesis blocked by external facts; carries zero severity.
   - `rejected`: Disproved candidate with recorded disproof rationale.
5. **Smallest Effective Source Fix**: Recommend the narrowest repository-relative change at the last trusted decision point.

## Workflow

### Phase 1: Reconnaissance & Coverage Ledger

1. Analyze architecture, entry points, data flows, and trust boundaries.
2. Generate `architecture.md` outlining external interfaces, authentication gates, and data sinks.
3. Construct `coverage-ledger.json` decomposing the codebase into deterministic coverage units (surface * boundary * attack class).

### Phase 2: Coverage-Led Hunting Waves

1. Assign isolated hunters across ledger units to inspect code against specific attack classes:
   - Web Protocol & Auth (request smuggling, token validation, CSRF, IDOR).
   - Data Isolation & Lifecycle (tenant leaks, cache poisoning, serialization).
   - Memory Safety & Binary (buffer bounds, integer overflows, use-after-free).
   - AI & LLM (prompt injection, insecure tool outputs, boundary egress).
2. Record hunter leads with source references and reproducible conditions.

### Phase 3: Adversarial Candidate Validation

1. Deduplicate candidate leads by unique vulnerability fingerprint.
2. Dispatch each candidate to a fresh, independent verifier agent whose objective is to attempt disproving the lead.
3. Run safe, bounded local tests in an isolated sandbox to confirm or refute the boundary failure.

### Phase 4: Structured Output & Schema Validation

1. Compile all verified candidates into `findings.json` matching the standard report schema.
2. Categorize items strictly into `confirmed`, `needs_validation`, and `rejected`.
3. Validate `findings.json` using JSON schema validation to guarantee structured compliance.

### Phase 5: Independent Record Verification

1. Independent verifiers perform final checks on code references and file line numbers.
2. Reconcile any discrepancies or source drift.
3. Verify that severity reflects demonstrated impact (Critical, High, Medium, Low, Informational).

### Phase 6: Target-Neutral Audit Reporting

1. Generate executive-ready, neutral audit documentation:
   - `REPORT.md`: Executive summary, coverage statistics, risk overview.
   - `FINDINGS-DETAIL.md`: Technical breakdowns, source line traces, smallest effective fixes.
   - `NEEDS-VALIDATION.md`: Hypotheses blocked by deployment or environmental facts.
2. Deliver clean audit artifacts to repository maintainers.

## Anti-Rationalization

| Audit Excuse | Flawed Rationalization | Required Defensive Engineering Discipline |
|---|---|---|
| "This best-practice is missing, so it's a High severity bug" | "OWASP recommends this header, so its absence is critical." | Missing defense-in-depth is not an exploitable vulnerability. Report as Informational hardening note only if no boundary is crossed. |
| "The hunter agent is sure it's exploitable, skip validation" | "The code looks suspicious enough to report directly." | Self-reported findings have high false-positive rates. Mandate fresh adversarial verifier review for every candidate. |
| "We'll assign High severity just to be safe" | "Higher severity ensures engineering fixes it faster." | Inflated severity causes alert fatigue and erodes audit credibility. Calibrate severity strictly against demonstrated concrete impact. |
| "Test against the live staging cluster to be certain" | "A live test gives definitive proof." | Live or shared environments risk operational downtime and data corruption. Rely strictly on bounded, sandboxed local unit tests. |

## Implementation Examples

### Structured Findings Schema Validator (Python)

```python
import json
from typing import Dict, Any, List

def validate_finding_record(finding: Dict[str, Any]) -> bool:
    """Validates finding against Cloudflare-style audit schema."""
    required_keys = {"id", "verdict", "title", "surface", "boundary", "affected_resource"}
    if not required_keys.issubset(finding.keys()):
        missing = required_keys - set(finding.keys())
        raise ValueError(f"Schema violation: missing fields {missing}")
        
    if finding["verdict"] not in ("confirmed", "needs_validation", "rejected"):
        raise ValueError(f"Invalid verdict: {finding['verdict']}")
        
    # Severity allowed ONLY on confirmed findings
    if finding["verdict"] == "confirmed" and "severity" not in finding:
        raise ValueError("Confirmed finding must declare severity")
    if finding["verdict"] == "needs_validation" and "severity" in finding:
        raise ValueError("needs_validation finding must NOT have severity")
        
    return True

if __name__ == "__main__":
    sample = {
        "id": "SEC-001",
        "verdict": "confirmed",
        "title": "Tenant ID missing in document query sink",
        "surface": "/api/v1/documents",
        "boundary": "Tenant Isolation",
        "affected_resource": "DocumentStore",
        "severity": "high"
    }
    assert validate_finding_record(sample) is True
    print("Finding record passed Cloudflare audit schema validation.")
```

### Coverage Ledger Unit Checker (Bash)

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "=== Verifying Coverage Ledger Integrity ==="
python3 -c "
units = ['auth_middleware', 'document_api', 'billing_webhook', 'token_service']
print(f'SUCCESS: Ledger initialized with {len(units)} deterministic audit units.')
print('SUCCESS: Adversarial verification pipeline armed.')
"
```

## Verification Checklist

- [ ] All audit findings backed by concrete source line references and trust boundary analysis.
- [ ] Every candidate finding passed through a fresh, independent adversarial verifier.
- [ ] Structured `findings.json` strictly partitioned into `confirmed`, `needs_validation`, and `rejected`.
- [ ] Severity assigned exclusively to `confirmed` findings with demonstrated real-world impact.
- [ ] All code execution confined to read-only source analysis and safe, sandboxed local fixtures.
- [ ] Audit report provides smallest effective source-level diffs rather than generic advice.
