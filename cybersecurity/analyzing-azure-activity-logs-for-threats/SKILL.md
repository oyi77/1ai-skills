---
name: analyzing-azure-activity-logs-for-threats
description: 'Queries Azure Monitor activity logs and sign-in logs via azure-monitor-query to detect suspicious administrative
  operations, impossible travel, privilege escalation, and resource modifications. Builds KQL queries for threat hunting in
  Azure environments. Use when investigating suspicious Azure tenant activity or building cloud SIEM detections.

  '
domain: cybersecurity
tags:
- azure
- cloud-security
- azure-monitor
- kql
- threat-hunting
- activity-logs
subdomain: security-operations
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- DE.CM-01
- RS.MA-01
- GV.OV-01
- DE.AE-02
---
# Analyzing Azure Activity Logs For Threats

## When to Use

- When investigating security incidents that require analyzing azure activity logs for threats
- When building detection rules or threat hunting queries for this domain
- When SOC analysts need structured procedures for this analysis type
- When validating security monitoring coverage for related attack techniques

## Prerequisites

- Familiarity with security operations concepts and tools
- Access to a test or lab environment for safe execution
- Python 3.8+ with required dependencies installed
- Appropriate authorization for any testing activities

## Workflow

1. **Scope the Analysis** — Define what azure activity logs artifacts or data sources to examine and the investigation timeline.
2. **Preserve Evidence** — Create forensic copies of relevant data. Maintain chain of custody documentation.
3. **Extract Key Indicators** — Use threats to parse and extract relevant azure activity logs data points from collected artifacts.
4. **Correlate Findings** — Cross-reference extracted data with other sources (threat intel, logs, timelines).
5. **Build Timeline** — Construct a chronological sequence of events related to azure activity logs.
6. **Document Analysis** — Write findings report with evidence, conclusions, and recommendations.

## Tools

- **threats** — Primary tool for this skill
- **Forensic Toolkit** — Evidence collection and analysis
- **Timeline Tools** — Chronological event reconstruction
- **Log Analysis Platform** — Centralized log parsing and search

## Verification

- [ ] All azure activity logs procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
