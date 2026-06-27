---
name: detecting-supply-chain-attacks-in-ci-cd
description: 'Scans GitHub Actions workflows and CI/CD pipeline configurations for supply chain attack vectors including unpinned
  actions, script injection via expressions, dependency confusion, and secrets exposure. Uses PyGithub and YAML parsing for
  automated audit. Use when hardening CI/CD pipelines or investigating compromised build systems.

  '
domain: cybersecurity
tags:
- detecting
- supply
- chain
- attacks
subdomain: security-operations
version: '1.0'
author: mahipal
license: Apache-2.0
atlas_techniques:
- AML.T0010
- AML.T0104
nist_ai_rmf:
- GOVERN-5.2
- MAP-1.6
- MANAGE-2.2
nist_csf:
- DE.CM-01
- RS.MA-01
- GV.OV-01
- DE.AE-02
---
# Detecting Supply Chain Attacks In Ci Cd

## When to Use

- When investigating security incidents that require detecting supply chain attacks in ci cd
- When building detection rules or threat hunting queries for this domain
- When SOC analysts need structured procedures for this analysis type
- When validating security monitoring coverage for related attack techniques

## Prerequisites

- Familiarity with security operations concepts and tools
- Access to a test or lab environment for safe execution
- Python 3.8+ with required dependencies installed
- Appropriate authorization for any testing activities

## Workflow

1. **Define Detection Scope** — Identify the specific supply chain attacks in ci cd techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for supply chain attacks in ci cd.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting supply chain attacks in ci cd indicators.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All supply chain attacks in ci cd procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
