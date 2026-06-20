---
name: analyzing-web-server-logs-for-intrusion
description: Parse Apache and Nginx access logs to detect SQL injection attempts, local file inclusion, directory traversal,
  web scanner fingerprints, and brute-force patterns. Uses regex-based pattern matching against OWASP attack signatures, GeoIP
  enrichment for source attribution, and statistical anomaly detection for request frequency and response size outliers.
domain: cybersecurity
tags:
- analyzing
- web
- server
- logs
subdomain: security-operations
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- DE.CM-01
- RS.MA-01
- GV.OV-01
- DE.AE-02
---


# Analyzing Web Server Logs for Intrusion


## When to Use

- When investigating security incidents that require analyzing web server logs for intrusion
- When building detection rules or threat hunting queries for this domain
- When SOC analysts need structured procedures for this analysis type
- When validating security monitoring coverage for related attack techniques

## Prerequisites

- Familiarity with security operations concepts and tools
- Access to a test or lab environment for safe execution
- Python 3.8+ with required dependencies installed
- Appropriate authorization for any testing activities

## Instructions

1. Install dependencies: `pip install geoip2 user-agents`
2. Collect web server access logs in Combined Log Format (Apache) or Nginx default format.
3. Parse each log entry extracting: IP, timestamp, method, URI, status code, response size, user-agent, referer.
4. Apply detection rules:
   - SQL injection: `UNION SELECT`, `OR 1=1`, `' OR '`, hex encoding patterns
   - LFI/Path traversal: `../`, `/etc/passwd`, `/proc/self`, `php://filter`
   - XSS: `<script>`, `javascript:`, `onerror=`, `onload=`
   - Scanner signatures: nikto, sqlmap, dirbuster, gobuster, wfuzz user-agents
   - Brute force: >50 POST requests to login endpoints from same IP in 5 minutes
5. Enrich with GeoIP data and generate a prioritized findings report.

```bash
python scripts/agent.py --log-file /var/log/nginx/access.log --geoip-db GeoLite2-City.mmdb --output web_intrusion_report.json
```

## Examples

```bash
# Basic usage example
# Replace with domain-specific commands from the workflow above
```
### Detect SQLi in URI
```
192.168.1.100 - - [15/Jan/2024:10:30:45 +0000] "GET /products?id=1' UNION SELECT username,password FROM users-- HTTP/1.1" 200 4532
```

### Scanner User-Agent Detection
```
Nikto/2.1.6, sqlmap/1.7, DirBuster-1.0-RC1, gobuster/3.1.0
```
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
- Testing without rate limiting, potentially causing service degradation
- Storing sensitive test data (credentials, tokens) in plain text logs
- Using automated scanners blindly without reviewing results for false positives
## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Vulnerabilities reproduced with proof-of-concept and impact analysis
- False positives filtered out through manual verification
- Fix recommendations include code-level remediation guidance

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
