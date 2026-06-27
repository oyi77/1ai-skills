---
name: performing-ics-asset-discovery-with-claroty
description: 'Perform comprehensive ICS/OT asset discovery using Claroty xDome platform, leveraging passive monitoring, Claroty
  Edge active queries, and integration ecosystem to gain full visibility into industrial control system assets including PLCs,
  RTUs, HMIs, and network infrastructure across Purdue Model levels.

  '
domain: cybersecurity
tags:
- ot-security
- ics
- asset-discovery
- claroty
- xdome
- scada
- network-visibility
- iec62443
subdomain: ot-ics-security
version: '1.0'
author: mahipal
license: Apache-2.0
nist_ai_rmf:
- MEASURE-2.7
- MAP-5.1
- MANAGE-2.4
atlas_techniques:
- AML.T0070
- AML.T0066
- AML.T0082
nist_csf:
- PR.IR-01
- DE.CM-01
- ID.AM-05
- GV.OC-02
---
# Performing Ics Asset Discovery With Claroty

## When to Use

- When gaining initial visibility into an OT environment with unknown or poorly documented assets
- When preparing for an IEC 62443 risk assessment requiring a complete asset inventory
- When onboarding Claroty xDome into a brownfield industrial environment
- When validating existing asset inventory against actual network communications
- When identifying shadow OT devices or unauthorized connections in the control network

**Do not use** for IT-only asset discovery (use tools like Nessus or Qualys), for active scanning of sensitive PLC networks without vendor approval, or for environments where Claroty is not the deployed platform (see implementing-ot-network-traffic-analysis-with-nozomi).

## Prerequisites

- Claroty xDome SaaS subscription or on-premises deployment
- Network TAP or SPAN port configured at OT network boundaries (Levels 1-3 of Purdue Model)
- Claroty Edge collector deployed for safe active querying of hard-to-reach network segments
- Integration credentials for CMDB tools (ServiceNow, BMC) if used
- Network architecture diagram showing VLANs, switches, and firewall zones

## Workflow

1. **Plan Operations** — Define objectives, scope, and success criteria for ics asset discovery operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for ics asset discovery.
3. **Execute Core Workflow** — Use claroty to perform ics asset discovery operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **claroty** — Primary tool for this skill
- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All ics asset discovery procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
