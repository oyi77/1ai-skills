---
name: auditing-tls-certificate-transparency-logs
description: Monitors Certificate Transparency (CT) logs to detect unauthorized certificate issuance, discover subdomains
  via CT data, and alert on suspicious certificate activity for owned domains. Uses the crt.sh API and direct CT log querying
  based on RFC 6962 to build continuous monitoring pipelines that catch rogue certificates, track CA behavior, and map the
  external attack surface.
domain: cybersecurity
tags:
- certificate-transparency
- CT-logs
- crt-sh
- subdomain-discovery
- TLS-monitoring
- RFC-6962
subdomain: threat-intelligence
version: 1.0.0
author: mukul975
license: Apache-2.0
nist_csf:
- ID.RA-01
- ID.RA-05
- DE.CM-01
- DE.AE-02
---
# Auditing Tls Certificate Transparency Logs

## When to Use

- Monitoring owned domains for unauthorized or unexpected certificate issuance by unknown Certificate Authorities
- Discovering subdomains and hidden services through certificates logged in public CT logs
- Detecting phishing infrastructure that uses look-alike domain certificates (typosquatting, homograph attacks)
- Auditing Certificate Authority compliance by verifying all issued certificates appear in CT logs as required by browser policies
- Building continuous certificate monitoring into a security operations pipeline with alerting for new issuances

**Do not use** for attacking or disrupting Certificate Authorities, for scraping CT logs in violation of rate limits or terms of service, or as the sole method of subdomain enumeration without corroborating results through DNS verification.

## Prerequisites

- Python 3.10+ with `requests`, `cryptography`, and `pyOpenSSL` libraries installed
- Network access to crt.sh (HTTPS) and public CT log servers
- A list of domains to monitor (owned domains, brand variations, typosquat candidates)
- SMTP credentials or webhook URL for alerting on new certificate discoveries
- Basic understanding of X.509 certificate structure and TLS certificate chain validation

## Workflow

1. **Define Objectives** — Clarify the goals and scope for tls certificate transparency logs.
2. **Gather Resources** — Collect tools, data, and access needed for tls certificate transparency logs.
3. **Execute Process** — Carry out tls certificate transparency logs operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All tls certificate transparency logs procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
