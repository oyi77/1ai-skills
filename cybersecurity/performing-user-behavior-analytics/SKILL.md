---
name: performing-user-behavior-analytics
description: 'Performs User and Entity Behavior Analytics (UEBA) to detect anomalous user activities including impossible
  travel, unusual access patterns, privilege abuse, and insider threats using SIEM-based behavioral baselines and statistical
  analysis. Use when SOC teams need to identify compromised accounts or insider threats through deviation from established
  behavioral norms.

  '
domain: cybersecurity
tags:
- soc
- ueba
- user-behavior
- insider-threat
- anomaly-detection
- splunk
- baseline
subdomain: soc-operations
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- DE.CM-01
- DE.AE-02
- RS.MA-01
- DE.AE-06
---
# Performing User Behavior Analytics

## When to Use

Use this skill when:
- SOC teams need to detect compromised accounts through abnormal authentication patterns
- Insider threat programs require behavioral monitoring beyond rule-based detection
- Impossible travel or geographic anomalies indicate credential compromise
- Privileged account monitoring requires baseline deviation detection

**Do not use** as the sole basis for disciplinary action — UEBA findings are indicators requiring investigation, not proof of malicious intent.

## Prerequisites

- SIEM with 30+ days of authentication and access log history for baseline creation
- VPN, O365, and Active Directory authentication logs normalized to CIM
- GeoIP database (MaxMind GeoLite2) for location-based anomaly detection
- Identity enrichment data (department, role, manager, typical work hours)
- Splunk Enterprise Security with UBA module or equivalent UEBA capability

## Workflow

1. **Plan Operations** — Define objectives, scope, and success criteria for user behavior analytics operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for user behavior analytics.
3. **Execute Core Workflow** — Perform the user behavior analytics operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All user behavior analytics procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
