---
name: performing-endpoint-forensics-investigation
description: 'Performs digital forensics investigation on compromised endpoints including memory acquisition, disk imaging,
  artifact analysis, and timeline reconstruction. Use when investigating security incidents, collecting evidence for legal
  proceedings, or analyzing endpoint compromise scope. Activates for requests involving endpoint forensics, memory analysis,
  disk forensics, or incident investigation.

  '
domain: cybersecurity
tags:
- endpoint
- forensics
- memory-analysis
- disk-imaging
- incident-investigation
- Volatility
subdomain: endpoint-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- PR.PS-02
- DE.CM-01
- PR.IR-01
---
# Performing Endpoint Forensics Investigation

## When to Use

Use this skill when:
- Investigating a confirmed or suspected endpoint compromise requiring forensic analysis
- Collecting volatile and non-volatile evidence for incident response or legal proceedings
- Analyzing memory dumps for malware, injected code, or credential theft artifacts
- Reconstructing attacker timelines from endpoint artifacts (prefetch, shimcache, amcache)

**Do not use** this skill for live threat hunting (use EDR/SIEM) or network forensics.

## Prerequisites

- Forensic workstation with analysis tools (Volatility 3, KAPE, Autopsy, Eric Zimmerman tools)
- Write-blocker for disk imaging (hardware or software)
- Secure evidence storage with chain-of-custody documentation
- Memory acquisition tool (WinPMEM, FTK Imager, Magnet RAM Capture)
- Administrative access to the target endpoint (or physical access)

## Workflow

1. **Plan Operations** — Define objectives, scope, and success criteria for endpoint forensics investigation operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for endpoint forensics investigation.
3. **Execute Core Workflow** — Perform the endpoint forensics investigation operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All endpoint forensics investigation procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
