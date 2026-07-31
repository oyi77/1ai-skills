---
name: onchain-transaction-forensics
description: Trace and analyze blockchain transactions to investigate illicit fund flows, identify wallet clusters,
  and map transaction graphs across multiple blockchains. Use when investigating stolen funds, following money trails on-chain,
  analyzing suspicious addresses, or tracing cross-chain transactions.
domain: cybersecurity
license: Apache-2.0
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
author: oyi77
---

# On-Chain Transaction Forensics

## Overview

Blockchain transaction forensics involves tracing and analyzing cryptocurrency transactions to investigate illicit fund flows, identify wallet clusters, and map transaction graphs across multiple chains. Unlike traditional financial forensics, blockchain provides a public, immutable ledger where every transaction is permanently recorded. Every hop a stolen fund takes — from initial theft through mixers, bridges, DEX swaps, and exchange deposits — leaves indelible evidence.

This skill covers collecting transaction data via block explorer APIs and RPC nodes, building directed transaction flow graphs with NetworkX, applying clustering heuristics (peel chain detection, consolidation patterns, CoJoin clustering for UTXO chains, address reuse), identifying mixing services and cross-chain bridges by scanning event logs and known contract registries, and producing investigator-ready trace reports with Sankey flow visualization. The techniques here apply to EVM chains (Ethereum, BNB Chain, Polygon, Arbitrum, Optimism, Avalanche), Bitcoin-family UTXO chains, Solana, and TRON.

## When to Use

**Trigger phrases:**
- "onchain transaction forensics"
- "Trace stolen funds on the blockchain"
- "Follow the money on-chain"
- "Analyze suspicious wallet transactions"
- "Where did the stolen crypto go"
- "Fund flow analysis"
- "Blockchain investigation"

- When investigating theft, rug pull, or hack incidents that require tracing stolen cryptocurrency
- When building evidence chains for law enforcement or bounty submissions (Arkham, Lazarus Bounty)
- When analyzing suspicious wallet activity for compliance or risk assessment
- When reconstructing the flow of funds through mixers, bridges, or exchanges
- When preparing transaction trace reports as a paid forensic service
- When mapping the flow of illicit funds from a known attacker address
- When performing due diligence on a large transaction or wallet before a business deal

## When NOT to Use

- You need real-time monitoring of transactions (use a blockchain monitoring service or webhook provider)
- Task requires recovering private keys or seed phrases (use wallet recovery tools)
- You need to analyze smart contract logic, not transaction flow (use smart contract analysis skills)
- The blockchain is privacy-focused (Monero, Zcash) where on-chain analysis is limited to public data
- You don't have access to a reliable RPC node or block explorer API
- The investigation requires off-chain data (social media, KYC records, exchange logs) that you cannot correlate
- You are analyzing a DeFi protocol for smart contract vulnerabilities rather than following fund movements

## Prerequisites

- Python 3.8+ with web3.py, requests, pandas, networkx, numpy, plotly
- Access to at least one Ethereum RPC node (Infura, Alchemy, or local node)
- Etherscan API key (or equivalent block explorer API key for target chains)
- Basic understanding of blockchain transaction structure (inputs, outputs, logs, events)
- Graph visualization tools (Graphviz `dot` for DOT rendering, or plotly for HTML output)
- For UTXO chains: understanding of inputs/outputs, addresses vs public keys, change addresses
- At least 2 GB RAM for processing large transaction datasets (100k+ txs)
- Basic knowledge of DeFi protocols, bridge contracts, mixer mechanics

## Multi-Chain Block Explorer Reference

| Chain | Block Explorer | API Base URL | API Key Required | Notes |
|---|---|---|---|---|
| Ethereum | Etherscan | `https://api.etherscan.io/api` | Yes | Most comprehensive EVM explorer |
| Ethereum (batch) | Etherscan V2 | `https://api.etherscan.io/v2/api` | Yes | Supports `chainid` param |
| BNB Chain | BscScan | `https://api.bscscan.com/api` | Yes | Same API shape as Etherscan |
| Polygon | Polygonscan | `https://api.polygonscan.com/api` | Yes | Same API shape as Etherscan |
| Arbitrum | Arbiscan | `https://api.arbiscan.io/api` | Yes | Same API shape as Etherscan |
| Optimism | Optimistic Etherscan | `https://api-optimistic.etherscan.io/api` | Yes | Same API shape as Etherscan |
| Avalanche C-Chain | Snowtrace | `https://api.snowtrace.io/api` | Yes | Same API shape as Etherscan |
| Base | Basescan | `https://api.basescan.org/api` | Yes | Same API shape as Etherscan |
| TRON | Trongrid | `https://api.trongrid.io` | Yes (optional) | REST API, different structure |
| Solana | Solscan | `https://api.solscan.io` | Yes | Different API from EVM explorers |
| Bitcoin | Blockchair | `https://api.blockchair.com/bitcoin` | Yes (free tier) | UTXO-specific endpoints |
| Bitcoin | mempool.space | `https://mempool.space/api` | No | Public, rate-limited |
| Bitcoin | Blockchain.com | `https://blockchain.info` | No | Legacy API, rate-limited |
| Multi-chain | Covalent | `https://api.covalenthq.com/v1` | Yes | Unified API across 100+ chains |
| Multi-chain | BitQuery | `https://graphql.bitquery.io` | Yes | GraphQL, supports many chains |

### Etherscan-like API Wrapper

The following chains use an identical API schema to Etherscan. A single helper class handles all of them:

```python
import requests
from typing import Optional

EXPLORERS = {
    "ethereum": "https://api.etherscan.io/api",
    "bsc": "https://api.bscscan.com/api",
    "polygon": "https://api.polygonscan.com/api",
    "arbitrum": "https://api.arbiscan.io/api",
    "optimism": "https://api-optimistic.etherscan.io/api",
    "avalanche": "https://api.snowtrace.io/api",
    "base": "https://api.basescan.org/api",
}

class ExplorerClient:
    """Unified client for Etherscan-family block explorers."""

    def __init__(self, api_key: str, chain: str = "ethereum"):
        self.api_key = api_key
        base = EXPLORERS.get(chain)
        if not base:
            raise ValueError(f"Unsupported chain: {chain}")
        self.base = base

    def _call(self, params: dict) -> list:
        params["apikey"] = self.api_key
        resp = requests.get(self.base, params=params, timeout=30)
        data = resp.json()
        if data.get("status") != "1":
            return []
        return data.get("result", [])

    def normal_txs(self, address: str) -> list[dict]:
        return self._call({
            "module": "account", "action": "txlist",
            "address": address, "startblock": 0,
            "endblock": 99999999, "sort": "asc"
        })

    def internal_txs(self, address: str) -> list[dict]:
        return self._call({
            "module": "account", "action": "txlistinternal",
            "address": address, "startblock": 0,
            "endblock": 99999999, "sort": "asc"
        })

    def erc20_transfers(self, address: str) -> list[dict]:
        return self._call({
            "module": "account", "action": "tokentx",
            "address": address, "startblock": 0,
            "endblock": 99999999, "sort": "asc"
        })

    def erc721_transfers(self, address: str) -> list[dict]:
        return self._call({
            "module": "account", "action": "tokennfttx",
            "address": address, "startblock": 0,
            "endblock": 99999999, "sort": "asc"
        })

    def get_logs(self, address: str, from_block: int = 0,
                 to_block: int = 99999999, topic0: Optional[str] = None) -> list[dict]:
        params = {
            "module": "logs", "action": "getLogs",
            "address": address, "fromBlock": from_block,
            "toBlock": to_block,
        }
        if topic0:
            params["topic0"] = topic0
        return self._call(params)
```

## Core Workflow: Data Collection

### Etherscan V2 Batch API

The Etherscan V2 API supports multi-chain queries via a single endpoint by passing `chainid`. This reduces complexity when tracing funds across chains:

```python
def get_txs_v2(address: str, api_key: str, chain_id: int = 1) -> list[dict]:
    """Fetch normal transactions via Etherscan V2 batch API."""
    url = f"https://api.etherscan.io/v2/api"
    params = {
        "chainid": chain_id,
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": api_key
    }
    resp = requests.get(url, params=params, timeout=30)
    return resp.json().get("result", [])


def get_internal_txs_v2(address: str, api_key: str, chain_id: int = 1) -> list[dict]:
    """Fetch internal transactions via Etherscan V2 batch API."""
    url = "https://api.etherscan.io/v2/api"
    params = {
        "chainid": chain_id,
        "module": "account",
        "action": "txlistinternal",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": api_key
    }
    resp = requests.get(url, params=params, timeout=30)
    return resp.json().get("result", [])


def get_erc20_transfers_v2(address: str, api_key: str, chain_id: int = 1) -> list[dict]:
    """Fetch ERC-20 token transfers via Etherscan V2 batch API."""
    url = "https://api.etherscan.io/v2/api"
    params = {
        "chainid": chain_id,
        "module": "account",
        "action": "tokentx",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": api_key
    }
    resp = requests.get(url, params=params, timeout=30)
    return resp.json().get("result", [])


def get_token_balances_v2(address: str, api_key: str, chain_id: int = 1) -> list[dict]:
    """Fetch ERC-20 token balances via Etherscan V2."""
    url = "https://api.etherscan.io/v2/api"
    params = {
        "chainid": chain_id,
        "module": "account",
        "action": "tokenlist",
        "address": address,
        "apikey": api_key
    }
    resp = requests.get(url, params=params, timeout=30)
    return resp.json().get("result", [])
```

**Chain IDs reference:**

| Chain | chainid |
|---|---|
| Ethereum Mainnet | 1 |
| BNB Chain | 56 |
| Polygon | 137 |
| Arbitrum One | 42161 |
| Optimism | 10 |
| Avalanche C-Chain | 43114 |
| Base | 8453 |
| Linea | 59144 |
| Scroll | 534352 |

### Bitcoin Transaction Fetcher (mempool.space)

```python
def get_btc_address_txs(address: str) -> list[dict]:
    """Fetch Bitcoin transaction history via mempool.space (no API key needed)."""
    url = f"https://mempool.space/api/address/{address}/txs"
    resp = requests.get(url, timeout=30)
    return resp.json()


def get_btc_tx_details(txid: str) -> dict:
    """Fetch full Bitcoin transaction details."""
    url = f"https://mempool.space/api/tx/{txid}"
    resp = requests.get(url, timeout=30)
    return resp.json()
```

### TRON Transaction Fetcher

```python
def get_tron_txs(address: str, api_key: str = "") -> list[dict]:
    """Fetch TRON transactions via Trongrid."""
    headers = {"TRON-PRO-API-KEY": api_key} if api_key else {}
    url = f"https://api.trongrid.io/v1/accounts/{address}/transactions"
    resp = requests.get(url, headers=headers, timeout=30)
    return resp.json().get("data", [])
```

## Step-by-Step Methodology

### Step 1: Collect All Transactions for Target Addresses

Start with the primary address from the incident — the theft wallet, the hacker's known address from a Rug Pull, or the suspicious deposit address.

```python
def collect_all_txs(address: str, api_key: str, chain_id: int = 1) -> dict:
    """Collect normal, internal, and ERC-20 tx history for one address."""
    return {
        "normal": get_txs_v2(address, api_key, chain_id),
        "internal": get_internal_txs_v2(address, api_key, chain_id),
        "erc20": get_erc20_transfers_v2(address, api_key, chain_id),
    }
```

- **Normal TXs**: Standard ETH/BNB/MATIC transfers where `from` and `to` are directly visible
- **Internal TXs**: Transfers triggered by contract CALL opcodes — these are NOT visible in normal tx lists but move ETH. Critical for tracing through DEX swaps, DeFi interactions, and bridge deposits
- **ERC-20 transfers**: Token movements (`transfer` events). The most common value transfer mechanism in DeFi hacks
- **ERC-721 / ERC-1155**: NFT transfers. Relevant for NFT theft and phishing investigations

**Pagination**: Etherscan API returns up to 10,000 rows per call. For addresses with more transactions, pass the `page` parameter:

```python
def collect_all_txs_paginated(address: str, api_key: str, chain: str = "ethereum",
                               max_pages: int = 10) -> list[dict]:
    """Paginate through large transaction histories."""
    client = ExplorerClient(api_key, chain)
    all_txs = []
    for page in range(1, max_pages + 1):
        params = {
            "module": "account", "action": "txlist",
            "address": address, "startblock": 0,
            "endblock": 99999999, "sort": "asc",
            "page": page, "offset": 10000
        }
        txs = client._call(params)
        if not txs:
            break
        all_txs.extend(txs)
        if len(txs) < 10000:
            break
    return all_txs
```

### Step 2: Parse and Normalize Transaction Data

Parse the raw API responses into a uniform format suitable for graph construction:

```python
import pandas as pd

def normalize_txs(raw_txs: list[dict], tx_type: str = "normal") -> pd.DataFrame:
    """Convert raw Etherscan API results to a normalized DataFrame."""
    rows = []
    for tx in raw_txs:
        row = {
            "hash": tx.get("hash"),
            "block": int(tx.get("blockNumber", 0)),
            "timestamp": int(tx.get("timeStamp", 0)),
            "from": tx.get("from", "").lower(),
            "to": tx.get("to", "").lower(),
            "value_wei": int(tx.get("value", 0)),
            "value_eth": int(tx.get("value", 0)) / 1e18,
            "gas": int(tx.get("gas", 0)),
            "gas_price": int(tx.get("gasPrice", 0)),
            "input": tx.get("input", ""),
            "is_error": tx.get("isError", "0") == "1",
            "tx_type": tx_type,
        }
        if tx_type == "erc20":
            row["token_symbol"] = tx.get("tokenSymbol", "")
            row["token_name"] = tx.get("tokenName", "")
            row["token_decimal"] = int(tx.get("tokenDecimal", 18))
            row["value_token"] = int(tx.get("value", 0)) / (10 ** int(tx.get("tokenDecimal", 18)))
        rows.append(row)
    return pd.DataFrame(rows)


def normalize_btc_txs(raw_txs: list[dict]) -> pd.DataFrame:
    """Normalize Bitcoin mempool.space transactions."""
    rows = []
    for tx in raw_txs:
        txid = tx.get("txid", "")
        for vin in tx.get("vin", []):
            rows.append({
                "hash": txid,
                "from": vin.get("prevout", {}).get("scriptpubkey_address", ""),
                "to": "",
                "value_btc": vin.get("prevout", {}).get("value", 0) / 1e8,
                "type": "input",
            })
        for vout in tx.get("vout", []):
            rows.append({
                "hash": txid,
                "from": "",
                "to": vout.get("scriptpubkey_address", ""),
                "value_btc": vout.get("value", 0) / 1e8,
                "type": "output",
            })
    return pd.DataFrame(rows)
```

### Step 3: Build a Directed Transaction Graph

Construct a NetworkX directed graph from the normalized transaction data. Each node is an address, each directed edge is a transaction with amount, hash, and timestamp as edge attributes.

```python
import networkx as nx
from typing import Optional

def build_tx_graph(df: pd.DataFrame) -> nx.DiGraph:
    """Build a directed transaction graph from normalized transaction data.

    Edges: from → to, attributes include value_eth, hash, timestamp, token_symbol.
    Self-loops (from == to) are excluded.
    """
    G = nx.DiGraph()
    for _, row in df.iterrows():
        src = str(row.get("from", "")).lower()
        dst = str(row.get("to", "")).lower()
        if not src or not dst or src == dst:
            continue
        val = row.get("value_eth", 0) or row.get("value_token", 0) or 0
        G.add_edge(src, dst, **{
            "hash": row.get("hash", ""),
            "value": float(val),
            "timestamp": int(row.get("timestamp", 0)),
            "token": row.get("token_symbol", "ETH"),
        })
    return G


def graph_summary(G: nx.DiGraph) -> dict:
    """Return summary statistics for a transaction graph."""
    return {
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "total_volume": sum(d["value"] for _, _, d in G.edges(data=True)),
        "unique_sources": sum(1 for n, d in G.in_degree() if d == 0),
        "unique_sinks": sum(1 for n, d in G.out_degree() if d == 0),
        "density": nx.density(G),
    }


def filter_by_value(G: nx.DiGraph, min_value: float = 0.01) -> nx.DiGraph:
    """Return a subgraph containing only edges above a minimum value threshold."""
    edges_to_keep = [(u, v, d) for u, v, d in G.edges(data=True)
                     if d.get("value", 0) >= min_value]
    H = nx.DiGraph()
    H.add_edges_from(edges_to_keep)
    return H
```

### Step 4: Export Graph to DOT and GraphML

Generate visualization-ready graph formats for use with Graphviz and analysis tools:

```python
def export_dot(G: nx.DiGraph, path: str = "tx_graph.dot") -> str:
    """Export the transaction graph as a DOT file for Graphviz rendering."""
    # Relabel nodes to quoted strings for DOT compatibility
    H = nx.DiGraph()
    for u, v, d in G.edges(data=True):
        label = f"{d.get('value', 0):.4f} {d.get('token', 'ETH')}"
        H.add_edge(f'"{u[:10]}…"', f'"{v[:10]}…"', label=label)
    nx.nx_pydot.write_dot(H, path)
    return path


def export_graphml(G: nx.DiGraph, path: str = "tx_graph.graphml") -> str:
    """Export the transaction graph as GraphML for Gephi or yEd."""
    nx.write_graphml(G, path)
    return path
```

### Step 5: Compute Graph Centrality and Find Key Nodes

Identify the most important addresses in the flow — the sink where funds concentrate, the original source, and intermediary hubs:

```python
def find_source_nodes(G: nx.DiGraph) -> list[str]:
    """Return nodes with zero in-degree (original sources of funds)."""
    return [n for n, d in G.in_degree() if d == 0]


def find_sink_nodes(G: nx.DiGraph) -> list[str]:
    """Return nodes with zero out-degree (endpoints — mixers, exchanges, bridges)."""
    return [n for n, d in G.out_degree() if d == 0]


def rank_by_centrality(G: nx.DiGraph, top_n: int = 10) -> pd.DataFrame:
    """Rank addresses by weighted betweenness centrality.

    Higher centrality means the address sits on more fund flow paths.
    """
    if G.number_of_nodes() < 2:
        return pd.DataFrame()
    # Use edge weight (value) to weight paths
    weight_attr = "value"
    try:
        centrality = nx.betweenness_centrality(G, weight=weight_attr)
    except Exception:
        centrality = nx.betweenness_centrality(G)
    ranked = sorted(centrality.items(), key=lambda x: -x[1])
    return pd.DataFrame(ranked[:top_n], columns=["address", "centrality"])


def find_top_volume_hubs(G: nx.DiGraph, top_n: int = 10) -> pd.DataFrame:
    """Find addresses with the highest total transaction volume (in + out)."""
    volume = {}
    for u, v, d in G.edges(data=True):
        val = d.get("value", 0)
        volume[u] = volume.get(u, 0) + val
        volume[v] = volume.get(v, 0) + val
    ranked = sorted(volume.items(), key=lambda x: -x[1])
    return pd.DataFrame(ranked[:top_n], columns=["address", "total_value"])
```

## Peel Chain Detection Algorithm

A peel chain is a money-laundering pattern where a large amount of cryptocurrency is split into gradually smaller amounts through a chain of addresses, obscuring the trail. Each address in the chain typically passes most of the funds forward while peeling off a small amount.

```python
def detect_peel_chains(G: nx.DiGraph, max_path_length: int = 20,
                       min_hops: int = 3, value_decay_threshold: float = 0.95) -> list[dict]:
    """Detect peel chain patterns in a transaction graph.

    A peel chain is a path where each hop passes most of the value forward
    (value_decay_threshold controls how much value must be passed), with
    small amounts peeled off along the way. Returns list of detected chains.
    """
    chains = []
    sources = find_source_nodes(G)

    for src in sources:
        visited = set()
        path = []
        current = src
        while current and len(path) < max_path_length:
            visited.add(current)
            out_edges = list(G.out_edges(current, data=True))
            if not out_edges:
                break
            # Sort outgoing edges by value descending
            out_edges.sort(key=lambda e: e[2].get("value", 0), reverse=True)
            best = out_edges[0]
            next_addr = best[1]
            val = best[2].get("value", 0)

            # Check: does this edge pass most of the known incoming value?
            in_edges = list(G.in_edges(current, data=True))
            total_in = sum(e[2].get("value", 0) for e in in_edges)

            if total_in > 0 and val / total_in < (1 - value_decay_threshold):
                # This hop peeled off too much — likely a consolidation, not a peel chain
                pass

            path.append({
                "from": current,
                "to": next_addr,
                "value": val,
                "hash": best[2].get("hash", ""),
            })

            if next_addr in visited:
                break
            current = next_addr

        if len(path) >= min_hops:
            chains.append({
                "start": src,
                "end": current,
                "hops": len(path),
                "total_volume": sum(h["value"] for h in path),
                "path": path,
            })

    return chains


def detect_peel_chain_heuristic_simple(address: str, txs: list[dict],
                                       threshold_ratio: float = 0.8) -> list[dict]:
    """Detect peel chains using a simplified heuristic on raw transaction data.

    A peel chain address sends most of its incoming value to a single output,
    suggesting gradual fund distribution. This works on individual address analysis
    without needing a full graph.
    """
    outgoing = {}
    for tx in txs:
        frm = tx.get("from", "").lower()
        to = tx.get("to", "").lower()
        val = int(tx.get("value", 0))
        if frm == address:
            outgoing[to] = outgoing.get(to, 0) + val

    if not outgoing:
        return []

    total_out = sum(outgoing.values())
    chains = []
    for dst, val in sorted(outgoing.items(), key=lambda x: -x[1]):
        ratio = val / total_out if total_out > 0 else 0
        if ratio >= threshold_ratio:
            chains.append({
                "from": address,
                "to": dst,
                "value": val,
                "ratio": round(ratio, 4),
                "pattern": "peel_chain_hop",
            })
    return chains
```

## Consolidation Pattern Detector

Consolidation is the opposite of a peel chain — multiple addresses send funds to a single address. This is typical before an exchange deposit or when a hacker collects funds spread across many wallets.

```python
def detect_consolidation(G: nx.DiGraph, min_sources: int = 3,
                         time_window_hours: int = 24) -> list[dict]:
    """Detect consolidation patterns in the transaction graph.

    A consolidation is a node with N incoming edges from distinct addresses
    within a time window. This is a classic exchange deposit / fund collection pattern.
    """
    consolidations = []
    for node in G.nodes():
        in_edges = list(G.in_edges(node, data=True))
        if len(in_edges) < min_sources:
            continue

        unique_sources = set(e[0] for e in in_edges)
        if len(unique_sources) < min_sources:
            continue

        # Check time window
        timestamps = [e[2].get("timestamp", 0) for e in in_edges]
        timestamps = [t for t in timestamps if t > 0]
        if timestamps:
            span_hours = (max(timestamps) - min(timestamps)) / 3600
            if span_hours > time_window_hours:
                continue

        total_value = sum(e[2].get("value", 0) for e in in_edges)
        consolidations.append({
            "sink": node,
            "sources": list(unique_sources),
            "num_sources": len(unique_sources),
            "total_value": total_value,
            "time_window_hours": round(span_hours, 2) if timestamps else 0,
            "tx_hashes": [e[2].get("hash", "") for e in in_edges],
        })

    return sorted(consolidations, key=lambda c: -c["num_sources"])


def detect_consolidation_simple(txs: list[dict], min_sources: int = 5) -> list[dict]:
    """Detect consolidation by checking which addresses receive from many distinct senders.

    Works on raw transaction data without a full graph.
    """
    from collections import Counter
    receivers = Counter()
    receiver_txs = {}
    for tx in txs:
        to = tx.get("to", "").lower()
        frm = tx.get("from", "").lower()
        if to and frm:
            receivers[to] += 1
            if to not in receiver_txs:
                receiver_txs[to] = []
            receiver_txs[to].append(tx)

    consolidations = []
    for addr, count in receivers.most_common():
        if count >= min_sources:
            total_val = sum(int(tx.get("value", 0)) for tx in receiver_txs[addr])
            consolidations.append({
                "address": addr,
                "incoming_count": count,
                "total_value": total_val,
                "source_addresses": list(set(
                    tx.get("from", "").lower() for tx in receiver_txs[addr]
                )),
            })
    return consolidations
```

## Mixer Identification

### Known Mixer/Sanitizer Contract Addresses

| Service | Chain | Address | Type | Notes |
|---|---|---|---|---|
| Tornado Cash | Ethereum | `0x12d66f87a04a9e220743712ce6d9bb1b5616b8fc` | ETH mixer | 0.1 ETH pool |
| Tornado Cash | Ethereum | `0x47ce0c6ed5b0ce3d3a51fdb1c52dc66a7c3c2936` | ETH mixer | 1 ETH pool |
| Tornado Cash | Ethereum | `0x910cbd523d972eb0a6f4cae4618ad62622b39dbf` | ETH mixer | 10 ETH pool |
| Tornado Cash | Ethereum | `0xa160cdab2250da5b3f80029b6b82e1d5d0c30efb` | ETH mixer | 100 ETH pool |
| Tornado Cash | BSC | `0x1e34a77868e19a6647b1f2f47b51ed72dede95dd` | BNB mixer | 100 BNB pool |
| Tornado Cash | Polygon | `0x47ce0c6ed5b0ce3d3a51fdb1c52dc66a7c3c2936` | MATIC mixer | 1000 MATIC pool |
| Sinbad | Ethereum | `0x1e31cb9b6b69a7df3225220a0ef1f0a76586d5a3` | ETH mixer | |
| Sinbad | Ethereum | `0x8589427373d6d84e98730d7795d8f6f8731fda16` | ETH mixer | |
| Wasabi Wallet | Bitcoin | `bc1q…` (varies) | BTC CoinJoin | Uses PayNym, no fixed address |
| Samourai Whirlpool | Bitcoin | (Coordinator) | BTC CoinJoin | No fixed deposit address |
| ChainFlip | Ethereum | `0x60fB0B27447480E3304bB7b2660e9C081D3775fc` | Cross-chain mixer | |
| eXch | Ethereum | (varies) | Swap-based mixer | Swaps and splits |
| FixedFloat | Multi | (varies) | Swap-based mixer | No-KYC exchange used for obfuscation |

### Mixer Deposit Detection Heuristics

```python
# Known mixer contract addresses (Ethereum mainnet)
MIXER_ADDRESSES = {
    # Tornado Cash deposit addresses (by pool size)
    "0x12d66f87a04a9e220743712ce6d9bb1b5616b8fc": "tornado_0.1_eth",
    "0x47ce0c6ed5b0ce3d3a51fdb1c52dc66a7c3c2936": "tornado_1_eth",
    "0x910cbd523d972eb0a6f4cae4618ad62622b39dbf": "tornado_10_eth",
    "0xa160cdab2250da5b3f80029b6b82e1d5d0c30efb": "tornado_100_eth",
    # Sinbad
    "0x1e31cb9b6b69a7df3225220a0ef1f0a76586d5a3": "sinbad_1",
    "0x8589427373d6d84e98730d7795d8f6f8731fda16": "sinbad_2",
}


def tag_mixer_interactions(df: pd.DataFrame) -> pd.DataFrame:
    """Tag transactions involving known mixer addresses."""
    df_lower = df.copy()
    df_lower["to"] = df_lower["to"].str.lower()
    df_lower["from"] = df_lower["from"].str.lower()
    df_lower["mixer"] = "unknown"
    for addr, name in MIXER_ADDRESSES.items():
        mask = (df_lower["to"] == addr) | (df_lower["from"] == addr)
        df_lower.loc[mask, "mixer"] = name
    return df_lower


def detect_mixer_deposit_by_amount(address: str, txs: list[dict],
                                   known_amounts: list[float] = None) -> bool:
    """Detect potential mixer deposits by checking for exact-amount patterns.

    Mixers use fixed deposit amounts (e.g., Tornado Cash pools).
    If an address sends an exact pool amount to a contract, it's likely a mixer deposit.
    """
    if known_amounts is None:
        known_amounts = [0.1, 1.0, 10.0, 100.0]  # Tornado Cash standard pool amounts

    for tx in txs:
        frm = tx.get("from", "").lower()
        val_eth = int(tx.get("value", 0)) / 1e18
        if frm == address.lower() and val_eth in known_amounts:
            # Verify the recipient has contract code (mixer contract, not EOA)
            return True
    return False


def detect_mixer_timing_anomaly(txs: list[dict], time_window_minutes: int = 30) -> list[dict]:
    """Detect mixer deposit patterns by timing.

    Mixer deposits often cluster in tight time windows.
    Multiple deposits to different addresses from the same source within a short window
    is a strong mixer indicator.
    """
    from collections import defaultdict
    windows = defaultdict(list)

    for tx in txs:
        ts = int(tx.get("timeStamp", 0))
        to = tx.get("to", "").lower()
        if ts:
            bucket_key = ts // (time_window_minutes * 60)  # bucket by time window
            windows[bucket_key].append(tx)

    suspicious = []
    for bucket, group in windows.items():
        unique_recipients = set(t.get("to", "").lower() for t in group)
        if len(unique_recipients) >= 3:
            total_val = sum(int(t.get("value", 0)) for t in group) / 1e18
            suspicious.append({
                "time_bucket": bucket,
                "num_txs": len(group),
                "unique_recipients": len(unique_recipients),
                "total_value_eth": total_val,
                "txs": [t.get("hash", "") for t in group[:10]],
            })

    return suspicious
```

## Cross-Chain Bridge Tracing

Bridges are the most common obfuscation technique post-hack. The attacker deposits on Chain A and withdraws on Chain B, often swapping the asset type.

### Known Bridge Contract Addresses

| Bridge | Chain | Contract Address | Event Signature |
|---|---|---|---|
| LayerZero Endpoint | Ethereum | `0x66A71Dcef29A0fFBDBE3c6a460a3B5BC225Cd675` | `MessagePayload` |
| Stargate Router | Ethereum | `0x8731d54E9D02c286767d56ac03e8037C07e01e98` | `Swap` |
| Stargate Router | Arbitrum | `0x53Bf833A5d6c4ddA888F69c22C88C9f356a41614` | `Swap` |
| Wormhole Core | Ethereum | `0x98f3c9e6E3fAce36bAAd05FE09d375Ef1464288B` | `LogMessagePublished` |
| Wormhole Token Bridge | Ethereum | `0x3ee18B2214AFF97000D974cf647E7C347E8fa585` | `TransferRedeemed` |
| Across | Ethereum | `0x5c7BCd6E7De5423a257D81B442095A1a6ced35C5` | `FundsDeposited` |
| Across | Arbitrum | `0x3bB4445D30AC020a84c1b5A8A2C6248ebC9779D0` | `FundsDeposited` |
| Synapse | Ethereum | `0x2796317b0fF8538F253012862c06787Adfb8c3aC` | `TokenDeposit` |
| Synapse | Arbitrum | `0x9D33eeE1540BdA15C2021C22E14dfdB41c58485b` | `TokenDeposit` |
| Hop | Ethereum | `0x3666f603Cc164936C1b87e207F36BEBa4AC5f18a` | `TransferSent` |
| Hop | Polygon | `0x3666f603Cc164936C1b87e207F36BEBa4AC5f18a` | `TransferSent` |
| AnySwap (Multichain) | Ethereum | `0x6b7a87899490EcE95443e979cA9485CBE7E71522` | `AnySwapOut` |
| Celer cBridge | Ethereum | `0x1619DE6B6B20eD217a58d00f37B9d47C7663feca` | `Send` |

### Bridge Detection Code

```python
BRIDGE_CONTRACTS = {
    "layerzero_endpoint": {
        "ethereum": ["0x66a71dcef29a0ffbdbe3c6a460a3b5bc225cd675"],
        "arbitrum": ["0x3c2269811836af69497e5f486a85d7316753cf02"],
        "polygon": ["0x3c2269811836af69497e5f486a85d7316753cf02"],
    },
    "stargate_router": {
        "ethereum": ["0x8731d54e9d02c286767d56ac03e8037c07e01e98"],
        "arbitrum": ["0x53bf833a5d6c4dda888f69c22c88c9f356a41614"],
        "polygon": ["0x53bf833a5d6c4dda888f69c22c88c9f356a41614"],
    },
    "across": {
        "ethereum": ["0x5c7bcd6e7de5423a257d81b442095a1a6ced35c5"],
        "arbitrum": ["0x3bb4445d30ac020a84c1b5a8a2c6248ebc9779d0"],
    },
    "synapse": {
        "ethereum": ["0x2796317b0ff8538f253012862c06787adfb8c3ac"],
        "arbitrum": ["0x9d33eee1540bda15c2021c22e14dfdb41c58485b"],
    },
    "wormhole": {
        "ethereum": ["0x98f3c9e6e3face36baad05fe09d375ef1464288b"],
    },
    "hop": {
        "ethereum": ["0x3666f603cc164936c1b87e207f36beba4ac5f18a"],
        "polygon": ["0x3666f603cc164936c1b87e207f36beba4ac5f18a"],
    },
    "celer": {
        "ethereum": ["0x1619de6b6b20ed217a58d00f37b9d47c7663feca"],
    },
}

# Flatten bridge addresses to a single set for fast lookup
ALL_BRIDGE_ADDRESSES = set()
for name, chains in BRIDGE_CONTRACTS.items():
    for chain_addrs in chains.values():
        ALL_BRIDGE_ADDRESSES.update(chain_addrs)


def tag_bridge_interactions(df: pd.DataFrame) -> pd.DataFrame:
    """Tag transactions involving known bridge contracts."""
    df_lower = df.copy()
    for col in ["to", "from"]:
        df_lower[col] = df_lower[col].str.lower()

    def lookup(addr):
        addr = addr.lower()
        for name, chains in BRIDGE_CONTRACTS.items():
            for chain_addrs in chains.values():
                if addr in chain_addrs:
                    return name
        return ""

    df_lower["bridge"] = df_lower["to"].apply(lookup)
    # Also check 'from' field for bridge interactions
    mask_from = df_lower["bridge"] == ""
    df_lower.loc[mask_from, "bridge"] = df_lower.loc[mask_from, "from"].apply(lookup)
    return df_lower


def detect_bridge_transfer(tx: dict, receipt_logs: list[dict]) -> dict:
    """Detect bridge transfer from a transaction's event logs.

    Returns destination chain info if a bridge event is found.
    """
    for log in receipt_logs:
        addr = log.get("address", "").lower()
        topics = log.get("topics", [])

        # Stargate Swap event: topics[0] = Swap(uint16,uint16,address,address,uint256,uint256)
        if addr in ALL_BRIDGE_ADDRESSES and len(topics) >= 3:
            return {
                "bridge_detected": True,
                "contract": addr,
                "tx_hash": tx.get("hash", ""),
                "topics": topics,
                "data": log.get("data", ""),
                "note": "Bridge interaction detected — check destination chain in event data",
            }

    return {"bridge_detected": False}


def extract_bridge_destination(tx_hash: str, web3_provider, bridge_address: str) -> int:
    """Extract destination chain ID from a Stargate bridge event.

    Stargate emits Swap(uint16 chainIdFrom, uint16 chainIdTo, ...).
    The chainIdTo is typically topic[2] in the Swap event.
    """
    receipt = web3_provider.eth.get_transaction_receipt(tx_hash)
    for log in receipt.logs:
        if log.address.lower() == bridge_address.lower():
            topics = log.topics
            if len(topics) >= 3:
                dest_chain_id = int.from_bytes(topics[2], "big")
                return dest_chain_id
    return 0
```

## Wallet Clustering Implementation

### CoJoin / Common-Input Clustering (UTXO Chains)

Bitcoin-like UTXO chains enable a powerful clustering heuristic: if two addresses appear as inputs in the same transaction, they are controlled by the same entity (assuming multi-signature or CoinJoin is not involved). This is called CoJoin or Common-Input-Ownership Heuristic.

```python
def cluster_by_common_input(txs_utxo: list[dict]) -> dict[str, set[str]]:
    """Cluster Bitcoin addresses by common-input ownership heuristic.

    If addresses A and B appear as inputs in the same transaction,
    they are likely controlled by the same entity. Returns a dict
    mapping cluster_id -> set of addresses.
    """
    address_to_tx = {}
    tx_to_addresses = {}

    for tx in txs_utxo:
        txid = tx.get("txid", "")
        input_addresses = set()
        for vin in tx.get("vin", []):
            addr = vin.get("prevout", {}).get("scriptpubkey_address", "")
            if addr:
                input_addresses.add(addr)
        if len(input_addresses) >= 2:
            tx_to_addresses[txid] = input_addresses
            for addr in input_addresses:
                if addr not in address_to_tx:
                    address_to_tx[addr] = []
                address_to_tx[addr].append(txid)

    # Union-Find to merge clusters
    parent = {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    all_addresses = set()
    for addresses in tx_to_addresses.values():
        addrs = list(addresses)
        for addr in addrs:
            if addr not in parent:
                parent[addr] = addr
            all_addresses.add(addr)
        for i in range(1, len(addrs)):
            union(addrs[0], addrs[i])

    # Build clusters
    clusters = {}
    for addr in all_addresses:
        root = find(addr)
        if root not in clusters:
            clusters[root] = set()
        clusters[root].add(addr)

    return clusters


def cluster_by_deposit_address(txs: list[dict], exchange_pattern: str = "binance") -> list[dict]:
    """Identify exchange deposit addresses by known patterns.

    Many exchanges use deterministic deposit addresses.
    This heuristic clusters addresses that receive from many senders
    as potential exchange deposit addresses.
    """
    from collections import Counter, defaultdict
    deposits_to = Counter()
    depositors = defaultdict(set)

    for tx in txs:
        to = tx.get("to", "").lower()
        frm = tx.get("from", "").lower()
        if to and frm:
            deposits_to[to] += 1
            depositors[to].add(frm)

    clusters = []
    for addr, count in deposits_to.most_common(50):
        if count >= 10:
            clusters.append({
                "deposit_address": addr,
                "incoming_count": count,
                "unique_depositors": len(depositors[addr]),
                "likely_entity": exchange_pattern if count > 50 else "unknown",
            })

    return clusters
```

### EVM Address Reuse Clustering

Even on account-based chains, addresses can be clustered by behavioral patterns:

```python
def cluster_by_behavior(df: pd.DataFrame, min_interactions: int = 5) -> dict[str, list[str]]:
    """Cluster EVM addresses by behavioral similarity.

    If two addresses interact with the same set of contracts/protocols,
    they may be controlled by the same entity.
    """
    from collections import defaultdict
    addr_contracts = defaultdict(set)

    for _, row in df.iterrows():
        frm = str(row.get("from", "")).lower()
        to = str(row.get("to", "")).lower()
        if frm and to:
            addr_contracts[frm].add(to)
        if to:
            addr_contracts[to]  # ensure key exists

    # Jaccard similarity between address contract sets
    addrs = list(addr_contracts.keys())
    clusters = defaultdict(list)
    assigned = set()

    for i, a1 in enumerate(addrs):
        if a1 in assigned:
            continue
        set1 = addr_contracts[a1]
        if len(set1) < min_interactions:
            continue
        cluster = [a1]
        assigned.add(a1)
        for a2 in addrs[i + 1:]:
            if a2 in assigned:
                continue
            set2 = addr_contracts[a2]
            if len(set2) < min_interactions:
                continue
            intersection = len(set1 & set2)
            union = len(set1 | set2)
            if union > 0 and intersection / union >= 0.7:
                cluster.append(a2)
                assigned.add(a2)
        if len(cluster) >= 2:
            clusters[f"behavioral_cluster_{len(clusters)}"] = cluster

    return clusters
```

## Sankey / Flow Diagram Visualization

Generate an interactive HTML flow visualization using Plotly. This produces a browser-ready trace report.

```python
import plotly.graph_objects as go
from typing import Optional

def build_sankey_diagram(G: nx.DiGraph, title: str = "Transaction Flow",
                         max_nodes: int = 50, min_value: float = 0.01,
                         output_path: Optional[str] = "tx_flow.html") -> Optional[str]:
    """Generate an interactive Sankey diagram from the transaction graph.

    Nodes are addresses, link thickness represents transaction value.
    Only the top-max_nodes by volume are included for readability.
    """
    # Filter by value and take top nodes
    H = filter_by_value(G, min_value)

    # Compute total flow per node and keep top
    node_volume = {}
    for u, v, d in H.edges(data=True):
        val = d.get("value", 0)
        node_volume[u] = node_volume.get(u, 0) + val
        node_volume[v] = node_volume.get(v, 0) + val

    top_nodes = set(sorted(node_volume, key=node_volume.get, reverse=True)[:max_nodes])
    H = H.subgraph(top_nodes)

    # Map addresses to labels
    nodes = list(H.nodes())
    node_map = {n: i for i, n in enumerate(nodes)}
    labels = [f"{n[:6]}…{n[-4:]}" for n in nodes]

    # Build Sankey links
    sources, targets, values, hover_texts = [], [], [], []
    for u, v, d in H.edges(data=True):
        sources.append(node_map[u])
        targets.append(node_map[v])
        val = d.get("value", 0)
        values.append(max(val * 100, 1))  # Scale for visibility
        h = d.get("hash", "")[:10]
        ts = d.get("timestamp", 0)
        token = d.get("token", "ETH")
        hover_texts.append(
            f"From: {u[:6]}…{u[-4:]}<br>"
            f"To: {v[:6]}…{v[-4:]}<br>"
            f"Value: {val:.4f} {token}<br>"
            f"Tx: {h}…<br>"
            f"Timestamp: {ts}"
        )

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color="blue",
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            hovertext=hover_texts,
            hoverinfo="text",
        )
    )])

    fig.update_layout(title=title, font_size=12, height=800)

    if output_path:
        fig.write_html(output_path)
    return output_path


def build_consolidation_sankey(clusters: list[dict], output_path: str = "consolidation.html") -> str:
    """Generate a Sankey diagram focused on consolidation patterns.

    Shows multiple source addresses flowing into each sink.
    """
    sources, targets, values, hover_texts = [], [], [], []
    labels = []

    idx = 0
    for cluster in clusters[:20]:  # Limit to top 20 clusters
        sink = cluster.get("sink", cluster.get("address", ""))
        if sink not in labels:
            labels.append(sink)
            sink_idx = len(labels) - 1
        else:
            sink_idx = labels.index(sink)

        for src in cluster.get("sources", [])[:10]:  # Limit to 10 sources per sink
            if src not in labels:
                labels.append(src)
                src_idx = len(labels) - 1
            else:
                src_idx = labels.index(src)
            sources.append(src_idx)
            targets.append(sink_idx)
            values.append(5)  # Uniform thickness
            hover_texts.append(f"{src[:6]}…→ {sink[:6]}…")

    fig = go.Figure(data=[go.Sankey(
        node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5),
                  label=[f"{l[:6]}…{l[-4:]}" for l in labels]),
        link=dict(source=sources, target=targets, value=values,
                  hovertext=hover_texts, hoverinfo="text"),
    )])

    fig.update_layout(title="Consolidation Patterns", height=600)
    fig.write_html(output_path)
    return output_path
```

## Case Study: Tracing a Simulated Bridge Hack Fund Flow

This scenario demonstrates a realistic theft investigation. Adapt the addresses and step sequence to your actual case.

**Scenario:** The XYZ Bridge was exploited for 5,000 ETH on Ethereum mainnet. The attacker address is `0xAttackerXYZ...`.

```python
# === PHASE 1: Initial Theft ===
# The attacker drained 5,000 ETH from the bridge contract on Ethereum.
# Target address: 0xAttackerXYZ (replace with actual address)

api_key = "YOUR_ETHERSCAN_API_KEY"

# Step A: Collect all transaction data from the attacker address
attacker_txs = collect_all_txs("0xAttackerXYZ...", api_key, chain_id=1)
df_attacker = normalize_txs(attacker_txs["normal"])
df_attacker_internal = normalize_txs(attacker_txs["internal"])
df_attacker_erc20 = normalize_txs(attacker_txs["erc20"], tx_type="erc20")

# Combine all transactions
df_all = pd.concat([df_attacker, df_attacker_internal, df_attacker_erc20],
                   ignore_index=True)
print(f"Collected {len(df_all)} transactions for attacker address")

# Step B: Build the transaction graph
G = build_tx_graph(df_all)
summary = graph_summary(G)
print(f"Graph: {summary['nodes']} nodes, {summary['edges']} edges")

# Step C: Find the first outgoing transaction (likely proceeds movement)
first_out = df_all[df_all["from"] == "0xattackerxyz..."] \
    .sort_values("timestamp").head(5)
print("First outgoing transactions from attacker:")
print(first_out[["hash", "to", "value_eth", "timestamp"]].to_string())

# === PHASE 2: Follow the Money ===
# The attacker split the funds across multiple addresses (peel chain).
peel_chains = detect_peel_chains(G, min_hops=3)
print(f"Detected {len(peel_chains)} potential peel chains")

for chain in peel_chains:
    print(f"  Peel chain: {chain['start']} → {chain['end']} "
          f"({chain['hops']} hops, {chain['total_volume']:.2f} ETH)")

# === PHASE 3: Identify Mixer Deposits ===
# Check if any trace deposits to Tornado Cash
df_tagged = tag_mixer_interactions(df_all)
mixer_txs = df_tagged[df_tagged["mixer"] != "unknown"]
print(f"\nMixer interactions: {len(mixer_txs)}")
for _, tx in mixer_txs.iterrows():
    print(f"  {tx['hash']}: → {tx['to']} ({tx['mixer']}) "
          f"value={tx['value_eth']:.4f} ETH")

# === PHASE 4: Bridge to Another Chain ===
# Check if the attacker used a bridge
df_bridge = tag_bridge_interactions(df_all)
bridge_txs = df_bridge[df_bridge["bridge"] != ""]
print(f"\nBridge interactions: {len(bridge_txs)}")
for _, tx in bridge_txs.iterrows():
    print(f"  {tx['hash']}: → {tx['to']} (bridge={tx['bridge']}) "
          f"value={tx['value_eth']:.4f} ETH")

# === PHASE 5: Detect Consolidation ===
# Eventually, funds consolidate before an exchange deposit
consolidations = detect_consolidation(G, min_sources=3)
print(f"\nConsolidation patterns: {len(consolidations)}")
for c in consolidations[:5]:
    print(f"  Sink: {c['sink'][:10]}... "
          f"Sources: {c['num_sources']} "
          f"Value: {c['total_value']:.2f} ETH")

# === PHASE 6: Generate Sankey Visualization ===
build_sankey_diagram(G, title="Bridge Hack Fund Flow",
                     max_nodes=40, min_value=0.1,
                     output_path="bridge_hack_trace.html")
print("\nFlow diagram generated: bridge_hack_trace.html")

# === PHASE 7: Export Graph for Analysis ===
export_dot(G, "bridge_hack_trace.dot")
export_graphml(G, "bridge_hack_trace.graphml")
print("Graph exported to DOT and GraphML formats")
```

**Expected trace result for this scenario:**
1. `0xAttackerXYZ` → receives 5,000 ETH from bridge drain
2. Splits into 5 x 1,000 ETH transfers to intermediate wallets (peel chain hop 1)
3. Each intermediate sends ∼997 ETH to Tornado Cash 1,000 ETH pool (mixer deposit)
4. Small amount (∼3 ETH) moves to another peel chain layer
5. After mixing: funds emerge on Arbitrum via LayerZero bridge
6. Consolidate to one address on Arbitrum
7. Deposit to Binance (consolidation detected: 15+ source addresses → 1 sink)
8. Trace ends at CEX deposit — submit subpoena request

## Money Section

Turn on-chain forensic skills into multiple revenue streams:

### Service Tiers for Trace Reports

| Tier | Scope | Deliverables | Price (USD) |
|---|---|---|---|
| Basic | Single address, single chain, < 50 transactions | Transaction list + simple flow diagram + entity tags | $200 – $500 |
| Standard | Multi-address, single chain, up to 1,000 transactions | Full trace report with cluster analysis, Sankey diagram, DOT/GraphML exports | $1,000 – $3,000 |
| Premium | Cross-chain, multi-address, unlimited transactions | Complete forensic report with all algorithms (peel chain, consolidation, mixer, bridge detection), interactive flow HTML, raw data exports, expert affidavit | $5,000 – $15,000 |
| Enterprise | Ongoing monitoring, wallet tracking, custom alerting | Dashboard with real-time graph updates, API access, weekly briefings | $10,000 – $50,000/month |

### Law Enforcement / Legal Consulting Rates

| Service | Rate |
|---|---|
| Expert witness testimony (deposition) | $500 – $1,000/hour |
| Expert witness testimony (trial) | $1,000 – $3,000/hour |
| Forensic report for litigation | $5,000 – $25,000 flat |
| Case consultation (hourly) | $300 – $500/hour |

### Bounty Hunting Revenue

| Platform | Typical Payout | Notes |
|---|---|---|
| Arkham Intelligence | $500 – $50,000+ per bounty | Requires verified wallet attribution |
| Lazarus Bounty | Up to 10% of recoverable funds | Focused on North Korean hacker wallets |
| Immunefi (trace required) | Part of larger bug bounty | Trace + smart contract audit combined |
| HackerOne/ Bugcrowd | Variable | Some programs pay for fund flow analysis |
| Private crypto investigation firms | Contract rates | Chainalysis, TRM Labs, CipherTrace partners |

### Business Models

1. **Per-report consulting**: Charge per trace report for incident victims. Most crypto thefts >$100K have victims willing to pay $2K-$10K for a professional trace.

2. **Subscription monitoring**: Recurring fee for wallet/address monitoring with alerts on fund movement. Target: DeFi protocols, VCs, high-net-worth individuals.

3. **Bounty hunting**: Register on Arkham, Lazarus Bounty, and Immunefi. Spend 20-40 hours per lead. Hit rate varies but single bounties can exceed $50K.

4. **Expert witness**: Build relationships with law firms handling crypto fraud and bankruptcy cases. Bill at $500-$3K/hour.

5. **Training/education**: Sell courses on blockchain forensics. Pre-recorded course $500-$2K per student. Corporate training $5K-$20K per session.

6. **Tool licensing**: Build a SaaS tool wrapping these algorithms. $50-$500/month per user.

## Expected Output

A forensic trace report containing:
- Transaction flow graph (interactive HTML Sankey diagram + DOT/GraphML format)
- Wallet cluster table with entity attributions (exchange, mixer, bridge, DeFi protocol, EOA)
- Timeline of fund movements with USD values at time of each transaction
- List of endpoints where funds cannot be further traced (mixers, exchange deposits, or bridges to unmonitored chains)
- Detected patterns: peel chains, consolidations, mixer deposits, bridge interactions
- Confidence scores for each hop and attribution
- Raw data exports (CSV, GraphML) for independent verification
- For legal use: expert affidavit summarizing methodology and findings

## Red Flags

- Attempting to deanonymize addresses without proper authorization or legal basis
- Drawing conclusions from incomplete data (missing internal transactions or token transfers)
- Over-relying on a single block explorer that may have incomplete indexing
- Assuming a wallet belongs to an entity without cross-referencing multiple data sources
- Treating change addresses (UTXO) as separate entities from the spending wallet
- Ignoring transaction fees in value calculations — they affect net amounts in peel chains
- Conflating internal transactions (contract CALLs) with external ETH transfers
- Assuming a CoinJoin transaction implies address clustering — it's designed to break this heuristic
- Trusting a single API response without retrying on rate-limit errors (429 responses)
- Failing to account for wrapped assets (wETH, wBTC) as equivalent to the underlying asset

## Process

1. **Data Collection** — Gather all transaction data for target addresses from block explorers and RPC nodes. Use pagination for high-volume addresses. Collect normal, internal, and token transfers for EVM chains; UTXO inputs/outputs for Bitcoin.

2. **Flow Mapping** — Build a directed transaction graph using NetworkX. Apply filtering thresholds to remove dust transactions. Compute graph statistics (source/sink nodes, centrality, volume hubs).

3. **Pattern Detection** — Run peel chain detection, consolidation detection, mixer identification, and bridge extraction algorithms. Each pattern provides labeled subgraphs for the investigator.

4. **Entity Attribution** — Cross-reference addresses against known entity databases (mixer addresses table, bridge contracts table, known exchange wallets). Tag each node with its likely entity type.

5. **Clustering** — Apply CoJoin clustering for UTXO addresses, behavioral similarity clustering for EVM addresses. Merge clusters into entity-level groups.

6. **Cross-Chain Tracking** — Follow funds through bridges by scanning interaction with known bridge contracts. Extract destination chain IDs from bridge event logs. Re-query the destination chain with the output address.

7. **Visualization** — Generate Sankey flow diagrams and DOT/GraphML exports. Produce both summary view (all hops) and filtered view (significant transfers only).

8. **Reporting** — Produce structured trace report with flow diagrams, confidence scores, endpoint identification, and raw data exports.

## Verification

- Every trace hop verified against the source block explorer (not just API data)
- Transaction hashes cross-referenced on at least two independent explorers where possible
- Entity attributions confirmed by multiple data points, not single-source assumptions
- Graph visualization matches the raw transaction data (no skipped or double-counted hops)
- Internal transaction values summed and cross-checked against normal transaction balances
- Bridge event logs parsed and verified for correct destination chain ID
- NetworkX graph edge count matches the number of filtered transactions
- USD value conversions use historical price data (CoinGecko or similar) at the block timestamp
- Sankey diagram total inflow matches total outflow (conservation of value)
- Report includes raw data exports so findings can be independently verified


## RPC & API Endpoint Management

### Multi-Provider Fallback Strategy

```python
import os, time, requests

BLOCK_EXPLORERS = {
    "ethereum": [{"name": "etherscan",  "base": "https://api.etherscan.io/api",       "key_env": "ETHERSCAN_API_KEY"},
                 {"name": "etherscan-2","base": "https://api.etherscan.io/api",       "key_env": "ETHERSCAN_API_KEY_2"}],
    "bsc":      [{"name": "bscscan",    "base": "https://api.bscscan.com/api",        "key_env": "BSCSCAN_API_KEY"}],
    "polygon":  [{"name": "polygonscan","base": "https://api.polygonscan.com/api",    "key_env": "POLYGONSCAN_API_KEY"}],
}

def robust_explorer_call(chain: str, params: dict, retries: int = 3) -> dict | None:
    """Call block explorer API with per-chain fallback and rate-limit backoff."""
    providers = BLOCK_EXPLORERS.get(chain, [])
    for provider in providers:
        api_key = os.environ.get(provider["key_env"])
        if not api_key:
            continue
        params["apikey"] = api_key
        for attempt in range(retries):
            try:
                resp = requests.get(provider["base"], params=params, timeout=30)
                data = resp.json()
                if data.get("status") == "1":
                    return data
                if "rate limit" in str(data).lower():
                    time.sleep(2 ** attempt)  # exponential backoff
                    continue
                return data  # non-rate-limit error, return anyway
            except (requests.ConnectionError, requests.Timeout):
                time.sleep(2 ** attempt)
    return None
```

### Key Hygiene

- Store keys in `.env` with per-chain names (`ETHERSCAN_API_KEY`, `BSCSCAN_API_KEY`).
- Add a second Etherscan key (`ETHERSCAN_API_KEY_2`) for high-volume traces — the rate limit is per-key.
- **No key?** Use the Covalent free tier (1 key, 30+ chains, 5 req/s) or the block explorer web UI (curl-able, no key for individual lookups).

## When the Trace Goes Cold

### Common Dead Ends and Real Resolutions

| On-Chain Signal | Interpretation | Action |
|---|---|---|
| Funds hit a CEX deposit address | Last on-chain point — exchange owns the address | Document tx hash + timestamp. This is a subpoena/subpoena-ready endpoint. |
| Funds enter a privacy mixer (Tornado Cash, RAILGUN) | Intentional obfuscation | Record deposit amount + block. Scan ±200 blocks for matching withdrawal amounts. |
| Transaction is a `create2` deployment | Counterfactual contract — may not exist yet | Compute predicted address from deployer + salt. Monitor for creation tx. |
| Target address has zero outgoing txs for 72h+ | Sleeping address or intentional hold | Set up a cron job (`crontab -e`, check every 6h via `txlist`) to detect future movement. |
| Funds bridged to another chain | Cross-chain escape | Parse the `Transfer`/`Swap` event on the source bridge contract. Extract `destinationChainId` and `receiver`. Re-query on the target chain. |
| Contract self-destructed | Intentional state destruction | Investigate deployer address. The `SELFDESTRUCT` opcode sends remaining ETH to a target — follow that. |
| UTXO chain — single input, single output | Normal spend | Check for address reuse patterns; if none, this branch is cold. |

### The 10/3 Rule

If you have made 10 API lookups on a single address and found 0 new leads in the last 3, **stop**. Archive the investigation with:

```python
def archive_cold_trail(address: str, chain: str, last_tx: str, notes: str):
    """Log a cold trail for periodic re-check."""
    record = {"address": address, "chain": chain, "last_tx_hash": last_tx,
              "archived_at": time.time(), "notes": notes, "next_check": time.time() + 604800}
    # Append to cold_trails.jsonl — re-check weekly
    with open("cold_trails.jsonl", "a") as f:
        f.write(json.dumps(record) + "\n")
```

**Do not delete cold trails.** The trace is not dead — it's waiting for the next transaction that hasn't happened. Archive with a weekly re-check window and move to higher-signal addresses.
## Practices from Top Investigators

### The ZachXBT Methodology

ZachXBT is the most recognized on-chain investigator, having traced over $243M in stolen crypto
funds. His methodology combines on-chain analysis with extensive cross-platform OSINT, turning
blockchain pseudonymity into identity evidence. This section codifies his proven techniques.

### The 12-Tool Arsenal

| Tool | Purpose | When to Use |
|---|---|---|
| **Etherscan / Solscan** | Primary chain explorer (tx list, internal txs, token transfers) | Every trace — start here |
| **Arkham Intelligence** | Visual fund flow graphs, entity tags, exchange hot wallets | Mid-trace: visualize complex hop chains |
| **MetaSleuth** | Cross-chain fund flow visualization with one-click explorer links | When traces span 3+ chains |
| **Cielo** | Real-time wallet monitoring, push alerts on target addresses | After identifying key addresses — set alerts before sleeping |
| **TRM Labs** | Sanctions screening, risk scoring, entity attribution | Every address before publishing results |
| **Breadcrumbs** | Bitcoin UTXO clustering, peel chain detection | BTC traces — clusters by co-spend heuristic |
| **Blockchair** | BTC/ETH privacy analysis, entity tags, mixing detection | When mixers or privacy tools are suspected |
| **Dune Analytics** | Custom SQL queries on decoded event data | When you need to aggregate thousands of events |
| **DeBank** | Cross-chain portfolio view — balance history over time | Quick assessment of a wallet's activity pattern |
| **OKLink** | Multi-chain explorer with cross-chain bridge tracking | Following funds across L1s and L2s |
| **OMNIA** | Mempool monitoring, pending tx capture | Catching transactions before they confirm |
| **MetaSuites** | Batch address lookups, legacy labeling data | De-anonymizing old addresses with pre-2020 data |

### Funding Chain Tracing (His Signature Method)

The core insight: **trace the attacker's funding, not just the stolen funds.** Attackers almost
always fund their operations from an earlier hack or a tied wallet. Tracing backward from the
attack transaction to the original source of the ETH used for gas fees often reveals:

- The same attacker's previous hacks (same funding source → same person)
- Exchange deposit patterns that reveal identity
- Timing links between multiple attacks

```python
def trace_funding_chain(attacker_address: str, chain: str = "ethereum") -> list[dict]:
    """Trace attacker's funding chain backward from attack tx.

    ZachXBT technique: find where the ATTACKER got their gas money.
    The funding source often ties multiple hacks to the same person.
    """
    from etherscan_v2_api import fetch_txlist, fetch_internal_txlist
    from collections import deque

    visited = {attacker_address}
    queue = deque([attacker_address])
    funding_chain = []
    max_depth = 5  # attackers rarely fund more than 5 hops deep

    while queue and len(funding_chain) < max_depth:
        addr = queue.popleft()
        # Get the FIRST transaction the address ever received (its funding)
        txs = fetch_txlist(addr, chain, sort="asc", limit=1) or []
        internal_txs = fetch_internal_txlist(addr, chain, sort="asc", limit=1) or []

        earliest = (txs or internal_txs)[0] if (txs or internal_txs) else None
        if not earliest:
            funding_chain.append({"address": addr, "funding_source": "unknown", "depth": len(funding_chain)})
            continue

        sender = earliest.get("from", "")
        funding_chain.append({
            "address": addr,
            "funded_by": sender,
            "value_eth": earliest.get("value_eth", earliest.get("value", 0)),
            "block": earliest.get("blockNumber"),
            "tx_hash": earliest.get("hash") or earliest.get("transactionHash"),
        })

        if sender and sender not in visited:
            visited.add(sender)
            queue.append(sender)

    # Check: do any funding sources overlap with known hacker addresses?
    # This is the key pattern — same funder = same attacker across exploits
    return funding_chain
```

### Cross-Platform OSINT Integration

ZachXBT never stops at the blockchain. Every address is cross-referenced with:

1. **Twitter/X** — Deleted tweets, handle changes, engagement patterns
2. **Discord/Telegram** — Invite links from scam websites, group memberships
3. **GitHub** — Repository contributions, commit timestamps matching attack blocks
4. **ENS/Unstoppable Domains** — Metadata that links to real-world identities
5. **Forum posts** (BitcoinTalk, Reddit) — Historical posts with wallet mentions

```python
def cross_platform_lookup(address: str, identity_hints: dict[str, str] = None) -> dict:
    """Cross-reference an address across OSINT sources.

    identity_hints: {"twitter": "handle", "github": "username", "ens": "name.eth"}
    """
    results = {"address": address, "platforms": {}}

    # 1. ENS reverse lookup
    try:
        resp = requests.get(f"https://api.ensideas.com/ens/resolve/{address}", timeout=10)
        if resp.ok:
            data = resp.json()
            results["platforms"]["ens"] = {"name": data.get("ens"), "avatar": data.get("avatar")}
    except Exception:
        pass

    # 2. Check known exploit databases for this address
    try:
        resp = requests.get(
            "https://raw.githubusercontent.com/The-Blockchain-Repository/Hack-Transactions/main/data/latest.json",
            timeout=10)
        if resp.ok:
            exploits = [e for e in resp.json() if address.lower() in str(e).lower()]
            if exploits:
                results["platforms"]["exploit_db"] = {"matches": len(exploits)}
    except Exception:
        pass

    # 3. If we have social media hints, search for them (pseudocode — API keys vary)
    if identity_hints:
        results["platforms"]["hints_provided"] = identity_hints
        results["note"] = "Cross-reference identity hints against on-chain activity timestamps"

    return results
```

### Address Cluster Publication

ZachXBT publicly releases address clusters on Twitter/X after investigations. This creates a
positive feedback loop: the community cross-references new scams against published clusters,
identifying repeat offenders across projects.

**Publishing strategy:**
- **Include all identified addresses** (EOAs, contracts, intermediate wallets)
- **Label each address** with its role (deployer, funder, intermediate, exchange deposit)
- **Chain + tx hash evidence** for every link — no unsupported claims
- **Timestamp the publication** to establish timeline priority

### The Bounty Model

ZachXBT demonstrates that on-chain investigation is a viable career. Revenue sources:

- **Community-funded bounties** — Twitter/X tip jar, Gitcoin grants, mirror.xyz articles
- **Exchange bug bounties** — Exchanges pay for intelligence that helps them freeze stolen funds
- **Project recovery bounties** — 5-15% of recovered funds for tracing assistance
- **Media consulting** — Journalists pay for investigation reports on high-profile incidents
- **Private investigations** — Law firms and insurance companies contract for court-ready reports


## Anti-Rationalization Table
## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Blockchain is anonymous so tracing is impossible" | Blockchain is pseudonymous, not anonymous. Every transaction is permanently recorded and analyzable. |
| "Mixers make tracing impossible" | Mixers complicate but don't prevent tracing. Timing analysis, amount patterns, and deposit/withdrawal correlations often deanonymize users. |
| "The amount is too small to trace" | Small amounts are often test transactions. Follow the same address for larger patterns — test txs confirm control. |
| "Cross-chain transactions break the trail" | Bridge contracts, wrapped assets, and event logs leave permanent on-chain evidence on both chains. The trail is cross-referencable. |
| "Peel chains are too complex to map" | Peel chains show a statistical signature (decaying value per hop) that is algorithmically detectable. Graph analysis reveals the structure. |
| "Exchange deposits are dead ends" | Most regulated exchanges require KYC. A deposit address + timestamp is sufficient for subpoena or law enforcement request. |
| "UTXO chains can't be clustered" | CoJoin heuristic (multiple inputs = common owner) clusters 60-80% of addresses on Bitcoin. CoinJoin must be explicitly filtered. |
| "I need full node data to trace" | Public block explorer APIs (Etherscan, mempool.space) are sufficient for 90% of cases. RPC nodes are only needed for raw event log parsing. |
| "Only one chain matters, the rest are noise" | Attackers almost always bridge to another chain. Ignoring cross-chain means missing the destination of funds. |
| "The trace is done when I hit a DeFi protocol" | DEX swaps and DeFi deposits leave logs too. Follow the LP tokens, check withdraw events, track the swap output tokens. |
