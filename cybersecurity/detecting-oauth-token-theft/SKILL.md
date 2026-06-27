---
name: detecting-oauth-token-theft
description: 'Detects and responds to OAuth token theft and replay attacks in cloud environments, focusing on Microsoft Entra
  ID (Azure AD) token protection, conditional access policies, and sign-in anomaly detection. Covers access token theft, refresh
  token replay, Primary Refresh Token (PRT) abuse, and pass-the-cookie attacks. Activates for requests involving OAuth token
  theft detection, token replay prevention, Azure AD conditional access token protection, or cloud identity attack investigation.

  '
domain: cybersecurity
tags:
- oauth
- token-theft
- azure-ad
- entra-id
- conditional-access
- token-replay
- identity-security
- PRT
subdomain: cloud-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- ID.AM-08
- GV.SC-06
- DE.CM-01
---
# Detecting Oauth Token Theft

## When to Use

- Investigating alerts for impossible travel or anomalous token usage in Microsoft Entra ID
- Responding to a suspected session hijacking or pass-the-cookie attack
- Configuring proactive defenses against OAuth token theft in an Azure/M365 environment
- Detecting OAuth device code phishing campaigns that bypass MFA
- Analyzing sign-in logs for token replay indicators
- Implementing Token Protection conditional access policies to bind tokens to devices

**Do not use** for on-premises Kerberos ticket attacks (pass-the-ticket, golden ticket); use Active Directory-specific investigation techniques for those scenarios.

## Prerequisites

- Microsoft Entra ID P2 license (required for Identity Protection risk detections and conditional access)
- Global Administrator or Security Administrator role in the Entra admin center
- Microsoft Defender for Cloud Apps (MDCA) license for session anomaly detection
- Access to Entra ID Sign-in Logs and Audit Logs (requires Diagnostic Settings configured to Log Analytics or Sentinel)
- Familiarity with OAuth 2.0 authorization flows (authorization code, device code, client credentials)
- Microsoft Sentinel or equivalent SIEM ingesting Entra ID sign-in and audit logs

## Workflow

1. **Define Detection Scope** — Identify the specific oauth token theft techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for oauth token theft.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting oauth token theft indicators.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All oauth token theft procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
