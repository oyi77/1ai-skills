---
name: wallet-address-intelligence
description: Profile and cluster blockchain wallet addresses to identify entity associations, assess risk levels,
  and build address reputation intelligence across multiple chains. Use when analyzing wallet behavior, clustering
  related addresses, assessing counterparty risk, or building address intelligence reports.
domain: cybersecurity
subdomain: blockchain-security
tags:
- blockchain
- wallet
- address
- intelligence
- clustering
- profiling
- risk
- investigation
- entity
- money
version: '1.0'
author: ''
---

# Wallet & Address Intelligence

## Overview

Wallet address intelligence is the practice of profiling blockchain addresses to identify the entities behind them, assess risk levels, and build behavioral profiles. Unlike simple balance checks, address intelligence combines on-chain transaction analysis, entity clustering heuristics, known-address databases, behavioral pattern matching, and cross-chain correlation. This skill covers building address profiles with transaction demographics, applying clustering algorithms (Cointracking, CommonInput, behavioral similarity), tagging addresses with entity attributions, assessing risk scores for compliance (AML/KYC), and producing comprehensive address intelligence reports.

## When to Use

**Trigger phrases:**
- "wallet address intelligence"
- "Profile a blockchain wallet"
- "Check if an address is risky"
- "Cluster related crypto wallets"
- "Build address reputation"

- When performing due diligence on a counterparty before a transaction
- When investigating suspicious addresses for compliance or AML purposes
- When building a wallet clustering system for forensic investigations
- When assessing the risk profile of an address interacting with your protocol
- When attributing addresses to known entities (exchanges, protocols, exploiters)

## Prerequisites

- Python 3.8+ with web3.py, requests, pandas, networkx
- Block explorer API keys (Etherscan, BscScan, etc.)
- Access to an address labeling dataset (Etherscan labels, tagged addresses from block explorers)
- Basic understanding of graph theory for clustering algorithms
- Optional: DeBank or similar API for multi-chain wallet views

## Core Workflow

```python
# Example: Build a basic address profile
import requests
from datetime import datetime

def build_address_profile(address: str, etherscan_key: str) -> dict:
    """Build a comprehensive profile for a single address."""
    profile = {"address": address, "tags": [], "risk_indicators": [], "activity": {}}

    # 1. Basic balance and transaction count
    balance = _fetch_balance(address, etherscan_key)
    tx_count = _fetch_tx_count(address, etherscan_key)

    profile["eth_balance"] = balance
    profile["total_txns"] = tx_count

    # 2. First and last activity
    txs = _fetch_tx_list(address, etherscan_key)
    if txs:
        profile["first_seen"] = datetime.utcfromtimestamp(int(txs[-1]["timeStamp"]))
        profile["last_active"] = datetime.utcfromtimestamp(int(txs[0]["timeStamp"]))

    # 3. Interaction diversity
    unique_interactors = set()
    for tx in txs:
        unique_interactors.add(tx["from"].lower())
        unique_interactors.add(tx["to"].lower())

    # 4. Known entity labels
    labels = _check_known_labels(address)
    if labels:
        profile["tags"].extend(labels)

    return profile

def _fetch_balance(address: str, api_key: str) -> float:
    """Fetch ETH balance from Etherscan."""
    params = {"module": "account", "action": "balance", "address": address, "apikey": api_key}
    resp = requests.get("https://api.etherscan.io/api", params=params)
    data = resp.json()
    if data.get("status") == "1":
        return int(data["result"]) / 1e18
    return 0.0

def _fetch_tx_count(address: str, api_key: str) -> int:
    """Fetch total transaction count."""
    params = {"module": "account", "action": "txlist", "address": address, "startblock": 0, "endblock": 99999999,
              "sort": "desc", "apikey": api_key}
    resp = requests.get("https://api.etherscan.io/api", params=params)
    data = resp.json()
    return len(data.get("result", []))
```

### Step 1: Build Address Profile

Collect the following dimensions for the target address:
- **Balance and transaction history** — current balance, total sent/received, total transaction count
- **Activity timeline** — first seen block, last active block, activity frequency, dormant periods
- **Interaction network** — which contracts and EOAs has this address interacted with?
- **Token holdings** — all ERC-20 and NFT balances, both current and historical
- **Gas spending** — total gas spent, average gas price preference (indicates sophistication)
- **Protocol usage** — which DeFi protocols, NFT marketplaces, or DEXes has this address used?

### Step 2: Entity Clustering

Group related addresses into entity clusters:
- **CommonInput clustering** — addresses that appear as inputs together in the same transaction (Bitcoin)
- **Funds flow clustering** — addresses that consolidate to or distribute from a common address
- **Behavioral similarity** — addresses with similar interaction patterns, timing, and protocol usage
- **CEX deposit/withdrawal linkage** — addresses that deposit to/withdraw from the same exchange account
- **Social graph linkage** — ENS names, social media profiles, and off-chain identity correlations

### Step 3: Risk Scoring

Assess the address across multiple risk dimensions:
- **Sanctions/Terrorism financing** — match against OFAC, EU, and UN sanctions lists
- **Mixer/Tumbler interaction** — has the address interacted with Tornado Cash, Wasabi, or similar?
- **Exploit/Hack involvement** — is the address connected to known exploit or hack transactions?
- **Scam/Phishing association** — has the address received funds from or sent to known scam addresses?
- **Darknet marketplace** — interaction with known darknet markets
- **Ransomware payments** — receipt of funds from known ransomware addresses
- **Liquidity risks** — is the address a large LP holder with potential to manipulate?

### Step 4: Entity Attribution

Attempt to attribute the address to a known entity:
- **Exchange deposit addresses** — addresses that match known exchange deposit patterns
- **Protocol deployer wallets** — wallets that deployed known smart contracts
- **MEV searcher/validator** — identifiable by MEV bundle submission patterns
- **Whale/investor** — large holders with characteristic accumulation patterns
- **Team/insider wallet** — wallets funded by project treasury or multi-sig
- **De-anonymization through off-chain data** — ENS, social media, GitHub, forum posts

### Step 5: Produce Intelligence Report

Generate a structured intelligence report:
- **Executive summary** — who is likely behind this address and what risk level do they represent
- **Profile card** — balance, age, transaction count, protocol usage summary
- **Cluster map** — related addresses in the entity's cluster with relationship descriptions
- **Risk assessment** — scored across each risk dimension with confidence levels
- **Transaction sample** — representative transactions showing typical behavior
- **Entity attribution** — best-guess entity name with confidence score and evidence

## Expected Output

A structured address intelligence report containing: profile card (balance, age, activity level), entity cluster visualization (GraphML or DOT format), multi-axis risk score with evidence for each dimension, entity attribution with confidence score, and a plain-text summary suitable for compliance or investigation use.

## When NOT to Use

- You need to trace stolen funds along a specific path (use onchain-transaction-forensics skill)
- You need to analyze a specific DeFi protocol hack (use defi-incident-analysis skill)
- You need to check if a token is a scam (use token-nft-scam-investigation skill)
- You need real-time transaction monitoring (use a blockchain analytics platform)
- The address is on a privacy-focused blockchain where clustering is infeasible

## Red Flags

- Claiming definitive entity attribution from incomplete clustering data
- Over-relying on a single clustering heuristic (CommonInput alone is not sufficient)
- Ignoring false positives in sanctions list matching (false positives are common with fuzzy matching)
- Drawing conclusions about an address without checking all chains it has transacted on
- Publishing or sharing address intelligence without proper data protection and authorization

## Process

1. **Data Gathering** — Collect on-chain data, transaction history, and interaction network for target address
2. **Profile Construction** — Build behavioral profile with activity patterns, protocol usage, and asset holdings
3. **Clustering** — Apply multiple clustering algorithms to discover related addresses
4. **Risk Assessment** — Score against risk dimensions using known databases and behavioral indicators
5. **Attribution** — Attempt entity attribution with confidence scoring
6. **Reporting** — Produce structured intelligence report with evidence for each claim

## Verification

- Every cluster connection verified by at least two independent heuristics (not just one)
- Entity attributions cross-checked against at least two independent data sources
- Risk scores manually reviewed for false positives before reporting
- Cluster visualizations inspected for obvious errors (mislinked addresses, missing connections)
- All claims supported by verifiable on-chain transaction hashes or external references

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "The address only has a few transactions, it's not important" | Small addresses can be test wallets, intermediaries, or deliberately kept clean for separation. |
| "The address has no known tags, it's clean" | Absence of tags means only that no one has identified it, not that it's benign. |
| "I can cluster with just one method" | Single-method clustering has high false positive/negative rates. Multi-method is essential. |
| "The address is associated with a mixer so it's criminal" | Mixer interaction may indicate privacy preference, not criminal activity. Context matters. |
