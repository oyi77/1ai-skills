---
name: performing-subdomain-enumeration-with-subfinder
description: Enumerate subdomains of target domains using ProjectDiscovery's Subfinder passive reconnaissance tool to map
  the attack surface during security assessments.
domain: cybersecurity
tags:
- subdomain-enumeration
- reconnaissance
- bug-bounty
- attack-surface
- subfinder
- passive-recon
- osint
subdomain: web-application-security
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- ID.RA-01
- PR.DS-10
- DE.CM-01
---
# Performing Subdomain Enumeration With Subfinder

## When to Use
- During the reconnaissance phase of penetration testing or bug bounty hunting
- When mapping the external attack surface of a target organization
- Before performing vulnerability scanning on discovered subdomains
- When building an asset inventory for continuous security monitoring
- During red team engagements requiring passive information gathering

## Prerequisites
- Go 1.21+ installed for building from source
- Subfinder v2 installed (`go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest`)
- API keys configured for passive sources (Shodan, Censys, VirusTotal, SecurityTrails, Chaos)
- Provider configuration file at `$HOME/.config/subfinder/provider-config.yaml`
- Network access to passive DNS and certificate transparency sources
- httpx or httprobe for validating discovered subdomains

## Workflow

1. **Plan Operations** — Define objectives, scope, and success criteria for subdomain enumeration operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for subdomain enumeration.
3. **Execute Core Workflow** — Use subfinder to perform subdomain enumeration operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **subfinder** — Primary tool for this skill
- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All subdomain enumeration procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
