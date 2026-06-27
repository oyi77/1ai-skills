---
name: correlating-security-events-in-qradar
description: 'Correlates security events in IBM QRadar SIEM using AQL (Ariel Query Language), custom rules, building blocks,
  and offense management to detect multi-stage attacks across network, endpoint, and application log sources. Use when SOC
  analysts need to investigate QRadar offenses, build correlation rules, or tune detection logic for reducing false positives.

  '
domain: cybersecurity
tags:
- soc
- qradar
- siem
- aql
- correlation
- offense-management
- ibm
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
# Correlating Security Events In Qradar

## When to Use

Use this skill when:
- SOC analysts need to investigate QRadar offenses and correlate events across multiple log sources
- Detection engineers build custom correlation rules to identify multi-stage attacks
- Alert tuning is required to reduce false positive offenses and improve signal quality
- The team migrates from basic event monitoring to behavior-based correlation

**Do not use** for log source onboarding or parsing — that requires QRadar administrator access and DSM editor knowledge.

## Prerequisites

- IBM QRadar SIEM 7.5+ with offense management enabled
- AQL knowledge for ad-hoc event and flow queries
- Log sources normalized with proper QID mappings (Windows, firewall, proxy, endpoint)
- User role with offense management, rule creation, and AQL search permissions
- Reference sets/maps configured for whitelist and watchlist management

## Workflow

1. **Define Objectives** — Clarify the goals and scope for security events in qradar.
2. **Gather Resources** — Collect tools, data, and access needed for security events in qradar.
3. **Execute Process** — Carry out security events in qradar operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All security events in qradar procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
