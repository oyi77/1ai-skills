---
name: dependency-scanner
description: Automated dependency auditing for npm, pip, cargo, go. Detect vulnerabilities, outdated packages, license conflicts,
  and supply chain risks. Generate SBOMs and compliance reports.
domain: development
tags:
- security
- dependencies
- vulnerabilities
- supply-chain
- sbom
- compliance
---
# Dependency Scanner

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

## Overview

Dependency Scanner supports coding practices with best practices and proven patterns.

## Workflow

1. **Understand requirements** — Clarify acceptance criteria and constraints
2. **Design solution** — Plan architecture and identify patterns
3. **Implement** — Write code following project conventions
4. **Test** — Unit tests, integration tests, edge cases
5. **Review** — Code review for quality, security, and performance
6. **Document** — Update relevant docs and changelogs

## Quality Gates

- [ ] All tests passing
- [ ] No lint errors or warnings
- [ ] Code coverage meets threshold (≥70%)
- [ ] No security vulnerabilities detected
- [ ] Documentation updated

## Best Practices

- Follow SOLID principles and KISS
- Write self-documenting code with clear naming
- Handle errors explicitly — no silent failures
- Keep functions small and focused (<50 lines)
- Use immutable data patterns where possible

