---
name: performing-purple-team-atomic-testing
description: Use when executing Atomic Red Team tests mapped to MITRE ATT&CK techniques,
  performing coverage gap analysis across the ATT&CK matrix, and running detection
  validation loops to measure blue team visibility. Covers Invoke-AtomicRedTeam PowerShell
  execution, ATT&CK Navigator layer generation for heatmaps, Sigma rule correlation,
  and continuous atomic testing pipelines.
domain: cybersecurity
tags:
- purple-team
- atomic-red-team
- mitre-attack
- detection-engineering
- adversary-emulation
subdomain: purple-team
version: 1.0.0
author: oyi77
license: Apache-2.0
nist_ai_rmf:
- MEASURE-2.7
- MAP-5.1
- MANAGE-2.4
atlas_techniques:
- AML.T0070
- AML.T0066
- AML.T0082
d3fend_techniques:
- Executable Denylisting
- Execution Isolation
- File Metadata Consistency Validation
- Content Format Conversion
- File Content Analysis
nist_csf:
- ID.RA-01
- DE.AE-07
- GV.OV-02
category: cybersecurity
---

# Performing Purple Team Atomic Testing

## Overview

Cybersecurity skill for performing purple team atomic testing. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "performing purple team atomic testing"
- "Use when working with performing purple team atomic testing"


- Validating detection coverage against specific MITRE ATT&CK techniques
- Running purple team exercises using Atomic Red Team test library
- Performing ATT&CK coverage gap analysis to identify blind spots in SIEM/EDR
- Building a detection validation loop: execute atomic test, check SIEM, tune rule, retest
- Generating ATT&CK Navigator heatmap layers for executive reporting
- Automating continuous atomic testing in CI/CD or scheduled pipelines
- Mapping threat intelligence reports to executable atomic tests

**Do not use** for full-scope red team engagements requiring custom implants or live adversary simulation beyond atomic tests; use Caldera, SCYTHE, or Cobalt Strike for advanced adversary emulation.

**DISCLAIMER**: Atomic Red Team tests execute real attack techniques. Run only on systems you own or have explicit written authorization to test. Many tests modify system state, create artifacts, or trigger security alerts. Always execute cleanup commands after testing. Never run atomic tests in production without risk acceptance from stakeholders.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Windows host with PowerShell 5.1+ or PowerShell Core 7+ (Linux/macOS supported for cross-platform atomics)
- Invoke-AtomicRedTeam PowerShell module installed from PSGallery
- Atomic Red Team atomics repository cloned locally
- SIEM/EDR with log ingestion from test endpoints (Splunk, Elastic, Microsoft Sentinel, CrowdStrike)
- MITRE ATT&CK Navigator (web-based or local instance) for layer visualization
- Python 3.9+ with `mitreattack-python`, `pyyaml`, and `requests` for automation scripts
- Sigma rules repository for detection correlation
- Administrative/root access on test endpoints
- Isolated test environment (lab, sandbox, or dedicated test range)

## Workflow (authorized lab only)

1. **Authorize and scope** — Written owner approval, named hosts/accounts, test window, allowed ATT&CK techniques, operator, stop contact, and rollback plan. Do not run against third-party or production assets without explicit authorization and change approval.
2. **Select atomics** — Choose the least-impact Atomic Red Team test that exercises the detection hypothesis. Read its prerequisites, input args, cleanup steps, and impact before execution.
3. **Baseline** — Confirm endpoint/EDR/SIEM agent healthy; record clock, host ID, sensor status, and relevant existing alerts. Save test ID and expected telemetry.
4. **Execute one test at a time** — Use the documented Invoke-AtomicRedTeam command with explicit test GUID and input args; no broad “run all” in shared environments.
5. **Observe detection** — Verify expected telemetry, alert, severity, latency, and ATT&CK mapping in the SIEM/EDR. A test running successfully does not prove detection worked.
6. **Cleanup/rollback** — Run the atomic's cleanup command; verify processes/files/config changes are gone and host returns to baseline. Stop immediately on unexpected impact.
7. **Report and tune** — Record test ID, host, time, expected vs observed signals, alert evidence, missed detections, false positives, and remediation owner. Re-test after the rule change.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Design** — Define interface, identify patterns, plan implementation
1. **Implement** — Write code following existing conventions, add tests
1. **Verify** — Run tests, check integration, validate behavior

## Verification

- [ ] All purple team atomic testing procedures executed completely and documented
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