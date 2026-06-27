---
name: deploying-osquery-for-endpoint-monitoring
description: 'Deploys and configures osquery for real-time endpoint monitoring using SQL-based queries to inspect running
  processes, open ports, installed software, and system configuration. Use when building visibility into endpoint state, threat
  hunting across fleet, or implementing compliance monitoring. Activates for requests involving osquery deployment, endpoint
  visibility, fleet management, or SQL-based endpoint querying.

  '
domain: cybersecurity
tags:
- endpoint
- osquery
- endpoint-monitoring
- threat-hunting
- fleet-management
subdomain: endpoint-security
mitre_attack:
- T1547
- T1049
- T1620
- T1053.003
- T1548.001
- T1552
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- PR.PS-02
- DE.CM-01
- PR.IR-01
---
# Deploying Osquery For Endpoint Monitoring

## When to Use

Use this skill when:
- Deploying osquery across Windows, macOS, and Linux endpoints for fleet-wide visibility
- Building threat hunting queries using osquery's SQL interface
- Monitoring endpoint compliance (installed software, open ports, running services)
- Integrating osquery data with SIEM or Kolide/Fleet for centralized management

**Do not use** for real-time alerting (osquery is periodic/on-demand; use EDR for real-time).

## Prerequisites

- Osquery package for target OS (https://osquery.io/downloads)
- Fleet management server (Kolide Fleet or FleetDM) for enterprise deployment
- TLS certificates for secure agent-to-server communication
- Log aggregation pipeline (Filebeat, Fluentd) for osquery result logs

## Workflow

1. **Define Objectives** — Clarify the goals and scope for osquery.
2. **Gather Resources** — Collect tools, data, and access needed for osquery.
3. **Execute Process** — Carry out osquery operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **endpoint monitoring** — Primary tool for this skill
- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All osquery procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
