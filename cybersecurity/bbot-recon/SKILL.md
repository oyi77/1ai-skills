---
name: bbot-recon
description: Automated reconnaissance using BBOT (Black Lantern Security's recursive internet scanner). Use when performing bug bounty recon, attack surface management, subdomain enumeration, web spidering, or OSINT gathering for authorized security assessments.
domain: cybersecurity
subdomain: penetration-testing
tags:
- bbot
- recon
- bug-bounty
- subdomain-enum
- osint
- attack-surface
- automation
- nuclei
- yara
version: '1.0'
license: AGPL-3.0
nist_csf:
- ID.RA-01
- ID.RA-02
- DE.CM-01
---

# BBOT Recon Skill

## Overview

BBOT (Bee·bot) is a multipurpose recursive internet scanner by Black Lantern Security, inspired by SpiderFoot. It automates reconnaissance for bug bounties and Attack Surface Management (ASM) with 200+ modules, NLP-powered subdomain mutations, custom YARA rules, Lightfuzz, and native output to Neo4j, SIEMs, and databases. BBOT consistently finds 20-50% more subdomains than competing tools.

## When to Use

- Starting bug bounty reconnaissance on authorized targets
- Enumerating subdomains for a target domain
- Crawling/spidering web applications for endpoint discovery
- Gathering emails and OSINT data for social engineering assessments
- Mapping attack surface across cloud, code repos, and web assets
- Building target profiles for penetration testing engagements
- Running custom vulnerability scans with YARA rules
- Fuzzing web parameters with Lightfuzz
- Correlating findings in graph databases

## When NOT to Use

- Target has no bug bounty program or written authorization
- Simple single-endpoint testing (use nuclei directly)
- Real-time monitoring (use dedicated ASM platforms)
- Source code review (use SAST tools directly)

## Prerequisites

- Python 3.9+
- pipx (recommended) or pip
- Docker (optional, for full stack)
- Optional: API keys for enhanced module coverage (Shodan, SecurityTrails, VirusTotal, etc.)

## Installation

```bash
# Install stable version via pipx
pipx install bbot

# Bleeding edge (dev branch)
pipx install --pip-args '\--pre' bbot

# Docker
docker run -it blacklanternsecurity/bbot --help

# Full stack with Neo4j
git clone https://github.com/blacklanternsecurity/bbot.git
cd bbot
docker compose up -d
```

## The Process

1. **Scope the task** — define objectives, boundaries, and success criteria
2. **Gather information** — collect all necessary data and context before proceeding
3. **Execute the core workflow** — follow the domain-specific steps methodically
4. **Validate results** — verify outputs against expected outcomes or baselines
5. **Document findings** — record results, anomalies, and recommendations

### Step 1: Scope Validation

Verify the target is authorized before any scanning begins.

1. Confirm written authorization exists for the target
2. Define target type: domain, IP, IP range, URL, or organization
3. Check for rate limiting requirements or testing windows
4. Record scope in local config for downstream reference

### Step 2: Target Configuration

BBOT accepts multiple target types:

```bash
# Domain
bbot -t evilcorp.com -p subdomain-enum

# IP/Range
bbot -t 1.2.3.0/24 -p subdomain-enum

# URL
bbot -t https://www.evilcorp.com -p web-basic

# Organization
bbot -t ORG:evilcorp -p subdomain-enum

# Username
bbot -t USER:bobsmith -p subdomain-enum

# Mobile App
bbot -t MOBILE_APP:https://play.google.com/store/apps/details?id=com.evilcorp.app

# Multiple targets
bbot -t evilcorp.com evilcorp.org 1.2.3.0/24 -p subdomain-enum

# From file
bbot -t targets.txt -p subdomain-enum
```

### Step 3: Select Preset

BBOT presets are pre-configured scan profiles:

| Preset | Purpose | Modules Enabled |
|--------|---------|-----------------|
| `subdomain-enum` | Subdomain discovery | APIs, DNS brute-force, mutations |
| `spider` | Web crawling | Recursive link following, email extraction |
| `email-enum` | Email gathering | APIs, scraping, pattern matching |
| `web-basic` | Light web scan | IIS shortnames, basic web modules |
| `web-thorough` | Aggressive web scan | All web-basic + deeper analysis |
| `cloud-enum` | Cloud asset discovery | S3, Azure, GCP bucket enumeration |
| `code-enum` | Code repo discovery | GitHub, GitLab secrets/repos |
| `paramminer` | Parameter discovery | Hidden params, API keys |
| `dirbust-light` | Directory brute-force | Light directory enumeration |
| `web-screenshots` | Screenshot capture | Visual target mapping |
| `kitchen-sink` | Everything | All above combined |

```bash
# Subdomain enumeration
bbot -t evilcorp.com -p subdomain-enum

# Web spider
bbot -t evilcorp.com -p spider

# Full attack surface
bbot -t evilcorp.com -p kitchen-sink --allow-deadly

# Custom combination
bbot -t evilcorp.com -p subdomain-enum spider web-basic
```

### Step 4: Module Selection

BBOT has 200+ modules organized by category:

#### Subdomain Modules
- `subfinder` — Subfinder integration
- `amass` — Amass integration  
- `crt` — Certificate transparency
- `dnscommonsrv` — Common SRV records
- `massdns` — High-speed DNS resolution
- `shodan_dns` — Shodan DNS lookup
- `virustotal` — VirusTotal subdomains
- `chaos` — ProjectDiscovery Chaos
- `securitytrails` — SecurityTrails API
- `c99` — C99 API
- `facebook` — Facebook CT logs
- `rapiddns` — RapidDNS lookup
- `threatminer` — ThreatMiner intel

#### Web Modules
- `httpx` — HTTP probing
- `nuclei` — Vulnerability scanning
- `paramminer` — Parameter discovery
- `dirbust` — Directory brute-force
- `badsecrets` — Secret detection
- `baddns` — DNS misconfiguration
- `lightfuzz` — Web fuzzing
- `ffuf` — Directory/file fuzzing
- `iis-shortnames` — IIS shortname enumeration
- `wappalyzer` — Technology detection

#### OSINT Modules
- `github` — GitHub code/search
- `gitlab` — GitLab code/search
- `emails` — Email harvesting
- `urlscan` — URLScan.io integration
- `wayback` — Wayback Machine
- `otx` — AlienVault OTX
- `hunterio` — Hunter.io emails
- `hibp` — Have I Been Pwned

#### Cloud Modules
- `bucket_amazon` — AWS S3 bucket enum
- `bucket_azure` — Azure blob enum
- `bucket_firebase` — Firebase enum
- `bucket_google` — GCP bucket enum
- `cloudcheckr` — Cloud resource discovery

```bash
# Enable specific modules
bbot -t evilcorp.com -m subfinder httpx nuclei

# Disable specific modules
bbot -t evilcorp.com -p subdomain-enum -em amass

# List all modules
bbot --list-modules

# List modules by flag
bbot --list-flags
```

### Step 5: Output Configuration

BBOT supports multiple output formats:

```bash
# JSON output
bbot -t evilcorp.com -p subdomain-enum -o json

# CSV output
bbot -t evilcorp.com -p subdomain-enum -o csv

# Subdomains only (TXT)
bbot -t evilcorp.com -p subdomain-enum -om subdomains

# Neo4j graph database
bbot -t evilcorp.com -p subdomain-enum -om neo4j

# Splunk
bbot -t evilcorp.com -p subdomain-enum -om splunk

# Discord notifications
bbot -t evilcorp.com -p subdomain-enum -om discord

# Slack notifications
bbot -t evilcorp.com -p subdomain-enum -om slack

# Teams notifications
bbot -t evilcorp.com -p subdomain-enum -om teams

# Elasticsearch
bbot -t evilcorp.com -p subdomain-enum -om elasticsearch

# SQLite
bbot -t evilcorp.com -p subdomain-enum -om sqlite

# PostgreSQL
bbot -t evilcorp.com -p subdomain-enum -om postgres

# MySQL
bbot -t evilcorp.com -p subdomain-enum -om mysql

# Webhook (HTTP POST)
bbot -t evilcorp.com -p subdomain-enum -om http
```

### Step 6: API Key Configuration

Enhance module coverage with API keys in `~/.config/bbot/bbot.yml`:

```yaml
modules:
  shodan_dns:
    api_key: YOUR_SHODAN_KEY
  virustotal:
    api_key: YOUR_VT_KEY
  securitytrails:
    api_key: YOUR_ST_KEY
  github:
    api_key: YOUR_GITHUB_KEY
  c99:
    api_key:
      - KEY1
      - KEY2
      - KEY3
  chaos:
    api_key: YOUR_CHAOS_KEY
  hunterio:
    api_key: YOUR_HUNTER_KEY
  urlscan:
    api_key: YOUR_URLSCAN_KEY
```

Or via command line:

```bash
bbot -c modules.virustotal.api_key=YOUR_KEY -t evilcorp.com -p subdomain-enum
```

### Step 7: Advanced Techniques

#### NLP Subdomain Mutations
BBOT uses NLP to generate target-specific subdomain mutations:

```bash
# Automatic mutations based on discovered subdomains
bbot -t evilcorp.com -p subdomain-enum

# Custom word cloud
bbot -t evilcorp.com -p subdomain-enum -w /path/to/wordlist.txt

# Disable mutations
bbot -t evilcorp.com -p subdomain-enum -c dns.disable_mutations=true
```

#### Scope Control
```bash
# Strict scope (only target domain)
bbot -t evilcorp.com -p subdomain-enum --strict-scope

# Include subdomains of subdomains
bbot -t evilcorp.com -p subdomain-enum --scope-distance 2

# Blacklist specific subdomains
bbot -t evilcorp.com -p subdomain-enum -b "test.evilcorp.com"
```

#### Rate Limiting
```bash
# Limit requests per second
bbot -t evilcorp.com -p web-thorough --rate-limit 50

# Custom DNS threads
bbot -t evilcorp.com -p subdomain-enum -c dns.threads=25 dns.brute_threads=1000

# Web request delay
bbot -t evilcorp.com -p web-thorough -c web.request_delay=0.5
```

#### Custom YARA Rules
BBOT supports custom YARA rules for scanning:

```bash
# Create YARA rule
cat > custom.yar << 'EOF'
rule Find_API_Keys {
    meta:
        description = "Finds potential API keys"
    strings:
        $key1 = /sk-[a-zA-Z0-9]{32,}/
        $key2 = /AKIA[0-9A-Z]{16}/
        $key3 = /ghp_[a-zA-Z0-9]{36}/
    condition:
        any of them
}
EOF

# Run with YARA rules
bbot -t evilcorp.com -p spider -c modules.github.yara_rules=custom.yar
```

#### Lightfuzz Module
BBOT's built-in fuzzer for web parameters:

```bash
# Enable lightfuzz
bbot -t www.evilcorp.com -p web-basic -m lightfuzz

# Custom fuzzing intensity
bbot -t www.evilcorp.com -m lightfuzz -c modules.lightfuzz.intensity=high
```

#### Nuclei Integration
BBOT integrates with Nuclei for vulnerability scanning:

```bash
# Run nuclei through BBOT
bbot -t evilcorp.com -p subdomain-enum -m nuclei

# Custom nuclei templates
bbot -t evilcorp.com -p subdomain-enum -m nuclei -c modules.nuclei.templates=/path/to/templates

# Severity filter
bbot -t evilcorp.com -p subdomain-enum -m nuclei -c modules.nuclei.severity=high,critical
```

#### Interactsh (Out-of-Band Testing)
BBOT uses Interactsh for OOB vulnerability detection:

```bash
# BBOT automatically uses Interactsh for SSRF, blind XSS, etc.
bbot -t evilcorp.com -p web-thorough

# Custom Interactsh server
bbot -t evilcorp.com -p web-thorough -c interactsh.server=custom.server.com
```

### Step 8: Custom Preset Creation

Create reusable scan configurations:

```yaml
# ~/.config/bbot/presets/my-recon.yml
description: Custom bug bounty recon preset

include:
  - subdomain-enum
  - spider
  - web-basic

flags:
  - subdomain-enum
  - web-basic

modules:
  - nuclei
  - paramminer
  - lightfuzz

config:
  dns:
    threads: 25
    brute_threads: 1000
  web:
    spider_distance: 3
    spider_depth: 5
  modules:
    nuclei:
      severity: high,critical

output_modules:
  - json
  - subdomains
  - neo4j
```

```bash
# Use custom preset
bbot -t evilcorp.com -p my-recon
```

### Step 9: Python API Usage

```python
# Synchronous
from bbot.scanner import Scanner

if __name__ == "__main__":
    scan = Scanner("evilcorp.com", presets=["subdomain-enum"])
    for event in scan.start():
        print(event)

# Asynchronous
from bbot.scanner import Scanner

async def main():
    scan = Scanner("evilcorp.com", presets=["subdomain-enum"])
    async for event in scan.async_start():
        print(event.json())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

# With custom modules
from bbot.scanner import Scanner

async def main():
    scan = Scanner(
        "evilcorp.com",
        modules=["subfinder", "httpx", "nuclei"],
        output_modules=["json", "neo4j"],
        config={"modules": {"nuclei": {"severity": "high,critical"}}}
    )
    async for event in scan.async_start():
        if event.type == "VULNERABILITY":
            print(f"Found vuln: {event.data}")

import asyncio
asyncio.run(main())
```

### Step 10: Event Correlation with Neo4j

```bash
# Start Neo4j
docker run -d --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/bbotpassword \
  neo4j:community

# Run scan with Neo4j output
bbot -t evilcorp.com -p kitchen-sink -om neo4j

# Query Neo4j (Cypher)
# Find all subdomains
MATCH (n:DNS_NAME) RETURN n

# Find all URLs pointing to same IP
MATCH (n:DNS_NAME)-[:RESOLVES_TO]->(ip:IP_ADDRESS)<-[:RESOLVES_TO]-(m:DNS_NAME)
MATCH (n)-[:URL]->(u:URL)
RETURN u

# Find potential attack paths
MATCH path=(target:DNS_NAME {data: 'evilcorp.com'})-[*1..3]->(vuln:VULNERABILITY)
RETURN path
```

## Scan Profiles for Bug Bounty

Recommended scan profiles by time budget and target type:

### Quick Recon (5 min)
```bash
bbot -t evilcorp.com -p subdomain-enum -rf passive
```

### Standard Recon (30 min)
```bash
bbot -t evilcorp.com -p subdomain-enum spider email-enum
```

### Deep Recon (2+ hours)
```bash
bbot -t evilcorp.com -p kitchen-sink --allow-deadly
```

### Web Application Focus
```bash
bbot -t www.evilcorp.com -p web-thorough paramminer dirbust
```

### Cloud Asset Discovery
```bash
bbot -t evilcorp.com -p cloud-enum code-enum
```

### Bug Bounty Pipeline
```bash
# Phase 1: Subdomain enum
bbot -t evilcorp.com -p subdomain-enum -o json -om subdomains -o subdomains.json

# Phase 2: Web scan on discovered subdomains
bbot -t subdomains.json -p web-basic -m nuclei lightfuzz

# Phase 3: Deep spider on interesting targets
bbot -t interesting_targets.txt -p spider -c web.spider_distance=3
```

## Expected Output

BBOT produces structured events:

```json
{
  "type": "DNS_NAME",
  "data": "subdomain.evilcorp.com",
  "module": "subfinder",
  "timestamp": "2024-01-15T10:30:00",
  "tags": ["subdomain"],
  "parent": "evilcorp.com",
  "scope_distance": 1
}
```

Key output types:
- `DNS_NAME` — Discovered subdomains
- `IP_ADDRESS` — Resolved IP addresses
- `URL` — Discovered URLs/endpoints
- `EMAIL` — Harvested email addresses
- `TECHNOLOGY` — Detected technologies
- `VULNERABILITY` — Found vulnerabilities
- `FINDING` — Security findings
- `OPEN_TCP_PORT` — Open ports
- `SOCIAL` — Social media profiles
- `CODE_REPOSITORY` — Code repos

## Docker Compose Stack

Full BBOT stack with Neo4j and output modules:

```yaml
# docker-compose.yml
version: '3.8'
services:
  bbot:
    image: blacklanternsecurity/bbot:latest
    volumes:
      - ./bbot_config:/root/.config/bbot
      - ./output:/output
    command: -t evilcorp.com -p kitchen-sink -om neo4j -o /output
    depends_on:
      - neo4j

  neo4j:
    image: neo4j:community
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      NEO4J_AUTH: neo4j/bbotpassword
    volumes:
      - neo4j_data:/data

volumes:
  neo4j_data:
```

## Red Flags

- Scanning targets without explicit written authorization
- Exceeding rate limits or causing denial of service
- Scanning out-of-scope assets
- Storing scan results insecurely (contains sensitive data)
- Running aggressive scans (`--allow-deadly`) without understanding implications
- Ignoring program-specific rules for bug bounty targets
- Exfiltrating data beyond what's needed for the assessment

## Verification

- Target is explicitly authorized for testing
- Scan completed without errors
- Output files generated and accessible
- API keys configured for enhanced coverage (optional)
- Results deduplicated and filtered for actionable findings
- Scope compliance documented
- Rate limits respected

## Integration with Other Skills

Combine BBOT recon with:

- `bug-hunting` — Validate discovered vulnerabilities
- `bounty-target-finder` — Prioritize targets by payout potential
- `web3-auditor` — For blockchain/Web3 targets
- `smart-contract-exploiter` — When BBOT discovers Web3 endpoints
- `recon-automation` — Build automated recon pipelines

## Troubleshooting

Common issues and performance tuning for BBOT scans:

### Common Issues

```bash
# Module not working
bbot -t evilcorp.com -p subdomain-enum -v  # verbose output

# DNS resolution issues
bbot -t evilcorp.com -p subdomain-enum -c dns.server=8.8.8.8

# Module dependencies missing
bbot --install-all-deps

# Check module status
bbot --list-modules

# Debug specific module
bbot -t evilcorp.com -m subfinder -v --debug
```

### Performance Tuning

```bash
# Increase threads for faster scanning
bbot -t evilcorp.com -p subdomain-enum -c dns.threads=50

# Reduce for stability
bbot -t evilcorp.com -p subdomain-enum -c dns.threads=10

# Limit concurrent web requests
bbot -t evilcorp.com -p web-thorough -c web.max_concurrent=10
```

## References

- [BBOT Documentation](https://www.blacklanternsecurity.com/bbot/)
- [BBOT GitHub](https://github.com/blacklanternsecurity/bbot)
- [BBOT Module List](https://www.blacklanternsecurity.com/bbot/Stable/modules/list_of_modules/)
- [BBOT Presets](https://www.blacklanternsecurity.com/bbot/Stable/scanning/presets_list/)
- [BBOT YARA Rules](https://www.blacklanternsecurity.com/bbot/Stable/modules/custom_yara_rules/)
- [BBOT Lightfuzz](https://www.blacklanternsecurity.com/bbot/Stable/modules/lightfuzz/)
- [BBOT Nuclei Integration](https://www.blacklanternsecurity.com/bbot/Stable/modules/nuclei/)

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
