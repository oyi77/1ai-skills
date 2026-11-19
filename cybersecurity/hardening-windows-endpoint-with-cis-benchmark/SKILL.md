---
name: hardening-windows-endpoint-with-cis-benchmark
description: 'Use when hardens Windows endpoints using CIS (Center for Internet Security)
  Benchmark recommendations to reduce attack surface, enforce security baselines,
  and meet compliance requirements. Use when deploying new Windows workstations or
  servers, remediating audit findings, or establishing organization-wide security
  baselines. Activates for requests involving Windows hardening, CIS benchmarks, GPO
  security baselines, or endpoint configuration compliance.

  '
domain: cybersecurity
tags:
- endpoint
- hardening
- windows-security
- CIS-benchmark
- GPO
- baseline-configuration
subdomain: endpoint-security
version: 1.0.0
author: oyi77
license: Apache-2.0
nist_csf:
- PR.PS-01
- PR.PS-02
- DE.CM-01
- PR.IR-01
category: cybersecurity
---

# Hardening Windows Endpoint With Cis Benchmark

## Overview

Cybersecurity skill for hardening windows endpoint with cis benchmark. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "hardening windows endpoint with cis benchmark"
- "Deploying new Windows 10/11 or Server 2019/2022 endpoints that require security"
- "Establishing organization-wide security baselines using CIS Level 1 or Level 2 p"
- "Remediating findings from compliance audits (PCI DSS, HIPAA, SOC 2) that referen"


Use this skill when:
- Deploying new Windows 10/11 or Server 2019/2022 endpoints that require security hardening
- Establishing organization-wide security baselines using CIS Level 1 or Level 2 profiles
- Remediating findings from compliance audits (PCI DSS, HIPAA, SOC 2) that reference CIS benchmarks
- Validating existing endpoint configurations against current CIS benchmark versions

**Do not use** this skill for Linux endpoints (use hardening-linux-endpoint-with-cis-benchmark) or for cloud-native workloads that require CIS cloud benchmarks.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Windows 10/11 Enterprise or Windows Server 2019/2022 target endpoints
- Active Directory Group Policy Management Console (GPMC) for enterprise deployment
- CIS-CAT Pro Assessor or CIS-CAT Lite for automated benchmark assessment
- Administrative access to target endpoints or domain controller
- Current CIS Benchmark PDF for the target Windows version (download from cisecurity.org)

## Workflow

1. **Freeze scope and rollback** — record host name/image, OS/version, owner, maintenance window, baseline config, backup/snapshot, rollback command, and SCCM/GPO restore plan.
2. **Select the correct benchmark** — CIS profile/version must match Windows edition/release and domain policy; record exceptions; do not claim compliance from another release.
3. **Assess before remediate** — run CIS-CAT Lite/Pro or Windows Security Compliance Toolkit assessment; record rule ID, current value, expected value, severity, and evidence.
4. **Prioritize** — remediate critical/high findings that fit the threat model first; review availability impact for account policies, firewall, kernel-mode drivers, authentication, auditing, and logging changes.
5. **Apply controlled changes** — Group Policy Object via GPMC with a test OU first, then organizational unit rollout; document each change and revert procedure; never paste an unverified registry/GPO script into production.
6. **Re-assess and test** — rerun CIS-CAT; test logon, RDP, service health, logging, patch application, authentication, and required application flows.
7. **Document exceptions** — each exception has owner, rationale, compensating control, expiry/review date, evidence, final report, and rollback instructions.

## Tools

- **cis benchmark** — Primary tool for this skill
- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run hardening windows endpoint with cis benchmark workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All windows endpoint procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |