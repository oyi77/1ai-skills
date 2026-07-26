---
name: collecting-open-source-intelligence
description: "Quick reference for OSINT collection — passive data gathering from public sources for threat intelligence and reconnaissance. Use when collecting open source intelligence."
domain: cybersecurity
tags: [osint, threat-intelligence, reconnaissance, passive, ct-logs]
version: 1.1.0
---

# Quick Reference: Collecting Open-Source Intelligence

> **Full OSINT workflow**: See `../performing-open-source-intelligence-gathering/SKILL.md` for comprehensive offensive and defensive OSINT methodologies. This page is a focused quick-reference for the automated collection phase.

## Overview

OSINT collection is the systematic gathering of publicly available information from sources like Certificate Transparency logs, passive DNS databases, breach repositories, social media platforms, and search engines. Unlike active reconnaissance, passive collection leaves no network traces and can run continuously without alerting the target. This reference covers automated collection patterns suitable for both red-team reconnaissance and defensive threat intelligence pipelines.

## When to Use

- You need to gather intelligence on a target without active scanning or direct interaction
- You're building a continuous OSINT collection pipeline that runs on a schedule
- You need to automate multi-source data gathering for enrichment and correlation
- You're conducting initial recon for a red team engagement or threat assessment

## Quick Start

1. **Scope sources** — Identify 3-5 passive sources per intelligence category (domains: CT logs + passive DNS; people: social + breach DBs; tech: Shodan historical + job postings)
2. **Run collection** — Execute parallel collection scripts with rate-limit-aware scheduling; log source attribution and timestamps for every finding
3. **Normalize output** — Deduplicate across sources, unify into structured JSON with consistent fields (value, source, timestamp, confidence), and stage for enrichment

## Code Example: Multi-Source Subdomain Collection

```python
import requests, json
from datetime import datetime, timedelta

def collect_subdomains(domain: str) -> dict:
    """Passive subdomain collection from 3 sources. No direct target interaction."""
    results = {"domain": domain, "subdomains": set(), "sources": {}, "timestamp": datetime.utcnow().isoformat()}

    # Source 1: Certificate Transparency (crt.sh)
    try:
        resp = requests.get(
            f"https://crt.sh/?q=%25.{domain}&output=json&excluded=expired",
            timeout=30, headers={"User-Agent": "OSINT-Collect/1.0"}
        )
        for entry in resp.json():
            for name in entry.get("name_value", "").split("\n"):
                name = name.strip().lower()
                if name.endswith(f".{domain}"):
                    results["subdomains"].add(name)
        results["sources"]["crt.sh"] = len(results["subdomains"])
    except Exception as e:
        results["sources"]["crt.sh"] = f"error: {e}"

    # Source 2: SecurityTrails (passive DNS — requires free API key)
    try:
        st_key = "YOUR_SECURITYTRAILS_KEY"  # Set via env var in production
        if st_key and st_key != "YOUR_SECURITYTRAILS_KEY":
            resp = requests.get(
                f"https://api.securitytrails.com/v1/domain/{domain}/subdomains",
                headers={"APIKEY": st_key, "Accept": "application/json"},
                timeout=15
            )
            if resp.ok:
                for sub in resp.json().get("subdomains", []):
                    results["subdomains"].add(f"{sub}.{domain}")
        results["sources"]["securitytrails"] = len(results["subdomains"])
    except Exception as e:
        results["sources"]["securitytrails"] = f"error: {e}"

    # Source 3: Web archive (search for historical DNS records)
    try:
        resp = requests.get(
            f"https://web.archive.org/cdx/search/cdx?url=*.{domain}&output=json&fl=original&limit=100",
            timeout=30
        )
        for row in resp.json()[1:]:  # Skip header row
            url = row[0].lower() if isinstance(row, list) else str(row)
            results["subdomains"].add(url.split("/")[2] if "://" in url else url)
        results["sources"]["wayback"] = len(results["subdomains"])
    except Exception as e:
        results["sources"]["wayback"] = f"error: {e}"

    # Deduplicate and sort
    results["subdomains"] = sorted(results["subdomains"])
    results["total_unique"] = len(results["subdomains"])
    return results

# Usage:
# with open("api_keys.json") as f: os.environ.update(json.load(f))
# data = collect_subdomains("example.com")
# print(json.dumps(data, indent=2))
```

## Verification Checklist

- [ ] Collection is 100% passive — no packets sent to target-owned infrastructure (no DNS queries, no HTTP probes to origin)
- [ ] At least 3 independent sources are used per intelligence category
- [ ] All findings are timestamped and source-attributed for chain of custody
- [ ] Results are deduplicated at collection time (set-based or hash-based)
- [ ] Rate limits and terms of service are respected for every API source
- [ ] API keys for paid/enriched sources are stored in environment variables, never in code
- [ ] Collection errors are logged but do not halt the pipeline (handled per-source)

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll just run Nmap — active scanning is faster" | Active scanning alerts defenses and may violate authorization scope. Passive OSINT reveals historical data (old subdomains, leaked creds, expired certs) that active scans never see. |
| "More sources always means better intel" | Unfocused collection drowns signal in noise. Each source should answer a specific Intelligence Requirement (IR); collect with purpose, not volume. |
| "One CT log source is enough for subdomain discovery" | crt.sh alone misses wildcard certs, expired-but-cached entries, and non-HTTPS services. Combine CT logs + passive DNS + web archives for 3x coverage. |
| "I'll deduplicate later during analysis" | Duplicates compound in multi-source pipelines. Deduplicate at collection time with a set-based merging step, or risk inflated counts and false correlations. |

## Workflow
Redirected to parent skill at `../performing-open-source-intelligence-gathering/SKILL.md`.
