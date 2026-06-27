---
name: deploying-edr-agent-with-crowdstrike
description: 'Deploys and configures CrowdStrike Falcon EDR agents across enterprise endpoints to enable real-time threat
  detection, behavioral analysis, and automated response. Use when onboarding endpoints to EDR coverage, configuring detection
  policies, or integrating Falcon telemetry with SIEM platforms. Activates for requests involving CrowdStrike deployment,
  Falcon sensor installation, EDR policy configuration, or endpoint detection and response.

  '
domain: cybersecurity
tags:
- endpoint
- edr
- CrowdStrike
- Falcon
- threat-detection
- sensor-deployment
subdomain: endpoint-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_ai_rmf:
- GOVERN-1.1
- MEASURE-2.7
- MANAGE-3.1
- MAP-5.1
- MANAGE-2.4
atlas_techniques:
- AML.T0070
- AML.T0066
- AML.T0082
nist_csf:
- PR.PS-01
- PR.PS-02
- DE.CM-01
- PR.IR-01
---
# Deploying Edr Agent With Crowdstrike

## When to Use

Use this skill when:
- Deploying CrowdStrike Falcon sensors to Windows, macOS, or Linux endpoints
- Configuring Falcon prevention and detection policies for different endpoint groups
- Integrating CrowdStrike telemetry with SIEM (Splunk, Elastic, Sentinel) for correlated detection
- Troubleshooting sensor connectivity, performance, or detection issues

**Do not use** this skill for deploying other EDR solutions (Carbon Black, SentinelOne) or for Falcon cloud workload protection (use cloud-specific deployment guides).

## Prerequisites

- CrowdStrike Falcon console access with Falcon Administrator role
- Customer ID (CID) and Falcon sensor installer package
- Administrative/root access on target endpoints
- Network access: endpoints must reach CrowdStrike cloud (ts01-b.cloudsink.net on port 443)
- Deployment tool: SCCM, Intune, GPO, Ansible, or manual installation

## Workflow

1. **Define Objectives** — Clarify the goals and scope for edr agent.
2. **Gather Resources** — Collect tools, data, and access needed for edr agent.
3. **Execute Process** — Carry out edr agent operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **crowdstrike** — Primary tool for this skill
- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All edr agent procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
