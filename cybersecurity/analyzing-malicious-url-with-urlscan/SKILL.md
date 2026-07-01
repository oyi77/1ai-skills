---
name: analyzing-malicious-url-with-urlscan
description: URLScan.io is a free service for scanning and analyzing suspicious URLs. It captures screenshots, DOM content,
  HTTP transactions, JavaScript behavior, and network connections of web pages in an isolat. Use when working with analyzing malicious url with urlscan.
domain: cybersecurity
subdomain: phishing-defense
tags:
- phishing
- email-security
- social-engineering
- dmarc
- awareness
- url-analysis
- threat-intelligence
version: '1.0'
author: mahipal
license: Apache-2.0
atlas_techniques:
- AML.T0052
nist_csf:
- PR.AT-01
- DE.CM-09
- RS.CO-02
- DE.AE-02
---
# Analyzing Malicious URL with URLScan

## Overview
URLScan.io is a free service for scanning and analyzing suspicious URLs. It captures screenshots, DOM content, HTTP transactions, JavaScript behavior, and network connections of web pages in an isolated environment. This skill covers using URLScan's web interface and API to investigate phishing URLs, credential harvesting pages, and malicious redirects without exposing the analyst's system to risk.


## When to Use
**Trigger phrases:**
- "analyzing malicious url with urlscan"
- "URLScan"


- When investigating security incidents that require analyzing malicious url with urlscan
- When building detection rules or threat hunting queries for this domain
- When SOC analysts need structured procedures for this analysis type
- When validating security monitoring coverage for related attack techniques

## Prerequisites
- URLScan.io account (free tier available, API key for automation)
- Python 3.8+ with requests library
- Understanding of HTTP protocols and web technologies
- Familiarity with phishing URL patterns

## Key Concepts

This section covers key concepts for analyzing malicious url with urlscan.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### URLScan Capabilities
1. **Safe browsing**: Renders URLs in isolated Chromium instance
2. **Screenshot capture**: Visual snapshot of the rendered page
3. **DOM analysis**: Full HTML content after JavaScript execution
4. **Network log**: All HTTP requests made by the page (HAR format)
5. **Certificate analysis**: SSL/TLS certificate details
6. **Technology detection**: Identifies web frameworks and libraries
7. **IP/ASN mapping**: Infrastructure intelligence
8. **Verdict**: Community and automated classification

### Phishing URL Red Flags
- Newly registered domains (< 30 days)
- Free hosting services (Wix, GitHub Pages, Firebase)
- URL shorteners hiding final destination
- Excessive subdomain depth (login.microsoft.com.evil.com)
- Brand name in subdomain or path, not domain
- Non-standard ports
- Data URIs or base64-encoded content
- JavaScript-heavy pages with minimal HTML

## Workflow

1. **Scope the task** — define objectives, boundaries, and success criteria
2. **Gather information** — collect all necessary data and context before proceeding
3. **Execute the core workflow** — follow the domain-specific steps methodically
4. **Validate results** — verify outputs against expected outcomes or baselines
5. **Document findings** — record results, anomalies, and recommendations
### Step 1: Submit URL to URLScan
```
Web: Navigate to https://urlscan.io and submit the suspicious URL
API: POST https://urlscan.io/api/v1/scan/
     Header: API-Key: your-api-key
     Body: {"url": "https://suspicious-url.com", "visibility": "private"}
```

### Step 2: Analyze Results
- Review screenshot for brand impersonation
- Check redirects and final destination URL
- Examine DOM for credential input forms
- Review network requests for data exfiltration endpoints
- Check SSL certificate validity and issuer

### Step 3: Extract IOCs
- Domains and IPs contacted
- URLs in redirect chain
- SHA-256 hashes of page resources
- JavaScript file hashes

### Step 4: Cross-Reference with Threat Intelligence
Use the `scripts/process.py` to automate URL scanning, extract IOCs, and cross-reference with VirusTotal, PhishTank, and Google Safe Browsing.

## When NOT to Use

- You need to perform the attack, not analyze it (use performing-* skills)
- Task is about detection, not analysis (use detecting-* skills)
- You need to implement controls (use implementing-* skills)
- Task is about threat hunting, not post-incident analysis (use hunting-* skills)
- You don't have access to the artifacts/logs to analyze
- Task requires real-time monitoring (use SOC tools)


## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Acting on threat intelligence without validating source reliability
- Sharing classified or sensitive indicators without proper handling procedures
- Alerting threat actors to detection capabilities through visible response actions

## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Results validated against known-good baselines or reference implementations
- Documentation complete enough for another analyst to reproduce findings

## Tools & Resources
- **URLScan.io**: https://urlscan.io/
- **URLScan API**: https://urlscan.io/docs/api/
- **VirusTotal URL Scanner**: https://www.virustotal.com/
- **PhishTank**: https://phishtank.org/
- **Google Safe Browsing**: https://transparencyreport.google.com/safe-browsing/search
- **Any.Run**: https://any.run/ (interactive sandbox)
- **Hybrid Analysis**: https://www.hybrid-analysis.com/

## Validation
- Successfully scan a suspicious URL via API
- Extract screenshot and identify brand impersonation
- Document complete redirect chain
- Generate IOC list from scan results
- Cross-reference findings with at least 2 threat intelligence sources

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |