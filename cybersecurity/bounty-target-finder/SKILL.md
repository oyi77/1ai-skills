---
name: bounty-target-finder
description: Find and prioritize high-paying bug bounty programs. Use when discovering new targets, comparing bounty payouts,
  filtering programs by scope, or building a target pipeline for continuous hunting.
domain: cybersecurity
author: oyi77
license: Apache-2.0
subdomain: general-cybersecurity
tags:
- bounty
- cybersecurity
- finder
- money
- pipeline
- security
- target
- threat-defense
version: 1.0.0
---

# Bounty Target Finder

## Overview

Find, filter, and prioritize bug bounty programs that maximize payout per hour hunted. This skill surfaces high-value in-scope targets, ranks them by expected value (payout probability × bounty range), and builds a continuous hunting pipeline so you never waste time on low-reward or over-saturated programs.

## When to Use

- Starting a new bug bounty hunting cycle
- Looking for fresh targets with less competition
- Comparing payouts across platforms
- Building a continuous hunting pipeline
- Finding programs that match your skill set

## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope
- When you need to hunt *right now* instead of planning — just pick the first target from your existing list

## Money-Making Overview

**Buyer persona:** Full-time and part-time bug bounty hunters who want to maximize payout per hour. These are security researchers, pentesters, and hackers who treat bounty hunting as a primary or secondary income stream.

**What they'll pay for:** Prioritized target lists that surface high-payout, low-competition programs. Time saved on recon = more time finding bugs = more bounties collected.

**Pricing tiers (service model):**

| Tier | Price | Deliverable | Timeline |
|------|-------|-------------|----------|
| **Starter** | $50 | Top 10 targets from one platform (HackerOne or Bugcrowd), ranked by max bounty, with in-scope scope summary | 1 day |
| **Pro** | $200 | Top 30 targets across 3 platforms, ranked by estimated payout/hour, includes competition analysis (recent submissions count), scope detail, and technology stack | 3 days |
| **Elite** | $500 | Top 100 targets with full pipeline, weekly refresh, custom filters (skill match, tech stack, P1/P2 historical bounty data), Slack/Telegram alerts when new high-value programs appear | Ongoing weekly |

**First-dollar timeline:** Deliver Starter within 1 day. First payment clears within 48 hours of delivery. Pro clients typically convert from Starter, so every output is a sales document.

## First Action in 60 Minutes

Run this script to scrape HackerOne and Bugcrowd for programs with the highest max bounties and in-scope web/API targets:

```bash
#!/bin/bash
# bounty-sweep.sh — Find high-paying programs in ~10 minutes
# Usage: bash bounty-sweep.sh

mkdir -p bounty_targets

# --- HackerOne Hacktivity (public programs with disclosed reports) ---
echo "[*] Fetching HackerOne programs..."
curl -s "https://hackerone.com/programs/search?query=type:hackerone&sort=popularity&page[size]=100" \
  -H "Accept: application/json" \
  -o bounty_targets/h1_raw.json

# --- Bugcrowd programs ---
echo "[*] Fetching Bugcrowd programs..."
curl -s "https://bugcrowd.com/programs.json?sort[]=promoted&page=1" \
  -H "Accept: application/json" \
  -o bounty_targets/bc_raw.json

# --- Filter and rank by max bounty ---
python3 << 'PYEOF'
import json, sys

programs = []

# Parse HackerOne
try:
    h1 = json.load(open("bounty_targets/h1_raw.json"))
    for p in h1.get("data", []):
        attrs = p.get("attributes", {})
        name = attrs.get("name", "N/A")
        max_bounty = attrs.get("maximum_bounty", 0) or 0
        min_bounty = attrs.get("minimum_bounty", 0) or 0
        offers_bounties = attrs.get("offers_bounties", False)
        if offers_bounties and max_bounty >= 500:
            programs.append({
                "platform": "HackerOne",
                "name": name,
                "url": f"https://hackerone.com/{attrs.get('handle', name)}",
                "max_bounty": max_bounty,
                "min_bounty": min_bounty,
                "score": max_bounty * (1 if max_bounty <= 5000 else 0.8)  # diminishing returns on massive bounties
            })
except Exception as e:
    print(f"[!] H1 parse error: {e}")

# Parse Bugcrowd
try:
    bc = json.load(open("bounty_targets/bc_raw.json"))
    for p in bc:
        max_b = 0
        if p.get("max_payout"):
            max_b = int(p["max_payout"].replace(",", "").replace("$", ""))
        name = p.get("name", p.get("title", "N/A"))
        if max_b >= 500:
            programs.append({
                "platform": "Bugcrowd",
                "name": name,
                "url": f"https://bugcrowd.com/{p.get('slug', name)}",
                "max_bounty": max_b,
                "min_bounty": 0,
                "score": max_b * (1 if max_b <= 5000 else 0.8)
            })
except Exception as e:
    print(f"[!] BC parse error: {e}")

# Rank
programs.sort(key=lambda x: x["score"], reverse=True)

print(f"{'Platform':<12} {'Program':<40} {'Max Bounty':<12} {'Score':<8}")
print("="*72)
for p in programs[:20]:
    print(f"{p['platform']:<12} {p['name'][:39]:<40} ${p['max_bounty']:<9,} {p['score']:<8.0f}")

# Save
with open("bounty_targets/ranked_targets.json", "w") as f:
    json.dump(programs[:20], f, indent=2)
print("\n[+] Saved top 20 to bounty_targets/ranked_targets.json")
PYEOF
```

**What to do next:** Open `bounty_targets/ranked_targets.json`, pick the top 3-5 programs. For each, visit the program page, note the exact in-scope targets, and start recon (subdomain enumeration, technology fingerprinting). Track time: target selection should take ≤30 minutes total.

## Deliverable Format

When delivering a target list to a client, use this invoice-ready template:

```
╔══════════════════════════════════════════════════════════════╗
║              PRIORITIZED BOUNTY TARGET REPORT               ║
║                    [Client Name] — [Date]                   ║
╚══════════════════════════════════════════════════════════════╝

TOP 10 TARGETS (ranked by estimated payout/hour)

RANK │ PLATFORM  │ PROGRAM              │ MAX BOUNTY │ COMPETITION │ EST. PAYOUT/HR
─────┼───────────┼──────────────────────┼────────────┼─────────────┼───────────────
  1  │ HackerOne │ example-program      │   $5,000   │ Low (3/wk)  │   $250-500
  2  │ Bugcrowd  │ another-target       │   $3,500   │ Med (8/wk)  │   $150-300
  ...

TARGET PROFILES (detail for top 3)

1. example-program (HackerOne)
   URL: https://hackerone.com/example-program
   Max Bounty: $5,000  |  Min Bounty: $300
   Scope: *.example.com, api.example.com (API, Web)
   Out of Scope: *.staging.example.com, *.dev.example.com
   Tech Stack: React, Node.js, AWS
   Competition: Low (3 disclosed reports in last 30 days)
   Notes: Recently expanded scope — first-mover advantage

LABOR SUMMARY
  Research & ranking: 1.5 hours
  Total fee: $200 (Pro tier)

PAYMENT: USDC / Bank Transfer / PayPal (net 15)
```

## Workflow

1. **Scrape Platforms** — Pull programs from HackerOne, Bugcrowd, Intigriti, Synack
2. **Filter by Payout** — Keep only programs with max bounty ≥ $500 (minimum viable target)
3. **Assess Competition** — Check disclosure activity / recent submissions to gauge saturation
4. **Match to Skills** — Prefer targets matching your expertise (web, mobile, API, infra)
5. **Prioritize & Rank** — Score by: payout × (1 − competition_factor) × skill_match
6. **Output Report** — Deliver ranked list with payout estimates and scope summaries

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll wait until I'm a better hacker before submitting" | You improve by submitting, not by studying. Send your best finding now. |
| "That program has too many hunters already" | Most hunters only test the first 3 endpoints. Find the hidden ones. |
| "The payout is too low for my time" | A $500 finding in 2 hours is $250/hr. That beats most consulting rates. |
| "I need to find a critical, not a low-hanging medium" | Three mediums paying $500 each is $1,500. Ship what you find. |
| "I'll take a full day to do proper recon first" | 60-minute light recon is enough to find your first vulnerability. Start shallow. |
