---
name: collecting-open-source-intelligence
description: Collects and synthesizes open-source intelligence (OSINT) about threat actors, malicious infrastructure, and
  attack campaigns using publicly available data sources, passive reconnaissance tools, and dark web monitoring. Use when
  investigating external threat actor infrastructure, performing pre-engagement reconnaissance for authorized red team assessments,
  or enriching CTI reports with publicly available adversary context.
domain: cybersecurity
tags:
- OSINT
- Maltego
- Shodan
- Recon-ng
- SpiderFoot
- threat-intelligence
- ATT&CK-T1591
- NIST-CSF
subdomain: threat-intelligence
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- ID.RA-01
- ID.RA-05
- DE.CM-01
- DE.AE-02
---
# Collecting Open Source Intelligence

## When to Use

Use this skill when:
- Investigating external infrastructure associated with a phishing campaign targeting your organization
- Enriching threat actor profiles with publicly observable indicators (WHOIS, ASN data, SSL certificates)
- Conducting authorized attack surface discovery to understand your organization's external exposure

**Do not use** this skill for active scanning against targets without explicit written authorization — OSINT collection must remain passive (no packets sent to target systems) unless scope permits active recon.

## Prerequisites

- Maltego CE or commercial license for graph-based link analysis
- Shodan API key (https://shodan.io) for internet-wide device/service discovery
- OSINT Framework familiarity (https://osintframework.com) for tool selection
- SpiderFoot HX or open-source SpiderFoot for automated OSINT correlation

## Workflow

1. **Define Objectives** — Clarify the goals and scope for open source intelligence.
2. **Gather Resources** — Collect tools, data, and access needed for open source intelligence.
3. **Execute Process** — Carry out open source intelligence operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All open source intelligence procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
