---
name: analyzing-usb-device-connection-history
description: Investigate USB device connection history from Windows registry, event logs, and setupapi logs to track removable
  media usage and potential data exfiltration.
domain: cybersecurity
tags:
- forensics
- usb-forensics
- removable-media
- registry-analysis
- data-exfiltration
- device-history
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
# Analyzing Usb Device Connection History

## When to Use
- When investigating potential data exfiltration via removable storage devices
- During insider threat investigations to track USB device usage
- For compliance audits verifying removable media policy enforcement
- When correlating USB connections with file access and copy events
- For establishing a timeline of device connections during an incident

## Prerequisites
- Forensic image or extracted registry hives and event logs
- Access to SYSTEM, SOFTWARE, and NTUSER.DAT registry hives
- SetupAPI logs (setupapi.dev.log)
- Windows Event Logs (System, Security, DriverFrameworks-UserMode)
- USBDeview, USB Forensic Tracker, or RegRipper
- Understanding of USB device identification (VID, PID, serial number)

## Workflow

1. **Scope the Analysis** — Define what usb device connection history artifacts or data sources to examine and the investigation timeline.
2. **Preserve Evidence** — Create forensic copies of relevant data. Maintain chain of custody documentation.
3. **Extract Key Indicators** — Parse and extract relevant usb device connection history data points from collected artifacts.
4. **Correlate Findings** — Cross-reference extracted data with other sources (threat intel, logs, timelines).
5. **Build Timeline** — Construct a chronological sequence of events related to usb device connection history.
6. **Document Analysis** — Write findings report with evidence, conclusions, and recommendations.

## Tools

- **Forensic Toolkit** — Evidence collection and analysis
- **Timeline Tools** — Chronological event reconstruction
- **Log Analysis Platform** — Centralized log parsing and search

## Verification

- [ ] All usb device connection history procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
