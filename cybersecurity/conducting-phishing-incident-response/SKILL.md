---
name: conducting-phishing-incident-response
description: 'Responds to phishing incidents by analyzing reported emails, extracting indicators, assessing credential compromise,
  quarantining malicious messages across the organization, and remediating affected accounts. Covers email header analysis,
  URL/attachment sandboxing, and mailbox-wide purge operations. Activates for requests involving phishing response, email
  incident, credential phishing, spear phishing investigation, or phishing remediation.

  '
domain: cybersecurity
tags:
- phishing-response
- email-security
- credential-compromise
- email-header-analysis
- mailbox-remediation
subdomain: incident-response
mitre_attack:
- T1566
- T1204
- T1534
- T1598
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- RS.MA-01
- RS.MA-02
- RS.AN-03
- RC.RP-01
---
# Conducting Phishing Incident Response

## When to Use

- A user reports receiving a suspicious email via the phishing report button or abuse mailbox
- Email gateway detects a malicious email that bypassed initial filtering
- Threat intelligence indicates an active phishing campaign targeting the organization
- A user confirms they clicked a link or opened an attachment from a suspicious email
- Credentials have been entered on a suspected phishing page

**Do not use** for business email compromise (BEC) involving compromised internal accounts; use BEC response procedures which focus on account takeover investigation.

## Prerequisites

- Email security gateway with message trace and quarantine capabilities (Microsoft Defender for Office 365, Proofpoint, Mimecast)
- Microsoft 365 admin access or Google Workspace admin for mailbox search and purge
- Malware sandbox for attachment and URL analysis (ANY.RUN, Joe Sandbox, Hybrid Analysis)
- Email header analysis tools (MXToolbox Header Analyzer, Google Admin Toolbox)
- Identity provider access for account remediation (Azure AD, Okta, Duo)
- Phishing report intake process (dedicated mailbox or integrated report button)

## Workflow

1. **Scope the Analysis** — Define what phishing incident response artifacts or data sources to examine and the investigation timeline.
2. **Preserve Evidence** — Create forensic copies of relevant data. Maintain chain of custody documentation.
3. **Extract Key Indicators** — Parse and extract relevant phishing incident response data points from collected artifacts.
4. **Correlate Findings** — Cross-reference extracted data with other sources (threat intel, logs, timelines).
5. **Build Timeline** — Construct a chronological sequence of events related to phishing incident response.
6. **Document Analysis** — Write findings report with evidence, conclusions, and recommendations.

## Tools

- **Forensic Toolkit** — Evidence collection and analysis
- **Timeline Tools** — Chronological event reconstruction
- **Log Analysis Platform** — Centralized log parsing and search

## Verification

- [ ] All phishing incident response procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
