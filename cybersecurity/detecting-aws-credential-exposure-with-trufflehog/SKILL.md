---
name: detecting-aws-credential-exposure-with-trufflehog
description: 'Detecting exposed AWS credentials in source code repositories, CI/CD pipelines, and configuration files using
  TruffleHog, git-secrets, and AWS-native detection mechanisms to prevent credential theft and unauthorized account access.

  '
domain: cybersecurity
tags:
- cloud-security
- aws
- credential-exposure
- trufflehog
- secrets-detection
- devsecops
subdomain: cloud-security
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- ID.AM-08
- GV.SC-06
- DE.CM-01
---
# Detecting Aws Credential Exposure With Trufflehog

## When to Use

- When integrating secrets detection into CI/CD pipelines to prevent credential commits reaching production
- When performing a security audit of existing repositories for historically committed AWS credentials
- When responding to an AWS GuardDuty alert about credential usage from an unexpected IP or region
- When onboarding repositories from acquired companies or third-party vendors
- When validating that credential rotation processes have removed all references to old access keys

**Do not use** for real-time credential monitoring (use AWS GuardDuty or Amazon Macie), for managing secrets (use AWS Secrets Manager or HashiCorp Vault), or for detecting non-credential sensitive data like PII (use Amazon Macie or DLP tools).

## Prerequisites

- TruffleHog v3 installed (`brew install trufflehog` or `pip install trufflehog`)
- git-secrets installed for pre-commit hook integration (`brew install git-secrets`)
- Access to source code repositories (GitHub, GitLab, Bitbucket, or local git repos)
- AWS CLI configured with permissions to check key status (`iam:ListAccessKeys`, `iam:GetAccessKeyLastUsed`)
- GitHub or GitLab API token for scanning organization-wide repositories

## Workflow

1. **Define Detection Scope** — Identify the specific aws credential exposure techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for aws credential exposure.
3. **Build Detection Queries** — Write trufflehog queries targeting aws credential exposure indicators. Use platform-specific query language for optimal performance.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **trufflehog** — Primary tool for this skill
- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All aws credential exposure procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
