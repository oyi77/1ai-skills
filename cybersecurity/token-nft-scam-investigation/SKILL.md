---
name: token-nft-scam-investigation
description: Investigate token and NFT scams including rug pulls, honeypot tokens, pump-and-dump schemes,
  wash trading, and NFT floor manipulation to identify fraudulent patterns and trace perpetrator wallets.
  Use when analyzing suspicious token launches, investigating NFT fraud, or detecting market manipulation.
domain: cybersecurity
subdomain: blockchain-security
tags:
- blockchain
- token
- nft
- scam
- investigation
- rug-pull
- honeypot
- wash-trading
- fraud
- money
version: '1.0'
---

# Token & NFT Scam Investigation

## Overview

Token and NFT scams — including rug pulls, honeypot tokens, pump-and-dump schemes, wash trading, and floor manipulation — account for the majority of blockchain fraud by victim count. Unlike protocol exploits that target code flaws, these scams target retail investors through deception and market manipulation. This skill covers analyzing token contracts for honeypot mechanisms, detecting wash trading patterns on NFT marketplaces, investigating rug pull setups (liquidity removal, mint权限, proxy upgrades), identifying pump-and-dump coordination, and tracing scam proceeds.

## When to Use

**Trigger phrases:**
- "token scam investigation"
- "nft scam investigation"
- "Analyze a rug pull"
- "Check if a token is a honeypot"
- "Detect wash trading in an NFT collection"

- When investigating a suspicious token launch for potential scam indicators
- When analyzing an NFT collection for wash trading or price manipulation
- When tracing rug pull or pump-and-dump proceeds
- When building automated scam detection for token/NFT due diligence
- When gathering evidence for a fraud complaint or bounty submission

## Prerequisites

- Python 3.8+ with web3.py, requests, pandas
- Ethereum RPC node access (or chain-specific node)
- Block explorer API (Etherscan, BscScan, etc.)
- Solidity understanding (for contract-level scam analysis)
- NFT marketplace API access (OpenSea, Blur, LooksRare) for trading data

## Core Workflow

```python
# Example: Check basic token contract scam indicators
from web3 import Web3

def check_token_indicators(w3: Web3, token_address: str) -> dict:
    """Check common honeypot and rug pull indicators."""
    erc20_abi = [
        {"inputs": [], "name": "name", "outputs": [{"type": "string"}], "stateMutability": "view", "type": "function"},
        {"inputs": [], "name": "symbol", "outputs": [{"type": "string"}], "stateMutability": "view", "type": "function"},
        {"inputs": [], "name": "decimals", "outputs": [{"type": "uint8"}], "stateMutability": "view", "type": "function"},
        {"inputs": [], "name": "totalSupply", "outputs": [{"type": "uint256"}], "stateMutability": "view", "type": "function"},
        {"inputs": [{"type": "address"}], "name": "balanceOf", "outputs": [{"type": "uint256"}], "stateMutability": "view", "type": "function"},
    ]
    contract = w3.eth.contract(address=token_address, abi=erc20_abi)
    result = {}
    try:
        result["name"] = contract.functions.name().call()
        result["symbol"] = contract.functions.symbol().call()
        result["decimals"] = contract.functions.decimals().call()
        result["total_supply"] = contract.functions.totalSupply().call()
        # Check top holders
        result["top_holder_pct"] = _check_top_holder_concentration(w3, token_address)
    except Exception as e:
        result["error"] = str(e)
    return result

def _check_top_holder_concentration(w3, token):
    """Check if top holder has suspiciously large supply."""
    # Simplified — real implementation fetches Transfer events to find holders
    return 0.0

def check_ownership(w3: Web3, token_address: str) -> dict:
    """Check if ownership has been renounced."""
    ownership_abi = [
        {
            "inputs": [],
            "name": "owner",
            "outputs": [{"type": "address"}],
            "stateMutability": "view",
            "type": "function",
        }
    ]
    try:
        contract = w3.eth.contract(address=token_address, abi=ownership_abi)
        owner = contract.functions.owner().call()
        return {"owner": owner, "renounced": owner == "0x0000000000000000000000000000000000000000"}
    except Exception:
        return {"owner": None, "renounced": None, "note": "No owner() function"}
```

### Step 1: Token Contract Analysis

Examine the token contract for scam indicators:
- **Honeypot detection** — can the token be bought but not sold? Check for blacklist functions, transfer fee manipulation, or balance restrictions
- **Ownership not renounced** — deployer can still mint, pause transfers, or blacklist addresses
- **Suspicious fee structure** — extremely high buy/sell taxes that benefit the deployer
- **Honeypot simulation** — simulate a buy and sell transaction to verify both succeed
- **Proxy/upgradeable pattern** — contract can be upgraded to malicious logic later
- **Mint function** — unlimited mint capability that dilutes holders
- **TOP10 holder concentration** — if 90%+ supply is in a few addresses, risk of dump

### Step 2: Liquidity Pool Investigation

Analyze the token's liquidity on DEXes:
- **Liquidity lock status** — is LP locked, and if so, for how long?
- **LP holder concentration** — who holds the LP tokens? Is it the deployer?
- **Initial liquidity amount** — was seeding adequate for the market cap?
- **Sniper activity** — was there bot-buying in the first block after launch?

### Step 3: NFT Wash Trading Detection

For NFT collections, detect market manipulation:
- **Same-wallet cycling** — NFT moving between same wallets repeatedly
- **Circular trading** — wallet A sells to B, B sells to C, C sells to A
- **Price laddering** — artificially inflating floor prices through self-deals
- **Volume farming** — generating fake volume to attract organic buyers
- **Cross-marketplace arbitrage manipulation** — wash trading across platforms

### Step 4: Social and On-Chain Correlation

Cross-reference on-chain data with off-chain signals:
- **Team doxxing status** — is the team known or anonymous?
- **Social media hygiene** — are there red flags on Twitter, Discord, Telegram?
- **Deployer wallet history** — has this wallet deployed other scam tokens?
- **Funding source** — where did the deployer get initial funds? Connected to other scams?

### Step 5: Scam Proceeds Tracing

Track where victim funds went:
- **Liquidity removal** — when LP was pulled and where the funds went
- **DEX dumping** — sell transactions by the deployer wallet
- **Bridge/CEX deposit** — funds moved to a bridge or centralized exchange for cash-out
- **Cross-chain transfer** — funds moved to another chain to obscure trail

## Expected Output

A scam investigation report containing: contract analysis results (honeypot check, ownership status, fee structure), liquidity analysis (LP lock status, holder concentration), trading pattern analysis (sniper activity, wash trading evidence), deployer wallet history and connections, and fund flow tracing if proceeds have been moved.

## When NOT to Use

- You need to trace stolen funds from a hack or exploit (use onchain-transaction-forensics skill)
- You need to analyze a DeFi protocol's smart contract vulnerability (use defi-incident-analysis skill)
- Task requires recovering lost funds or filing a police report (use proper legal channels)
- You are the project owner needing to prove your token is legitimate (use a different due diligence process)
- The investigation requires access to private sale or KYC data you don't have

## Red Flags

- Making public accusations based on incomplete on-chain analysis without social confirmation
- Confusing a buggy but legitimate token with a deliberate scam
- Assuming LP renouncement means safety — proxy contracts can still be upgraded
- Using only one data source for holder analysis — wallets can be split across many addresses

## Process

1. **Contract Review** — Analyze token/NFT contract for scam indicators (honeypot, ownership, fees, mint)
2. **Liquidity Assessment** — Check LP lock, holder concentration, and initial liquidity
3. **Trading Pattern Analysis** — Detect wash trading, sniping, and market manipulation
4. **Off-Chain Investigation** — Cross-reference deployer history, social signals, and funding sources
5. **Reporting** — Produce structured investigation report with evidence and confidence scores

## Verification

- Honeypot check verified by simulating both buy AND sell transactions (with actual gas estimation)
- LP lock status confirmed by reading the lock contract directly, not just a third-party claim
- Wash trading detection verified by checking actual wallet ownership on-chain, not just marketplace labels
- Deployer connections confirmed by tracing initial funding transaction back to the source
- Every claim in the report supported by a verifiable on-chain transaction or external link

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "The token has a verified contract, it's legit" | Verification only proves the source matches bytecode, not that the logic is honest. |
| "The team is doxxed, they wouldn't rug" | Doxxed teams have rugged too. Credentials don't guarantee integrity. |
| "LP is locked so it's safe" | Locked LP prevents liquidity removal but doesn't prevent minting, proxy upgrades, or blacklist abuse. |
| "Low market cap means less risk" | Low cap tokens are the most common rug pull targets. Market cap has no correlation with safety. |
