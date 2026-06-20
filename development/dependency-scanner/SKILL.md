---
name: dependency-scanner
description: Automated dependency auditing for npm, pip, cargo, go. Detect vulnerabilities, outdated packages, license conflicts, and supply chain risks. Generate SBOMs and compliance reports.
domain: development
tags: [security, dependencies, vulnerabilities, supply-chain, sbom, compliance]
---

# Dependency Scanner

Automated dependency auditing for npm, pip, cargo, go. Detect vulnerabilities, outdated packages, license conflicts, and supply chain risks. Generate Software Bills of Materials (SBOMs) and compliance reports.

**Source:** Developer tooling trends, supply chain security best practices

## When to Use

**Trigger phrases:**
- "Scan dependencies for vulnerabilities"
- "Check for outdated packages"
- "Audit project dependencies"
- "Generate SBOM"
- "License compliance check"
- "Supply chain security audit"

**Use cases:**
- Pre-release security checks
- CI/CD pipeline integration
- Compliance auditing (SOC2, GDPR, HIPAA)
- Open source license management
- Dependency update planning

**When NOT to use:**
- When using vendored dependencies with known state
- For runtime-only security (use SAST/DAST instead)

## Supported Ecosystems

| Ecosystem | Package File | Tools |
|-----------|--------------|-------|
| **npm** | `package.json`, `package-lock.json` | npm audit, snyk |
| **pip** | `requirements.txt`, `Pipfile`, `pyproject.toml` | pip-audit, safety |
| **cargo** | `Cargo.toml`, `Cargo.lock` | cargo audit |
| **go** | `go.mod`, `go.sum` | govulncheck |
| **brew** | `Brewfile` | brew audit |
| **docker** | `Dockerfile`, `docker-compose.yml` | trivy, grype |

## Installation

```bash
# npm ecosystem
npm install -g npm-check-updates

# pip ecosystem
pip install pip-audit safety

# cargo ecosystem
cargo install cargo-audit

# go ecosystem
go install golang.org/x/vuln/cmd/govulncheck@latest

# Multi-ecosystem (Docker)
docker pull aquasec/trivy
docker pull anchore/grype
```

## Quick Start

### Basic Audit

```bash
# npm
npm audit

# pip
pip-audit

# cargo
cargo audit

# go
govulncheck ./...
```

### Multi-Ecosystem Scan

```python
from dependency_scanner import DependencyScanner

scanner = DependencyScanner()

# Auto-detect ecosystems
report = scanner.scan(".")

print(f"Vulnerabilities: {report.vulnerability_count}")
print(f"Critical: {report.critical}")
print(f"High: {report.high}")
print(f"Medium: {report.medium}")
print(f"Low: {report.low}")
```

### Detailed Report

```python
report = scanner.scan(".", include={
    "vulnerabilities": True,
    "outdated": True,
    "licenses": True,
    "supply_chain": True
})

# Print vulnerabilities
for vuln in report.vulnerabilities:
    print(f"[{vuln.severity}] {vuln.package} {vuln.version}")
    print(f"  Fix: {vuln.fixed_version}")
    print(f"  CVE: {vuln.cve}")
```

## Advanced Features

### SBOM Generation

```python
from dependency_scanner import SBOMGenerator

generator = SBOMGenerator()

# Generate CycloneDX SBOM
sbom = generator.generate(
    ".",
    format="cyclonedx",  # or "spdx"
    output="sbom.json"
)

print(f"Components: {sbom.component_count}")
print(f"Dependencies: {sbom.dependency_count}")
print(f"Generated: {sbom.timestamp}")
```

### License Compliance

```python
report = scanner.audit_licenses(".", policy={
    "allowed": ["MIT", "Apache-2.0", "BSD-3-Clause", "ISC"],
    "blocked": ["GPL-3.0", "AGPL-3.0"],
    "review_required": ["LGPL-2.1", "MPL-2.0"]
})

for violation in report.violations:
    print(f"⚠️  {violation.package}: {violation.license}")
    print(f"   Policy: {violation.policy_violation}")
```

### Supply Chain Risk Assessment

```python
risk = scanner.assess_supply_chain(".")

print(f"Risk Score: {risk.score}/100")
print(f"\nRisks:")
for r in risk.risks:
    print(f"  - [{r.severity}] {r.description}")
    print(f"    Mitigation: {r.mitigation}")
```

### Dependency Graph

```python
graph = scanner.dependency_graph(".")

# Find problematic patterns
print(f"Circular dependencies: {graph.circular_count}")
print(f"Max depth: {graph.max_depth}")
print(f"Unused dependencies: {graph.unused_count}")

# Visualize (generates DOT file)
graph.visualize("deps.dot")
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Dependency Audit
on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Dependency Scanner
        run: |
          npm install -g dependency-scanner
          dependency-scanner scan . --format github > results.json
          
      - name: Create PR Comment
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const results = JSON.parse(fs.readFileSync('results.json'));
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: `## Dependency Audit\n\n${results.summary}`
            });
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: dependency-audit
        name: Dependency Audit
        entry: dependency-scanner scan --fail-on high
        language: system
        files: (package\.json|requirements\.txt|Cargo\.toml|go\.mod)
```

## Output Formats

### JSON Report

```json
{
  "timestamp": "2026-06-18T12:00:00Z",
  "project": "1ai-skills",
  "ecosystems": ["npm", "pip"],
  "summary": {
    "total_packages": 156,
    "vulnerabilities": {
      "critical": 0,
      "high": 2,
      "medium": 5,
      "low": 8
    },
    "outdated": 12,
    "license_violations": 0
  },
  "vulnerabilities": [
    {
      "package": "axios",
      "version": "0.21.1",
      "severity": "high",
      "cve": "CVE-2023-45857",
      "description": "SSRF vulnerability",
      "fixed_version": "1.6.0"
    }
  ]
}
```

### Markdown Report

```markdown
# Dependency Audit Report
Generated: 2026-06-18

## Summary
- **Total packages:** 156
- **Vulnerabilities:** 15 (0 critical, 2 high, 5 medium, 8 low)
- **Outdated:** 12 packages
- **License violations:** 0

## Critical Vulnerabilities
None found ✅

## High Vulnerabilities
| Package | Version | CVE | Fix |
|---------|---------|-----|-----|
| axios | 0.21.1 | CVE-2023-45857 | 1.6.0 |
| lodash | 4.17.20 | CVE-2021-23337 | 4.17.21 |

## Recommendations
1. Update axios to 1.6.0 immediately
2. Update lodash to 4.17.21
3. Consider replacing unmaintained package X
```

## Best Practices

### Regular Auditing

```bash
# Run weekly in CI
dependency-scanner scan . --fail-on critical

# Run before releases
dependency-scanner scan . --include sbom,licenses

# Monitor for new CVEs
dependency-scanner monitor --notify slack
```

### Dependency Policy

```yaml
# dependency-policy.yaml
allowed_licenses:
  - MIT
  - Apache-2.0
  - BSD-3-Clause
  - ISC

blocked_packages:
  - left-pad  # Historical incidents
  - event-stream  # Supply chain attack

max_age_months: 24  # Flag packages not updated in 2 years

required_maintainers: 2  # Packages need multiple maintainers
```

### Update Strategy

```python
# Prioritize updates
priorities = scanner.get_update_priorities(".", strategy="security-first")

for update in priorities:
    print(f"[{update.priority}] {update.package}")
    print(f"  Current: {update.current_version}")
    print(f"  Latest: {update.latest_version}")
    print(f"  Breaking: {update.breaking_changes}")
    print(f"  Tests: {update.test_status}")
```

## Integration with Other Skills

### Pre-commit Pipeline

1. **This skill** — Dependency audit
2. `skill://code-reviewer` — Code review
3. `skill://auto-git-commiter` — Git hooks

### CI/CD Pipeline

1. **This skill** — Audit on every PR
2. `skill://cicd-deployment` — GitHub Actions
3. `skill://requesting-code-review` — Block on critical CVEs

### Security Workflow

1. **This skill** — Dependency scanning
2. `skill://security-agent-hardening` — Agent security
3. `skill://best-hacker` — Penetration testing

## Troubleshooting

### False positives
```bash
# Ignore specific CVE
dependency-scanner ignore CVE-2023-XXXXX --reason "Not applicable"

# Ignore package
dependency-scanner ignore-package legacy-pkg --reason "Vendor managed"
```

### Slow scans
```bash
# Skip dev dependencies
dependency-scanner scan . --skip-dev

# Use cache
dependency-scanner scan . --cache-dir .scanner-cache
```

### Lock file issues
```bash
# Regenerate lock file
npm install --package-lock-only
pip-compile requirements.in
```

## Verification Checklist

- [ ] Scanner installed for each ecosystem
- [ ] Basic scan completes successfully
- [ ] SBOM generation works
- [ ] License checking configured
- [ ] CI/CD integration working
- [ ] False positives configured
- [ ] Alerts configured

## Related Skills

- `skill://code-reviewer` — Code quality review
- `skill://security-agent-hardening` — Agent security
- `skill://auto-git-commiter` — Git automation
- `skill://best-hacker` — Security testing
 `skill://cicd-deployment` — Pipeline integration
