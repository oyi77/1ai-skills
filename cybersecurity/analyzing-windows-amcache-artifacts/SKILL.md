---
name: analyzing-windows-amcache-artifacts
description: 'Parses and analyzes the Windows Amcache.hve registry hive to extract evidence of program execution, application
  installation, and driver loading for digital forensics investigations. Uses Eric Zimmerman''s AmcacheParser and Timeline
  Explorer for artifact extraction, SHA-1 hash correlation with threat intel, and timeline reconstruction. Activates for requests
  involving Amcache forensics, program execution evidence, Windows artifact analysis, or application compatibility cache investigation.

  '
domain: cybersecurity
tags:
- amcache
- windows-forensics
- program-execution
- AmcacheParser
- eric-zimmerman
- timeline-analysis
- DFIR
subdomain: digital-forensics
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- RS.AN-01
- RS.AN-03
- DE.AE-02
- RS.MA-01
---
# Analyzing Windows Amcache Artifacts

## When to Use

- Determining which programs have existed or executed on a Windows system during incident response
- Correlating SHA-1 hashes from Amcache against known malware databases (VirusTotal, CIRCL, MISP)
- Building an application installation and execution timeline for forensic investigations
- Identifying deleted executables that leave traces in Amcache even after file removal
- Investigating insider threats by documenting which portable or unauthorized applications were present
- Analyzing driver loading history to detect rootkits or malicious kernel modules

**Do not use** as sole proof of program execution. Amcache proves file existence and metadata registration, but ShimCache (AppCompatCache) and Prefetch provide stronger execution evidence. Use all three artifacts together for conclusive analysis.

## Prerequisites

- A forensic image or live triage copy of `C:\Windows\appcompat\Programs\Amcache.hve` (and associated `.LOG1`, `.LOG2` transaction logs)
- Eric Zimmerman's AmcacheParser (`AmcacheParser.exe`) downloaded from https://ericzimmerman.github.io/
- Eric Zimmerman's Timeline Explorer for viewing parsed CSV output
- Optionally: Registry Explorer for manual hive inspection
- A SHA-1 whitelist of known-good executables (e.g., NSRL hashset) for filtering
- .NET 6+ runtime installed (required by current EZ tools)
- Write access to an output directory for CSV results

## Workflow

1. **Scope the Analysis** — Define what windows amcache artifacts artifacts or data sources to examine and the investigation timeline.
2. **Preserve Evidence** — Create forensic copies of relevant data. Maintain chain of custody documentation.
3. **Extract Key Indicators** — Parse and extract relevant windows amcache artifacts data points from collected artifacts.
4. **Correlate Findings** — Cross-reference extracted data with other sources (threat intel, logs, timelines).
5. **Build Timeline** — Construct a chronological sequence of events related to windows amcache artifacts.
6. **Document Analysis** — Write findings report with evidence, conclusions, and recommendations.

## Tools

- **Forensic Toolkit** — Evidence collection and analysis
- **Timeline Tools** — Chronological event reconstruction
- **Log Analysis Platform** — Centralized log parsing and search

## Verification

- [ ] All windows amcache artifacts procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
