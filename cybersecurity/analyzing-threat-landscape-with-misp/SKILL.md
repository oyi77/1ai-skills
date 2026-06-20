---
name: analyzing-threat-landscape-with-misp
description: Analyze the threat landscape using MISP (Malware Information Sharing Platform) by querying event statistics,
  attribute distributions, threat actor galaxy clusters, and tag trends over time. Uses PyMISP to pull event data, compute
  IOC type breakdowns, identify top threat actors and malware families, and generate threat landscape reports with temporal
  trends.
domain: cybersecurity
tags:
- analyzing
- threat
- landscape
- with
subdomain: threat-intelligence
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- File Metadata Consistency Validation
- Application Protocol Command Analysis
- Identifier Analysis
- Content Format Conversion
- Message Analysis
nist_csf:
- ID.RA-01
- ID.RA-05
- DE.CM-01
- DE.AE-02
---


# Analyzing Threat Landscape with MISP


## When to Use

- When investigating security incidents that require analyzing threat landscape with misp
- When building detection rules or threat hunting queries for this domain
- When SOC analysts need structured procedures for this analysis type
- When validating security monitoring coverage for related attack techniques

## Prerequisites

- Familiarity with threat intelligence concepts and tools
- Access to a test or lab environment for safe execution
- Python 3.8+ with required dependencies installed
- Appropriate authorization for any testing activities

## Instructions

1. Install dependencies: `pip install pymisp`
2. Configure MISP URL and API key.
3. Run the agent to generate threat landscape analysis:
   - Pull event statistics by threat level and date range
   - Analyze attribute type distributions (IP, domain, hash, URL)
   - Identify top MITRE ATT&CK techniques from event tags
   - Track threat actor activity via galaxy clusters
   - Generate temporal trend analysis of IOC submissions

```bash
python scripts/agent.py --misp-url https://misp.local --api-key YOUR_KEY --days 90 --output landscape_report.json
```

## Examples

```bash
# Basic usage example
# Replace with domain-specific commands from the workflow above
```
### Threat Landscape Summary
```
Period: Last 90 days
Events analyzed: 1,247
Top threat level: High (43%)
Top attribute type: ip-dst (31%), domain (22%), sha256 (18%)
Top MITRE technique: T1566 Phishing (89 events)
Top threat actor: APT28 (34 events)
```
## When NOT to Use

- You need to perform the attack, not analyze it (use performing-* skills)
- Task is about detection, not analysis (use detecting-* skills)
- You need to implement controls (use implementing-* skills)
- Task is about threat hunting, not post-incident analysis (use hunting-* skills)
- You don't have access to the artifacts/logs to analyze
- Task requires real-time monitoring (use SOC tools)


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

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
