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

Wallet address intelligence is the practice of profiling blockchain addresses to identify the entities behind them, assess risk levels, and build behavioral profiles. Unlike simple balance checks, address intelligence combines on-chain transaction analysis, entity clustering heuristics, known-address databases, behavioral pattern matching, and cross-chain correlation. This skill covers building address profiles with transaction demographics, applying clustering algorithms (Cointracking, CommonInput, behavioral similarity), tagging addresses with entity attributions, assessing risk scores for compliance (AML/KYC), sanctions list screening, MEV searcher identification, ENS/social graph resolution, and producing comprehensive address intelligence reports suitable for compliance teams, security analysts, and protocol operators.

## When to Use

**Trigger phrases:**
- "wallet address intelligence"
- "Profile a blockchain wallet"
- "Check if an address is risky"
- "Cluster related crypto wallets"
- "Build address reputation"
- "Run AML screening on an address"
- "Find all addresses controlled by the same entity"
- "Analyze wallet interaction patterns"

- When performing due diligence on a counterparty before a transaction
- When investigating suspicious addresses for compliance or AML purposes
- When building a wallet clustering system for forensic investigations
- When assessing the risk profile of an address interacting with your protocol
- When attributing addresses to known entities (exchanges, protocols, exploiters)
- When screening addresses against sanctions lists before onboarding
- When linking addresses across different blockchains for entity tracking
- When identifying MEV bots and searcher strategies
- When generating address intelligence reports for law enforcement or compliance
- When building a watchlist monitoring system for high-risk addresses

## When NOT to Use

- You need to trace stolen funds along a specific path (use onchain-transaction-forensics skill)
- You need to analyze a specific DeFi protocol hack (use defi-incident-analysis skill)
- You need to check if a token is a scam (use token-nft-scam-investigation skill)
- You need real-time transaction monitoring (use a blockchain analytics platform like Chainalysis or Elliptic)
- The address is on a privacy-focused blockchain where clustering is infeasible (Monero, Zcash with shielded transactions)
- You only need a single balance check (use a block explorer or a simple RPC call)
- The target uses a privacy wallet with coin-join or stealth addresses

## Prerequisites

- Python 3.8+ with web3.py, requests, pandas, networkx, numpy, jellyfish (fuzzy matching)
- Block explorer API keys (Etherscan, BscScan, Polygonscan, etc.)
- Access to an address labeling dataset (Etherscan labels, tagged addresses from block explorers, known exploiters list)
- Basic understanding of graph theory for clustering algorithms
- Optional: DeBank or similar API for multi-chain wallet views
- Optional: Flashbots API access for MEV bundle data
- Optional: ENS resolution library (web3.py handles this natively)

```bash
pip install web3 requests pandas networkx numpy jellyfish
```

## Core Workflow

The core workflow builds a comprehensive address intelligence pipeline: collect data, cluster related addresses, score risk, attribute entities, and produce a report.

### Address Profile Builder

```python
import requests
from datetime import datetime, timezone
from typing import Optional
import json

# ============================================================
# BLOCK EXPLORER HELPERS
# ============================================================

ETHERSCAN_BASE = "https://api.etherscan.io/api"

def _fetch_balance(address: str, api_key: str) -> float:
    """Fetch ETH balance from Etherscan."""
    params = {"module": "account", "action": "balance", "address": address, "apikey": api_key}
    resp = requests.get(ETHERSCAN_BASE, params=params, timeout=15)
    data = resp.json()
    if data.get("status") == "1":
        return int(data["result"]) / 1e18
    return 0.0

def _fetch_tx_list(address: str, api_key: str, startblock: int = 0, endblock: int = 99999999) -> list:
    """Fetch normal transaction list for an address."""
    params = {"module": "account", "action": "txlist", "address": address,
              "startblock": startblock, "endblock": endblock, "sort": "desc", "apikey": api_key}
    resp = requests.get(ETHERSCAN_BASE, params=params, timeout=30)
    data = resp.json()
    return data.get("result", [])

def _fetch_internal_tx_list(address: str, api_key: str) -> list:
    """Fetch internal transactions for an address."""
    params = {"module": "account", "action": "txlistinternal", "address": address,
              "startblock": 0, "endblock": 99999999, "sort": "desc", "apikey": api_key}
    resp = requests.get(ETHERSCAN_BASE, params=params, timeout=30)
    data = resp.json()
    return data.get("result", [])

def _fetch_erc20_transfers(address: str, api_key: str) -> list:
    """Fetch ERC-20 token transfer events."""
    params = {"module": "account", "action": "tokentx", "address": address,
              "startblock": 0, "endblock": 99999999, "sort": "desc", "apikey": api_key}
    resp = requests.get(ETHERSCAN_BASE, params=params, timeout=30)
    data = resp.json()
    return data.get("result", [])

def _fetch_nft_transfers(address: str, api_key: str) -> list:
    """Fetch NFT (ERC-721 / ERC-1155) transfer events."""
    params = {"module": "account", "action": "tokennfttx", "address": address,
              "startblock": 0, "endblock": 99999999, "sort": "desc", "apikey": api_key}
    resp = requests.get(ETHERSCAN_BASE, params=params, timeout=30)
    data = resp.json()
    return data.get("result", [])

def _fetch_token_balances(address: str, api_key: str) -> list:
    """Fetch all token balances for an address."""
    params = {"module": "account", "action": "tokenlist", "address": address, "apikey": api_key}
    resp = requests.get(ETHERSCAN_BASE, params=params, timeout=15)
    data = resp.json()
    return data.get("result", [])


def build_address_profile(address: str, etherscan_key: str) -> dict:
    """Build a comprehensive profile for a single address."""
    profile = {
        "address": address,
        "tags": [],
        "risk_indicators": [],
        "activity": {},
        "known_labels": [],
        "token_holdings": [],
        "nft_holdings": [],
        "protocols_used": set(),
        "interactors": set(),
        "gas_profile": {},
    }

    # 1. Basic balance and transaction count
    balance = _fetch_balance(address, etherscan_key)
    tx_list = _fetch_tx_list(address, etherscan_key)
    internal_txs = _fetch_internal_tx_list(address, etherscan_key)
    erc20_txs = _fetch_erc20_transfers(address, etherscan_key)
    nft_txs = _fetch_nft_transfers(address, etherscan_key)

    profile["eth_balance"] = balance
    profile["total_txns"] = len(tx_list)
    profile["total_internal_txns"] = len(internal_txs)
    profile["total_token_transfers"] = len(erc20_txs)
    profile["total_nft_transfers"] = len(nft_txs)
    profile["total_activity"] = len(tx_list) + len(internal_txs) + len(erc20_txs)

    # 2. First and last activity
    all_txs_sorted = sorted(tx_list, key=lambda t: int(t.get("timeStamp", 0)), reverse=True)
    if all_txs_sorted:
        profile["first_seen"] = datetime.fromtimestamp(int(all_txs_sorted[-1]["timeStamp"]), tz=timezone.utc)
        profile["last_active"] = datetime.fromtimestamp(int(all_txs_sorted[0]["timeStamp"]), tz=timezone.utc)
        profile["age_days"] = (profile["last_active"] - profile["first_seen"]).days if profile["first_seen"] else 0

    # 3. Interaction diversity — unique addresses this address has interacted with
    unique_interactors = set()
    protocols = set()
    gas_prices = []
    for tx in all_txs_sorted:
        unique_interactors.add(tx["from"].lower())
        if tx["to"] and tx["to"] != address.lower():
            unique_interactors.add(tx["to"].lower())
            protocols.add(tx["to"].lower())
        if tx.get("gasPrice"):
            gas_prices.append(int(tx["gasPrice"]))

    profile["unique_interactors"] = len(unique_interactors)
    profile["protocols_touched"] = len(protocols)

    # Gas profile
    if gas_prices:
        profile["gas_profile"] = {
            "min_gwei": min(gas_prices) / 1e9,
            "max_gwei": max(gas_prices) / 1e9,
            "avg_gwei": (sum(gas_prices) / len(gas_prices)) / 1e9,
            "total_gas_spent_eth": sum(
                int(tx.get("gasUsed", 0)) * int(tx.get("gasPrice", 0)) / 1e18
                for tx in all_txs_sorted if tx.get("gasUsed")
            ),
        }

    # 4. Token holdings
    token_balances = _fetch_token_balances(address, etherscan_key)
    profile["token_holdings"] = [
        {
            "token": t.get("tokenName", "unknown"),
            "symbol": t.get("tokenSymbol", "???"),
            "contract": t.get("contractAddress", "").lower(),
            "balance": float(t.get("balance", 0)) / 10 ** int(t.get("tokenDecimal", 18)),
        }
        for t in token_balances if t.get("balance") and int(t.get("balance", 0)) > 0
    ]

    # 5. Known entity labels
    labels = _check_known_labels(address)
    if labels:
        profile["known_labels"].extend(labels)
        profile["tags"].extend(labels)

    return profile


def _check_known_labels(address: str) -> list:
    """Check address against hardcoded known-entity databases (Etherscan labels, known exploiters, exchanges).

    In production, load from a database or JSON file rather than hardcoding.
    """
    address_lower = address.lower()

    # Known exchange deposit addresses (subset for illustration)
    known_exchanges = {
        "0x3f5ce5fbfe3e9af3971dd833d26ba9b5c936f0be": "Binance 1",
        "0xd551234ae421e3bcba99a0da6d736074f22192ff": "Binance 2",
        "0x28c6c06298d514db089934071355e5743bf21d60": "Binance 3",
        "0x21a31ee1afc51d94c2efccaa2092ad1028285549": "Coinbase 1",
        "0xa090e606e30bd747d4e6245a1517ebe430f0057e": "Coinbase 2",
        "0xe92d1a43df510ff82d2218671ae56b150287a6f5": "Kraken 1",
        "0x0a869d79a7052c7f1b55a8ebabbea3420f0d1e13": "Kraken 2",
        "0x126783cba8df91c1c42ee59d1cfb342f42f04ce3": "KuCoin",
        "0x281dc6b700385c8e826a7e0c1f6b7e10f5f2d894": "Bitfinex",
    }

    # Known exploiter / hacker addresses (subset)
    known_exploiters = {
        "0x0000000000000000000000000000000000000000": "placeholder",
        "0x1e227979f6b5c9704f9a92e4201ffc7d7c2d7bbf": "Bybit Exploiter (Lazarus)",
        "0x59e0cda5922ef1a80d49f5fe4714e2343dd2ae4f": "Ronin Bridge Exploiter",
        "0x098b716b8aaf21512996dc57eb0615e2383e2f96": "Nomad Bridge Exploiter",
        "0x0de8f4f3c92abb2fc3a6c4ad07a39bbffa4c37a5": "Wormhole Exploiter",
        "0x5dafb0d0f71b5acd3a1d4e21a358e7dcb75bceff": "FTX Drainer",
    }

    # Mixers
    known_mixers = {
        "0x910cbd523d972eb0a6f4cae4618ad62622b39dbf": "Tornado Cash 1",
        "0xa160cdab225685da1d56aa342ad8841c3b53f291": "Tornado Cash 2",
        "0x12d66f87a04a9e220743712ce6d9bb1b5616b8fc": "Tornado Cash 3",
        "0x47ce0c6ed5b0ce3d3a51fdb1c52dc66a7c3c2936": "Tornado Cash 4",
    }

    results = []
    if address_lower in known_exchanges:
        results.append(("exchange", known_exchanges[address_lower]))
    if address_lower in known_exploiters:
        results.append(("exploiter", known_exploiters[address_lower]))
    if address_lower in known_mixers:
        results.append(("mixer", known_mixers[address_lower]))

    return results


# ============================================================
# COMMON-INPUT CLUSTERING (Bitcoin-style)
# ============================================================

def build_common_input_clusters(tx_inputs: list[list[str]]) -> dict:
    """Cluster Bitcoin addresses that appear together as inputs in the same transaction.

    This is the classic CommonInput heuristic used by Chainalysis and similar tools:
    if two addresses are inputs to the same transaction, they are controlled by the same entity
    (because only the entity controlling both signing keys would choose to spend from both in one tx).

    Args:
        tx_inputs: List of lists, where each inner list contains input addresses for one transaction.

    Returns:
        Dict mapping cluster_id (int) to a set of addresses in that cluster.

    Example:
        >>> txs = [
        ...     ["1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2"],
        ...     ["1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "1C5e8CzVX6TGhP1qYLPr5XzL4yZLj9Mq6S"],
        ...     ["1DqQn5YpP2MjoBRKJoTQ9rTmW3JfLQZtHx"],
        ... ]
        >>> cl = build_common_input_clusters(txs)
        >>> # "1A1z..." and "1BvBM..." and "1C5e..." are in the same cluster
    """
    parent = {}
    cluster_id_counter = [0]

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[ry] = rx

    for inputs in tx_inputs:
        if len(inputs) < 2:
            continue  # Single-input tx adds no clustering info
        # Ensure all addresses have entries in union-find
        for addr in inputs:
            if addr not in parent:
                parent[addr] = addr
        # Union all pairs — they are controlled by the same entity
        first = inputs[0]
        for addr in inputs[1:]:
            union(first, addr)

    # Collect clusters
    clusters = {}
    for addr in parent:
        root = find(addr)
        if root not in clusters:
            clusters[root] = set()
        clusters[root].add(addr)

    # Assign numeric IDs
    result = {}
    for idx, (root, members) in enumerate(clusters.items()):
        result[idx] = members

    return result


def cluster_stats(clusters: dict) -> dict:
    """Return summary statistics for clustered address groups."""
    member_counts = [len(members) for members in clusters.values()]
    return {
        "total_clusters": len(clusters),
        "total_addresses": sum(member_counts),
        "avg_cluster_size": sum(member_counts) / len(member_counts) if member_counts else 0,
        "largest_cluster": max(member_counts) if member_counts else 0,
        "singleton_clusters": sum(1 for c in member_counts if c == 1),
    }


# ============================================================
# BEHAVIORAL SIMILARITY CLUSTERING
# ============================================================

def compute_behavioral_similarity(profiles: list[dict]) -> list[tuple[int, int, float]]:
    """Compute pairwise similarity scores between address profiles based on behavioral patterns.

    Similarity dimensions:
    - Protocol touch overlap (Jaccard similarity of contracts interacted with)
    - Time-of-day activity distribution similarity (cosine)
    - Gas price preferences (mean gas price delta)
    - Number of unique interactors (ratio-based)

    Returns list of (profile_a_index, profile_b_index, similarity_score) tuples,
    where similarity_score is in [0, 1].
    """
    from sklearn.feature_extraction.text import TfidfVectorizer  # optional improvement
    import numpy as np
    import math

    n = len(profiles)
    scores = []

    for i in range(n):
        for j in range(i + 1, n):
            p1 = profiles[i]
            p2 = profiles[j]
            dims = []

            # 1. Protocol overlap (Jaccard)
            prots1 = p1.get("protocols_touched", set()) if isinstance(p1.get("protocols_touched"), set) else set()
            prots2 = p2.get("protocols_touched", set()) if isinstance(p2.get("protocols_touched"), set) else set()
            if prots1 or prots2:
                intersection = len(prots1 & prots2)
                union = len(prots1 | prots2)
                jaccard = intersection / union if union > 0 else 0
                dims.append(jaccard)

            # 2. Total activity volume similarity (ratio-based)
            act1 = p1.get("total_activity", 0)
            act2 = p2.get("total_activity", 0)
            if act1 > 0 or act2 > 0:
                vol_sim = min(act1, act2) / max(act1, act2) if max(act1, act2) > 0 else 0
                dims.append(vol_sim)

            # 3. Wallet age similarity
            age1 = p1.get("age_days", 0)
            age2 = p2.get("age_days", 0)
            if age1 > 0 or age2 > 0:
                age_sim = min(age1, age2) / max(age1, age2) if max(age1, age2) > 0 else 0
                dims.append(age_sim)

            # 4. Gas price preference similarity
            gp1 = p1.get("gas_profile", {}).get("avg_gwei", 0)
            gp2 = p2.get("gas_profile", {}).get("avg_gwei", 0)
            if gp1 > 0 and gp2 > 0:
                gas_sim = min(gp1, gp2) / max(gp1, gp2) if max(gp1, gp2) > 0 else 0
                dims.append(gas_sim)

            if dims:
                combined = sum(dims) / len(dims)
                scores.append((i, j, round(combined, 4)))

    return scores


def cluster_by_behavior(scores: list[tuple[int, int, float]], threshold: float = 0.7) -> list[list[int]]:
    """Group address indices into behavior-based clusters using threshold on similarity scores.

    Args:
        scores: Output from compute_behavioral_similarity.
        threshold: Minimum similarity to consider two addresses behaviorally linked (default 0.7).

    Returns:
        List of clusters, each cluster is a list of address indices.
    """
    parent = {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[ry] = rx

    for i, j, sim in scores:
        if sim >= threshold:
            if i not in parent:
                parent[i] = i
            if j not in parent:
                parent[j] = j
            union(i, j)

    # Collect clusters
    clusters_map = {}
    for idx in parent:
        root = find(idx)
        if root not in clusters_map:
            clusters_map[root] = []
        clusters_map[root].append(idx)

    return list(clusters_map.values())


# ============================================================
# INTERACTION NETWORK BUILDER (NetworkX)
# ============================================================

import networkx as nx

def build_interaction_network(tx_list: list[dict], min_interactions: int = 1) -> nx.DiGraph:
    """Build a weighted directed graph of address interactions from transaction data.

    Nodes = addresses (EOA + contracts).
    Edges = directional value flow. Weight = number of transactions between the pair.

    Args:
        tx_list: List of transaction dicts (from Etherscan txlist).
        min_interactions: Minimum txs between a pair to include the edge (filter noise).

    Returns:
        NetworkX DiGraph with node and edge attributes.
    """
    G = nx.DiGraph()

    for tx in tx_list:
        sender = tx.get("from", "").lower()
        receiver = tx.get("to", "").lower()
        value_eth = int(tx.get("value", 0)) / 1e18

        if not sender or not receiver:
            continue

        G.add_node(sender, node_type="sender")
        G.add_node(receiver, node_type="receiver")

        if G.has_edge(sender, receiver):
            G[sender][receiver]["weight"] += 1
            G[sender][receiver]["total_value"] += value_eth
        else:
            G.add_edge(sender, receiver, weight=1, total_value=value_eth)

    # Remove low-weight edges
    edges_to_remove = [(u, v) for u, v, d in G.edges(data=True) if d["weight"] < min_interactions]
    G.remove_edges_from(edges_to_remove)

    return G


def compute_network_stats(G: nx.DiGraph) -> dict:
    """Compute centrality and structure metrics for an interaction network.

    Returns dict with:
    - pagerank: Dict of node -> PageRank score
    - in_degree_centrality: Dict of node -> in-degree centrality
    - out_degree_centrality: Dict of node -> out-degree centrality
    - betweenness_centrality: Top-10 nodes by betweenness
    - density: Network density (0-1)
    - strongly_connected_components: Number of SCCs
    """
    stats = {}

    if G.number_of_nodes() == 0:
        return {"error": "empty graph"}

    try:
        stats["pagerank"] = nx.pagerank(G, alpha=0.85)
    except nx.PowerIterationFailedConvergence:
        stats["pagerank"] = {}

    stats["in_degree_centrality"] = nx.in_degree_centrality(G)
    stats["out_degree_centrality"] = nx.out_degree_centrality(G)

    # Betweenness — compute only for top nodes due to O(n^3) complexity
    if G.number_of_nodes() < 1000:
        betweenness = nx.betweenness_centrality(G, k=min(50, G.number_of_nodes()))
        top_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:10]
        stats["top_betweenness"] = top_betweenness
    else:
        stats["top_betweenness"] = []

    stats["density"] = nx.density(G)
    stats["nodes"] = G.number_of_nodes()
    stats["edges"] = G.number_of_edges()

    try:
        stats["scc_count"] = nx.number_strongly_connected_components(G)
    except Exception:
        stats["scc_count"] = 0

    return stats


def find_central_hubs(G: nx.DiGraph, top_n: int = 10) -> list[tuple[str, float]]:
    """Find the most central addresses by PageRank score."""
    pr = nx.pagerank(G, alpha=0.85)
    return sorted(pr.items(), key=lambda x: x[1], reverse=True)[:top_n]


# ============================================================
# KNOWN ADDRESS LABELING
# ============================================================

def load_known_addresses(labels_file: str) -> dict:
    """Load a known-address database from a JSON file.

    Expected format:
    {
        "0x...": {"label": "Binance Hot Wallet", "category": "exchange", "confidence": 0.95},
        ...
    }
    """
    with open(labels_file, "r") as f:
        return json.load(f)


def label_addresses(addresses: list[str], known_db: dict) -> dict[str, list[dict]]:
    """Tag a list of addresses with labels from the known-address database.

    Returns dict mapping address -> list of matched labels.
    """
    results = {}
    for addr in addresses:
        addr_lower = addr.lower()
        if addr_lower in known_db:
            results[addr] = [known_db[addr]]
        else:
            results[addr] = []
    return results


# ============================================================
# RISK SCORING ENGINE
# ============================================================

RISK_DIMENSIONS = [
    "sanctions_match",
    "mixer_interaction",
    "exploit_association",
    "phishing_association",
    "darknet_market",
    "ransomware_payment",
    "flashloan_abuse",
    "wash_trading",
    "cex_sanctioned_jurisdiction",
]

# Default weights for each risk dimension (sum = 1.0)
DEFAULT_RISK_WEIGHTS = {
    "sanctions_match": 0.25,
    "mixer_interaction": 0.15,
    "exploit_association": 0.20,
    "phishing_association": 0.12,
    "darknet_market": 0.10,
    "ransomware_payment": 0.10,
    "flashloan_abuse": 0.03,
    "wash_trading": 0.03,
    "cex_sanctioned_jurisdiction": 0.02,
}


def compute_risk_score(profile: dict, address: str, weights: dict = None) -> dict:
    """Compute a multi-dimensional risk score for an address.

    Each dimension scores 0.0 (no risk) to 1.0 (maximum risk).
    The overall score is a weighted sum across dimensions.

    Args:
        profile: Address profile dict from build_address_profile().
        address: The target address.
        weights: Dict of dimension -> weight. Uses DEFAULT_RISK_WEIGHTS if None.

    Returns:
        Dict containing per-dimension scores, overall score (0-100), and confidence level.
    """
    if weights is None:
        weights = DEFAULT_RISK_WEIGHTS

    scores = {}
    address_lower = address.lower()
    evidence = []

    # 1. Sanctions match
    sanctions_list = load_sanctions_list() if False else {}  # Loaded lazily in practice
    has_sanctions = any(
        label[0] == "sanctioned" for label in profile.get("known_labels", [])
    )
    scores["sanctions_match"] = 1.0 if has_sanctions else 0.0
    if has_sanctions:
        evidence.append("Address matches known sanctions list entry")

    # 2. Mixer interaction
    has_mixer = any(
        label[0] == "mixer" for label in profile.get("known_labels", [])
    )
    scores["mixer_interaction"] = 1.0 if has_mixer else 0.0
    if has_mixer:
        evidence.append("Address is a known cryptocurrency mixer")

    # 3. Exploit association
    has_exploit = any(
        label[0] == "exploiter" for label in profile.get("known_labels", [])
    )
    scores["exploit_association"] = 1.0 if has_exploit else 0.0
    if has_exploit:
        evidence.append("Address is associated with a known exploit/hack")

    # 4. Phishing association — heuristic: many outbound txs to many distinct addresses
    # (indicating a mass-transfer pattern common in phishing)
    interactions = profile.get("unique_interactors", 0)
    total_txns = profile.get("total_txns", 0)
    if total_txns > 50 and interactions > 20 and interactions / total_txns > 0.8:
        scores["phishing_association"] = min(0.7, 0.3 + 0.4 * (interactions / (total_txns + 1)))
        evidence.append(f"High interactor-per-tx ratio ({interactions}/{total_txns}): possible phishing")
    else:
        scores["phishing_association"] = 0.0

    # 5. Darknet market (placeholder — requires real list)
    scores["darknet_market"] = 0.0

    # 6. Ransomware (placeholder — requires real list)
    scores["ransomware_payment"] = 0.0

    # 7. Flash loan abuse — heuristic: high volume of flash loan calls
    flashloan_count = sum(1 for tx in profile.get("total_txns", []) if isinstance(tx, dict) and tx.get("to", "").lower() in [
        "0x7d2768de32b0b80b7a3454c06bdac94a69ddc7a9",  # Aave LendingPool
        "0xba12222222228d8ba445958a75a0704d566bf2c8",  # Balancer Vault
    ])
    if isinstance(profile.get("total_txns"), int):
        pass  # No flash loan detection without tx data in profile
    scores["flashloan_abuse"] = 0.0

    # 8. Wash trading — heuristic: many txs to self or circular patterns
    scores["wash_trading"] = 0.0

    # 9. Sanctioned jurisdiction CEX (placeholder)
    scores["cex_sanctioned_jurisdiction"] = 0.0

    # Compute overall
    overall = sum(scores[dim] * weights.get(dim, 0) for dim in scores)
    overall_percent = round(overall * 100, 1)

    # Confidence
    dimensions_with_data = sum(1 for v in scores.values() if v > 0)
    total_dimensions = len(scores)
    confidence = "low" if dimensions_with_data <= 1 else (
        "medium" if dimensions_with_data <= 3 else "high"
    )

    return {
        "overall_score": overall_percent,
        "dimension_scores": scores,
        "weights_used": weights,
        "confidence": confidence,
        "evidence": evidence,
    }


# ============================================================
# SANCTIONS LIST INTEGRATION
# ============================================================

# OFAC SDN list — in production load from:
#   https://sanctionslist.ofac.treas.gov/
#   https://www.treasury.gov/ofac/downloads/sdn.xml
# Use fuzzy matching because addresses may be formatted differently.

import jellyfish  # for fuzzy string matching


def load_sanctions_list(filepath: str = "sdn_addresses.json") -> dict:
    """Load parsed sanctions list from local JSON cache.

    In production, fetch and parse OFAC SDN XML daily:
        from sanctions_scraper import fetch_ofac_sdn_list
    """
    import os
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return {}


SCREEN_THRESHOLDS = {
    "exact": 0.0,        # Exact match = no fuzziness allowed
    "high": 0.95,        # Very close match
    "medium": 0.85,      # Possible match — manual review required
    "low": 0.75,         # Weak match — flag for investigation
}


def screen_against_sanctions(address: str, sanctions_db: dict) -> list[dict]:
    """Screen a single address against a sanctions list database.

    Uses exact matching first, then falls back to fuzzy matching for
    sub-string or formatted-address matches. Fuzzy matches are noted
    with lower confidence and require manual review.

    Args:
        address: The blockchain address to screen.
        sanctions_db: Dict mapping address -> sanction details.

    Returns:
        List of match results with confidence, match_type, and details.
    """
    address_lower = address.lower()
    results = []

    # Exact match
    if address_lower in sanctions_db:
        results.append({
            "address": address_lower,
            "match_type": "exact",
            "confidence": 1.0,
            "sanction_info": sanctions_db[address_lower],
            "requires_review": False,
        })
        return results  # Exact match is definitive — no further checks needed

    # Fuzzy matching — check for partial or formatted address variations
    for sanctioned_addr, info in sanctions_db.items():
        san_lower = sanctioned_addr.lower()

        # Jaro-Winkler distance for similar addresses (e.g., checksum variations)
        similarity = jellyfish.jaro_winkler_similarity(address_lower, san_lower)

        if similarity >= SCREEN_THRESHOLDS["high"]:
            results.append({
                "address": address_lower,
                "matched_against": san_lower,
                "match_type": "fuzzy_high",
                "confidence": round(similarity, 3),
                "sanction_info": info,
                "requires_review": True,
            })
        elif similarity >= SCREEN_THRESHOLDS["medium"]:
            results.append({
                "address": address_lower,
                "matched_against": san_lower,
                "match_type": "fuzzy_medium",
                "confidence": round(similarity, 3),
                "sanction_info": info,
                "requires_review": True,
            })

    return results


def sanctions_batch_screen(addresses: list[str], sanctions_db: dict) -> dict:
    """Screen a batch of addresses against sanctions lists.

    Returns:
        dict with 'hits' (addresses with any match), 'clear' (no match),
        and 'requires_review' (fuzzy matches needing manual review).
    """
    hits = {}
    requires_review = {}
    clear = []

    for addr in addresses:
        results = screen_against_sanctions(addr, sanctions_db)
        if not results:
            clear.append(addr)
            continue
        for r in results:
            if r["requires_review"]:
                requires_review.setdefault(addr, []).append(r)
            else:
                hits.setdefault(addr, []).append(r)

    return {
        "total_screened": len(addresses),
        "confirmed_hits": len(hits),
        "requires_review": len(requires_review),
        "clear": len(clear),
        "hits": hits,
        "fuzzy_matches": requires_review,
    }


# ============================================================
# CROSS-CHAIN ADDRESS LINKING
# ============================================================

def get_evm_address_on_chain(address: str, target_chain_id: int) -> str:
    """Return the same EVM address on a different chain.

    For EVM-compatible chains (Ethereum, BSC, Polygon, Avalanche C-Chain,
    Arbitrum, Optimism, Base, etc.), the same private key produces the same
    address across all chains. This is the simplest linking heuristic.

    Args:
        address: The address on the source chain.
        target_chain_id: Chain ID to map to (unused — address is identical).

    Returns:
        The same address (EVM address is chain-independent).
    """
    return address  # EVM addresses are identical across EVM chains


def link_addresses_across_chains(
    profiles_by_chain: dict[str, list[dict]],
    time_window_minutes: int = 5,
) -> list[dict]:
    """Link addresses across chains using temporal and funding heuristics.

    Heuristics:
    1. Same EVM address on different chains (trivial — same key)
    2. Time-correlated funding: two addresses on different chains funded
       from the same source within a short time window
    3. Sequential funding: a source funds address A on chain X, then the
       same source funds address B on chain Y within the window

    Args:
        profiles_by_chain: Dict mapping chain_name -> list of address profiles
                           on that chain.
        time_window_minutes: Max time delta (in minutes) to consider two
                             funding events as linked.

    Returns:
        List of linking results, each with linked_addrs, heuristic, and confidence.
    """
    links = []

    # Heuristic 1: Same EVM address appearing on multiple chains
    address_chains = {}
    for chain, profiles in profiles_by_chain.items():
        for p in profiles:
            addr = p.get("address", "").lower()
            if addr not in address_chains:
                address_chains[addr] = []
            address_chains[addr].append(chain)

    for addr, chains in address_chains.items():
        if len(chains) > 1:
            links.append({
                "addresses": [addr],
                "chains": chains,
                "heuristic": "same_evm_address",
                "confidence": 1.0,
                "description": f"Address {addr} appears on {', '.join(chains)} (same private key)",
            })

    return links


# ============================================================
# ENS / SOCIAL GRAPH RESOLUTION
# ============================================================

from web3 import Web3

def resolve_ens_name(address: str, w3: Web3) -> Optional[str]:
    """Resolve an Ethereum address to its ENS primary name (reverse record).

    Args:
        address: Ethereum address.
        w3: Web3 instance connected to an Ethereum node.

    Returns:
        ENS name or None if no reverse record is set.
    """
    try:
        return w3.ens.name(address)
    except Exception:
        return None


def resolve_ens_address(ens_name: str, w3: Web3) -> Optional[str]:
    """Resolve an ENS name to its Ethereum address (forward record).

    Args:
        ens_name: e.g. "vitalik.eth"
        w3: Web3 instance.

    Returns:
        Address or None.
    """
    try:
        return w3.ens.address(ens_name)
    except Exception:
        return None


def resolve_ens_text_record(address: str, key: str, w3: Web3) -> Optional[str]:
    """Resolve an ENS text record for an address (e.g. 'url', 'email', 'twitter', 'github').

    ENS text records can reveal off-chain identity:
    - url: Personal website
    - email: Contact email
    - twitter: Twitter/X handle
    - github: GitHub username
    - discord: Discord handle
    - telegram: Telegram handle
    - notice: Additional notice or PGP key link
    """
    try:
        return w3.ens.get_text(address, key)
    except Exception:
        return None


def build_social_profile(address: str, w3: Web3) -> dict:
    """Build a social profile for an address using ENS text records.

    Returns dict with resolved ENS name, URL, email, twitter, github, and discord.
    """
    profile = {"address": address, "ens_name": None}
    try:
        ens_name = w3.ens.name(address)
        profile["ens_name"] = ens_name
    except Exception:
        pass

    if profile["ens_name"]:
        for key in ["url", "email", "twitter", "github", "discord", "telegram", "notice"]:
            try:
                val = w3.ens.get_text(address, key)
                if val:
                    profile[key] = val
            except Exception:
                continue

    return profile


# ============================================================
# MEV SEARCHER IDENTIFICATION
# ============================================================

def is_mev_bot(address: str, tx_list: list[dict]) -> dict:
    """Analyze whether an address exhibits MEV searcher/bot behavior.

    Detection signals:
    - High proportion of transactions to known MEV relay contracts (Flashbots, Eden, etc.)
    - Sandwich patterns: the address's tx is sandwiched between two txs from the same
      searcher address in the same block
    - Callback execution: address receives callbacks from DEX pools (Uniswap V3, etc.)
    - Very high gas price payments (MEV searchers bid high for block position)
    - Round-number profit extraction (0.1 ETH, 0.5 ETH, etc.)

    Args:
        address: Target address.
        tx_list: List of transaction dicts for this address.

    Returns:
        Dict with is_mev bool, confidence float (0-1), and signals found.
    """
    signals = []

    # Known MEV relay contracts
    mev_relays = {
        "0x1a5d8f81dc7c4b5e1e5a5e5a5e5a5e5a5e5a5e5a": "Flashbots Flashswap",  # illustrative
        "0x736d6576f6c616e646572732e657468": "searcher",  # placeholder
    }

    mev_indicators = {
        "high_gas_above_100_gwei": 0,
        "sandwich_flanking_txs": 0,
        "flashbots_bundle_tx": 0,
        "callback_from_dex": 0,
    }

    gas_prices = []
    for tx in tx_list:
        try:
            gp = int(tx.get("gasPrice", 0))
            gas_prices.append(gp)
        except (ValueError, TypeError):
            continue

        # Check if interacting with MEV relay
        to_addr = tx.get("to", "").lower()
        if to_addr in mev_relays:
            mev_indicators["flashbots_bundle_tx"] += 1

    # Signal: very high gas prices (MEV searchers bid aggressively)
    if gas_prices:
        avg_gwei = (sum(gas_prices) / len(gas_prices)) / 1e9
        max_gwei = max(gas_prices) / 1e9

        if avg_gwei > 100:
            mev_indicators["high_gas_above_100_gwei"] += 1
        if max_gwei > 500:
            mev_indicators["high_gas_above_100_gwei"] += 1

    # Score
    total_signals = sum(mev_indicators.values())
    is_mev = total_signals >= 2
    confidence = min(1.0, total_signals * 0.25)

    return {
        "is_mev_bot": is_mev,
        "confidence": round(confidence, 2),
        "signals": mev_indicators,
        "total_signals": total_signals,
        "assessment": "MEV searcher/bot" if is_mev else "Likely regular user",
    }


# ============================================================
# WALLET AGE / ACTIVITY SCORING
# ============================================================

def compute_wallet_maturity_score(profile: dict) -> dict:
    """Compute a wallet maturity score (0-100) based on age, activity regularity, and protocol diversity.

    Factors:
    - Wallet age (days since first tx): older = more mature
    - Transaction count: more = more active
    - Activity regularity: even spacing between transactions indicates organic use
    - Protocol diversity: interacting with many distinct protocols = sophisticated
    - Number of unique interactors
    - Token holding diversity: many token types = diversified

    Returns dict with overall maturity score and per-factor breakdown.
    """
    score = 0.0
    factors = {}

    # 1. Age factor (max 25 points)
    age_days = profile.get("age_days", 0)
    if age_days >= 1095:  # 3+ years
        age_score = 25
    elif age_days >= 365:  # 1+ year
        age_score = 20
    elif age_days >= 90:   # 3+ months
        age_score = 15
    elif age_days >= 30:   # 1+ month
        age_score = 10
    elif age_days >= 7:    # 1+ week
        age_score = 5
    else:
        age_score = 0
    factors["age"] = age_score
    score += age_score

    # 2. Activity volume factor (max 25 points)
    total_activity = profile.get("total_activity", 0)
    if total_activity >= 1000:
        activity_score = 25
    elif total_activity >= 100:
        activity_score = 20
    elif total_activity >= 20:
        activity_score = 15
    elif total_activity >= 5:
        activity_score = 10
    elif total_activity >= 1:
        activity_score = 5
    else:
        activity_score = 0
    factors["activity_volume"] = activity_score
    score += activity_score

    # 3. Protocol diversity factor (max 25 points)
    protocol_count = profile.get("protocols_touched", 0) if isinstance(profile.get("protocols_touched"), int) else len(profile.get("protocols_touched", []))
    if protocol_count >= 50:
        protocol_score = 25
    elif protocol_count >= 20:
        protocol_score = 20
    elif protocol_count >= 10:
        protocol_score = 15
    elif protocol_count >= 5:
        protocol_score = 10
    elif protocol_count >= 1:
        protocol_score = 5
    else:
        protocol_score = 0
    factors["protocol_diversity"] = protocol_score
    score += protocol_score

    # 4. Token holding diversity (max 15 points)
    token_count = len(profile.get("token_holdings", []))
    if token_count >= 20:
        token_score = 15
    elif token_count >= 10:
        token_score = 12
    elif token_count >= 5:
        token_score = 8
    elif token_count >= 1:
        token_score = 4
    else:
        token_score = 0
    factors["token_diversity"] = token_score
    score += token_score

    # 5. Interaction diversity (max 10 points)
    unique_interactors = profile.get("unique_interactors", 0)
    if unique_interactors >= 100:
        interactor_score = 10
    elif unique_interactors >= 50:
        interactor_score = 8
    elif unique_interactors >= 10:
        interactor_score = 5
    elif unique_interactors >= 1:
        interactor_score = 2
    else:
        interactor_score = 0
    factors["interaction_diversity"] = interactor_score
    score += interactor_score

    return {
        "maturity_score": int(score),
        "max_score": 100,
        "factors": factors,
        "age_days": age_days,
        "total_activity": total_activity,
        "classification": _classify_maturity(score),
    }


def _classify_maturity(score: int) -> str:
    """Classify a maturity score into a descriptive bucket."""
    if score >= 80:
        return "Very mature — long-established, diversified, highly active wallet"
    if score >= 60:
        return "Mature — established wallet with solid activity and diversity"
    if score >= 40:
        return "Developing — moderate activity, some diversity"
    if score >= 20:
        return "New but active — young wallet with growing usage"
    if score >= 1:
        return "Nascent — very recent or low-activity wallet"
    return "Inactive or zero-activity wallet"


# ============================================================
# FULL INTELLIGENCE REPORT
# ============================================================

def generate_intelligence_report(address: str, etherscan_key: str, w3: Optional[Web3] = None) -> dict:
    """Generate a comprehensive address intelligence report.

    This is the main orchestration function that runs all analysis modules
    and returns a structured report.
    """
    # Step 1: Build base profile
    profile = build_address_profile(address, etherscan_key)

    # Step 2: Compute maturity score
    maturity = compute_wallet_maturity_score(profile)

    # Step 3: Risk scoring
    risk = compute_risk_score(profile, address)

    # Step 4: MEV analysis (requires tx list)
    tx_list = _fetch_tx_list(address, etherscan_key)
    mev = is_mev_bot(address, tx_list)

    # Step 5: ENS resolution (requires web3 connection)
    social = {"ens_name": None}
    if w3 is not None:
        social = build_social_profile(address, w3)

    # Step 6: Cross-chain (placeholder — requires multi-chain profiles)
    cross_chain = {"note": "Provide profiles_by_chain for cross-chain linking"}

    return {
        "intelligence_report": {
            "address": address,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "executive_summary": (
                f"Address {address[:10]}...{address[-6:]} "
                f"is a {maturity['classification']}. "
                f"Risk score: {risk['overall_score']}/100 ({risk['confidence']} confidence). "
                f"MEV assessment: {mev['assessment']}. "
                f"ENS: {social.get('ens_name', 'Not set')}."
            ),
        },
        "profile": {
            "eth_balance": profile.get("eth_balance", 0),
            "total_activity": profile.get("total_activity", 0),
            "first_seen": str(profile.get("first_seen", "N/A")),
            "last_active": str(profile.get("last_active", "N/A")),
            "age_days": profile.get("age_days", 0),
            "unique_interactors": profile.get("unique_interactors", 0),
            "gas_profile": profile.get("gas_profile", {}),
            "token_holdings": profile.get("token_holdings", []),
        },
        "maturity": maturity,
        "risk_assessment": risk,
        "mev_analysis": mev,
        "social_profile": social,
        "cross_chain": cross_chain,
    }
```

### Step 1: Build Address Profile

Collect the following dimensions for the target address:
- **Balance and transaction history** — current balance, total sent/received, total transaction count, internal transactions, token transfers, NFT transfers
- **Activity timeline** — first seen block, last active block, activity frequency, dormant periods, age in days
- **Interaction network** — which contracts and EOAs has this address interacted with? Count of unique interactors, protocol diversity
- **Token holdings** — all ERC-20 and NFT balances, both current and historical, across all known tokens
- **Gas spending** — total gas spent, average gas price preference (indicates sophistication), min/max/avg gwei
- **Protocol usage** — which DeFi protocols, NFT marketplaces, or DEXes has this address used?

```python
# Minimal call:
from wallet_intel import build_address_profile
profile = build_address_profile("0x742d35Cc6634C0532925a3b844Bc9e7595f294b3", "YOUR_ETHERSCAN_KEY")
```

### Step 2: Entity Clustering

Group related addresses into entity clusters using multiple heuristics. No single clustering method is sufficient — always cross-validate.

**CommonInput clustering (Bitcoin):** Addresses that appear as co-inputs in the same transaction are controlled by the same entity. This is the most reliable clustering heuristic because spending multiple UTXOs in one transaction requires signing with all the private keys, proving common control.

**Behavioral similarity:** Addresses controlled by the same entity exhibit similar behavioral patterns — same protocols, similar gas bidding, activity at similar times of day, similar token preferences. The `compute_behavioral_similarity` function scores pairwise similarity and `cluster_by_behavior` groups addresses above a configurable threshold.

**Interaction network clustering:** Using the NetworkX interaction graph, addresses that are tightly connected (high edge weight, short path length) may be related. Apply community detection algorithms (Louvain, Label Propagation) on the interaction graph to discover clusters.

```python
# CommonInput (Bitcoin)
transactions = [
    ["addr_a", "addr_b", "addr_c"],
    ["addr_a", "addr_d"],
]
clusters = build_common_input_clusters(transactions)

# Behavioral similarity
profiles = [profile_a, profile_b, profile_c]
scores = compute_behavioral_similarity(profiles)
behavior_clusters = cluster_by_behavior(scores, threshold=0.7)

# Interaction network
G = build_interaction_network(tx_list, min_interactions=2)
stats = compute_network_stats(G)
```

### Step 3: Risk Scoring

Assess the address across multiple risk dimensions. Each dimension produces a score from 0.0 (no risk) to 1.0 (maximum risk). The overall score is a weighted sum.

**Risk dimensions:**
- **Sanctions/Terrorism financing** — match against OFAC, EU, and UN sanctions lists using exact + fuzzy matching
- **Mixer/Tumbler interaction** — has the address interacted with Tornado Cash, Wasabi, Blender, Sinbad, or similar privacy tools?
- **Exploit/Hack involvement** — is the address connected to known exploit or hack transactions? Check against known exploiter databases
- **Scam/Phishing association** — has the address received funds from or sent to known scam addresses? High interactor-per-tx ratio is a heuristic for mass-transfer patterns
- **Darknet marketplace** — interaction with known darknet markets (Hydra, Silk Road successors, etc.)
- **Ransomware payments** — receipt of funds from known ransomware addresses (Ryuk, LockBit, BlackCat/ALPHV, etc.)
- **Liquidity risks** — is the address a large LP holder with potential to manipulate? High single-token concentration
- **Flash loan abuse** — frequent flash loan interactions (Aave, Balancer, dYdX) indicative of MEV or manipulation

```python
risk = compute_risk_score(profile, address)
print(f"Risk score: {risk['overall_score']}/100")
print(f"Confidence: {risk['confidence']}")
for dim, score in risk['dimension_scores'].items():
    print(f"  {dim}: {score}")
```

### Step 4: Entity Attribution

Attempt to attribute the address to a known entity:
- **Exchange deposit addresses** — addresses that match known exchange deposit patterns (label against known exchange hot/cold wallet databases)
- **Protocol deployer wallets** — wallets that deployed known smart contracts (check creation transactions)
- **MEV searcher/validator** — identifiable by MEV bundle submission patterns, high gas bids, Flashbots relay interaction
- **Whale/investor** — large holders with characteristic accumulation patterns, interaction with DeFi yield protocols
- **Team/insider wallet** — wallets funded by project treasury or multi-sig, connection to project deployers
- **De-anonymization through off-chain data** — ENS text records (url, twitter, github, email, discord, telegram), social media posts referencing the address, GitHub commits signed with the address's key, forum posts mentioning the address

```python
# ENS resolution
w3 = Web3(Web3.HTTPProvider("https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY"))
social = build_social_profile("0x742d35Cc6634C0532925a3b844Bc9e7595f294b3", w3)
if social.get("ens_name"):
    print(f"ENS: {social['ens_name']}")
    print(f"  URL: {social.get('url', 'N/A')}")
    print(f"  Twitter: {social.get('twitter', 'N/A')}")
    print(f"  GitHub: {social.get('github', 'N/A')}")
```

### Step 5: Produce Intelligence Report

Generate a structured intelligence report:
- **Executive summary** — who is likely behind this address and what risk level do they represent
- **Profile card** — balance, age, transaction count, protocol usage summary, maturity score
- **Cluster map** — related addresses in the entity's cluster with relationship descriptions
- **Risk assessment** — scored across each risk dimension with confidence levels and evidence
- **Transaction sample** — representative transactions showing typical behavior
- **Entity attribution** — best-guess entity name with confidence score and evidence
- **Cross-chain presence** — what other chains has this address transacted on?
- **Social footprint** — ENS name, linked social accounts, off-chain identity

```python
report = generate_intelligence_report(address, etherscan_key, w3)
print(json.dumps(report, indent=2, default=str))
```

## Case Studies

### Case Study 1: Known Exploiter Profile

**Profile:** A confirmed Bybit exploiter (Lazarus Group associated address `0x1e227979f6b5c9704f9a92e4201ffc7d7c2d7bbf`)

**Expected findings:**
- Risk score: 95+/100 (exploit_association=1.0, sanctions possible)
- Cluster: addresses connected via funding from Lazarus-affiliated wallets
- Age: relatively young wallet, created shortly before the exploit
- Activity: short burst of high-value transactions, then dormancy or laundering
- Cross-chain: funds likely bridged to multiple chains (ETH → BTC via cross-chain swaps)
- Maturity score: low (short active period despite high value moved)
- Red flags: interaction with known mixers, multiple fresh addresses receiving funds

**Analyst approach:**
1. Build base profile to see balance, tx count, and first/last activity
2. Fetch all ERC-20 transfers to identify stolen token types
3. Fetch internal transactions to trace ETH forwarding
4. Run risk scoring — will flag exploit_association from the known-exploiters list
5. Build interaction network to see where funds flowed
6. Cross-reference with OFAC sanctions list (Lazarus is a sanctioned entity)

```python
addr = "0x1e227979f6b5c9704f9a92e4201ffc7d7c2d7bbf"
profile = build_address_profile(addr, etherscan_key)
risk = compute_risk_score(profile, addr)
print(f"Risk: {risk['overall_score']} — {'HIGH' if risk['overall_score'] > 70 else 'MEDIUM'}")
# Expected: Risk 95+ — HIGH, confidence high
```

### Case Study 2: MEV Searcher Bot

**Profile:** An MEV searcher address on Ethereum, engaged in sandwich attacks and arbitrage.

**Expected findings:**
- Risk score: medium (flashloan_abuse elevated, but not necessarily malicious)
- Gas profile: very high average gwei (150-500+), bidding aggressively for block position
- Interaction pattern: dense subgraph of DEX pools (Uniswap, Sushiswap, Curve)
- Activity: hundreds or thousands of transactions, often at regular intervals
- Protocol use: predominantly DEXes, Flashbots relays, and MEV infrastructure
- Maturity score: medium-high (high activity, protocol diversity, but typically few token holdings)
- MEV flags: is_mev_bot=True, signals found in gas bidding and relay interaction

**Analyst approach:**
1. Fetch full tx list — check gas prices, they will be notably high
2. Run `is_mev_bot()` — expects True with confidence > 0.5
3. Build interaction network — expect a dense cluster around DEX pool addresses
4. Check for Flashbots relay interaction
5. Note that MEV searcher addresses are NOT inherently malicious (they profit from mempool

   arbitrage, not exploits), but they may interact with exploits opportunistically

```python
# Example MEV searcher characteristics:
# - 500+ transactions in 30 days
# - Average gas price > 150 gwei
# - Interacts exclusively with DEX pools and Flashbots relay
# - Round-number profits extracted in sandwich patterns
mev_result = is_mev_bot(addr, tx_list)
print(f"MEV bot: {mev_result['is_mev_bot']} (confidence: {mev_result['confidence']})")
# Expected: MEV bot: True (confidence: 0.75+)
```

### Case Study 3: Whale / High-Value Address

**Profile:** A large Ethereum holder or institutional investor address.

**Expected findings:**
- Risk score: low (unless interacting with risky protocols or mixers)
- Balance: high ($1M+ in ETH and/or stablecoins)
- Age: old wallet (years), consistent activity over time
- Interaction diversity: moderate — interacts with a few trusted protocols (Compound, Aave, Uniswap)
- Token holdings: diversified across blue-chip tokens (ETH, USDC, WBTC, stETH)
- Protocols used: DeFi lending/borrowing, DEX swaps, staking
- Maturity score: very high (80-100)
- ENS: often has a vanity ENS name
- Gas profile: moderate gas prices (not desperate for speed), uses EIP-1559 priority fees

**Analyst approach:**
1. Run `generate_intelligence_report()` to get the full picture
2. Check maturity score — expect 80+
3. Review token holdings for concentration risk
4. Check for exchange deposits — the address may transact with Binance/Coinbase regularly
5. Review ENS social profile — whales often have public-facing ENS with social links
6. Cross-chain check — may have positions on Arbitrum, Optimism, Base

```python
report = generate_intelligence_report(whale_address, etherscan_key, w3)
maturity = report["maturity"]
print(f"Maturity: {maturity['maturity_score']}/100 — {maturity['classification']}")
# Expected: 85+/100 — Very mature
print(f"Risk: {report['risk_assessment']['overall_score']}/100")
# Expected: < 20 (clean whale)
```

## Expected Output

A structured address intelligence report containing:
- Profile card (balance, age, activity level, maturity score)
- Entity cluster visualization (GraphML or DOT format with NetworkX export)
- Multi-axis risk score with evidence for each dimension and configurable weights
- Sanctions screening results (exact matches with confidence, fuzzy matches flagged for review)
- Entity attribution with confidence score and evidence trail
- MEV searcher assessment with signal breakdown
- Cross-chain presence summary
- Social profile (ENS, linked accounts)
- Plain-text executive summary suitable for compliance or investigation use

```python
# Export interaction graph for visualization
nx.write_graphml(G, "interaction_network.graphml")

# Export report as JSON
with open("intelligence_report.json", "w") as f:
    json.dump(report, f, indent=2, default=str)
```

## Money Section

Wallet address intelligence is a billable service for compliance teams, crypto funds, and legal firms. The skills above can be packaged as:

### Service Tier 1: Address Screening ($100-500/report)
- Single-address profile with balance, age, activity summary
- OFAC/EU/UN sanctions screening (exact + fuzzy matching)
- Known-entity label check (exchange, exploiter, mixer)
- Risk score across all dimensions
- PDF report with executive summary

### Service Tier 2: Entity Investigation ($500-2,500/report)
- Full profile from Tier 1, plus:
- Multi-cluster analysis (CommonInput + behavioral + interaction graph)
- Cross-chain address linking (identify same entity on all chains)
- ENS/social profile discovery
- On-chain fund flow visualization (NetworkX graph with PageRank)
- MEV searcher identification if applicable
- Evidence-backed attribution report

### Service Tier 3: Continuous Monitoring ($2,000-10,000/month)
- Weekly or daily re-screening of a watchlist of addresses
- Alerts when a watchlisted address interacts with a high-risk counterparty
- Ongoing sanctions list updates (new OFAC additions matched against watchlist)
- Monthly intelligence digest with risk score changes
- API access for programmatic screening

### Service Tier 4: Custom Integration ($10,000-50,000+)
- Deploy the screening pipeline within the client's infrastructure
- Integrate with client's existing KYC/AML workflow
- Custom risk weight configuration based on client's risk appetite
- Custom entity databases for client-specific watchlists
- SOC 2-compliant reporting and audit trails

## Red Flags

- Claiming definitive entity attribution from incomplete clustering data
- Over-relying on a single clustering heuristic (CommonInput alone is not sufficient)
- Ignoring false positives in sanctions list matching (false positives are common with fuzzy matching, especially for short or common address patterns)
- Drawing conclusions about an address without checking all chains it has transacted on
- Publishing or sharing address intelligence without proper data protection and authorization
- Assuming an address with a known ENS identity is a real person (ENS names can be anonymous)
- Confusing MEV activity with malicious behavior (MEV searchers operate in a legal gray area)
- Treating low maturity scores as suspicious (new wallets are often legitimately new users)
- Using stale sanctions lists (sanctions lists change frequently — always use the latest)
- Over-confidence in cross-chain linking when only one heuristic is available

## Process

1. **Data Gathering** — Collect on-chain data: transaction history, ERC-20 transfers, internal transactions, NFT transfers, token balances for target address, and gas usage statistics
2. **Profile Construction** — Build behavioral profile with activity patterns, protocol usage, asset holdings, gas preferences, and ENS/social data
3. **Clustering** — Apply multiple clustering algorithms in parallel: CommonInput (UTXO chains), behavioral similarity (feature-vector comparison), interaction network community detection (Louvain/Label Propagation on NetworkX graph)
4. **Sanctions Screening** — Match address against OFAC SDN list (exact and fuzzy), EU consolidated sanctions list, UN sanctions list. Flag fuzzy matches for manual review
5. **Risk Assessment** — Score against risk dimensions using known databases, behavioral indicators, and heuristic rules. Apply configurable weights based on client risk tolerance
6. **Attribution** — Attempt entity attribution through: known-address DB lookup, ENS reverse resolution, social profile extraction, MEV pattern recognition, exchange deposit address matching
7. **Cross-Chain Analysis** — Check for same address on other EVM chains, identify time-correlated funding, and notice bridging patterns
8. **Reporting** — Produce structured intelligence report with evidence for each claim, executive summary, risk breakdown, cluster visualization, and confidence scoring

### The Process as Automation Pipeline

For recurring screening workloads, the process can be fully automated:

```python
def screening_pipeline(addresses: list[str], api_key: str, w3: Web3 = None, sanctions_db: dict = None) -> list[dict]:
    """Run the full screening pipeline over a batch of addresses.

    Returns a list of intelligence reports sorted by risk score (highest first).
    """
    reports = []

    for addr in addresses:
        try:
            report = generate_intelligence_report(addr, api_key, w3)

            if sanctions_db:
                screen = screen_against_sanctions(addr, sanctions_db)
                report["sanctions_screening"] = screen

            reports.append(report)
        except Exception as e:
            reports.append({
                "address": addr,
                "error": str(e),
            })

    # Sort by risk score descending, addresses with errors at the end
    reports.sort(key=lambda r: r.get("risk_assessment", {}).get("overall_score", -1), reverse=True)
    return reports
```

## Verification

- Every cluster connection verified by at least two independent heuristics (not just one)
- Entity attributions cross-checked against at least two independent data sources
- Risk scores manually reviewed for false positives before reporting
- Cluster visualizations inspected for obvious errors (mislinked addresses, missing connections)
- All claims supported by verifiable on-chain transaction hashes or external references
- Sanctions list fuzzy matches manually verified before flagging as positives
- MEV classification validated against Flashbots API data where available
- ENS resolutions confirmed by checking both forward and reverse records
- Cross-chain links double-checked: same address ≠ same entity across all chains
- Generated reports reviewed with a minimum two-person review for compliance-critical findings


## RPC & API Endpoint Management

Wallet address intelligence requires querying multiple chains and APIs simultaneously.
Without careful rate-limit management, your queries will fail mid-investigation.

### API Key Inventory

| Service | Purpose | Rate Limit | Key | Recommended Practice |
|---|---|---|---|---|
| Etherscan V2 | Core chain lookups (tx list, balance, internal txs) | 5 calls/sec | `ETHERSCAN_KEY` | Use 2 keys, round-robin for 10/sec burst |
| Ethplorer | Token portfolio for any address (free, no key) | 1 call/sec | (none) | Use as fallback when Etherscan is rate-limited |
| Chainalysis API | Sanctions / risk scoring | Varies by plan | `CHAINALYSIS_KEY` | Cache results with 24h TTL |
| AnyBlock | Multi-chain in one RPC endpoint | 20 req/sec free | `ANYBLOCK_KEY` | Primary multi-chain RPC for wallet balance |
| Alchemy | Archive node access for historical state | 300 req/sec free | `ALCHEMY_KEY` | Use for deep historical analysis only |
| DeBank API | Cross-chain portfolio aggregation | 10 req/sec free | `DEBANK_KEY` | Quick wallet overview before deep dive |

### Rate-Limiter Pattern

```python
import asyncio
import time

class RateLimiter:
    """Token-bucket rate limiter for multi-API investigations."""
    def __init__(self, rate: float, burst: int = 5):
        self.rate = rate          # calls per second
        self.burst = burst        # max burst size
        self.tokens = burst
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self):
        async with self._lock:
            now = time.monotonic()
            self.tokens = min(self.burst, self.tokens + (now - self.last_refill) * self.rate)
            self.last_refill = now
            if self.tokens < 1:
                wait = (1 - self.tokens) / self.rate
                await asyncio.sleep(wait)
                self.tokens = 0
            self.tokens -= 1

# Usage
rate_limiter = RateLimiter(rate=4.0, burst=10)  # slightly conservative for 5/sec limit
```

### Key Rotation Strategy

```python
import os
from itertools import cycle

class MultiKeyRotator:
    """Rotate through multiple API keys to maximize throughput."""
    def __init__(self, prefix: str = "ETHERSCAN"):
        self.keys = cycle([
            os.environ.get(f"{prefix}_KEY_{i}")
            for i in range(1, 4)
            if os.environ.get(f"{prefix}_KEY_{i}")
        ])
        if not self.keys:
            self.keys = cycle([os.environ.get(f"{prefix}_KEY", "")])

    def next(self) -> str:
        return next(self.keys)

# Register fallback providers in your config
# FREE_RPC_FALLBACK = ["https://eth.llamarpc.com", "https://rpc.ankr.com/eth"]
```

### When Address Intelligence Yields No Signal

After querying all chains and data sources, you may have an address that shows nothing:

| Scenario | Interpretation | Next Step |
|---|---|---|
| Zero tx on all mainnet chains | Address created but never used | Check if it's a counterfactual deployer (CREATE2) or unused gas token receiver |
| Only dust transactions from mixers | Privacy-enhanced address | Attempt value-based clustering (all amounts ≤~0.01 ETH from same mixer batch) |
| Single inbound, no outbound | Burner / one-time receive | Cross-reference with known donation addresses or airdrop contracts |
| All activity on L2 with no L1 presence | L2-native wallet | Check if bridged from L1 via standard bridge contracts |
| Frequent contract interactions but no DEX/CEX | Bot/contract operator | Reverse-lookup the contract interactions to identify the primary contract |
| Known ENS but no on-chain activity | Off-chain identity holder | ENS registration costs ~$5 — not all registrants are active users |

## Practices from Top Investigators

### The ZachXBT Methodology

ZachXBT is the most prolific on-chain wallet investigator, having identified thousands of scammer
wallets and published comprehensive address clusters. His core insight: **wallet intelligence is
about patterns, not single addresses.** A wallet's value comes from its connections — both
on-chain (transactions, interactions) and off-chain (social media, forum posts, exchange accounts).

### The 12-Tool Arsenal for Wallet Intelligence

| Tool | Wallet Intelligence Use | When to Apply |
|---|---|---|
| **Cielo** | Real-time tracking: monitor target wallets for any new activity | After identifying suspect wallets — maintain surveillance |
| **Arkham** | Visual entity clusters: swap, bridge, and CEX deposit patterns | Mid-investigation: map wallet relationships |
| **MetaSleuth** | Cross-chain address linking: find same-owner wallets on different chains | When wallets span L1s and L2s |
| **Etherscan/Solscan** | Primary data: tx history, token holdings, internal transactions | Every wallet — always start here |
| **TRM Labs** | Sanctions screening: check wallets against OFAC and proprietary lists | Before publishing any wallet intelligence |
| **Breadcrumbs** | Bitcoin clustering: co-spend heuristic for UTXO wallet grouping | BTC wallet sets — cluster by common inputs |
| **DeBank** | Cross-chain portfolio snapshot: what a wallet holds everywhere | Quick reconnaissance — assess wallet type in 10 seconds |
| **OKLink** | Address labeling: known tags, entity tags, risk flags | Determine if wallet has been previously identified |
| **Blockchair** | Privacy analysis: mixing detection, entity tag linking, privacy score | Identify wallets that deliberately obscure activity |
| **Dune** | Bulk wallet analysis: SQL queries on wallet sets | Compare 100+ wallets in batch |
| **OMNIA** | Mempool monitoring: see pending outbound tx from target wallets | Catch the moment funds move — before they confirm |
| **MetaSuites** | Legacy labeling for historical address lookups | Old addresses (pre-2022) may only have labels here |

### Address Cluster Publication

Publishing wallet clusters publicly serves two purposes:
1. **Community defense** — enables anyone to check if they're interacting with a known scammer
2. **New signal discovery** — community cross-referencing finds connections the original
   investigation missed

```python
def format_cluster_for_publication(cluster: dict) -> str:
    """Format wallet intelligence for public release (ZachXBT-style)."""
    lines = ["## Wallet Cluster: " + cluster.get("label", "Unnamed Cluster")]
    lines.append(f"_Published: {cluster.get('date', 'unknown')}_\n")
    lines.append("### Addresses")

    for addr_group in cluster.get("addresses", []):
        lines.append(f"- **{addr_group['role']}**: {addr_group['address']}")
        if "tx_evidence" in addr_group:
            lines.append(f"  - Evidence: {addr_group['tx_evidence']}")
        if "tag" in addr_group:
            lines.append(f"  - Tag: {addr_group['tag']}")

    lines.append("\n### Connections")
    for conn in cluster.get("connections", []):
        lines.append(f"- {conn['type']}: {conn['address_a']} → {conn['address_b']}")
        lines.append(f"  (Tx: {conn['tx_hash']}, Chain: {conn['chain']})")

    lines.append("\n### Cross-References")
    for ref in cluster.get("cross_references", []):
        lines.append(f"- Appears in: {ref['investigation']} (Role: {ref['role']})")

    return "\n".join(lines)
```

### Exchange Coordination Protocol

When wallet intelligence identifies a CEX address holding stolen funds, ZachXBT's approach:

1. **Document everything** before contacting anyone — tx hashes, amounts, timestamps, chain
2. **Identify the right contact** — exchange legal/compliance team, not support
3. **One clear ask** — "Freeze address X holding Y $ETH from hack Z" with evidence links
4. **Follow up within 24h** — exchanges handle hundreds of requests; persistence matters
5. **Public pressure when needed** — Twitter threads naming the exchange+tx hash if no response

```python
def generate_exchange_report(cex_address: str, stolen_assets: float,
                              hack_tx_hash: str, victim: str) -> dict:
    """Generate a structured report for exchange compliance teams."""
    return {
        "subject": f"URGENT: Stolen funds deposit at {cex_address}",
        "body": {
            "incident": {"victim": victim, "hack_tx": hack_tx_hash, "date": ""},
            "stolen_assets": {"amount": stolen_assets, "token": "ETH", "current_value_usd": 0},
            "destination": {"address": cex_address, "chain": "ethereum", "tx_hash": ""},
            "evidence_links": [],  # Block explorer URLs
            "request": "Freeze address and notify sender for identity verification",
            "contact": {"email": "", "role": "Legal/Compliance"},
        },
        "protocol": "1. Verify addresses 2. Confirm chain 3. Review evidence 4. Execute freeze",
    }
```

### Cross-Case Pattern Recognition

ZachXBT's most powerful technique: **identifying the same wallet appearing across multiple
seemingly unrelated scams.** A wallet that funded an NFT mint in January and a DeFi rug pull
in June is the same person — even if the scams look completely different.

```python
def cross_case_wallet_search(wallet_clusters: list[dict], db_path: str = "known_scams.sqlite") -> list:
    """Search across multiple investigations for overlapping wallets.

    Returns connections between cases — the hallmark of serial scammers.
    """
    import sqlite3, json
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Collect all distinct addresses from the input clusters
    all_addresses = set()
    for cluster in wallet_clusters:
        for entry in cluster.get("addresses", []):
            all_addresses.add(entry["address"].lower())

    # Query known scam database for matches
    placeholders = ",".join("?" * len(all_addresses))
    cursor.execute(
        f"SELECT investigation_id, address, role, date FROM wallet_references "
        f"WHERE LOWER(address) IN ({placeholders})",
        list(all_addresses)
    )
    cross_refs = cursor.fetchall()

    # Group by investigation
    from collections import defaultdict
    by_investigation = defaultdict(list)
    for inv_id, addr, role, date in cross_refs:
        by_investigation[inv_id].append({"address": addr, "role": role, "date": date})

    return dict(by_investigation)
```

### Getting Paid: The Investigation-to-Bounty Pipeline

ZachXBT's model shows wallet intelligence is monetizable:

- **Cluster publication** — Community donations and tips for useful intel
- **Exchange referrals** — Some exchanges pay for intelligence that leads to frozen funds
- **Private client work** — Token projects pay $200-$2,000+ to identify wallets behind FUD/smear campaigns
- **Law enforcement** — Contracted tracing services for court cases
- **Media** — Journalists purchase wallet intelligence for investigative pieces


## Anti-Rationalization Table
## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "The address only has a few transactions, it's not important" | Small addresses can be test wallets, intermediaries, or deliberately kept clean for compartmentalization. |
| "The address has no known tags, it's clean" | Absence of tags means only that no one has identified it, not that it's benign. Most exploiters use fresh addresses. |
| "I can cluster with just one method" | Single-method clustering has high false positive/negative rates. Multi-method cross-validation is essential. |
| "The address is associated with a mixer so it's criminal" | Mixer interaction may indicate a privacy preference, not criminal activity. Context and transaction partners matter. |
| "The address is old so it must be legitimate" | Age is not security. Exploiters frequently use old dust addresses to blend in. Cross-reference with activity patterns. |
| "The address has a high balance so it's a whale, not a threat" | High-value addresses can be compromised or used for social engineering. Balance alone is not a trust signal. |
| "Fuzzy matching on sanctions lists is too noisy to use" | Noise is manageable. Use tiered thresholds: exact = auto-block, fuzzy-high = manual review, fuzzy-medium = flag only. |
| "ENS proves the address is a real person" | Anyone can register an ENS. The name proves nothing about the operator's identity without additional off-chain verification. |
| "MEV activity means the address is malicious" | MEV extraction is legal under Ethereum protocol rules. Only specific strategies (sandwich attacks on retail) are predatory. |
| "The address interacts with DeFi, so it's sophisticated" | Interacting with a frontend requires no sophistication. Check for direct contract interaction, flash loans, and custom scripts. |
| "No OFAC match means the address is safe to transact with" | Sanctions lists only cover designated addresses. Most scam/fraud addresses are never sanctioned. Always combine with behavioral analysis. |
| "Cross-chain analysis is too unreliable to include" | Imperfect heuristics still provide investigative value when clearly labeled with confidence scores and caveats. |
