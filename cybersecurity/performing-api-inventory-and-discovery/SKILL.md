---
name: performing-api-inventory-and-discovery
description: Performs API inventory and discovery to identify all API endpoints in an organization's environment including
  documented, undocumented, shadow, zombie, and deprecated APIs. The tester uses passive traffic analysis, active scanning,
  DNS enumeration, JavaScript analysis, and cloud resource inventory to build a comprehensive API catalog. Maps to OWASP API9:2023
  Improper Inventory Management.
domain: cybersecurity
tags:
- api-security
- owasp
- api-discovery
- shadow-api
- inventory
- attack-surface
subdomain: api-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- ID.RA-01
- PR.DS-10
- DE.CM-01
---
# Performing Api Inventory And Discovery

## When to Use

- Mapping the complete API attack surface of an organization before a security assessment
- Identifying shadow APIs deployed by development teams without security review
- Discovering deprecated or zombie API versions that remain accessible but unmaintained
- Finding undocumented API endpoints exposed through mobile applications, SPAs, or microservices
- Building an API inventory for compliance requirements (PCI-DSS, SOC2, GDPR)

**Do not use** without written authorization. API discovery involves scanning network infrastructure and analyzing traffic.

## Prerequisites

- Written authorization specifying the target domains and network ranges
- Passive traffic capture capability (network tap, proxy, or cloud traffic mirroring)
- Active scanning tools: Amass, subfinder, httpx, and nuclei
- JavaScript analysis tools: LinkFinder, JS-Miner, or custom parsers
- Access to cloud console (AWS, Azure, GCP) for API gateway inventory
- Burp Suite Professional for passive API endpoint discovery

## Workflow

1. **Plan Operations** — Define objectives, scope, and success criteria for api inventory and discovery operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for api inventory and discovery.
3. **Execute Core Workflow** — Perform the api inventory and discovery operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All api inventory and discovery procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
