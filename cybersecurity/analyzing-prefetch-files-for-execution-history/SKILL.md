---
name: analyzing-prefetch-files-for-execution-history
description: Parse Windows Prefetch files to determine program execution history including run counts, timestamps, and referenced
  files for forensic investigation.
domain: cybersecurity
tags:
- forensics
- prefetch
- windows-artifacts
- execution-history
- timeline-analysis
- evidence-collection
subdomain: digital-forensics
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- RS.AN-01
- RS.AN-03
- DE.AE-02
- RS.MA-01
---
# Analyzing Prefetch Files For Execution History

## When to Use
- When determining which programs were executed on a Windows system and when
- During malware investigations to confirm execution of suspicious binaries
- For establishing a timeline of application usage during an incident
- When correlating program execution with other forensic artifacts
- To identify anti-forensic tools or unauthorized software that was run

## Prerequisites
- Access to Windows Prefetch directory (C:\Windows\Prefetch\) from forensic image
- PECmd (Eric Zimmerman), WinPrefetchView, or python-prefetch parser
- Understanding of Prefetch file format (versions 17, 23, 26, 30)
- Windows system with Prefetch enabled (default on client OS, disabled on servers)
- Knowledge of Prefetch naming conventions (APPNAME-HASH.pf)

## Workflow

1. **Scope the Analysis** — Define what prefetch files artifacts or data sources to examine and the investigation timeline.
2. **Preserve Evidence** — Create forensic copies of relevant data. Maintain chain of custody documentation.
3. **Extract Key Indicators** — Use execution history to parse and extract relevant prefetch files data points from collected artifacts.
4. **Correlate Findings** — Cross-reference extracted data with other sources (threat intel, logs, timelines).
5. **Build Timeline** — Construct a chronological sequence of events related to prefetch files.
6. **Document Analysis** — Write findings report with evidence, conclusions, and recommendations.

## Tools

- **execution history** — Primary tool for this skill
- **Forensic Toolkit** — Evidence collection and analysis
- **Timeline Tools** — Chronological event reconstruction
- **Log Analysis Platform** — Centralized log parsing and search

## Verification

- [ ] All prefetch files procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
