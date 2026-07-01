---
name: scanning-container-images-with-grype
description: Scan container images for known vulnerabilities using Anchore Grype with SBOM-based matching and configurable
  severity thresholds. Use when scaning container images for known vulnerabilities using anchore grype with.
domain: cybersecurity
subdomain: container-security
tags:
- grype
- vulnerability-scanning
- container-security
- sbom
- anchore
- supply-chain
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- PR.IR-01
- ID.AM-08
- DE.CM-01
---

# Scanning Container Images with Grype

## Overview

Grype is an open-source vulnerability scanner from Anchore that inspects container images, filesystems, and SBOMs for known CVEs. It leverages Syft-generated SBOMs to match packages against multiple vulnerability databases including NVD, GitHub Advisories, and OS-specific feeds.


## When to Use
**Trigger phrases:**
- "scanning container images with grype"
- "Scan container images for known vulnerabilities using Anchore Grype with SBOM-ba"


- When conducting security assessments that involve scanning container images with grype
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites

- Docker or Podman installed
- Grype CLI installed (`curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin`)
- Syft CLI (optional, for SBOM generation)
- Network access to pull vulnerability databases

## Core Commands

This section covers core commands for scanning container images with grype.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### Install Grype

```bash
# Install via script
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin

# Verify installation
grype version

# Install via Homebrew (macOS/Linux)
brew install grype
```

### Scan Container Images

```bash
# Scan a Docker Hub image
grype nginx:latest

# Scan from Docker daemon
grype docker:myapp:1.0

# Scan a local archive
grype docker-archive:image.tar

# Scan an OCI directory
grype oci-dir:path/to/oci/

# Scan a Singularity image
grype sif:image.sif

# Scan a local directory / filesystem
grype dir:/path/to/project
```

### Output Formats

```bash
# Default table output
grype alpine:3.18

# JSON output for pipeline processing
grype alpine:3.18 -o json > results.json

# CycloneDX SBOM output
grype alpine:3.18 -o cyclonedx

# SARIF output for GitHub Security tab
grype alpine:3.18 -o sarif > grype.sarif

# Template-based custom output
grype alpine:3.18 -o template -t /path/to/template.tmpl
```

### Filtering and Thresholds

```bash
# Fail if vulnerabilities meet or exceed a severity
grype nginx:latest --fail-on critical

# Show only fixed vulnerabilities
grype nginx:latest --only-fixed

# Show only non-fixed vulnerabilities
grype nginx:latest --only-notfixed

# Filter by severity
grype nginx:latest --only-fixed -o json | jq '[.matches[] | select(.vulnerability.severity == "High")]'

# Explain a specific CVE
grype nginx:latest --explain --id CVE-2024-1234
```

### Working with SBOMs

```bash
# Generate SBOM with Syft then scan
syft nginx:latest -o spdx-json > nginx-sbom.json
grype sbom:nginx-sbom.json

# Scan CycloneDX SBOM
grype sbom:bom.json
```

### Configuration File (.grype.yaml)

```yaml
# .grype.yaml
check-for-app-update: false
fail-on-severity: "high"
output: "json"
scope: "squashed"  # or "all-layers"
quiet: false

ignore:
  - vulnerability: CVE-2023-12345
    reason: "False positive - not exploitable in our context"
  - vulnerability: CVE-2023-67890
    fix-state: unknown

db:
  auto-update: true
  cache-dir: "/tmp/grype-db"
  max-allowed-built-age: 120h  # 5 days

match:
  java:
    using-cpes: true
  python:
    using-cpes: true
  javascript:
    using-cpes: false
```

### CI/CD Integration

```yaml
# GitHub Actions
- name: Scan image with Grype
  uses: anchore/scan-action@v4
  with:
    image: "myregistry/myapp:${{ github.sha }}"
    fail-build: true
    severity-cutoff: high
    output-format: sarif
  id: scan

- name: Upload SARIF
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: ${{ steps.scan.outputs.sarif }}
```

```yaml
# GitLab CI
container_scan:
  stage: test
  image: anchore/grype:latest
  script:
    - grype ${CI_REGISTRY_IMAGE}:${CI_COMMIT_SHA} --fail-on high -o json > grype-report.json
  artifacts:
    reports:
      container_scanning: grype-report.json
```

## Database Management

```bash
# Check database status
grype db status

# Manually update vulnerability database
grype db update

# Delete cached database
grype db delete

# List supported database providers
grype db list
```

## Key Vulnerability Sources

| Source | Coverage |
|--------|----------|
| NVD | CVEs across all ecosystems |
| GitHub Advisories | Open source package vulnerabilities |
| Alpine SecDB | Alpine Linux packages |
| Amazon Linux ALAS | Amazon Linux AMI |
| Debian Security Tracker | Debian packages |
| Red Hat OVAL | RHEL, CentOS |
| Ubuntu Security | Ubuntu packages |
| Wolfi SecDB | Wolfi/Chainguard images |

## Best Practices

1. **Pin image tags** - Always scan specific digests, not `latest`
2. **Fail on severity** - Set `--fail-on high` or `critical` in CI gates
3. **Use SBOMs** - Generate SBOMs with Syft for reproducible scanning
4. **Suppress false positives** - Use `.grype.yaml` ignore rules with documented reasons
5. **Scan all layers** - Use `--scope all-layers` to catch vulnerabilities in intermediate layers
6. **Automate database updates** - Keep the vulnerability database current in CI runners
7. **Compare scans** - Track vulnerability count over time for regression detection
## When NOT to Use

- You need to perform manual testing (use performing-* skills)
- Task is about analyzing scan results (use analyzing-* skills)
- You need to implement scanning tools (use implementing-* skills)
- Task is about building scanning infrastructure (use building-* skills)
- You don't have network access to targets
- Task requires compliance validation (use auditing-* skills)


## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Failing to use write-blockers when acquiring forensic evidence
- Not verifying hash integrity before and after imaging
- Modifying original evidence during analysis
## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Hash values computed and verified match between source and image
- Chain of custody log complete with timestamps and examiner names
- Analysis tools and versions documented for reproducibility

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |