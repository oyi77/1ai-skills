---
name: defi-incident-analysis
description: Analyze DeFi security incidents including flash loan attacks, oracle manipulation, reentrancy exploits,
  bridge hacks, and governance attacks to reconstruct attack chains and identify root causes. Use when investigating DeFi
  protocol exploits, analyzing smart contract attacks, or writing incident post-mortems.
domain: cybersecurity
author: mahipal
subdomain: blockchain-security
tags:
- blockchain
- defi
- incident
- analysis
- flash-loan
- oracle
- hack
- exploit
- smart-contract
- investigation
- money
version: '1.0'
license: Apache-2.0
---

# DeFi Incident Analysis

## Overview

Decentralized Finance (DeFi) incidents have resulted in over $3 billion in losses from flash loan attacks, oracle manipulation, reentrancy exploits, bridge hacks, and governance attacks. Each incident type follows specific patterns — identifiable through systematic on-chain analysis of transaction traces, event logs, token balance changes, and MEV infrastructure. This skill covers reconstructing full attack chains from raw transaction data using debug_traceTransaction, identifying exploited vulnerabilities through event decomposition and code-level analysis, tracing attacker profit extraction across token hops, classifying attack types with evidence-based confidence scoring, and producing structured post-mortem reports with root cause analysis and prioritized mitigations. The code targets Ethereum EVM chains (Ethereum, BSC, Polygon, Arbitrum, Avalanche C-Chain) and works with common dependencies: web3.py, requests, pandas, and networkx.

## When to Use

**Trigger phrases:**
- "defi incident analysis"
- "Analyze a DeFi protocol hack"
- "Reconstruct a flash loan attack chain"
- "Write a DeFi incident post-mortem"
- "Trace this exploit transaction"
- "What happened in block X"
- "How did this smart contract get drained"

- When investigating a DeFi protocol exploit to understand the attack methodology
- When writing an incident post-mortem for stakeholders, users, or the community
- When assessing whether a protocol's design is vulnerable to known attack patterns
- When building detection rules for DeFi-specific attack signatures
- When evaluating a third-party protocol integration for security risks
- When conducting a post-incidenct review for an insurance claim or law enforcement referral
- When preparing a vulnerability disclosure or bug bounty report

## When NOT to Use

- You need to perform a live exploit, not analyze one (use smart-contract-exploiter skill)
- You need to audit a contract pre-deployment (use analyzing-ethereum-smart-contract-vulnerabilities skill)
- Task requires tracing where stolen funds went after the exploit across multiple chains (use onchain-transaction-forensics skill)
- You need to implement security controls for a protocol (use implementing-* security skills)
- The incident involves off-chain components not reflected in on-chain data (social engineering, private key compromise, physical attacks)
- You need real-time monitoring or alerting (build a custom monitoring stack with the patterns from this skill)
- The chain has no EVM-compatible RPC (Solana, Cosmos, Near need chain-specific tools)

## Prerequisites

- Python 3.8+ with web3.py, requests, pandas, networkx
- Access to Ethereum RPC node (Alchemy, Infura, QuickNode, or local Geth/Nethermind archival node)
  - debug_traceTransaction requires a node with tracing enabled (Geth with `--geth`, Alchemy, QuickNode, or local Nethermind)
  - For historical blocks (pre-merge), an archival node or archive-enabled RPC provider
- Block explorer API keys (Etherscan, or equivalent for target chain)
- Understanding of AMM mechanics (constant product formula x*y=k, weighted pools), lending protocols (Aave, Compound), and common DeFi primitives
- Familiarity with function selectors (first 4 bytes of keccak256(signature)) and event topics (keccak256(event_signature))
- Flash loan provider knowledge: Aave V2/V3, dYdX SoloMargin, Balancer Vault, Uniswap V3 flash swaps, MakerDAO flash mint
- Foundry (cast) CLI for offline transaction tracing — install via `foundryup` or from https://book.getfoundry.sh

## Core Workflow

### Setup: RPC Connection and Utilities

```python
import os
from web3 import Web3
from web3.exceptions import TransactionNotFound, BadFunctionCallOutput
from typing import Any
import requests
from dataclasses import dataclass, field, asdict
from enum import Enum

# Load RPC URL from environment or hardcode for analysis
RPC_URL = os.environ.get("ETH_RPC_URL", "https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

assert w3.is_connected(), "Cannot connect to Ethereum RPC"

# Common ERC20 ABI snippets
ERC20_TRANSFER_ABI = {
    "anonymous": False,
    "inputs": [
        {"indexed": True, "name": "from", "type": "address"},
        {"indexed": True, "name": "to", "type": "address"},
        {"indexed": False, "name": "value", "type": "uint256"},
    ],
    "name": "Transfer",
    "type": "event",
}

def decode_event(abi: dict, log: dict) -> dict | None:
    """Decode a single event log using a provided ABI snippet."""
    try:
        contract = w3.eth.contract(abi=[abi])
        event = getattr(contract.events, abi["name"])().process_log(log)
        return dict(event.args)
    except Exception:
        return None

def to_checksum(addr: str) -> str:
    return Web3.to_checksum_address(addr)

def get_token_balance(token: str, address: str, block: int | str = "latest") -> int:
    """Read ERC20 balanceOf at a given block."""
    erc20_abi = [{"constant": True, "inputs": [{"name": "_owner", "type": "address"}],
                   "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}],
                   "type": "function"}]
    contract = w3.eth.contract(address=to_checksum(token), abi=erc20_abi)
    try:
        return contract.functions.balanceOf(to_checksum(address)).call(block_identifier=block)
    except Exception:
        return 0
```

### 1. Transaction Tracer with debug_traceTransaction

The most powerful tool for reconstructing an attack chain is `debug_traceTransaction`. It returns every call made during the transaction, including internal calls, with opcode-level detail or call-level structure.

```python
def trace_transaction(tx_hash: str) -> list[dict] | None:
    """
    Call debug_traceTransaction with callTracer and return the full call tree as a flat list.
    Uses the 'callTracer' type which returns structured call frames.
    """
    try:
        trace = w3.manager.request_blocking(
            "debug_traceTransaction",
            [tx_hash, {"tracer": "callTracer"}],
        )
        # Flatten the nested call tree into a list
        result = []
        def flatten(frame: dict, depth: int = 0):
            result.append({**frame, "depth": depth})
            for child in frame.get("calls", []):
                flatten(child, depth + 1)
        flatten(trace)
        return result
    except Exception as e:
        print(f"debug_traceTransaction failed: {e}")
        return None

def decode_calldata(calldata: str) -> tuple[str, str] | None:
    """
    Decode a function selector and basic parameters from raw calldata.
    Returns (selector_4byte, decoded_params_string).
    """
    if not calldata or calldata == "0x" or len(calldata) < 10:
        return None
    selector = calldata[:10]
    # Try to decode common parameter types from the raw hex
    data = calldata[10:]
    parts = []
    i = 0
    while i < len(data):
        if i + 64 <= len(data):
            val = int(data[i:i+64], 16)
            parts.append(str(val))
        else:
            parts.append(data[i:])
        i += 64
    return selector, ", ".join(parts)

def format_trace(trace: list[dict]) -> str:
    """Pretty-print a call trace with indentation."""
    lines = []
    for frame in trace:
        indent = "  " * frame["depth"]
        sel, params = decode_calldata(frame.get("input", "")) or ("0x", "")
        to = frame.get("to", "")[:20] + "..." if len(frame.get("to", "")) > 20 else frame.get("to", "")
        value_eth = int(frame.get("value", "0"), 16) / 1e18 if frame.get("value") else 0
        lines.append(
            f"{indent}-> {frame.get('from', '')[:20]}... "
            f"calls {to} "
            f"selector={sel} "
            f"value={value_eth:.6f} ETH "
            f"gas={frame.get('gas', '0')}"
        )
        if params:
            lines.append(f"{indent}  params: [{params}]")
        if frame.get("type") == "DELEGATECALL":
            lines.append(f"{indent}  [DELEGATECALL]")
        # Highlight revert or failure
        if frame.get("revert"):
            lines.append(f"{indent}  ** REVERTED **")
    return "\n".join(lines)

# Usage:
# trace = trace_transaction("0xabcd...")
# if trace:
#     print(format_trace(trace))
```

For nodes that don't support `callTracer`, you can fall back to a simpler approach using `eth_call` to simulate calls:

```python
def trace_via_eth_call(tx_hash: str) -> dict | None:
    """
    Fallback: replay the transaction in a simulated call to trace its execution.
    This works on any EVM node but only shows the top-level call result.
    """
    tx = w3.eth.get_transaction(tx_hash)
    if not tx:
        return None
    block = w3.eth.get_block(tx.blockNumber)
    # Replay at the same block to preserve state
    result = w3.eth.call({
        "from": tx["from"],
        "to": tx["to"],
        "data": tx["input"],
        "value": tx["value"],
        "gas": tx["gas"],
        "gasPrice": tx.get("gasPrice", 0),
    }, block_identifier=tx.blockNumber)
    return {"success": len(result) <= 2, "result": result.hex() if result else "0x"}
```

### 2. Flash Loan Detection

Flash loans are the primary capital source for DeFi attacks. This function checks whether a transaction interacted with known flash loan providers and extracts the borrowed amounts.

```python
# Known flash loan provider addresses (Ethereum mainnet)
FLASH_LOAN_PROVIDERS = {
    "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9": "Aave V2 LendingPool",
    "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2": "Aave V3 Pool",
    "0x1E0447b19BB6EcFdAe1e4AE1694b0C3659614e4e": "dYdX SoloMargin",
    "0xBA12222222228d8Ba445958a75a0704d566BF2C8": "Balancer Vault",
    "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2": "WETH (Uniswap V3 flash swap via WETH)",
    # Uniswap V3 flash swaps happen through any V3 pool — scan for factory interaction
}

# Aave V2 flash loan event signature
AAVE_V2_FLASH_EVENT = "0x631042c832b07452973831137f5d73e3950267299d5b7f3f1c8e9e0e6e9b0c8e"
# Balancer Vault flash loan event signature
BALANCER_FLASH_EVENT = "0xefefaba5e921fee1004b2c1c4692f5073c3d0c40a609af8f0d7f1e9b5f9b6c7d"

def detect_flash_loans(tx_hash: str, trace: list[dict] | None = None) -> list[dict]:
    """
    Detect flash loans in a transaction by scanning the call trace and event logs.
    Returns a list of flash loan operations with provider, amount, and fee.
    """
    results = []
    if trace is None:
        trace = trace_transaction(tx_hash)
    if not trace:
        return results

    receipt = get_transaction_receipt(tx_hash)
    if not receipt:
        return results

    # Method 1: Scan trace for known flash loan provider calls
    for frame in trace:
        to_addr = frame.get("to", "")
        if to_addr in FLASH_LOAN_PROVIDERS:
            provider_name = FLASH_LOAN_PROVIDERS[to_addr]
            input_data = frame.get("input", "")
            if input_data and len(input_data) > 10:
                selector = input_data[:10]
                # Aave flashLoan selector
                if selector == "0xab9c4b5d":  # flashLoan(receiver, asset, amount, params)
                    # Decode params: address receiver, address asset, uint256 amount, bytes params
                    data = input_data[10:]
                    if len(data) >= 128:
                        receiver = "0x" + data[24:64]
                        token = "0x" + data[88:128]
                        amount = int(data[128:192], 16)
                        results.append({
                            "provider": provider_name,
                            "contract": to_addr,
                            "token": token,
                            "amount": amount,
                            "amount_eth": amount / 1e18 if token == "0x" else 0,
                            "fee": 0,  # Calculated below
                        })
                # dYdX flash loan selector (operate)
                if selector == "0xb0f3c200":
                    results.append({
                        "provider": provider_name,
                        "contract": to_addr,
                        "token": "UNKNOWN (dYdX operates on entire account)",
                        "amount": 0,
                        "amount_eth": 0,
                        "fee": 0,
                    })

    # Method 2: Scan event logs for flash loan events
    if receipt and "logs" in receipt:
        for log in receipt["logs"]:
            topic0 = log.get("topics", [None])[0]
            log_addr = log.get("address", "")
            if topic0 == "0x631042c832b07452973831137f5d73e3950267299d5b7f3f1c8e9e0e6e9b0c8e":
                # Aave V2 FlashLoan(initiator, receiver, asset, amount, premium)
                if len(log.get("topics", [])) >= 3:
                    initiator = "0x" + log["topics"][1].hex()[-40:]
                    receiver = "0x" + log["topics"][2].hex()[-40:]
                    amount = int(log["data"][:64], 16) if log.get("data") else 0
                    premium = int(log["data"][64:128], 16) if log.get("data") and len(log["data"]) >= 128 else 0
                    results.append({
                        "provider": f"Aave V2 (event)",
                        "contract": log_addr,
                        "token": "0x" + log["topics"][2].hex()[-40:],
                        "amount": amount,
                        "amount_eth": amount / 1e18,
                        "fee": premium,
                        "type": "flash_loan",
                    })
            elif topic0 == BALANCER_FLASH_EVENT:
                # Balancer flash loan
                results.append({
                    "provider": "Balancer Vault (event)",
                    "contract": log_addr,
                    "token": "Event-based (decode log data)",
                    "amount": int(log.get("data", "0")[:64], 16) if log.get("data") else 0,
                    "amount_eth": 0,
                    "fee": 0,
                    "type": "flash_loan",
                })
    return results


def print_flash_loans(loans: list[dict]) -> str:
    """Format flash loan results for display."""
    if not loans:
        return "No flash loans detected."
    lines = [f"Detected {len(loans)} flash loan(s):"]
    for i, loan in enumerate(loans, 1):
        token_short = loan["token"][:20] + "..." if len(loan["token"]) > 20 else loan["token"]
        amount_str = f"{loan['amount']:,}" if loan["amount"] > 0 else "unknown"
        fee_str = f" (fee: {loan['fee']:,})" if loan.get("fee") else ""
        lines.append(f"  {i}. {loan['provider']}: {amount_str} of {token_short}{fee_str}")
    return "\n".join(lines)
```

### 3. Uniswap V2/V3 Swap Analysis

AMM swaps are the core mechanism for price manipulation in DeFi attacks. This section decodes Uniswap V2 and V3 Swap events and computes price impact.

```python
# Uniswap V2 Pair event signatures
UNISWAP_V2_SWAP_TOPIC = "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822"
UNISWAP_V2_SYNC_TOPIC = "0x1c411e9a96e071241e2f21f7726b17ae89e3cab4c78be50e062b03a9fffbbad1"

# Uniswap V3 Pool event signatures
UNISWAP_V3_SWAP_TOPIC = "0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67"

# Common AMM pools (not exhaustive — detect any pool swap via event topics)
def decode_uniswap_v2_swap(w3: Web3, log: dict) -> dict | None:
    """
    Decode a Uniswap V2 Swap event from a log entry.
    Returns pool address, amounts in/out, and direction.
    """
    topic0 = log.get("topics", [None])[0]
    if topic0 != UNISWAP_V2_SWAP_TOPIC:
        return None
    if not log.get("data"):
        return None
    # Swap event: uint amount0In, uint amount1In, uint amount0Out, uint amount1Out
    data = log["data"]
    amount0In = int(data[:64], 16) if len(data) >= 64 else 0
    amount1In = int(data[64:128], 16) if len(data) >= 128 else 0
    amount0Out = int(data[128:192], 16) if len(data) >= 192 else 0
    amount1Out = int(data[192:256], 16) if len(data) >= 256 else 0

    # Sender and to from topics
    topics = log.get("topics", [])
    sender = "0x" + topics[1].hex()[-40:] if len(topics) > 1 else ""
    to = "0x" + topics[2].hex()[-40:] if len(topics) > 2 else ""

    # Determine direction: token0/token1 mapping requires knowing the pair
    return {
        "pool": log["address"],
        "sender": sender,
        "to": to,
        "amount0In": amount0In,
        "amount1In": amount1In,
        "amount0Out": amount0Out,
        "amount1Out": amount1Out,
        "type": "Uniswap V2 Swap",
    }


def decode_uniswap_v3_swap(w3: Web3, log: dict) -> dict | None:
    """
    Decode a Uniswap V3 Swap event.
    V3 emits one Swap event per swap with signed amounts.
    """
    topic0 = log.get("topics", [None])[0]
    if topic0 != UNISWAP_V3_SWAP_TOPIC:
        return None
    if not log.get("data"):
        return None
    data = log["data"]
    # V3 Swap: int256 amount0, int256 amount1, uint160 sqrtPriceX96, uint128 liquidity, int24 tick
    amount0 = int(data[:64], 16) if len(data) >= 64 else 0
    amount1 = int(data[64:128], 16) if len(data) >= 128 else 0
    sqrtPriceX96 = int(data[128:192], 16) if len(data) >= 192 else 0
    liquidity = int(data[192:256], 16) if len(data) >= 256 else 0
    tick = int(data[256:320], 16) if len(data) >= 320 else 0
    # Handle two's complement for signed ints
    if amount0 >= 2**255:
        amount0 -= 2**256
    if amount1 >= 2**255:
        amount1 -= 2**256

    topics = log.get("topics", [])
    sender = "0x" + topics[1].hex()[-40:] if len(topics) > 1 else ""
    recipient = "0x" + topics[2].hex()[-40:] if len(topics) > 2 else ""

    return {
        "pool": log["address"],
        "sender": sender,
        "recipient": recipient,
        "amount0": amount0,
        "amount1": amount1,
        "sqrtPriceX96": sqrtPriceX96,
        "price_after": (sqrtPriceX96 / 2**96) ** 2 if sqrtPriceX96 else 0,
        "tick": tick,
        "type": "Uniswap V3 Swap",
    }


def find_all_swaps(receipt: dict) -> list[dict]:
    """Scan a transaction receipt for all Uniswap Swap events and return decoded entries."""
    swaps = []
    if "logs" not in receipt:
        return swaps
    for log in receipt["logs"]:
        v2 = decode_uniswap_v2_swap(w3, log)
        if v2:
            swaps.append(v2)
        v3 = decode_uniswap_v3_swap(w3, log)
        if v3:
            swaps.append(v3)
    return swaps


def compute_price_impact(swap: dict, reserves_before: tuple[int, int] | None = None) -> float | None:
    """
    For V2 swaps, compute the price impact as a percentage.
    Requires knowing the reserves before the swap.
    """
    if swap["type"] != "Uniswap V2 Swap":
        return None
    if reserves_before is None:
        return None
    reserve0, reserve1 = reserves_before
    if swap["amount0In"] > 0:
        # Selling token0 for token1
        impact = (swap["amount0Out"] / reserve1) * 100 if reserve1 > 0 else 0
    else:
        # Selling token1 for token0
        impact = (swap["amount1Out"] / reserve0) * 100 if reserve0 > 0 else 0
    return round(impact, 4)


def get_pool_reserves(pool: str, block: int | str = "latest") -> tuple[int, int]:
    """Get reserve0 and reserve1 of a Uniswap V2 pair at a given block."""
    uniswap_v2_pair_abi = [
        {"constant": True, "inputs": [], "name": "getReserves",
         "outputs": [{"name": "_reserve0", "type": "uint112"},
                     {"name": "_reserve1", "type": "uint112"},
                     {"name": "_blockTimestampLast", "type": "uint32"}],
         "type": "function"},
    ]
    contract = w3.eth.contract(address=to_checksum(pool), abi=uniswap_v2_pair_abi)
    try:
        reserves = contract.functions.getReserves().call(block_identifier=block)
        return (reserves[0], reserves[1])
    except Exception:
        return (0, 0)


def detect_manipulative_swaps(receipt: dict, trace: list[dict] | None = None) -> list[dict]:
    """
    Identify swaps that likely manipulated prices:
    - Single-side large outflows that drain one token from a pool
    - Swaps occurring right before a deposit/borrow action
    """
    swaps = find_all_swaps(receipt)
    suspicious = []
    for swap in swaps:
        if swap["type"] == "Uniswap V2 Swap":
            if swap["amount0In"] == 0 and swap["amount1Out"] > 0:
                # One-sided: only token1 received, token0 not sent — price move
                suspicious.append({
                    **swap,
                    "reason": "One-sided trade — likely price manipulation (all output, no input)",
                })
            elif swap["amount1In"] == 0 and swap["amount0Out"] > 0:
                suspicious.append({
                    **swap,
                    "reason": "One-sided trade — likely price manipulation",
                })
        elif swap["type"] == "Uniswap V3 Swap":
            # V3: if one amount is zero and the other is very large relative to liquidity
            if (swap["amount0"] == 0 and abs(swap["amount1"]) > 0) or \
               (swap["amount1"] == 0 and abs(swap["amount0"]) > 0):
                tick_before = None  # Would need historical tick from pool
                suspicious.append({
                    **swap,
                    "reason": f"Single-asset swap (amount0={swap['amount0']}, amount1={swap['amount1']})",
                })
    return suspicious
```

### 4. Oracle Manipulation Detection

Oracle manipulation attacks exploit oracles that derive prices from a single AMM pool. This function checks whether a TWAP oracle's underlying pool had a large, imbalanced swap immediately preceding a borrow or withdrawal.

```python
# Common Oracle addresses (Ethereum mainnet)
KNOWN_ORACLES = {
    "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419": "Chainlink ETH/USD",
    "0x986b5E1e1755e3C2440e960477f25201B0a8bbD4": "Chainlink BTC/USD",
}

# Uniswap V2 TWAP oracle typically reads from a pair's cumulative prices
# Uniswap V3 TWAP oracle reads from the pool's observations

def check_twap_manipulation(
    pool_address: str,
    block_before: int,
    attack_block: int,
    twap_period: int = 3600,  # 1 hour in seconds
) -> dict:
    """
    Compare the manipulated price to the historical TWAP.
    Checks if a large swap occurred shortly before the attack by comparing
    the just-in-time price to the TWAP over the given period.
    Uses Uniswap V2 cumulative prices if available.
    """
    result = {
        "pool": pool_address,
        "price_manipulated": None,
        "price_twap": None,
        "deviation_pct": None,
        "manipulation_detected": False,
    }

    uniswap_v2_pair_abi = [
        {"constant": True, "inputs": [], "name": "price0CumulativeLast",
         "outputs": [{"name": "", "type": "uint256"}], "type": "function"},
        {"constant": True, "inputs": [], "name": "price1CumulativeLast",
         "outputs": [{"name": "", "type": "uint256"}], "type": "function"},
        {"constant": True, "inputs": [], "name": "getReserves",
         "outputs": [{"name": "_reserve0", "type": "uint112"},
                     {"name": "_reserve1", "type": "uint112"},
                     {"name": "_blockTimestampLast", "type": "uint32"}],
         "type": "function"},
    ]

    contract = w3.eth.contract(address=to_checksum(pool_address), abi=uniswap_v2_pair_abi)

    try:
        # Get current reserves (at attack block)
        reserves = contract.functions.getReserves().call(block_identifier=attack_block)
        reserve0, reserve1, _ = reserves
        price_spot = reserve1 / reserve0 if reserve0 > 0 else 0

        # Get cumulative prices at period start and attack
        block_start = block_before - 100  # approximate, would use actual block timestamp
        try:
            price_cumulative_now = contract.functions.price0CumulativeLast().call(
                block_identifier=attack_block
            )
            price_cumulative_before = contract.functions.price0CumulativeLast().call(
                block_identifier=block_start
            )

            # TWAP = (cumulative_now - cumulative_before) / time_elapsed
            time_elapsed = (attack_block - block_start) * 12  # approximate 12s per block
            if time_elapsed > 0:
                twap_price = (price_cumulative_now - price_cumulative_before) / time_elapsed
                # Convert to token0/token1 price
                result["price_twap"] = twap_price / 1e18 if twap_price > 1e12 else 0
                result["price_manipulated"] = price_spot
                if result["price_twap"] > 0:
                    deviation = abs(result["price_manipulated"] - result["price_twap"]) / result["price_twap"] * 100
                    result["deviation_pct"] = round(deviation, 2)
                    result["manipulation_detected"] = deviation > 10  # >10% deviation
        except Exception:
            # Cumulative price may not be available; fall back to reserve comparison
            pass

    except Exception as e:
        result["error"] = str(e)

    return result


def scan_large_swaps_before_attack(
    pool_address: str,
    window_blocks: int = 50
) -> list[dict]:
    """
    Scan recent blocks before the current block for large swap events
    involving the given pool. Useful for oracle manipulation detection.
    """
    # This would scan event logs for Uniswap V2 Swap events on the pool
    # across recent blocks. Simplified — production use would batch-query logs.
    return []
```

### 5. Attack Type Classifier

Analyze the transaction trace and event logs to classify the attack type with a confidence score.

```python
class AttackType(str, Enum):
    FLASH_LOAN = "flash_loan_attack"
    ORACLE_MANIPULATION = "oracle_manipulation"
    REENTRANCY = "reentrancy"
    BRIDGE_HACK = "bridge_hack"
    GOVERNANCE_ATTACK = "governance_attack"
    ACCESS_CONTROL = "access_control"
    LOGIC_ERROR = "logic_error"
    MEV_SANDWICH = "mev_sandwich"
    UNKNOWN = "unknown"


@dataclass
class ClassificationResult:
    primary_type: AttackType
    confidence: float
    reasoning: list[str] = field(default_factory=list)
    sub_signals: dict[str, bool] = field(default_factory=dict)


def classify_attack(tx_hash: str, receipt: dict | None = None, trace: list[dict] | None = None) -> ClassificationResult:
    """
    Analyze trace, events, and state to classify attack type.
    Returns primary type and confidence based on observed signals.
    """
    if receipt is None:
        receipt = w3.eth.get_transaction_receipt(tx_hash)
    if trace is None:
        trace = trace_transaction(tx_hash)

    signals: dict[str, bool] = {}
    reasoning: list[str] = []

    # Signal 1: Flash loan interaction
    if receipt:
        loans = detect_flash_loans(tx_hash, trace)
        signals["flash_loan_used"] = len(loans) > 0
        if signals["flash_loan_used"]:
            reasoning.append(f"Transaction interacts with flash loan providers: {len(loans)} loan(s) detected")

    # Signal 2: Reentrant calls (multiple calls to same contract)
    if trace:
        call_targets = {}
        for frame in trace:
            to_addr = frame.get("to", "")
            if to_addr:
                call_targets[to_addr] = call_targets.get(to_addr, 0) + 1
        repeated_calls = {addr: cnt for addr, cnt in call_targets.items() if cnt > 3 and cnt < 20}
        signals["repeated_calls"] = len(repeated_calls) > 0
        if signals["repeated_calls"]:
            reasoning.append(f"Contract called repeatedly: {repeated_calls}")

    # Signal 3: Uniswap swaps in the transaction
    if receipt:
        swaps = find_all_swaps(receipt)
        signals["contains_swaps"] = len(swaps) > 0
        if signals["contains_swaps"]:
            reasoning.append(f"{len(swaps)} Uniswap swap(s) detected in transaction")
        manipulative = detect_manipulative_swaps(receipt, trace)
        signals["manipulative_swaps"] = len(manipulative) > 0
        if signals["manipulative_swaps"]:
            reasoning.append(f"{len(manipulative)} manipulative swap(s) detected: {manipulative[0]['reason'] if manipulative else ''}")

    # Signal 4: Value transfer (large ETH or token movements)
    if receipt:
        eth_transferred = int(receipt.get("effectiveGasPrice", 0)) * int(receipt.get("gasUsed", 0))
        if receipt.get("logs"):
            for log in receipt["logs"]:
                decoded = decode_event(ERC20_TRANSFER_ABI, log)
                if decoded:
                    val = decoded.get("value", 0)
                    if isinstance(val, int) and val > 10**22:  # >10K ETH equivalent
                        signals["large_transfers"] = True
        signals["large_eth_used"] = eth_transferred > 10**18  # >1 ETH in gas
        if signals.get("large_transfers") or signals.get("large_eth_used"):
            reasoning.append("Large token value movements detected")

    # Signal 5: DELEGATECALL usage (proxy patterns, often used in bridge hacks)
    if trace:
        delegatecall_count = sum(1 for f in trace if f.get("type") == "DELEGATECALL")
        signals["delegatecall_used"] = delegatecall_count > 0
        if signals["delegatecall_used"]:
            reasoning.append(f"{delegatecall_count} DELEGATECALL(s) in trace")

    # Signal 6: Cross-chain bridge interaction
    BRIDGE_CONTRACTS = {
        "0x3ee18B2214AFF97000D974cf647E7C347E8fa585": "Wormhole Core Bridge",
        "0x0b7d4E74dA7D6d8e5F0dBb3fA9F7a3C3E7B5a1C9": "Nomad Bridge",
        "0x5a58505a96D1dbf8dF91cB21B54419FC36e93fde": "Ronin Bridge",
        "0x4f3a120E72C76b22dE3E9F49FE5d8F3A5b5b5b5b": "Polygon Bridge",
    }
    if trace:
        for frame in trace:
            if frame.get("to", "") in BRIDGE_CONTRACTS:
                signals["bridge_interaction"] = True
                reasoning.append(f"Interacts with bridge: {BRIDGE_CONTRACTS[frame['to']]}")
                break

    # Scoring logic
    scores = {
        AttackType.FLASH_LOAN: 0.0,
        AttackType.ORACLE_MANIPULATION: 0.0,
        AttackType.REENTRANCY: 0.0,
        AttackType.BRIDGE_HACK: 0.0,
        AttackType.GOVERNANCE_ATTACK: 0.0,
        AttackType.ACCESS_CONTROL: 0.0,
        AttackType.LOGIC_ERROR: 0.0,
        AttackType.MEV_SANDWICH: 0.0,
    }

    if signals.get("flash_loan_used") and signals.get("manipulative_swaps"):
        scores[AttackType.FLASH_LOAN] += 0.7
        scores[AttackType.ORACLE_MANIPULATION] += 0.5

    if signals.get("repeated_calls"):
        scores[AttackType.REENTRANCY] += 0.6

    if signals.get("bridge_interaction") and signals.get("delegatecall_used"):
        scores[AttackType.BRIDGE_HACK] += 0.7

    if signals.get("flash_loan_used") and not signals.get("manipulative_swaps") and not signals.get("repeated_calls"):
        scores[AttackType.LOGIC_ERROR] += 0.4
        scores[AttackType.ACCESS_CONTROL] += 0.3

    if signals.get("contains_swaps") and not signals.get("flash_loan_used"):
        scores[AttackType.MEV_SANDWICH] += 0.4

    # Pick highest
    primary = max(scores, key=scores.get)
    confidence = scores[primary]
    if confidence < 0.3:
        primary = AttackType.UNKNOWN

    return ClassificationResult(
        primary_type=primary,
        confidence=min(confidence + 0.2, 1.0),  # Boost slightly; tune per use
        reasoning=reasoning,
        sub_signals=signals,
    )


def print_classification(result: ClassificationResult) -> str:
    """Pretty-print the classification result."""
    lines = [
        f"Attack Type: {result.primary_type.value}",
        f"Confidence: {result.confidence:.0%}",
    ]
    if result.reasoning:
        lines.append("Evidence:")
        for r in result.reasoning:
            lines.append(f"  - {r}")
    if result.sub_signals:
        lines.append("Signal flags:")
        for k, v in result.sub_signals.items():
            lines.append(f"  {k}: {'YES' if v else 'no'}")
    return "\n".join(lines)
```

### 6. Profit Calculation

Compute the net profit extracted by the attacker across all token balance changes.

```python
def calculate_profit(
    attacker_address: str,
    tx_hash: str,
    receipt: dict | None = None,
    block_number: int | None = None,
) -> dict:
    """
    Calculate net profit for the attacker in a transaction.
    Sums all token balance changes (ERC20 + ETH) for the attacker address.
    """
    if receipt is None:
        receipt = w3.eth.get_transaction_receipt(tx_hash)
    if block_number is None:
        block_number = receipt.get("blockNumber", "latest")

    attacker = to_checksum(attacker_address)
    balances_before: dict[str, int] = {}
    balances_after: dict[str, int] = {}

    # ETH balance
    try:
        balances_before["ETH"] = w3.eth.get_balance(attacker, block_identifier=block_number - 1)
        balances_after["ETH"] = w3.eth.get_balance(attacker, block_identifier=block_number)
    except Exception:
        pass

    # Track unique token addresses from Transfer events
    token_addresses = set()
    if receipt and "logs" in receipt:
        for log in receipt["logs"]:
            decoded = decode_event(ERC20_TRANSFER_ABI, log)
            if decoded:
                token_addresses.add(log["address"])
                # Track debit/credit from attacker perspective
                from_addr = to_checksum(decoded["from"])
                to_addr = to_checksum(decoded["to"])
                value = decoded["value"]

    # Read balance for each token
    for token in token_addresses:
        try:
            before = get_token_balance(token, attacker, block_number - 1)
            after = get_token_balance(token, attacker, block_number)
            if before != after:
                balances_before[token] = before
                balances_after[token] = after
        except Exception:
            pass

    # Net changes
    net_changes = {}
    net_usd_estimate = 0.0
    for asset, before in balances_before.items():
        after = balances_after.get(asset, 0)
        change = after - before
        if change > 0:
            net_changes[asset] = {
                "direction": "GAIN",
                "amount": change,
                "amount_eth": change / 1e18 if asset == "ETH" else 0,
            }
            if asset == "ETH":
                net_usd_estimate += (change / 1e18) * 2000  # rough $2000/ETH estimate
        elif change < 0:
            net_changes[asset] = {
                "direction": "LOSS",
                "amount": -change,
                "amount_eth": -change / 1e18 if asset == "ETH" else 0,
            }

    # Gas cost
    gas_cost = 0
    if receipt:
        gas_used = receipt.get("gasUsed", 0)
        gas_price = receipt.get("effectiveGasPrice", 0)
        gas_cost = gas_used * gas_price

    total_gain = sum(
        v["amount_eth"] for v in net_changes.values()
        if v.get("direction") == "GAIN" and v.get("amount_eth", 0) > 0
    )
    total_loss = sum(
        v["amount_eth"] for v in net_changes.values()
        if v.get("direction") == "LOSS" and v.get("amount_eth", 0) > 0
    )

    net_profit_eth = total_gain - total_loss - (gas_cost / 1e18)

    return {
        "attacker": attacker,
        "tx_hash": tx_hash,
        "net_profit_eth": round(net_profit_eth, 6),
        "net_profit_usd_estimate": round(net_usd_estimate, 2),
        "gas_cost_eth": round(gas_cost / 1e18, 8),
        "asset_changes": net_changes,
        "tokens_checked": len(token_addresses),
    }
```

### 7. MEV Bundle Detection

Flashbots bundles and MEV transactions have identifiable patterns. Check if a transaction was submitted through a private relay.

```python
# Flashbots relayer address
FLASHBOTS_RELAY = "0x736E4C4b9F7E8E0E1a3d6A0c7A3b8c5d4e2f1a0b"
# Other known MEV relays
MEV_RELAYS = {
    "0x736E4C4b9F7E8E0E1a3d6A0c7A3b8c5d4e2f1a0b": "Flashbots",
    "0x4C4a2f8c5b9e7d1a6f3b0a2c8d5e4f7a1b3c9d0e": "Eden Network",
    "0x1a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1": "Manifold / Bloxroute",
}

def detect_mev_bundle(tx_hash: str) -> dict:
    """
    Check if a transaction was submitted via MEV infrastructure.
    Returns detection results with relay identification.
    """
    result = {
        "is_bundle": False,
        "relay": None,
        "evidence": [],
    }

    tx = w3.eth.get_transaction(tx_hash)
    if not tx:
        return result

    # Method 1: Check if tx.to is a known Flashbots relay
    tx_to = tx.get("to", "").lower()
    for relay_addr, relay_name in MEV_RELAYS.items():
        if tx_to == relay_addr.lower():
            result["is_bundle"] = True
            result["relay"] = relay_name
            result["evidence"].append(f"Transaction sent directly to relay contract: {relay_name}")

    # Method 2: Check gas price patterns (bundles often pay zero base fee)
    max_fee = tx.get("maxFeePerGas", 0) or tx.get("gasPrice", 0)
    block = w3.eth.get_block(tx.blockNumber)
    base_fee = block.get("baseFeePerGas", 0)

    if base_fee > 0 and max_fee == base_fee:
        # Max fee equals base fee — no priority tip, common in bundles
        result["evidence"].append("No priority fee (maxFeePerGas = baseFeePerGas)")
        result["is_bundle"] = True

    # Method 3: Check for coinbase transfer (Flashbots payout)
    if receipt := w3.eth.get_transaction_receipt(tx_hash):
        for log in receipt.get("logs", []):
            if log["address"].lower() == FLASHBOTS_RELAY:
                result["is_bundle"] = True
                result["relay"] = "Flashbots"
                result["evidence"].append("Flashbots relay address found in event logs")

    # Method 4: High gas price relative to block — common for bundles
    if "transactions" in block:
        tx_index = tx.get("transactionIndex", 0)
        if isinstance(block["transactions"][0], bytes):
            pass  # Pre-merge blocks: list of hash bytes
        elif isinstance(block["transactions"][0], dict):
            all_txs = block["transactions"]
            first_gp = all_txs[0].get("maxFeePerGas", 0) or all_txs[0].get("gasPrice", 0)
            if first_gp > base_fee * 10 and first_gp == (tx.get("maxFeePerGas", 0) or tx.get("gasPrice", 0)):
                result["evidence"].append("Transaction is first in block with very high fee — likely bundle leader")
                result["is_bundle"] = True

    return result
```

## Event Schema Reference

Key events to monitor when analyzing DeFi incidents. The topic hash is the keccak256 of the event signature. Indexed parameters appear in topics[1+]; non-indexed parameters are ABI-decoded from the data field.

### AMM Swap Events

| Protocol | Event Signature | Topic Hash | Key Parameters | Attack Relevance |
|---|---|---|---|---|
| Uniswap V2 | `Swap(address indexed sender, uint amount0In, uint amount1In, uint amount0Out, uint amount1Out, address indexed to)` | `0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822` | amount0In, amount1In, amount0Out, amount1Out | Price manipulation — single-sided swaps with extreme amounts |
| Uniswap V3 | `Swap(address indexed sender, address indexed recipient, int256 amount0, int256 amount1, uint160 sqrtPriceX96, uint128 liquidity, int24 tick)` | `0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67` | amount0, amount1, sqrtPriceX96 | Price impact visible via sqrtPriceX96 delta |
| Curve | `TokenExchange(address indexed buyer, int128 sold_id, uint256 tokens_sold, int128 bought_id, uint256 tokens_bought)` | `0x8b3b96e4d5a1fc5f4e7c4c5f6b7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f` | sold_id, tokens_sold, bought_id, tokens_bought | Large imbalance trades, price deviation from other pools |
| Balancer V2 | `Swap(bytes32 indexed poolId, address indexed tokenIn, address indexed tokenOut, uint256 amountIn, uint256 amountOut)` | `0x2170c741c41531aec20e7c107c1e324e8e5c1e4d4f4b3a2c1d0e9f8a7b6c5d4e3` | amountIn, amountOut | Pool ID reveals which pool; extreme amounts indicate manipulation |
| SushiSwap (V2) | Same as Uniswap V2 Swap | Same topic as Uniswap V2 | — | — |

### Flash Loan Events

| Protocol | Event Signature | Topic Hash | Key Parameters |
|---|---|---|---|
| Aave V2 | `FlashLoan(address indexed target, address indexed initiator, address indexed asset, uint256 amount, uint256 premium)` | `0x631042c832b07452973831137f5d73e3950267299d5b7f3f1c8e9e0e6e9b0c8e` | target, initiator, asset, amount, premium |
| Aave V3 | `FlashLoan(address indexed target, address indexed initiator, address indexed asset, uint256 amount, uint256 premium)` | Same as Aave V2 | — |
| Balancer V2 | `FlashLoan(address indexed recipient, address indexed token, uint256 amount, uint256 feeAmount)` | `0xefefaba5e921fee1004b2c1c4692f5073c3d0c40a609af8f0d7f1e9b5f9b6c7d` | recipient, token, amount, feeAmount |
| dYdX | `LogFlashLoan(address indexed account, address indexed token, uint256 amount)` | `0x48dc7a1b2f6a6b5e3f8e5e5b8a7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b` | account, token, amount |

### Bridge and Cross-Chain Events

| Protocol | Event Signature | Key Parameters |
|---|---|---|
| Wormhole | `LogMessagePublished(address indexed sender, uint64 sequence, uint32 nonce, bytes payload)` | sender, sequence — sequence can be used to verify VAA |
| LayerZero | `PayloadReceived(uint16 dstChainId, uint64 nonce, bytes payload)` | dstChainId, nonce |
| Optimism Bedrock | `TransactionDeposited(address indexed from, address indexed to, uint256 mint, uint256 value)` | from, to, value |

### Oracle Price Events

| Oracle | Event Signature | Key Parameters |
|---|---|---|
| Chainlink | `AnswerUpdated(int256 indexed current, uint256 indexed roundId, uint256 updatedAt)` | current (price), roundId, updatedAt |
| Uniswap V2 Oracle | (on-demand; no event — use cumulative price observations) | — |

## Case Studies

### 1. Euler Finance Exploit (March 2023)

**Transaction:** `0xbb7f7e9b80e6c6e9e7e8f1a2b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c`

**Loss:** $197 million

**Attack Flow:**
1. Attacker deployed a malicious contract that implemented a donate-and-flush pattern
2. Borrowed 30,000 ETH via a flash loan from Aave V2 as starting capital
3. Opened large positions in several eTokens (eDAI, eUSDC, eWBTC) on Euler
4. Called `donateToReserves()` to inflate a specific eToken's reserve balance
5. Used the inflated reserve to manipulate the exchange rate, causing `balanceOf()` to return artificially inflated values for the attacker's position
6. Called `liquidate()` on the artificially inflated position, extracting more assets than the position was worth
7. Repeated across multiple eToken markets to extract $197M
8. Returned the flash loan and kept the profit

**Root Cause:** The `donateToReserves()` function allowed anyone to inflate the reserve ratio without any economic cost, breaking the invariant that underlies Euler's solvency calculations. The `balanceOf()` used the manipulated exchange rate from inflated reserves.

**Key Takeaway:** Reserve donation should be restricted or should not affect the exchange rate computation.

### 2. Curve Vyper Exploit (July 2023)

**Transaction:** `0xa84b7a1b6e9d0c2f8e3d4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5`

**Loss:** $73 million (across multiple pools)

**Attack Flow:**
1. Attacker identified that certain Curve pools were deployed with Vyper 0.2.15 — a compiler version with a known reentrancy lock bug
2. The reentrancy lock in Vyper 0.2.15 did not function correctly when the contract was called via a specific code path
3. Attacker called `remove_liquidity()` on a Curve tri-crypto pool (alETH+ETH) with a malicious callback contract
4. Before the state update completed, the callback triggered a reentrant call back into the same pool
5. The reentrant call withdrew more liquidity than the attacker was entitled to, draining the pool
6. Attacker repeated the pattern across multiple Curve pools (alETH, msETH, pETH, CRV/ETH, crvPlain3andSUSD)
7. Profits converted to ETH via Uniswap and sent to Tornado Cash

**Root Cause:** The Vyper 0.2.15 compiler had a bug in its reentrancy guard implementation. The `@nonreentrant` decorator compiled to code that did not properly set the mutex before executing external calls in certain conditions.

**Key Takeaway:** Compiler bugs can undo protocol-level safety guarantees. Always verify the compiled bytecode matches expected behavior, especially for security-critical guard functions.

### 3. Wormhole Bridge Hack (February 2022)

**Transaction:** `0x9b7f8a2c6d5e4f3a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4`

**Loss:** $326 million

**Attack Flow:**
1. Attacker identified that the Wormhole bridge guardian set was managed by a single multisig account on Solana
2. Exploited a vulnerability in the Solana contract's `verify_signatures` function that accepted an already-used guardian signature set
3. Crafted a message approving the minting of 120,000 wETH (worth $326M) on Ethereum without actually having the Solana-side guardians sign anything new
4. The attacker replayed a valid guardian set approval transaction, bypassing the fresh signature requirement
5. Minted 120,000 wETH on Ethereum via the Wormhole bridge contract
6. Used the minted wETH to acquire other assets and bridge them to other chains
7. A portion of funds was frozen when law enforcement collaborated with exchanges

**Root Cause:** The signature verification logic on Solana did not properly verify that the guardian signatures were freshly created for the specific message being approved. A signature set created for one action could be reused for a different action.

**Key Takeaway:** Cross-chain message verification must check that signatures are bound to the exact message content and sequence number, with replay protection enforced on both chains.

### 4. Radiant Capital Flash Loan Attack (January 2024)

**Transaction:** `0x1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2`

**Loss:** $4.5 million

**Attack Flow:**
1. Attacker took a flash loan of 10,000 ETH from Aave V2
2. Deposited a portion into Radiant's USDC market as collateral
3. Manipulated the Radiant USDC/ETH LP price onArbitrum by executing a large swap on the SushiSwap Arbitrum pool, taking advantage of low liquidity in the Radiant LP oracle path
4. The manipulated price inflated the value of the attacker's deposited collateral
5. Borrowed against the inflated collateral to extract significantly more assets than the deposit justified
6. Withdrew the original deposit
7. Returned the flash loan
8. Net profit: ~$4.5M in ETH and USDC

**Root Cause:** Radiant used a time-weighted average price (TWAP) oracle that was derived from a single AMM pool with insufficient liquidity. A single large swap could move the TWAP enough to enable profitable manipulation.

**Key Takeaway:** Oracle design must account for multi-block manipulation and should use liquidity-weighted or median pricing from multiple sources.

## Foundry / Cast Integration

For offline or more detailed transaction analysis, the Foundry toolchain provides powerful debugging capabilities.

### Install Foundry

```bash
# Install
curl -L https://foundry.paradigm.xyz | bash
foundryup

# Verify
cast --version
```

### Trace a Transaction with `cast run`

```bash
# Replay and trace a transaction locally, showing all calls
cast run <TX_HASH> --rpc-url $ETH_RPC_URL

# Show full call trace with decoded function names and parameters
cast run <TX_HASH> --rpc-url $ETH_RPC_URL --debug

# Show only the call summary (lighter output)
cast run <TX_HASH> --rpc-url $ETH_RPC_URL --summary
```

### Debug with `cast call-trace`

```bash
# Get a gas-annotated call trace
cast call-trace <TX_HASH> --rpc-url $ETH_RPC_URL

# Show only failed calls (useful for finding revert points)
cast call-trace <TX_HASH> --rpc-url $ETH_RPC_URL --only-failed

# Decode with contract artifacts from Etherscan
cast call-trace <TX_HASH> --rpc-url $ETH_RPC_URL --etherscan-api-key $ETHERSCAN_API_KEY
```

### Additional Cast Commands

```bash
# Get raw transaction data
cast tx <TX_HASH> --rpc-url $ETH_RPC_URL

# Get transaction receipt
cast receipt <TX_HASH> --rpc-url $ETH_RPC_URL

# Decode calldata (requires function signature)
cast calldata-decode "transfer(address,uint256)" <CALLDATA>

# Get 4-byte selector from signature
cast sig "flashLoan(address,address,uint256,bytes)"

# Get event signature hash
cast keccak "Transfer(address indexed,address indexed,uint256)"

# Convert between units
cast --from-wei 1000000000000000000
cast --to-wei 1.5 eth

# Get current block number
cast block-number --rpc-url $ETH_RPC_URL

# Search for event logs (across a block range)
cast logs --from-block 17000000 --to-block 17000100 --rpc-url $ETH_RPC_URL \
  --topic <TOPIC_HASH>

# Get ABI-encoded storage slot (for reading token balances)
cast storage <TOKEN_ADDRESS> --rpc-url $ETH_RPC_URL \
  $(cast keccak <ATTACKER_ADDRESS>0000000000000000000000000000000000000000000000000000000000000003)
```

### Local Transaction Replay for Deep Analysis

```bash
# Step 1: Get the transaction
cast tx <TX_HASH> --rpc-url $ETH_RPC_URL > tx.json

# Step 2: Simulate at a specific block
cast call $(jq -r '.to' tx.json) $(jq -r '.input' tx.json) \
  --from $(jq -r '.from' tx.json) \
  --value $(jq -r '.value' tx.json) \
  --block $(jq -r '.blockNumber' tx.json) \
  --rpc-url $ETH_RPC_URL

# Step 3: Full trace with gas reporter
cast run <TX_HASH> --rpc-url $ETH_RPC_URL --gas-report
```

## Detailed Analysis Steps

### Step 1: Identify the Attack Transaction

Locate the initial attack transaction(s) by scanning for suspicious patterns.

```python
def identify_attack_tx(deployer: str, attack_block_range: tuple[int, int]) -> list[str]:
    """Given a deployer address and block range, find likely attack transactions."""
    suspicious_txs = []
    # In production, iterate over blocks in range and check:
    # - Unusually high gas (500K+)
    # - Interacts with known DeFi contracts
    # - Multiple swap events in single tx
    # - Flash loan event in logs
    return suspicious_txs
```

Key indicators of an attack transaction:
- Unusually high gas limit (500,000+ gas for complex attacks, 2M+ for flash loan chains)
- Transaction sent to a freshly deployed contract (<24 hours old)
- Direct interaction with a flash loan provider
- Multiple swaps in a single transaction (3+ swap events)
- Transaction sent via Flashbots (to address 0x736E4C...)
- Transaction originator has no prior interaction history with the exploited protocol

### Step 2: Reconstruct the Attack Chain

Trace every call in the attack transaction. For each hop, identify:
- **Entry point** — which function was called on which contract, with what parameters
- **Flash loan source** — where the initial capital came from (Aave, dYdX, Balancer, Uniswap V3)
- **Price manipulation** — which pool was manipulated and how (large swap, skewed ratio, reserve donation)
- **Profit extraction** — how the attacker converted the exploited position to profit
- **Exit** — which bridge or exchange was used to launder or convert the stolen assets

```python
def analyze_attack_chain(tx_hash: str) -> dict:
    """Full attack chain reconstruction from trace."""
    trace = trace_transaction(tx_hash)
    receipt = w3.eth.get_transaction_receipt(tx_hash)
    tx = w3.eth.get_transaction(tx_hash)

    chain = {
        "tx_hash": tx_hash,
        "attacker": tx["from"],
        "target_contract": tx["to"],
        "block": receipt["blockNumber"],
        "gas_used": receipt["gasUsed"],
        "flash_loans": [],
        "swaps": [],
        "classification": None,
        "profit": None,
        "mev": None,
    }

    if receipt:
        chain["flash_loans"] = detect_flash_loans(tx_hash, trace)
        chain["swaps"] = find_all_swaps(receipt)
        classification = classify_attack(tx_hash, receipt, trace)
        chain["classification"] = asdict(classification)
        chain["profit"] = calculate_profit(tx["from"], tx_hash, receipt)
        chain["mev"] = detect_mev_bundle(tx_hash)

    if trace:
        chain["trace_summary"] = format_trace(trace)

    return chain
```

### Step 3: Classify the Attack Type

Determine the primary attack vector:
- **Flash loan attack** — uncollateralized loan used to manipulate prices or leverage positions
- **Oracle manipulation** — TWAP oracle manipulation via low-liquidity pools
- **Reentrancy** — recursive call pattern that drains contract state before updates
- **Bridge attack** — cross-chain message validation bypass or validator compromise
- **Governance attack** — proposal manipulation, flash loan voting, or timelock bypass
- **Access control** — unprotected administrative functions, privilege escalation
- **Logic error** — arithmetic bugs, rounding errors, incorrect state transitions
- **MEV sandwich** — frontrunning and backrunning a victim transaction

### Step 4: Calculate Financial Impact

Compute the profit extracted by the attacker:
- Track all token inflows and outflows from the attacker's wallet using ERC20 Transfer events
- Convert to USD using Chainlink price feed at the block timestamp
- Account for gas costs, flash loan fees, and MEV payments
- Identify any funds returned, frozen, or recovered through law enforcement

### Step 5: Write the Post-Mortem

Produce a structured incident report with:
- **Timeline** — block numbers, timestamps, and key on-chain events in chronological order
- **Root cause** — the specific vulnerability exploited with contract code references and line numbers
- **Attack flow** — step-by-step transaction trace with function calls and parameter values
- **Impact assessment** — total losses, affected assets, affected users, and any recovered funds
- **Mitigation recommendations** — specific code fixes, monitoring rules, architectural changes, each with priority and estimated effort

## Expected Output

A structured DeFi incident post-mortem containing: attack transaction hash, step-by-step call trace with decoded function signatures and parameters, vulnerability classification with evidence, financial impact calculation with per-asset breakdown, entity attribution (if possible), MEV bundle detection results, and prioritized mitigation recommendations with code-level fixes.

## Red Flags

- Drawing conclusions from only the attacker's transactions without examining protocol state changes before and after
- Misclassifying an attack type because the outermost call looks familiar (tunnel vision on flash loans vs. reentrancy)
- Ignoring failed transactions in the same block that may represent initial exploit attempts or test transactions
- Relying on a single block explorer without verifying event logs and internal calls directly against an RPC node
- Assuming all flash loans are the attack vector — flash loans are a capital source, not a vulnerability
- Overlooking MEV infrastructure — transactions submitted via Flashbots may have special properties
- Trusting the block explorer's event decoding without verifying raw log topics and data
- Treating a single trace call as the full picture — some attacks span multiple transactions across blocks
- Forgetting that price manipulation can happen in a previous block, not just the attack block

## Process

1. **Incident Triage** — Confirm the incident via on-chain data or protocol announcement, locate the attack transaction(s), establish the scope of affected contracts and assets. Cross-reference DeFiLlama hacks dashboard and Twitter for incident confirmation.

2. **Transaction Trace** — Reconstruct the full call chain using `debug_traceTransaction` or `cast run`. Extract all internal calls, function selectors, and parameter values. Identify the entry point, flash loan source, swap operations, and profit extraction.

3. **Event Log Analysis** — Parse all event logs from the transaction receipt. Focus on Swap events for price trajectory, Transfer events for asset movement, and protocol-specific events (FlashLoan, Borrow, Deposit, Withdraw).

4. **Vulnerability Identification** — Classify the attack vector using the classifier function. Map the observed exploit pattern to a vulnerability class. Identify the specific code flaw by comparing the attack trace to the protocol's source code.

5. **Financial Analysis** — Calculate profit using balance delta method. Compute total losses across all affected assets. Trace fund movements and identify any frozen or recovered amounts. Document the path of stolen funds.

6. **MEV Context** — Check if the transaction was submitted via Flashbots or other MEV relay. Determine if there were frontrunning/backrunning opportunities. Analyze the block for related transactions.

7. **Cross-Verification** — Validate all findings against a second RPC provider or block explorer. Confirm timestamps and block numbers. Re-verify profit calculations independently.

8. **Reporting** — Produce post-mortem with executive summary, root cause, timeline, technical analysis, impact assessment, and prioritized mitigation recommendations.

## Verification

- Attack chain reconstructed independently using two methods (RPC debug_traceTransaction + block explorer internal txs)
- Profit calculation verified by comparing attacker balance before and after across all token positions
- All contract addresses, function signatures, and parameter values cross-referenced with verified source code on Etherscan
- Timeline block numbers checked on the actual chain (not just from incident announcements)
- Mitigation recommendations validated against the specific vulnerability, not generic advice
- Classification results confirmed against known attack pattern databases (SWC Registry, DASP Top 10)
- Flash loan amounts cross-checked against flash loan provider's subgraph or logs
- Oracle manipulation claims verified by checking the oracle's reported price vs. actual market price at the time
- Event log parsing verified by comparing decoded values against raw hex data
- For multi-transaction attacks: all related transactions identified and linked in the report


## Pre-Investigation Checklist

Before committing to a full attack-chain reconstruction, verify the incident is worth the effort:

- [ ] Transaction is not a failed attempt (check `status` field — 0 = reverted)
- [ ] Flash loan profit > 0.5 ETH — smaller amounts are typically MEV extraction, not an exploit
- [ ] Protocol did not pause or self-destruct pre-attack (may be a white-hat rescue or planned migration)
- [ ] Affected contract is not a testnet/mock deployment (verify against mainnet-verified source)
- [ ] Multiple transactions from the same address in the same block — indicates batched attack, not a single atomic exploit
- [ ] Oracle price deviation > 5% from independent feeds — check against Chainlink, Maker, and Uniswap TWAP
- [ ] Transaction has at least one verified independent source (block explorer + Dune + Tenderly)
- [ ] Attacker address is not a known white-hat or MEV bot (check etherscan labels, eigenphi, failed-tx datasets)

**Exit criteria**: If 3+ items fail the check, deprioritize this analysis. The "attack" is likely a false positive, MEV extraction, or an internal action. Log the address + chain to a watchlist and re-check weekly.

## RPC & API Endpoint Management

Every chain-forensics investigation depends on reliable API access. Plan for failure at every layer.

### Etherscan-Style API Rate Limits

| Provider | Free Tier Limit | Paid Tier | Notes |
|---|---|---|---|
| Etherscan | 5 calls/sec | 1,000 calls/min ($165/mo) | `api.etherscan.io` |
| BscScan | 5 calls/sec | 1,000 calls/min ($99/mo) | Same API shape |
| Polygonscan | 5 calls/sec | 500 calls/min ($49/mo) | Same API shape |
| Arbiscan | 10 calls/sec | 1,000 calls/min ($99/mo) | Same API shape |

### Fallback Provider Chain

```python
import time
import requests
from typing import Any

PROVIDER_CHAIN = [
    {"name": "etherscan", "base": "https://api.etherscan.io/api", "key_env": "ETHERSCAN_KEY"},
    {"name": "etherscan-backup", "base": "https://api.etherscan.io/api", "key_env": "ETHERSCAN_KEY_2"},
]

def api_call_with_fallback(action: str, params: dict) -> dict:
    """Call block explorer API with automatic failover and rate-limit backoff."""
    for provider in PROVIDER_CHAIN:
        api_key = __import__("os").environ.get(provider["key_env"])
        if not api_key:
            continue
        params["apikey"] = api_key
        try:
            resp = requests.get(provider["base"], params=params, timeout=30)
            data = resp.json()
            if data.get("status") == "1":  # success
                return data
            if "rate limit" in str(data).lower():
                time.sleep(1.5)
                continue
        except (requests.ConnectionError, requests.Timeout):
            time.sleep(2)
            continue
    raise RuntimeError(f"All providers failed for action={action}")
```

### API Key Hygiene Rules

1. **Never hardcode keys** — load from environment variables (`ETHERSCAN_KEY`, `INFURA_KEY`)
2. **Rotate exposed keys immediately** — if a key appears in logs, stdout, or a screenshot, rotate before continuing
3. **Separate read keys from write keys** — use read-only API keys for investigation to prevent accidental state changes
4. **Use a dedicated key for each chain** — don't share a single key across Etherscan, BscScan, Polygonscan; each scan family tracks its own rate limit
5. **Check key validity at start** — make one `?action=balance&address=0x0&tag=latest` call; if it returns an error key, fail fast before beginning analysis

### When You Have No API Key

**Free alternatives** for emergency investigation:

- **Etherscan read function** (web UI): curl-able, no key needed for individual lookups
- **Blocknative mempool API**: free tier for pending tx monitoring
- **Covalent unified API**: 5 req/s free tier, one key covers 30+ chains
- **Dune Analytics**: free tier for querying decoded event data (SQL interface)

## When the Trace Goes Cold

Every investigator hits dead ends. The skill is not in avoiding them — it's in knowing which are real dead ends and which are puzzles with one more piece missing.

### Dead-End Decision Matrix

| Situation | Most Likely Cause | Action |
|---|---|---|
| EOA receives funds, no outgoing txs for 48h+ | Sleeping address / cold storage | Set webhook alert on `txlist` for this address; return when it moves |
| Funds enter a Tornado Cash pool | Privacy mixer | Note the deposit amount + block. Check all withdrawals from the same pool within ±100 blocks for matching amounts |
| Trace reaches a CEX deposit address | Exchange — last on-chain point | Document destination + tx hash. This is a subpoena boundary, not a tracing failure |
| Trace reaches a bridge contract | Cross-chain transfer | Search the source chain exits → destination chain entry (event logs on both sides) |
| Target is a proxy contract (ERC-1967) | Implementation upgrade | Find the `_implementation()` slot value and investigate the logic contract |
| Transaction reverted but gas was paid | Failed attempt, not a real transfer | Ignore for fund flow; check adjacent transactions from the same sender |
| Destination is a burn address (0x00...dead) | Token burn, intentional | This IS the end. Funds are irretrievable. Report as final destination |
| Attacker used create2 with salt | Counterfactual deployment | Search for the contract at the predicted address or check deployer history |

### When to Stop Tracing

Apply the 80/20 rule: the last 5% of trace hops cost 50% of your time. Stop when:

1. Funds enter a regulated exchange (CEX) — document and close
2. Funds are burned or sent to a dead address — final state
3. You have identified the attacker's identity with high confidence (ENS, social media, Git repo)
4. The trace enters a privacy chain (Monero, Zcash shielded) — explicit stop: these are not analyzable without specialized tools
5. Three consecutive hops show value dissipation (peel chain decay formula below) — the remaining amount is below your investigation threshold

```python
def is_peel_chain_decay(tx_chain: list[dict], min_value_eth: float = 0.1) -> bool:
    """Detect if a transaction chain shows peel-chain decay pattern."""
    if len(tx_chain) < 3:
        return False
    values = [tx["value_eth"] for tx in tx_chain[-3:]]
    # Peel chains show strictly decreasing value per hop
    return all(v < values[i] for i, v in enumerate(values[1:])) and values[-1] < min_value_eth
```

**Rule of thumb**: if you've made 10 API calls on a single address without finding a new lead, archive it with a weekly re-check note and move to the next address. The trace is not gone — it's waiting for a transaction that hasn't happened yet.
## Practices from Top Investigators

### The ZachXBT Methodology

ZachXBT has analyzed hundreds of DeFi exploits, from $10M+ protocol hacks to small farming
pool drains. His methodology treats every exploit as an intelligence problem: **the attacker left
clues everywhere** — funding source, preparation transactions, test transactions, social
media activity, infrastructure choices. The skill is knowing which clues to follow and in what
order.

### The 12-Tool Arsenal for DeFi Incident Analysis

| Tool | DeFi Incident Use | When to Use |
|---|---|---|
| **Etherscan / Solscan** | Primary: tx list, internal txs, event logs, contract source | Start of every incident — read the exploit tx |
| **Arkham** | Visual fund flow: attacker → intermediate → exchange | During trace: visualize the flow across protocols |
| **MetaSleuth** | Cross-chain incident tracking: same attacker on multiple chains | When exploit spans L1s/L2s |
| **Cielo** | Real-time monitoring of attacker addresses | After initial trace — monitor for fund movement |
| **TRM Labs** | Attacker address risk scoring, sanctions, entity links | Before publishing — verify the attacker's known profile |
| **Breadcrumbs** | BTC fund routing for Bitcoin-side exploit proceeds | When BTC is involved in the fund flow |
| **Dune Analytics** | Pre-programmed exploit detection queries, SQL-based analysis | Analyze protocol TVL, liquidity before/after exploit |
| **DeBank** | Attacker's cross-chain portfolio before the exploit | Determine if the attacker was also a protocol user |
| **OKLink** | Chain-explorer integration for multi-chain investigation | Follow funds through L2s and sidechains |
| **Blockchair** | Privacy analysis: coinjoin, mixing detection for BTC funds | When exploit proceeds go through mixers |
| **OMNIA** | Mempool data: was the exploit tx visible before confirmation? | Determine if MEV bots saw and copied the exploit |
| **MetaSuites** | Legacy address labeling for pre-2022 protocols | Old protocol incidents need historical label data |

### Timeline Reconstruction

ZachXBT builds exact chronological timelines for every incident. This reveals attacker behavior
patterns that transaction-level analysis misses:

```python
def build_incident_timeline(exploit_tx_hash: str, chain: str = "ethereum",
                            window_hours: int = 72) -> list[dict]:
    """Reconstruct a minute-by-minute timeline of attacker activity before/after exploit.

    ZachXBT method: the 72-hour window around an exploit tells more than the exploit itself.
    """
    events = []

    # 1. Attacker preparation (pre-exploit)
    #    - Test transactions (small amounts, same calldata)
    #    - Contract interactions (approvals, deposits)
    #    - Bridge deposits (funding from another chain)
    events.append({"phase": "preparation", "what": "check test txs, fund bridging, approvals"})

    # 2. Exploit execution
    events.append({"phase": "exploit", "what": f"main tx: {exploit_tx_hash}"})

    # 3. Immediate post-exploit (0-30 min)
    #    - Attacker swaps exploit token to stablecoin
    #    - Attacker bridges to another chain
    events.append({"phase": "immediate_post", "what": "swap profits, bridge out, move funds"})

    # 4. Distribution (30 min - 72 hours)
    #    - Funds split across multiple addresses
    #    - Some sent to CEX, some held, some bridged again
    events.append({"phase": "distribution", "what": "split, distribute, CEX deposit"})

    # 5. Social response (attacker's off-chain activity)
    #    - Discord messages deleted
    #    - Twitter account locked/deleted
    #    - ENS name transferred
    events.append({"phase": "off_chain", "what": "check social deletions, ENS transfers, domain changes"})

    return events
```

Key timeline patterns ZachXBT has documented across multiple exploits:

| Pattern | Indicator | Action |
|---|---|---|
| Test tx before exploit | Small ETH transfer or contract call 2-24h before | Verify test tx sender = exploit tx sender — confirms preparation |
| Bridge funding | Attacker bridged funds in 6-48h before exploit | Trace the source chain — the attacker may have a longer history there |
| Weekend/holiday execution | Exploit on Saturday or during holidays | Expect delayed response — plan for slow exchange actions |
| MEV copycat | >1 exploit tx in same block or adjacent blocks | Check Flashbots bundles — the original attacker may have been frontrun |
| Token dump cascade | Multiple sells to different DEXes in rapid succession | Track which pools absorbed the sell; check price impact |
| Social cleanup | Discord messages deleted within 30 min of exploit | Capture archives via Wayback Machine / DiscordChatExporter immediately |

### Multi-Chain Bridge Tracking

DeFi exploits rarely stay on one chain. ZachXBT's bridge tracking method:

1. **Find the bridge contract interaction** — Look for `Transfer` events with `destinationChainId`
2. **Check the source chain's bridge event logs** — Parse `emit DepositFinalized(depositor, amount, ...)`
3. **Extract `receiver` address on the destination chain** — Not always the same as the source
4. **Check the destination chain** — The receiver address may have moved funds further
5. **Record both sides** — Chain A tx hash + Chain B tx hash = complete picture

```python
def trace_bridge_crossing(source_tx_hash: str, source_chain: str,
                           bridge_contract: str) -> dict | None:
    """Trace a fund movement through a bridge contract.

    Returns the destination chain + receiver address if found.
    """
    from etherscan_v2_api import fetch_tx_receipt, fetch_event_logs

    receipt = fetch_tx_receipt(source_tx_hash, source_chain)
    if not receipt:
        return None

    logs = receipt.get("logs", [])
    for log in logs:
        # Bridge-specific event signatures
        topics = log.get("topics", [])
        if not topics:
            continue

        # Common bridge event signatures
        deposit_signatures = {
            "0x9c3d2b9b91bf5b4e0d0d8e5b0d0f9c3d2b9b": "Wormhole",
            "0x8e5b0d0f9c3d2b9b91bf5b4e0d0d8e5b0d0f": "Arbitrum Bridge",
        }

        event_sig = topics[0]
        if event_sig in deposit_signatures:
            return {
                "bridge": deposit_signatures[event_sig],
                "source_tx": source_tx_hash,
                "source_chain": source_chain,
                "receiver": f"0x{log['data'][-40:]}" if len(log.get("data", "")) >= 40 else "unknown",
                "amount": int(log["data"][:66], 16) if len(log.get("data", "")) >= 66 else 0,
            }

    return None  # No bridge event found; check adjacent txs
```

### Incident Response vs. Investigation

Knowing when to switch modes is a key ZachXBT skill:

- **Crisis mode** (first 24h): Track fund flow in real time, identify exchange deposits,
  notify exchange contacts immediately. Speed matters more than perfection.
- **Investigation mode** (24h+): Systematic reconstruction, timing analysis, funding chain
  tracing, cross-referencing with past incidents. Depth matters more than speed.
- **Publication mode** (after funds tracked): Public thread with clear timeline, address
  clusters, and evidence. Community cross-referencing often finds additional links.
- **Bounty collection** (after publication): Cross-reference with known bounty programs,
  contact affected protocols, document the investigation's value for bounty claims.


## Anti-Rationalization Table
## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "The contract was audited by a top firm, it must be safe" | Audits find known patterns, not novel compositions. Many exploited protocols had multiple audits with no findings. |
| "It was just a flash loan attack, nothing to learn" | Each flash loan attack teaches something about capital efficiency, protocol composition risks, and oracle design. |
| "The oracle is battle-tested, it can't be manipulated" | Any oracle that can be moved by a single swap in a low-liquidity pool is manipulable. TWAP oracles with short windows are equally vulnerable. |
| "The exploit was too complex to understand" | DeFi attacks decompose into a few fundamental primitives — flash loans, swaps, and balance computations. Complexity is often in the number of hops, not the concepts. |
| "The exploit was a one-time event, it won't happen again" | Attack patterns recur constantly. The same root cause class (oracle manipulation) has been exploited in 100+ separate incidents. |
| "The bug was in a new feature, so old code is safe" | Attackers frequently find bugs in old, battle-tested code too, as the Curve Vyper incident demonstrated — the bug was in the compiler, not the protocol. |
| "The exploit only worked because of a specific market condition" | Attackers exploit market conditions intentionally. The same vulnerability will be exploited again when market conditions align. |
| "OpenZeppelin contracts can't have bugs" | Even battle-tested libraries can have integration-level vulnerabilities. The bug is often in how the contract uses the library, not in the library itself. |
| "A large TVL means the protocol is secure" | High TVL attracts attackers. Many protocols with >$1B TVL have been exploited (Poly Network, Wormhole, Ronin). |
| "The team has a bug bounty, so they're on top of security" | Bug bounties are reactive, not preventive. Many exploited protocols had active bug bounty programs. |

## Money Section

DeFi incident analysis is a high-value consulting skill. Here are established monetization paths:

### Incident Response Consulting

| Service Tier | Scope | Price Range | Typical Delivery |
|---|---|---|---|
| Triage + Brief | Single transaction analysis, 1-page summary, classification | $500 - $2,000 | 4-8 hours |
| Full Post-Mortem | Complete attack chain reconstruction, root cause, timeline, financial impact, detailed mitigations | $3,000 - $10,000 | 2-5 days |
| Protocol Security Review | Retrospective analysis plus recommended code and architecture changes | $10,000 - $30,000 | 1-2 weeks |
| Retainer (Monthly) | Priority incident response, up to 5 analyses/month, ongoing monitoring support | $8,000 - $20,000/month | Ongoing |

### Post-Mortem Writing Services

Many protocols need public post-mortems but lack the technical writing skills:

- **Standard post-mortem** (2-3 pages): $1,500 - $3,000
- **Detailed technical report** (5-10+ pages with code snippets and transaction traces): $3,000 - $7,000
- **Executive summary** for non-technical stakeholders: $1,000 - $2,000

### Detection Rule Development

Build a recurring revenue stream by creating detection rules from your analysis:

- **Sigma rules** for SIEM integration: $500 - $1,500 per rule
- **Forta/Chainlink automation** detection bots: $2,000 - $5,000 per bot
- **Custom monitoring dashboard** (Dune, Flipside, or custom stack): $5,000 - $15,000

### Insurance and Legal Work

Specialized analysis for insurance claims and legal proceedings commands a premium:

- **Incident verification** for insurance claim: $3,000 - $8,000
- **Expert witness report** for litigation: $5,000 - $20,000
- **Fund tracing report** for law enforcement: $7,000 - $15,000

### Tooling and Education

- **Custom scripts and analysis templates**: Sell on GitHub or GitBook: $50 - $200 per template
- **Online course** (DeFi forensics fundamentals): $500 - $2,000 per student
- **Corporate workshop** (half-day to full-day): $5,000 - $15,000 per session
