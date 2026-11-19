---
name: implementing-siem-use-cases-for-detection
description: 'Use when implements SIEM detection use cases by designing correlation
  rules, threshold alerts, and behavioral analytics mapped to MITRE ATT&CK techniques
  across Splunk, Elastic, and Sentinel. Use when SOC teams need to expand detection
  coverage, formalize use case lifecycle management, or build a detection library
  aligned to organizational threat profile.

  '
domain: cybersecurity
tags:
- soc
- siem
- use-cases
- detection-engineering
- mitre-attack
- splunk
- elastic
- sentinel
subdomain: soc-operations
version: '1.0'
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
- Token Binding
- Restore Access
- Password Authentication
- Reissue Credential
- Strong Password Policy
nist_csf:
- DE.CM-01
- DE.AE-02
- RS.MA-01
- DE.AE-06
category: cybersecurity
---

# Implementing Siem Use Cases For Detection

## Overview

Cybersecurity skill for implementing siem use cases for detection. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "implementing siem use cases for detection"
- "SOC teams need to build or expand their SIEM detection library from scratch"
- "Threat assessments identify ATT&CK technique gaps requiring new detection rules"
- "Detection engineers need a structured process for use case design, testing, and"


Use this skill when:
- SOC teams need to build or expand their SIEM detection library from scratch
- Threat assessments identify ATT&CK technique gaps requiring new detection rules
- Detection engineers need a structured process for use case design, testing, and deployment
- Compliance requirements mandate specific detection capabilities (PCI DSS, HIPAA, SOX)

**Do not use** for ad-hoc hunting queries — use cases are formalized, tested, and maintained detection rules, not exploratory searches.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- SIEM platform (Splunk ES, Elastic Security, or Microsoft Sentinel) with production data
- ATT&CK Navigator for coverage gap analysis
- Log sources normalized to CIM/ECS field standards
- Use case documentation framework (wiki, Git repo, or detection engineering platform)
- Testing environment with attack simulation tools (Atomic Red Team, MITRE Caldera)

## Workflow

1. **Choose one behavior** — define threat hypothesis, ATT&CK technique, assets/log sources, detection window, and response owner. Avoid vague goals such as “detect attacks”.
2. **Check telemetry first** — verify required fields are present, normalized to CIM/ECS, timestamps/timezones sane, and retention covers the detection window. Missing telemetry is a coverage gap, not a rule failure.
3. **Write the analytic** — start with the smallest query that expresses the behavior; document required fields, threshold/window, exclusions, severity, and expected alert volume.
4. **Test on labeled data** — run against known-positive emulation data and benign baseline; measure true positives, false positives per day, and latency. Use Atomic Red Team/Caldera only in authorized lab or approved test windows.
5. **Tune with evidence** — exclusions must be narrow, reviewed, and expiring; do not suppress an entire user/host/subnet to quiet noise.
6. **Deploy staged** — shadow/monitor-only first, then alert, then response automation only after approval. Include rollback to previous rule version.
7. **Own lifecycle** — assign rule owner, review cadence, data dependencies, and retirement criteria; re-test after schema, source, or ATT&CK mapping changes.

### Detection use-case template

```yaml
name: suspicious-powershell-download
hypothesis: A user process launches PowerShell with encoded/download behavior inconsistent with baseline.
attack_technique: T1059.001
log_sources: [windows_process_creation]
required_fields: [host, user, process_name, command_line, parent_process, timestamp]
window: 5m
severity: high
response_owner: soc-tier-2
mode: alert-only
false_positive_notes: Approved admin automation; narrow allowlist with owner + expiry.
rollback: Disable rule ID and restore prior version from version control.
```

### Rollout guard

Do not enable automated containment from a new analytic until the rule has passed positive/negative testing, false-positive review, and change approval. Keep the first production stage alert-only.

## Tools

- **detection** — Primary tool for this skill
- **Configuration Management** — Infrastructure as code and automation
- **Monitoring Stack** — Observability and alerting
- **Documentation Platform** — Runbooks and architecture docs


## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- [ ] All siem use cases procedures executed completely and documented
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