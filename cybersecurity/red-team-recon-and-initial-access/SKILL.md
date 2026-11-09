---
name: red-team-recon-and-initial-access
description: Use when orchestrating automated target reconnaissance, subdomain enumeration, cloud bucket discovery, and initial access campaigns using reconFTW, subzy, certSniff, CloudBrute, CredMaster, and King Phisher during authorized red team engagements.
domain: cybersecurity
subdomain: penetration-testing
category: cybersecurity
version: 1.0.0
author: oyi77
license: Apache-2.0
tags:
- red-team
- reconnaissance
- initial-access
- osint
- phishing
triggers:
- red team recon
- automated reconnaissance
- subdomain takeover
- certsniff
- cloudbrute
- password spraying
- qr phishing
---

# Red Team Recon and Initial Access

## Workflow

| Step | Action |
|---|---|
| Reconnaissance | Enumerate surface with reconFTW or passive only. |
| Takeover Test | Run subzy on discovered dangling records. |
| Cloud Probe | Query buckets with CloudBrute using allow-listed words. |
| Credential Spray | Spray with low frequency; confirm before lockout. |
| Phishing | Launch phishing campaign templates approved by the engagement sponsor. |
| Evidence Capture | Record C2 artifacts and parse logs for the report. |
## Overview

Cybersecurity playbook covering external attack surface mapping, automated multi-tool reconnaissance, and initial access execution. Emphasizes passive data collection, low-noise active probing, and authorized phishing / credential validation standards.

## When to Use

**Trigger phrases:**
- "red team external reconnaissance"
- "automate recon using reconftw"
- "test subdomain takeover with subzy"
- "enumerate cloud storage using cloudbrute"
- "execute password spray with credmaster"
- "orchestrate phishing campaign with king phisher"

- Mapping an enterprise's public-facing digital footprint and exposed infrastructure
- Validating dangling DNS records to prevent or demonstrate subdomain takeover risks
- Discovering misconfigured and publicly accessible cloud buckets across multi-cloud environments
- Testing authentication defenses and lockout policies via controlled, distributed password spraying
- Conducting authorized social engineering and phishing assessments to benchmark security awareness

## When NOT to Use

- When operating without formal, signed Rules of Engagement defining explicit in-scope domains
- When launching aggressive scans that violate acceptable use policies or create Denial of Service
- When harvesting credentials from unauthorized external third-party sites

## Prerequisites

- Signed RoE document specifying allowed domains, CIDR ranges, and excluded targets
- Offensive workstation with Go, Python 3, Docker, and standard OSINT toolchains
- Approved phishing templates and dedicated engagement redirector infrastructure

## Automated Reconnaissance Tooling

### reconFTW
Comprehensive reconnaissance automation framework:
- Orchestrates subdomain discovery, port scanning, screenshotting, and template vulnerability checks
- Supports passive-only modes (`-p`) to avoid generating direct traffic to the target

### subzy
High-speed subdomain takeover verification tool:
- Matches response fingerprints against known vulnerable cloud and SaaS hosting providers
- Validates dangling CNAME records without performing destructive state modifications

### CloudBrute
Multi-cloud asset and storage enumerator:
- Searches across AWS (S3), Google Cloud Platform (Storage), and Azure (Blobs) for organization-specific keywords
- Discovers exposed company files, configuration backups, and private assets

### certSniff
Real-time Certificate Transparency log monitor:
- Ingests the CertStream API to identify newly registered subdomains and domains matching target keywords
- Enables immediate discovery of newly provisioned staging or shadow IT infrastructure

## Initial Access Playbooks

### Controlled Password Spraying (CredMaster & TREVORspray)
- Rotates source IP addresses through AWS API Gateway or proxy pools to evade IP-based blocking.
- Enforces strict delay intervals between attempts per user account to prevent triggering lockout thresholds.

### Targeted Phishing Infrastructure (King Phisher & EvilGoPhish)
- Manages multi-template phishing engagements with granular click and credential entry tracking.
- Implements two-factor authentication reverse-proxy capture in authorized high-maturity assessments.

## Anti-Rationalization Table

| Excuse | Flawed Rationalization | Required Discipline |
|---|---|---|
| "Aggressive scanning gets results faster" | "Target won't notice high scan rates." | High-rate scanning triggers automated firewall bans and masks real vulnerabilities; use low-and-slow rate-limited scanning. |
| "Claim subdomain takeover without full proof" | "Dangling CNAME means it's vulnerable." | Always verify with fingerprint validation (subzy) and prove take-over via a benign static canary file only. |
| "Spray credentials until access is gained" | "Lockouts are the target's problem." | Account lockouts disrupt business operations; strictly adhere to the lockout limits specified in the RoE. |

## Verification Checklist

- [ ] All domains and IP targets verified against RoE authorization annex
- [ ] Subdomain takeovers validated using harmless canary verification
- [ ] Password spraying executed below documented lockout thresholds
- [ ] Phishing email headers, landing pages, and domains approved by engagement sponsor
- [ ] Complete raw scan logs and discovered artifacts archived for evidence
