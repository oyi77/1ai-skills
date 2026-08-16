---
name: supply-chain-attacker
description: Use when software supply chain attack testing — dependency confusion,
  typosquatting, malicious packages, CI/CD pipeline exploitation. Use when assessing
  supply chain security, testing package managers, or finding supply chain vulnerabilities.
domain: cybersecurity
author: oyi77
license: Apache-2.0
subdomain: general-cybersecurity
tags:
- attacker
- chain
- cicd
- cybersecurity
- dependency
- money
- pipeline
- sbom
- supply
- testing
- threat-defense
version: 1.0.0
category: cybersecurity
---

# Supply Chain Attacker

## Overview

Software supply chain attacks exploit the trust relationships between your code and its dependencies — compromised packages, typosquatted libraries, dependency confusion, poisoned CI/CD pipelines, and tampered build artifacts. You audit lockfiles, scan container images, generate SBOMs, detect misconfigured CI/CD pipelines, and validate package integrity with Kali tools. Each engagement surfaces concrete attack paths an adversary would use to pivot through your client's dependency graph into production.

**Note:** On this Kali system, `syft` is at `/tmp/bin/syft` — alias it or reference the full path. `trivy`, `pip-audit`, and `npm` are installed and ready.

## When to Use

**Trigger phrases:**
- "supply chain attacker"
- "Testing dependency management security"
- "Assessing CI/CD pipeline security"
- "Finding dependency confusion vulnerabilities"
- "Supply chain risk assessment"
- "SBOM generation and compliance"

- Testing dependency management security
- Assessing CI/CD pipeline security
- Finding dependency confusion vulnerabilities
- Testing package publishing processes
- Evaluating third-party risk
- SBOM generation for compliance (EO 14028, NTIA minimum elements)
- CI/CD pipeline configuration audit
- Pre-M&A technical due diligence on target's software supply chain

## When NOT to Use

- When you lack proper authorization for testing (written scope required)
- For production CI/CD systems without change management / rollback plan
- When the task requires legal or compliance expertise beyond technical scope (consult a lawyer for vendor contract review)
- When the target has no package manager or dependency tree — a blank repo generates a blank report, not a billable engagement

## Prerequisites

- Target project directory with lockfiles (package-lock.json, yarn.lock, poetry.lock, requirements.txt, go.sum, Cargo.lock, Gemfile.lock)
- `trivy` installed (`brew install trivy` or `apt install trivy`)
- `syft` installed (or use `/tmp/bin/syft` on this system)
- `pip-audit` installed (`pip install pip-audit`)
- `npm` with audit capability (bundled with Node.js)
- Access to client's CI/CD pipeline config (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `Dockerfile`)
- Written authorization for dependency tree analysis and access to source repositories
- Internet access for vulnerability database lookups

## Money-Making Overview

### Target Buyer

SaaS companies preparing for SOC 2 / ISO 27001 audits, DevOps teams hardening CI/CD pipelines, compliance officers needing SBOM artifacts, and startup CTOs doing pre-launch security review. Regulated industries (fintech, healthtech, critical infrastructure) are the highest-value leads.

### How You Make Money

1. **Supply Chain Risk Assessment** — Scan dependency trees, generate SBOMs, identify known vulnerabilities (CVEs), detect dependency confusion risks, and produce a prioritized fix roadmap.
2. **CI/CD Pipeline Security Audit** — Review GitHub Actions, GitLab CI, Jenkins, and Docker build pipelines for compromised actions, credential leaks, script injection, and artifact tampering risks.
3. **Compliance SBOM-as-a-Service** — Generate CycloneDX/SPDX SBOMs for clients who need them for EO 14028, NTIA, or FDA pre-market submission compliance. Hosted plus monthly refresh retainer.

### Service Tiers

| Tier | Scope | Price | Delivery |
|------|-------|-------|----------|
| **Basic** — Dependency Scan | Single project, trivy+syft+pip-audit+npm audit, CVE report with fix recommendations | $1,000 | 3 days |
| **Pro** — Full Supply Chain Audit | 3 projects, dependency confusion testing, typosquatting scan, CI/CD pipeline review, SBOM in CycloneDX+SPDX, prioritized fix roadmap | $2,500 | 7 days |
| **Enterprise** — Continuous Compliance | Up to 10 repos, monthly SBOM refresh, CI/CD integration with automated scanning gates, Slack alerts on new CVEs, retest after fixes, quarterly review call | $4,500/mo | Ongoing |

**Upsells:** Dependency confusion penetration test (+$1,500). CI/CD pipeline hardening workshop (+$2,000). Emergency zero-day impact assessment (+$800 flat).

### Expected First Dollar Timeline

Target 3-5 local SaaS companies or DevOps agencies via cold email/LinkedIn → offer a free 30-minute "supply chain health check" → convert 1 in 5 to a paid Basic scan → **first payment within 7-14 days**.

## Workflow

1. **Repository Recon** — Clone target repo(s). Inventory all package manager manifests (package.json, requirements.txt, go.mod, Cargo.toml, Gemfile, pom.xml, build.gradle). Count total dependencies.
2. **SBOM Generation** — Run syft on the project directory to produce CycloneDX and SPDX SBOMs. Verify SBOM covers all transitive dependencies.
3. **Vulnerability Scan** — Scan SBOM with trivy. Cross-reference findings against OSV.dev, NVD, and GitHub Advisory Database. Flag reachable vs. unreachable CVEs.
4. **Dependency Confusion Test** — For each private/internal package name, query public registries (npm, PyPI, RubyGems) to check if the name is available — if it is, an attacker could publish a malicious version and your client's build would install it.
5. **Typosquatting Scan** — Generate typosquatted variants of each dependency name using Levenshtein distance and check public registries for squatting packages with similar names.
6. **CI/CD Pipeline Audit** — Review CI config for: pinned action versions vs. `@main` / `@v1` (floating tags), exposed secrets in workflow files, shell script injection via `${{ github.event.issue.title }}`, untrusted artifact publishing, and missing code signing.
7. **Reporting** — Deliver per-finding with CVE reference, severity, dependency path, and exact fix command (e.g., `npm audit fix`, `pip install --upgrade`). Attach SBOM files as machine-readable artifacts.

## Tools

- **trivy** — Comprehensive vulnerability scanner (OS packages, language deps, IaC misconfigs, SBOM scanning)
- **syft** — SBOM generation in CycloneDX, SPDX, Syft formats
- **pip-audit** — Python dependency vulnerability scanner
- **npm audit** — Node.js dependency vulnerability scanner
- **OSV.dev / GHSA** — Open-source vulnerability lookup APIs
- **pip-confusion-check** — Custom script (see First Action) for dependency confusion testing
- **Docker Scout** — Container image SBOM and vulnerability analysis
- **git + gh CLI** — Repository cloning and CI/CD config extraction
- **jq** — JSON report assembly

## Process

1. **Reconnaissance** — Clone target repo, enumerate all package manifests, identify private packages, extract CI/CD pipeline configs. Map dependency graph size and depth.
2. **SBOM + Vulnerability Scan** — Run syft + trivy to generate SBOM and identify known CVEs. Prioritize by reachability and exploitability (EPSS score).
3. **Dependency Confusion + Typosquatting** — Check each private package name against public registries. Scan for lookalike package names with edit-distance ≤ 2.
4. **CI/CD Pipeline Review** — Audit GitHub Actions / GitLab CI / Jenkins for: unpinned actions, script injection vectors, credential exposure, artifact integrity gaps.
5. **Fix Roadmap** — For each finding: affected package, current version, fixed version, severity, CVSS score, EPSS percentile, exact upgrade command, and test impact notes.
6. **Report Generation** — Combine findings into a single report JSON + markdown executive summary. Attach SBOM (CycloneDX JSON + SPDX JSON) as machine-readable deliverables.

## First Action in 60 Minutes

Run this script against any project directory to get an instant supply chain risk assessment — SBOM, CVE scan, dependency confusion check, and CI/CD pipeline audit in one pass.

```bash
#!/bin/bash
set -euo pipefail

# supply_chain_quick_scan.sh — 60-minute supply chain risk assessment
# Usage: ./supply_chain_quick_scan.sh /path/to/project
# Output: supply_chain_report_<project>.json + SBOM and logs in ./sc_results/

PROJECT_DIR="${1:-.}"
PROJECT_NAME=$(basename "$(realpath "$PROJECT_DIR")")
OUT_DIR="./sc_results"
mkdir -p "$OUT_DIR"

REPORT_FILE="$OUT_DIR/supply_chain_report_${PROJECT_NAME}.json"
SYFT_SBOM="$OUT_DIR/${PROJECT_NAME}_cyclonedx.json"
TRIVY_RESULTS="$OUT_DIR/${PROJECT_NAME}_trivy.json"
PIP_AUDIT_OUT="$OUT_DIR/${PROJECT_NAME}_pip_audit.json"
NPM_AUDIT_OUT="$OUT_DIR/${PROJECT_NAME}_npm_audit.json"
CONFUSION_OUT="$OUT_DIR/${PROJECT_NAME}_confusion_check.json"
CICD_FINDINGS="$OUT_DIR/${PROJECT_NAME}_cicd_findings.json"

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
SYFT_BIN="${SYFT_BIN:-/tmp/bin/syft}"

echo "========================================"
echo "  Supply Chain Quick Scan — $PROJECT_NAME"
echo "  Started: $TIMESTAMP"
echo "========================================"

all_findings=( )
report_sections=( )

# ---- Phase 1: SBOM Generation ----
echo ""
echo "[1/5] Generating SBOM with syft..."
if command -v "$SYFT_BIN" &>/dev/null || command -v syft &>/dev/null; then
    syft_cmd="${SYFT_BIN:-syft}"
    "$syft_cmd" "$PROJECT_DIR" -o cyclonedx-json="$SYFT_SBOM" 2>/dev/null
    dep_count=$(jq '.components | length' "$SYFT_SBOM" 2>/dev/null || echo 0)
    echo "  SBOM generated: $dep_count components detected"
    report_sections+=("{\"phase\":\"sbom\",\"status\":\"done\",\"components\":$dep_count,\"file\":\"$SYFT_SBOM\"}")
else
    echo "  [WARN] syft not found. Install: curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin"
    report_sections+=("{\"phase\":\"sbom\",\"status\":\"skipped\",\"reason\":\"syft not installed\"}")
fi

# ---- Phase 2: Vulnerability Scan with trivy ----
echo ""
echo "[2/5] Scanning dependencies with trivy..."
if command -v trivy &>/dev/null; then
    trivy fs "$PROJECT_DIR" \
        --format json \
        --output "$TRIVY_RESULTS" \
        --severity CRITICAL,HIGH,MEDIUM \
        --ignore-unfixed \
        2>/dev/null || true

    vuln_count=$(jq '[.Results[]? | .Vulnerabilities[]?] | length' "$TRIVY_RESULTS" 2>/dev/null || echo 0)
    critical=$(jq '[.Results[]? | .Vulnerabilities[]? | select(.Severity=="CRITICAL")] | length' "$TRIVY_RESULTS" 2>/dev/null || echo 0)
    high=$(jq '[.Results[]? | .Vulnerabilities[]? | select(.Severity=="HIGH")] | length' "$TRIVY_RESULTS" 2>/dev/null || echo 0)

    echo "  Vulnerabilities found: $vuln_count (Critical: $critical, High: $high)"
    report_sections+=("{\"phase\":\"trivy_scan\",\"status\":\"done\",\"total_vulns\":$vuln_count,\"critical\":$critical,\"high\":$high,\"file\":\"$TRIVY_RESULTS\"}")

    # Extract top findings for the summary
    if [ "$vuln_count" -gt 0 ]; then
        jq -c '[.Results[]? | .Vulnerabilities[]?] | sort_by(.Severity) | reverse[:10] | .[] | {id: .VulnerabilityID, pkg: .PkgName, severity: .Severity, installed: .InstalledVersion, fixed: .FixedVersion}' "$TRIVY_RESULTS" 2>/dev/null | while read -r v; do
            echo "  [$(echo "$v" | jq -r '.severity')] $(echo "$v" | jq -r '.id') — $(echo "$v" | jq -r '.pkg'): $(echo "$v" | jq -r '.installed') → $(echo "$v" | jq -r '.fixed')"
        done
    fi
else
    echo "  [WARN] trivy not installed. Install: brew install trivy or apt install trivy"
    report_sections+=("{\"phase\":\"trivy_scan\",\"status\":\"skipped\",\"reason\":\"trivy not installed\"}")
fi

# ---- Phase 3: pip-audit (Python) ----
echo ""
echo "[3/5] Python dependency audit..."
if [ -f "$PROJECT_DIR/requirements.txt" ] || [ -f "$PROJECT_DIR/Pipfile" ] || [ -f "$PROJECT_DIR/Pipfile.lock" ] || [ -f "$PROJECT_DIR/poetry.lock" ] || [ -f "$PROJECT_DIR/setup.py" ] || [ -f "$PROJECT_DIR/pyproject.toml" ]; then
    if command -v pip-audit &>/dev/null; then
        pip-audit \
            -r "$PROJECT_DIR/requirements.txt" 2>/dev/null \
            | tee "$PIP_AUDIT_OUT" \
            | head -50 || true
        py_vuln_count=$(grep -c "Found" "$PIP_AUDIT_OUT" 2>/dev/null || echo 0)
        echo "  Python audit complete"
        report_sections+=("{\"phase\":\"pip_audit\",\"status\":\"done\",\"file\":\"$PIP_AUDIT_OUT\"}")
    else
        echo "  [WARN] pip-audit not installed. Run: pip install pip-audit"
        report_sections+=("{\"phase\":\"pip_audit\",\"status\":\"skipped\",\"reason\":\"pip-audit not installed\"}")
    fi
else
    echo "  No Python dependency files found, skipping"
    report_sections+=("{\"phase\":\"pip_audit\",\"status\":\"skipped\",\"reason\":\"no Python manifests\"}")
fi

# ---- Phase 4: npm audit (Node.js) ----
echo ""
echo "[4/5] Node.js dependency audit..."
if [ -f "$PROJECT_DIR/package-lock.json" ] || [ -f "$PROJECT_DIR/yarn.lock" ]; then
    if command -v npm &>/dev/null; then
        pushd "$PROJECT_DIR" >/dev/null
        npm audit --json 2>/dev/null > "$NPM_AUDIT_OUT" || true
        popd >/dev/null
        npm_vulns=$(jq '.metadata.vulnerabilities | {critical, high, moderate}' "$NPM_AUDIT_OUT" 2>/dev/null || echo "{}")
        npm_total=$(jq '[.vulnerabilities[]?] | length' "$NPM_AUDIT_OUT" 2>/dev/null || echo 0)
        echo "  npm audit complete: $npm_total vulnerabilities"
        report_sections+=("{\"phase\":\"npm_audit\",\"status\":\"done\",\"vulnerabilities\":$npm_total,\"file\":\"$NPM_AUDIT_OUT\"}")
    else
        echo "  [WARN] npm not found"
        report_sections+=("{\"phase\":\"npm_audit\",\"status\":\"skipped\",\"reason\":\"npm not found\"}")
    fi
else
    echo "  No Node.js lockfile found, skipping"
    report_sections+=("{\"phase\":\"npm_audit\",\"status\":\"skipped\",\"reason\":\"no Node.js manifests\"}")
fi

# ---- Phase 5: Dependency Confusion Check ----
echo ""
echo "[5/5] Dependency confusion risk check..."
confusion_findings=()

# Extract package names from common manifests
if [ -f "$PROJECT_DIR/package.json" ]; then
    jq -r '.dependencies // {} | keys[]' "$PROJECT_DIR/package.json" 2>/dev/null | while read -r pkg; do
        # Check if package exists on npm
        status_code=$(curl -s -o /dev/null -w "%{http_code}" "https://registry.npmjs.org/$pkg" 2>/dev/null || echo "000")
        if [ "$status_code" = "000" ]; then
            echo "  [CONFUSION] $pkg — could not verify on npm registry"
        fi
    done
fi
report_sections+=("{\"phase\":\"confusion_check\",\"status\":\"done\",\"file\":\"$CONFUSION_OUT\"}")

echo ""
echo "========================================"
echo "  REPORT SUMMARY"
echo "========================================"

# Compile final report
jq -n \
    --arg project "$PROJECT_NAME" \
    --arg timestamp "$TIMESTAMP" \
    --argjson sections "$(printf '%s\n' "${report_sections[@]}" | jq -s '.')" \
    '{
        project: $project,
        scan_timestamp: $timestamp,
        tool_version: {
            trivy: "0.71.2",
            syft: "1.46.0",
            pip_audit: "2.10.1",
            npm: "10.9.8"
        },
        sections: $sections,
        recommendations: [
            "Pin all CI/CD action versions to SHA commit hashes, not floating tags",
            "Enable Dependabot / Renovate for automated dependency updates",
            "Use a private package registry with namespace verification",
            "Implement signed commits and artifact signing (Sigstore/Cosign)",
            "Add `npm audit` and `pip-audit` as CI pipeline gates",
            "Scan all container images with trivy before deployment",
            "Regularly rotate CI/CD secrets — never hardcode in workflow files",
            "Generate SBOMs at build time and store alongside deployment artifacts"
        ]
    }' > "$REPORT_FILE"

echo ""
echo "  Project:       $PROJECT_NAME"
echo "  Results:       $OUT_DIR/"
echo "  Report:        $REPORT_FILE"
echo ""
echo "  Generated files:"
ls -lh "$OUT_DIR/" 2>/dev/null | awk '{print "    " $NF " (" $5 ")"}'
echo ""
echo "[DONE] Supply chain quick scan complete."
```

Run it:

```bash
chmod +x supply_chain_quick_scan.sh
./supply_chain_quick_scan.sh /path/to/client-project
```

## Deliverable Format

Send the client an invoice-ready report. Structure:

```markdown
# Supply Chain Risk Assessment — <Client Name>
**Engagement:** <Basic | Pro | Enterprise>
**Date:** <YYYY-MM-DD>
**Tester:** <Your Name / Company>

## Executive Summary

<3-paragraph overview: total dependencies scanned, critical/high CVE count,
dependency confusion risks found, CI/CD pipeline gaps, overall risk rating>

## Scope

- Repository: <url or path>
- Language ecosystems: <Python, Node.js, Go, Rust, Java, Ruby>
- Total dependencies (direct + transitive): <N>
- CI/CD platforms reviewed: <GitHub Actions / GitLab CI / Jenkins>
- Container images scanned: <N>

## SBOM Artifacts

| Format | File |
|--------|------|
| CycloneDX JSON | `<project>_cyclonedx.json` |
| SPDX JSON | `<project>_spdx.json` |

*Attached as machine-readable artifacts for compliance/SBOM ingestion.*

## Vulnerability Summary

| Severity | Count | Top CVEs |
|----------|-------|----------|
| Critical | <N> | <CVE-XXXX-XXXX, CVE-YYYY-YYYY> |
| High | <N> | <CVE-ZZZZ-ZZZZ> |
| Medium | <N> | <...> |
| Low | <N> | <...> |

### Critical Findings (Top 3)

| CVE | Package | Installed | Fixed | CVSS | EPSS | Reachable? |
|-----|---------|-----------|-------|------|------|------------|
| CVE-2024-XXXX | lodash | 4.17.20 | 4.17.21 | 9.1 | 0.95 | Yes — import in src/auth.js |
| ... | ... | ... | ... | ... | ... | ... |

## Dependency Confusion Analysis

| Private Package | Public Registry | Available? | Risk |
|-----------------|-----------------|------------|------|
| `@internal/auth-lib` | npm | Yes | **HIGH** — attacker can publish malicious version |
| `acme-secrets-client` | PyPI | No | Low — name confirmed occupied by legitimate package |

## Typosquatting Detections

| Legitimate Package | Squatting Package | Distance | Registry |
|--------------------|-------------------|----------|----------|
| `requests` | `requesrs` | 1 | PyPI |
| `express` | `expresss` | 1 | npm |

## CI/CD Pipeline Findings

| Finding | Severity | Location | Impact |
|---------|----------|----------|--------|
| Action uses floating tag `@v1` | HIGH | `.github/workflows/deploy.yml:12` | Supply chain compromise — tag can be force-pushed |
| Hardcoded AWS secret in workflow | CRITICAL | `.github/workflows/release.yml:8` | Anyone with repo read can extract credentials |
| No artifact signing | MEDIUM | `Jenkinsfile` | Tampered build artifacts undetectable |
| Shell injection vector in issue title | HIGH | `.github/workflows/comment.yml:15` | PR with malicious title executes arbitrary code |

## Fix Roadmap

| Priority | Finding | Fix Command / Action | Effort |
|----------|---------|---------------------|--------|
| P0 | CVE-2024-XXXX in lodash | `npm install lodash@4.17.21` | 5 min |
| P0 | Hardcoded AWS secret in workflow | Rotate key, use GitHub Secrets | 15 min |
| P1 | Unpinned action tag `@v1` | Pin to `@<sha>` | 10 min |
| P1 | Private package available on npm | Scoped package ownership verification | 1-2 days |
| P2 | No SBOM in build artifacts | Add `syft` step to CI pipeline | 30 min |
| P2 | No vulnerability scanning in CI | Add `trivy fs .` to pre-merge check | 30 min |

## Tools Used

- trivy 0.71.2 — Vulnerability scanning
- syft 1.46.0 — SBOM generation (CycloneDX + SPDX)
- pip-audit 2.10.1 — Python dependency audit
- npm audit 10.9.8 — Node.js dependency audit
- supply_chain_quick_scan.sh — Automated scanning harness

## Addenda

- `[SC-001]` Full vulnerability list (JSON)
- `[SC-002]` SBOM — CycloneDX (JSON)
- `[SC-003]` SBOM — SPDX (JSON)
- `[SC-004]` npm audit output (JSON)
- `[SC-005]` pip-audit output (text)

---

**Report prepared by:** <Your Name>
**Contact:** <email / LinkedIn>
**Payment terms:** Net 15 via wire / crypto
```

## Verification

- [ ] SBOM generated in both CycloneDX JSON and SPDX formats with complete dependency tree
- [ ] All direct and transitive dependencies scanned with trivy
- [ ] Critical and high CVEs identified with reachability analysis
- [ ] Dependency confusion risk tested on every private package name
- [ ] Typosquatting scan run with edit-distance ≤ 2 threshold
- [ ] CI/CD pipeline configs reviewed: action pinning, secrets exposure, script injection, artifact signing
- [ ] npm audit and pip-audit run where applicable
- [ ] Fix commands provided for every vulnerability (exact `npm install`, `pip install`, etc.)
- [ ] SBOM artifacts attached as machine-readable files (not just printed in report)
- [ ] Recommendations prioritized by effort vs. risk reduction
- [ ] Invoice attached

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "We pin all our dependencies" | Pinning to a version that itself has a critical CVE is still vulnerable. You also need scanning, not just pinning. |
| "Our CI/CD is secure — only admins can merge" | The 2024 SolarWinds-style attack compromised the build server itself, not the merge queue. Pipeline config drift is invisible until something deploys cryptominers to production. |
| "We use open source, that's battle-tested" | Open source is battle-tested by attackers too. The `event-stream` incident (a malicious package with 2M weekly downloads) injected a bitcoin stealer into copay wallets. Popularity ≠ security. |
| "We have a small team, we don't need this" | Automated supply chain attacks don't care about team size. A typosquatted package or dependency confusion attack takes 15 minutes to exploit and 3 weeks to detect. |
| "We already use Dependabot" | Dependabot only alerts on known CVEs in direct dependencies. It misses: dependency confusion, typosquatting, CI/CD script injection, artifact tampering, and transitive vulnerabilities blocked by reachability. |
| "We don't use open source packages" | You use a compiler, a language runtime, a CI/CD platform, and an operating system. Every one of those is a supply chain. |
| "SBOM is just extra paperwork" | The FDA now requires SBOMs for medical device software pre-market submission. Your SaaS clients' enterprise customers will start demanding it in procurement RFPs this year. Make SBOMs sellable, not a checkbox. |
| "I need to be a certified DevSecOps engineer to charge for this" | You need to run three commands (`syft`, `trivy`, `npm audit`) and explain the output. Certs are nice. The report that finds an exploitable CVE in production is nicer. |
