---
name: collecting-threat-intelligence-with-misp
description: MISP (Malware Information Sharing Platform) is an open-source threat intelligence platform for gathering, sharing,
  storing, and correlating Indicators of Compromise (IOCs) of targeted attacks, threat. Use when working with collecting threat intelligence with misp.
domain: cybersecurity
subdomain: threat-intelligence
tags:
- threat-intelligence
- cti
- ioc
- mitre-attack
- stix
- misp
- taxii
- threat-sharing
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- ID.RA-01
- ID.RA-05
- DE.CM-01
- DE.AE-02
---
# Collecting Threat Intelligence with MISP

## Overview

MISP (Malware Information Sharing Platform) is an open-source threat intelligence platform for gathering, sharing, storing, and correlating Indicators of Compromise (IOCs) of targeted attacks, threat intelligence, financial fraud information, vulnerability information, or counter-terrorism information. This skill covers deploying MISP, configuring threat feeds, using the PyMISP API for programmatic access, and building automated collection pipelines that aggregate IOCs from multiple community and commercial sources.


## When to Use
**Trigger phrases:**
- "collecting threat intelligence with misp"
- "MISP (Malware Information Sharing Platform) is an open-source threat intelligenc"


- When managing security operations that require collecting threat intelligence with misp
- When improving security program maturity and operational processes
- When establishing standardized procedures for security team workflows
- When integrating threat intelligence or vulnerability data into operations

## Prerequisites

- Python 3.9+ with `pymisp` library installed
- Docker and Docker Compose for MISP deployment
- Understanding of STIX 2.1 and TAXII 2.1 protocols
- Familiarity with IOC types: hashes, IP addresses, domains, URLs, email addresses
- Network access to MISP community feeds (circl.lu, botvrij.eu)

## Key Concepts

This section covers key concepts for collecting threat intelligence with misp.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### MISP Architecture

MISP operates on an event-based model where threat intelligence is organized into events containing attributes (IOCs), objects (structured groupings of attributes), galaxies (threat actor/malware clusters linked to MITRE ATT&CK), and tags for classification. Synchronization between MISP instances uses a pull/push model over HTTPS with API key authentication.

### Feed Types

- **MISP Feeds**: Native JSON/CSV feeds from MISP community (CIRCL OSINT, botvrij.eu)
- **Freetext Feeds**: Unstructured text feeds parsed for IOCs (abuse.ch, Feodo Tracker)
- **TAXII Feeds**: STIX/TAXII 2.1 compatible feeds from commercial and government sources
- **CSV Feeds**: Structured CSV feeds with configurable column mapping

### PyMISP API

PyMISP is the official Python library to access MISP platforms via their REST API. It supports fetching events, adding/updating events and attributes, uploading samples, and searching across the entire MISP dataset. Authentication uses an API key passed in the `Authorization` header.

## Workflow

1. **Isolate the sample** — ensure the malware is in a sandboxed environment with no network access
2. **Record file metadata** — hash the sample and note file type, size, and compile timestamp
3. **Static analysis** — examine strings, imports, and disassembled code without execution
4. **Dynamic analysis** — execute in a monitored sandbox and record behavior (file, registry, network)
5. **Document IOCs** — extract indicators of compromise and write the analysis report
### Step 1: Deploy MISP with Docker

```bash
git clone https://github.com/MISP/misp-docker.git
cd misp-docker
cp template.env .env
# Edit .env to set MISP_BASEURL, MISP_ADMIN_EMAIL, MISP_ADMIN_PASSPHRASE
docker compose up -d
```

### Step 2: Configure Default Feeds

Enable built-in MISP feeds via the web UI or API:

```python
from pymisp import PyMISP

misp = PyMISP('https://misp.local', 'YOUR_API_KEY', ssl=False)

# List available feeds
feeds = misp.feeds()
for feed in feeds:
    print(f"{feed['Feed']['id']}: {feed['Feed']['name']} - Enabled: {feed['Feed']['enabled']}")

# Enable CIRCL OSINT Feed
misp.enable_feed(feed_id=1)
misp.cache_feed(feed_id=1)
misp.fetch_feed(feed_id=1)
```

### Step 3: Add Custom Threat Feeds

```python
# Add abuse.ch URLhaus feed
feed_data = {
    'name': 'URLhaus Recent URLs',
    'provider': 'abuse.ch',
    'url': 'https://urlhaus.abuse.ch/downloads/csv_recent/',
    'source_format': 'csv',
    'input_source': 'network',
    'publish': False,
    'enabled': True,
    'headers': '',
    'distribution': 0,
    'sharing_group_id': 0,
    'tag_id': 0,
    'default': False,
    'lookup_visible': True
}
result = misp.add_feed(feed_data)
print(f"Feed added: {result}")
```

### Step 4: Programmatic Event Search and Retrieval

```python
from pymisp import PyMISP, MISPEvent
from datetime import datetime, timedelta

misp = PyMISP('https://misp.local', 'YOUR_API_KEY', ssl=False)

# Search for events from the last 7 days
result = misp.search(
    controller='events',
    date_from=(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
    type_attribute='ip-dst',
    to_ids=True,
    pythonify=True
)

for event in result:
    print(f"Event {event.id}: {event.info}")
    for attr in event.attributes:
        if attr.type == 'ip-dst' and attr.to_ids:
            print(f"  IOC: {attr.value} (category: {attr.category})")
```

### Step 5: Export IOCs for Downstream Tools

```python
# Export as STIX 2.1 bundle
stix_output = misp.search(
    controller='events',
    return_format='stix2',
    tags=['tlp:white'],
    published=True
)

# Export IDS-flagged attributes as Suricata rules
suricata_rules = misp.search(
    controller='attributes',
    return_format='suricata',
    to_ids=True,
    type_attribute=['ip-dst', 'domain', 'url']
)

# Export as CSV for SIEM ingestion
csv_output = misp.search(
    controller='attributes',
    return_format='csv',
    type_attribute='ip-dst',
    to_ids=True
)
```

## Validation Criteria

- MISP instance is deployed and accessible via HTTPS
- At least 3 community feeds are enabled and fetching data successfully
- PyMISP script can authenticate, search events, and retrieve IOCs
- Events contain properly tagged and categorized attributes
- Export to STIX 2.1 produces valid STIX bundles
- Automated feed fetch runs on schedule (cron or MISP scheduler)

## When NOT to Use

- You need to analyze collected intelligence (use analyzing-* skills)
- Task is about detecting collection activity (use detecting-* skills)
- You need to implement collection tools (use implementing-* skills)
- Task is about building collection infrastructure (use building-* skills)
- You don't have access to intelligence sources
- Task requires classified access (follow clearance process)


## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Analyzing malware on a machine connected to the production network
- Failing to isolate the analysis environment from the internet
- Executing samples without proper containment (VM, sandbox)

## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Sample hash recorded and verified (MD5, SHA-1, SHA-256)
- Analysis environment confirmed isolated from production network
- Indicators of compromise (IOCs) extracted and documented

## References

- [MISP Project Official Site](https://www.misp-project.org/)
- [PyMISP Documentation](https://pymisp.readthedocs.io/)
- [MISP GitHub Repository](https://github.com/MISP/MISP)
- [MISP OpenAPI Specification](https://www.misp-project.org/openapi/)
- [CIRCL OSINT Feed](https://www.circl.lu/doc/misp/feed-osint/)

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |