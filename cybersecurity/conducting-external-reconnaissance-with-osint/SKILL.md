---
name: conducting-external-reconnaissance-with-osint
description: Conducts external reconnaissance using Open Source Intelligence (OSINT) techniques to map an organization's external
  attack surface without directly interacting with target systems. The tester gathers information from public sources including
  DNS records, certificate transparency logs, search engines, social media, code repositories, and data breach databases to
  build a comprehensive target profile.
domain: cybersecurity
tags:
- OSINT
- reconnaissance
- attack-surface
- footprinting
- passive-recon
subdomain: penetration-testing
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- ID.RA-01
- ID.RA-06
- GV.OV-02
- DE.AE-07
---
# Conducting External Reconnaissance With Osint

## When to Use

- Performing the initial reconnaissance phase of a penetration test to gather intelligence before active scanning
- Mapping an organization's external attack surface to identify unknown or shadow IT assets
- Collecting employee information, email formats, and organizational structure for social engineering campaigns
- Identifying exposed credentials, leaked data, or sensitive documents published on the internet
- Scoping the breadth of an organization's digital footprint prior to a red team engagement

**Do not use** for stalking, harassment, or unauthorized surveillance of individuals. OSINT gathering must be conducted within the scope of an authorized engagement and comply with applicable privacy laws (GDPR, CCPA).

## Prerequisites

- Written authorization to perform reconnaissance against the target organization
- Dedicated research workstation with a VPN or Tor for anonymized queries when required
- OSINT framework tools installed: Amass, theHarvester, Shodan CLI, Recon-ng, SpiderFoot
- API keys for Shodan, Censys, SecurityTrails, Hunter.io, VirusTotal, and GitHub for enhanced results
- Disposable email accounts for accessing services that require registration during research

## Workflow

1. **Scope the Analysis** — Define what external reconnaissance artifacts or data sources to examine and the investigation timeline.
2. **Preserve Evidence** — Create forensic copies of relevant data. Maintain chain of custody documentation.
3. **Extract Key Indicators** — Use osint to parse and extract relevant external reconnaissance data points from collected artifacts.
4. **Correlate Findings** — Cross-reference extracted data with other sources (threat intel, logs, timelines).
5. **Build Timeline** — Construct a chronological sequence of events related to external reconnaissance.
6. **Document Analysis** — Write findings report with evidence, conclusions, and recommendations.

## Tools

- **osint** — Primary tool for this skill
- **Forensic Toolkit** — Evidence collection and analysis
- **Timeline Tools** — Chronological event reconstruction
- **Log Analysis Platform** — Centralized log parsing and search

## Verification

- [ ] All external reconnaissance procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
