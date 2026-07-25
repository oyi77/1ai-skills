---
name: onchain-transaction-forensics
description: Trace and analyze blockchain transactions to investigate illicit fund flows, identify wallet clusters,
  and map transaction graphs across multiple blockchains. Use when investigating stolen funds, following money trails on-chain,
  analyzing suspicious addresses, or tracing cross-chain transactions.
domain: cybersecurity
subdomain: blockchain-security
tags:
- blockchain
- forensics
- onchain
- transactions
- wallet
- tracing
- investigation
- evm
- bitcoin
- money
version: '1.0'
author: ''
---

# On-Chain Transaction Forensics

## Overview

Blockchain transaction forensics involves tracing and analyzing cryptocurrency transactions to investigate illicit fund flows, identify wallet clusters, and map transaction graphs. Unlike traditional financial forensics, blockchain provides a public, immutable ledger where every transaction is permanently recorded. This skill covers collecting transaction data via RPC nodes and block explorers, building transaction flow graphs, applying clustering heuristics (Cointracking, peel chain analysis, address reuse), identifying mixing/tumbling services and cross-chain bridges, and producing investigator-ready trace reports with visual flow maps.

## When to Use

**Trigger phrases:**
- "onchain transaction forensics"
- "Trace stolen funds on the blockchain"
- "Follow the money on-chain"
- "Analyze suspicious wallet transactions"

- When investigating theft, rug pull, or hack incidents that require tracing stolen cryptocurrency
- When building evidence chains for law enforcement or bounty submissions
- When analyzing suspicious wallet activity for compliance or risk assessment
- When reconstructing the flow of funds through mixers, bridges, or exchanges

## Prerequisites

- Python 3.8+ with web3.py, requests
- Access to an Ethereum RPC node (Infura, Alchemy, or local node)
- Etherscan API key (or equivalent block explorer API for target chain)
- Basic understanding of blockchain transaction structure (inputs, outputs, logs)
- Graph visualization tool (Graphviz, NetworkX, or D3.js) for flow mapping

## Core Workflow

```python
# Example: Fetch and parse transaction receipts via Etherscan API
import requests

ETHERSCAN_API = "https://api.etherscan.io/api"

def get_normal_txs(address: str, api_key: str) -> list[dict]:
    """Get regular ETH transfers for an address."""
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": api_key
    }
    resp = requests.get(ETHERSCAN_API, params=params)
    return resp.json().get("result", [])

def get_internal_txs(address: str, api_key: str) -> list[dict]:
    """Get internal ETH transfers (via CALL opcodes)."""
    params = {
        "module": "account",
        "action": "txlistinternal",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": api_key
    }
    resp = requests.get(ETHERSCAN_API, params=params)
    return resp.json().get("result", [])

def get_erc20_transfers(address: str, api_key: str) -> list[dict]:
    """Get ERC-20 token transfers involving this address."""
    params = {
        "module": "account",
        "action": "tokentx",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": api_key
    }
    resp = requests.get(ETHERSCAN_API, params=params)
    return resp.json().get("result", [])
```

### Step 1: Gather Transaction Data

Collect all transaction history for the target address: normal ETH transfers, internal transactions (CALL opcodes), and ERC-20/ERC-721 token transfers. For non-EVM chains, use the appropriate block explorer API (Blockchair for Bitcoin, Trongrid for TRON, Solscan for Solana).

### Step 2: Build Transaction Flow Graph

Construct a directed graph from the transaction data where edges represent value transfers between addresses. Apply heuristics to identify:
- **Peel chains** — gradual fund distribution through many addresses to obscure the trail
- **Consolidation patterns** — multiple addresses sending to a single address
- **Exchange deposits** — identifiable by known exchange wallet patterns and thresholds
- **Bridge interactions** — cross-chain transfers through bridge contract addresses

### Step 3: Apply Clustering Heuristics

Group related addresses into clusters using:
- **Address reuse** — multiple addresses spending from the same input (Bitcoin UTXO clustering)
- **Common spending authority** — addresses that appear together as inputs in the same transaction
- **Behavioral similarity** — addresses with matching interaction patterns with known services
- **CEX deposit address discovery** — finding exchange deposit addresses via transaction patterns

### Step 4: Trace Through Layer-2 and Cross-Chain

Follow funds through bridges, DEX swaps, and cross-chain messaging protocols. Track the original source chain through to the destination chain, noting conversion rates, wrapped token addresses, and bridge contract interactions.

### Step 5: Produce Trace Report

Generate a structured report with:
- Flow diagram showing all significant hops (address → address, with amounts and timestamps)
- Cluster identifications and entity tags (exchange, mixer, bridge, DeFi protocol)
- Estimated USD values at time of each transaction
- Confidence scores for each hop and attribution
- Timeline reconstruction of the entire fund movement

## Expected Output

A forensic trace report containing: transaction flow graph (visual + DOT/GraphML format), wallet cluster table with entity attributions, timeline of fund movements, and a list of endpoints (addresses where funds cannot be further traced — mixers, exchange deposits, or bridges to unmonitored chains).

## When NOT to Use

- You need real-time monitoring of transactions (use a blockchain monitoring service)
- Task requires recovering private keys or seed phrases (use wallet recovery tools)
- You need to analyze smart contract logic, not transaction flow (use smart contract analysis skills)
- The blockchain is privacy-focused (Monero, Zcash) where on-chain analysis is limited
- You don't have access to a reliable RPC node or block explorer API

## Red Flags

- Attempting to deanonymize addresses without proper authorization or legal basis
- Drawing conclusions from incomplete data (missing internal transactions or token transfers)
- Over-relying on a single block explorer that may have incomplete indexing
- Assuming a wallet belongs to an entity without cross-referencing multiple data sources

## Process

1. **Data Collection** — Gather all transaction data for target addresses from block explorers and RPC nodes
2. **Flow Mapping** — Build directed transaction graph and apply clustering heuristics
3. **Entity Attribution** — Cross-reference addresses against known entity databases and behavioral patterns
4. **Cross-Chain Tracking** — Follow funds through bridges, DEXes, and wrapped assets
5. **Reporting** — Produce structured trace report with flow diagrams, confidence scores, and endpoint identification

## Verification

- Every trace hop verified against the source block explorer (not just API data)
- Transaction hashes cross-referenced on at least two independent explorers
- Entity attributions confirmed by multiple data points, not single-source assumptions
- Graph visualization matches the raw transaction data (no skipped or double-counted hops)
- Report includes raw data exports so findings can be independently verified

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Blockchain is anonymous so tracing is impossible" | Blockchain is pseudonymous, not anonymous. Every transaction is permanently recorded and analyzable. |
| "Mixers make tracing impossible" | Mixers complicate but don't prevent tracing. Timing analysis and amount patterns often deanonymize. |
| "The amount is too small to trace" | Small amounts are often test transactions. Follow the same address for larger patterns. |
| "Cross-chain transactions break the trail" | Bridge contracts and wrapped assets leave permanent on-chain evidence on both chains. |
