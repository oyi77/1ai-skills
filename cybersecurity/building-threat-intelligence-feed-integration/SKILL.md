---
name: building-threat-intelligence-feed-integration
description: 'Builds automated threat intelligence feed integration pipelines connecting STIX/TAXII feeds, open-source threat
  intel, and commercial TI platforms into SIEM and security tools for real-time IOC matching and alerting. Use when SOC teams
  need to operationalize threat intelligence by automating feed ingestion, normalization, scoring, and distribution to detection
  systems.

  '
domain: cybersecurity
tags:
- soc
- threat-intelligence
- stix
- taxii
- misp
- feeds
- ioc
- siem-integration
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
# Building Threat Intelligence Feed Integration

## Overview

Cybersecurity skill for building threat intelligence feed integration. Follows industry best practices and security standards.

## When to Use

Use this skill when:
- SOC teams need automated ingestion of threat intelligence feeds into SIEM platforms
- Multiple TI sources require normalization into a common format (STIX 2.1)
- Detection systems need real-time IOC matching against network and endpoint telemetry
- TI feed quality assessment and deduplication processes need to be established

**Do not use** for manual IOC lookup — use dedicated enrichment tools (VirusTotal, AbuseIPDB) for ad-hoc queries.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- MISP instance or Threat Intelligence Platform (TIP) for feed aggregation
- STIX/TAXII client library (`taxii2-client`, `stix2` Python packages)
- SIEM platform (Splunk ES, Elastic Security, or Sentinel) with TI framework configured
- API keys for commercial and open-source feeds (AlienVault OTX, Abuse.ch, CISA AIS)
- Python 3.8+ for feed processing automation

## Workflow

```python
# Example: IOC detection
import re

IOC_PATTERNS = {
    "ip": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "domain": r"\b[a-z0-9-]+\.[a-z]{2,}\b",
    "hash_md5": r"\b[a-f0-9]{32}\b",
    "hash_sha256": r"\b[a-f0-9]{64}\b",
}

def extract_iocs(text: str) -> dict:
    return {k: re.findall(v, text) for k, v in IOC_PATTERNS.items()}
```

1. **Assess Requirements** — Evaluate current environment and define threat intelligence feed integration implementation requirements.
2. **Design Architecture** — Plan the threat intelligence feed integration architecture, including components, integrations, and data flows.
3. **Configure Components** — Set up and configure each threat intelligence feed integration component according to best practices.
4. **Test Integration** — Validate that all components work together. Run functional and security tests.
5. **Deploy to Production** — Roll out the implementation with monitoring and rollback capabilities.
6. **Validate and Document** — Verify the implementation meets requirements. Document configuration and runbooks.

## Tools

- **Configuration Management** — Infrastructure as code and automation
- **Monitoring Stack** — Observability and alerting
- **Documentation Platform** — Runbooks and architecture docs


## Process

1. **Design** — Define interface, identify patterns, plan implementation
1. **Implement** — Write code following existing conventions, add tests
1. **Verify** — Run tests, check integration, validate behavior

## Verification

- [ ] All threat intelligence feed integration procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |