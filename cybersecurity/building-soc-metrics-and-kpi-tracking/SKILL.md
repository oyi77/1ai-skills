---
name: building-soc-metrics-and-kpi-tracking
description: 'Use when builds SOC performance metrics and KPI tracking dashboards
  measuring Mean Time to Detect (MTTD), Mean Time to Respond (MTTR), alert quality
  ratios, analyst productivity, and detection coverage using SIEM data. Use when SOC
  leadership needs operational visibility, continuous improvement tracking, or executive-level
  reporting on security operations effectiveness.

  '
domain: cybersecurity
tags:
- soc
- metrics
- kpi
- mttd
- mttr
- dashboard
- reporting
- continuous-improvement
subdomain: soc-operations
version: '1.0'
author: oyi77
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
- DE.CM-01
- DE.AE-02
- RS.MA-01
- DE.AE-06
category: cybersecurity
---

# Building Soc Metrics And Kpi Tracking

## Overview

Cybersecurity skill for building soc metrics and kpi tracking. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "building soc metrics and kpi tracking"
- "SOC leadership needs data-driven visibility into operational performance"
- "Continuous improvement programs require baseline measurements and trend tracking"
- "Executive reporting demands quantified security posture and ROI metrics"


Use this skill when:
- SOC leadership needs data-driven visibility into operational performance
- Continuous improvement programs require baseline measurements and trend tracking
- Executive reporting demands quantified security posture and ROI metrics
- Staffing decisions need objective workload and capacity data
- Compliance audits require documented SOC performance evidence

**Do not use** metrics as punitive measures against analysts — metrics should drive process improvement, not individual performance management.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- SIEM with 90+ days of incident and alert disposition data
- Incident ticketing system (ServiceNow, Jira) with timestamp data for incident lifecycle
- Analyst shift schedules and staffing data
- ATT&CK Navigator for detection coverage tracking
- Dashboard platform (Splunk, Grafana, or Power BI)

## Workflow

1. **Pick outcomes, not vanity metrics** — choose a small set tied to decisions: detection quality, response speed, analyst workload, and coverage. Explicitly reject individual analyst ranking; use metrics for process improvement only.
2. **Define formulas and clocks** — document each KPI with exact data source, event start/end, timezone, exclusions, and whether the median or mean is used. Keep MTTD/MTTR definitions stable before trending.
3. **Establish baseline** — collect 30–90 days of clean data; record staffing, shifts, and major incidents so anomalies can be explained.
4. **Compute core measures** — mean/median time to detect and respond; alert-to-incident ratio; true-positive/false-positive rate; auto-close rate; reopen rate; incidents by severity; SLA attainment; detection coverage by ATT&CK technique; analyst queue depth and after-hours load.
5. **Build dashboards with drill-down** — every aggregate links back to the alerts/tickets behind it; add data-freshness timestamps and exclusions notes. Segment by severity/service/shift without exposing individual performance scores.
6. **Review and improve** — monthly operations review: identify trend shifts, ask why, assign owners for process changes; re-measure after change. Never use a metric as a quota or weapon.
7. **Version definitions** — store KPI definitions in version control with change dates; mark breaks in continuity on trend charts.

## Tools

- **Configuration Management** — Infrastructure as code and automation
- **Monitoring Stack** — Observability and alerting
- **Documentation Platform** — Runbooks and architecture docs


## KPI Definitions

| Metric | Definition | Guardrail |
|---|---|---|
| MTTD | median(detected_at − first_observed_at) for confirmed incidents | report only when both timestamps are reliable; segment by severity |
| MTTR | median(contained_at − declared_at) for confirmed incidents | do not mix containment with full recovery; track separately |
| Alert precision | true-positive alerts ÷ reviewed alerts | label sample window and review coverage |
| Alert-to-incident ratio | confirmed incidents ÷ total alerts | interpret with precision and coverage, not alone |
| ATT&CK coverage | tested techniques with active detections ÷ in-scope techniques | a technique counts covered only with telemetry + tested detection |
| SLA attainment | in-SLA incidents ÷ incidents with applicable SLA | disclose exclusions and severity mix |

Never set a “zero incidents” target: it rewards under-reporting. Pair speed metrics with quality measures and sample reviewed cases to catch gaming.

## Verification

- [ ] Each KPI has formula, clock source, timezone, exclusions, owner, and review cadence
- [ ] Baseline includes at least 30 days and notes staffing/incident anomalies
- [ ] Dashboard shows data freshness and links aggregates to source incidents/alerts
- [ ] Metrics are segmented by severity/service, not used to rank individual analysts
- [ ] ATT&CK coverage counts only tested detections with verified telemetry
- [ ] Definitions are versioned; historical trend breaks are annotated
- [ ] Improvement actions have owners and re-measurement dates

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |