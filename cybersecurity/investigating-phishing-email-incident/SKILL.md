---
name: investigating-phishing-email-incident
description: 'Investigates phishing email incidents from initial user report through header analysis, URL/attachment detonation,
  impacted user identification, and containment actions using SOC tools like Splunk, Microsoft Defender, and sandbox analysis
  platforms. Use when a reported phishing email requires full incident investigation to determine scope and impact.

  '
domain: cybersecurity
tags:
- soc
- phishing
- incident-response
- email-security
- splunk
- defender
- sandbox
subdomain: soc-operations
mitre_attack:
- T1566.001
- T1566.002
- T1204.001
- T1598.003
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- DE.CM-01
- DE.AE-02
- RS.MA-01
- DE.AE-06
---
# Investigating Phishing Email Incident

## When to Use

Use this skill when:
- A user reports a suspicious email via the phishing report button or helpdesk ticket
- Email security gateway flags a message that bypassed initial filters
- Automated detection identifies credential harvesting URLs or malicious attachments
- A phishing campaign targeting the organization requires scope assessment

**Do not use** for spam or marketing emails without malicious intent — route those to email administration for filter tuning.

## Prerequisites

- Access to email gateway logs (Proofpoint, Mimecast, or Microsoft Defender for Office 365)
- Splunk or SIEM with email log ingestion (O365 Message Trace, Exchange tracking logs)
- Sandbox access (Any.Run, Joe Sandbox, or Hybrid Analysis) for URL/attachment detonation
- Microsoft Graph API or Exchange Admin Center for email search and purge operations
- URLScan.io and VirusTotal API keys

## Workflow

1. **Define Objectives** — Clarify the goals and scope for phishing email incident.
2. **Gather Resources** — Collect tools, data, and access needed for phishing email incident.
3. **Execute Process** — Carry out phishing email incident operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All phishing email incident procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
