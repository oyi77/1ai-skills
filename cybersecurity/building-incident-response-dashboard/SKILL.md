---
name: building-incident-response-dashboard
description: 'Builds real-time incident response dashboards in Splunk, Elastic, or Grafana to provide SOC analysts and leadership
  with situational awareness during active incidents, tracking affected systems, containment status, IOC spread, and response
  timeline. Use when IR teams need unified visibility during incident coordination and post-incident reporting.

  '
domain: cybersecurity
tags:
- soc
- dashboard
- incident-response
- splunk
- visualization
- situational-awareness
- metrics
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
# Building Incident Response Dashboard

## When to Use

Use this skill when:
- IR teams need real-time dashboards during active incidents for coordination and tracking
- SOC leadership requires operational dashboards showing incident status and analyst workload
- Post-incident reviews need visual timelines and impact assessments
- Executive briefings require high-level incident metrics and trend analysis

**Do not use** for day-to-day SOC monitoring dashboards (use Incident Review instead) — IR dashboards are designed for active incident coordination and management reporting.

## Prerequisites

- SIEM platform (Splunk with Dashboard Studio, Elastic Kibana, or Grafana)
- Notable event and incident data in SIEM (Splunk ES incident_review index)
- Ticketing system integration (ServiceNow, Jira) for remediation tracking
- Asset and identity lookup tables for context enrichment
- Dashboard publishing access for SOC team and management distribution

## Workflow

1. **Assess Requirements** — Evaluate current environment and define incident response dashboard implementation requirements.
2. **Design Architecture** — Plan the incident response dashboard architecture, including components, integrations, and data flows.
3. **Configure Components** — Set up and configure each incident response dashboard component according to best practices.
4. **Test Integration** — Validate that all components work together. Run functional and security tests.
5. **Deploy to Production** — Roll out the implementation with monitoring and rollback capabilities.
6. **Validate and Document** — Verify the implementation meets requirements. Document configuration and runbooks.

## Tools

- **Configuration Management** — Infrastructure as code and automation
- **Monitoring Stack** — Observability and alerting
- **Documentation Platform** — Runbooks and architecture docs

## Verification

- [ ] All incident response dashboard procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
