---
name: processing-stix-taxii-feeds
description: 'Processes STIX 2.1 threat intelligence bundles delivered via TAXII 2.1 servers, normalizing objects into platform-native
  schemas and routing them to appropriate consuming systems. Use when onboarding new TAXII collection endpoints, automating
  bi-directional intelligence sharing with ISACs, or building pipeline validation for malformed STIX bundles. Activates for
  requests involving OASIS STIX, TAXII server configuration, MISP TAXII, or Cortex XSOAR feed integrations.

  '
domain: cybersecurity
tags:
- STIX-2.1
- TAXII-2.1
- OASIS
- MISP
- CTI
- IOC
- threat-intelligence
- NIST-SP-800-150
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
# Processing Stix Taxii Feeds

## When to Use

Use this skill when:
- Onboarding a new TAXII 2.1 collection from a government feed (CISA AIS, FS-ISAC) or commercial provider
- Validating that ingested STIX bundles conform to the OASIS STIX 2.1 specification before import
- Building automated pipelines that parse STIX relationship objects to reconstruct campaign context

**Do not use** this skill for proprietary vendor feed formats (Recorded Future JSON, CrowdStrike IOC lists) that require vendor-specific parsers rather than STIX processing.

## Prerequisites

- Python 3.9+ with `stix2` library (pip install stix2) and `taxii2-client` library
- Network access to TAXII 2.1 server endpoint with valid credentials
- Target TIP or SIEM with import API (MISP, OpenCTI, or Splunk ES)

## Workflow

1. **Define Objectives** — Clarify the goals and scope for stix taxii feeds.
2. **Gather Resources** — Collect tools, data, and access needed for stix taxii feeds.
3. **Execute Process** — Carry out stix taxii feeds operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All stix taxii feeds procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
