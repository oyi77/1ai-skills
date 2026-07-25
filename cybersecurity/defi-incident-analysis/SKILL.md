---
name: defi-incident-analysis
description: Analyze DeFi security incidents including flash loan attacks, oracle manipulation, reentrancy exploits,
  bridge hacks, and governance attacks to reconstruct attack chains and identify root causes. Use when investigating DeFi
  protocol exploits, analyzing smart contract attacks, or writing incident post-mortems.
domain: cybersecurity
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

Decentralized Finance (DeFi) incidents have resulted in over $3 billion in losses from flash loan attacks, oracle manipulation, reentrancy exploits, bridge hacks, and governance attacks. Each incident type follows specific patterns that can be identified through systematic on-chain analysis. This skill covers reconstructing attack chains from transaction data, identifying exploited vulnerabilities, tracing attacker profit extraction, and producing structured post-mortem reports with root cause analysis and recommended mitigations.

## When to Use

**Trigger phrases:**
- "defi incident analysis"
- "Analyze a DeFi protocol hack"
- "Reconstruct a flash loan attack chain"
- "Write a DeFi incident post-mortem"

- When investigating a DeFi protocol exploit to understand the attack methodology
- When writing an incident post-mortem for stakeholders or the community
- When assessing whether a protocol's design is vulnerable to known attack patterns
- When building detection rules for DeFi-specific attack signatures

## Prerequisites

- Python 3.8+ with web3.py, requests, pandas
- Access to Ethereum RPC node (or archival node for historical analysis)
- Block explorer API keys (Etherscan, or equivalent for target chain)
- Understanding of AMM mechanics, lending protocols, and common DeFi primitives
- Flash loan provider knowledge (Aave, dYdX, Balancer, Uniswap V3 flash swaps)

## Core Workflow

```python
# Example: Extract all events from a transaction
from web3 import Web3

def get_transaction_receipt(w3: Web3, tx_hash: str) -> dict:
    """Get the transaction receipt with all event logs."""
    return w3.eth.get_transaction_receipt(tx_hash)

def get_transaction(w3: Web3, tx_hash: str) -> dict:
    """Get the full transaction details."""
    return w3.eth.get_transaction(tx_hash)

def decode_erc20_transfer(w3: Web3, log: dict) -> dict | None:
    """Decode an ERC-20 Transfer event from a log entry."""
    erc20_abi = [
        {
            "anonymous": False,
            "inputs": [
                {"indexed": True, "name": "from", "type": "address"},
                {"indexed": True, "name": "to", "type": "address"},
                {"indexed": False, "name": "value", "type": "uint256"},
            ],
            "name": "Transfer",
            "type": "event",
        }
    ]
    contract = w3.eth.contract(abi=erc20_abi)
    try:
        event = contract.events.Transfer().process_log(log)
        return {"from": event.args.from_, "to": event.args.to, "value": event.args.value}
    except Exception:
        return None
```

### Step 1: Identify the Attack Transaction

Locate the initial attack transaction(s) by scanning for suspicious patterns: unusual gas prices, MEV-related transactions, interactions with known vulnerable contracts, or timestamp correlation with the incident announcement. On Ethereum, the attacker often uses Flashbots to avoid frontrunning.

### Step 2: Reconstruct the Attack Chain

Trace every call in the attack transaction using a transaction tracer or by parsing internal transactions. For each hop, identify:
- **Entry point** — which function was called on which contract
- **Flash loan source** — where the initial capital came from (Aave, dYdX, Balancer, Uniswap V3)
- **Price manipulation** — which pool was manipulated and how (large swap, skewed ratio)
- **Profit extraction** — how the attacker converted the exploited position to profit
- **Exit** — which bridge or exchange was used to launder or convert the stolen assets

### Step 3: Classify the Attack Type

Determine the primary attack vector:
- **Flash loan attack** — uncollateralized loan used to manipulate prices or leverage positions
- **Oracle manipulation** — TWAP oracle manipulation via low-liquidity pools
- **Reentrancy** — recursive call pattern that drains contract state before updates
- **Bridge attack** — cross-chain message validation bypass or validator compromise
- **Governance attack** — proposal manipulation, flash loan voting, or timelock bypass
- **Access control** — unprotected administrative functions, privilege escalation
- **Logic error** — arithmetic bugs, rounding errors, incorrect state transitions

### Step 4: Calculate Financial Impact

Compute the profit extracted by the attacker:
- Track all token inflows and outflows from the attacker's wallet
- Convert to USD using price at block timestamp
- Account for gas costs, flash loan fees, and MEV payments
- Identify any funds returned, frozen, or recovered

### Step 5: Write the Post-Mortem

Produce a structured incident report with:
- **Timeline** — block numbers, timestamps, and key on-chain events
- **Root cause** — the specific vulnerability exploited with code references
- **Attack flow** — step-by-step transaction trace with function calls and parameter values
- **Impact assessment** — total losses, affected assets, affected users
- **Mitigation recommendations** — specific code fixes, monitoring rules, and architectural changes

## Expected Output

A structured DeFi incident post-mortem containing: attack transaction hash, step-by-step call trace with function signatures and parameters, vulnerability classification, financial impact calculation, entity attribution (if possible), and prioritized mitigation recommendations with code-level fixes.

## When NOT to Use

- You need to perform a live exploit, not analyze one (use smart-contract-exploiter skill)
- You need to audit a contract pre-deployment (use analyzing-ethereum-smart-contract-vulnerabilities skill)
- Task requires tracing where stolen funds went after the exploit (use onchain-transaction-forensics skill)
- You need to implement security controls for a protocol (use implementing-* security skills)
- The incident involves off-chain components not reflected in on-chain data (social engineering, private key compromise)

## Red Flags

- Drawing conclusions from only the attacker's transactions without examining protocol state changes
- Misclassifying an attack type because the outermost call looks familiar
- Ignoring failed transactions in the same block that may represent initial exploit attempts
- Relying on a single block explorer without verifying event logs and internal calls directly

## Process

1. **Incident Triage** — Confirm the incident, locate the attack transaction(s), establish scope
2. **Transaction Trace** — Reconstruct the full call chain using RPC tracing or internal transaction parsing
3. **Vulnerability Identification** — Classify the attack vector and identify the specific code flaw
4. **Financial Analysis** — Calculate profit, losses, and track fund movements
5. **Reporting** — Produce post-mortem with root cause, timeline, impact, and mitigations

## Verification

- Attack chain reconstructed independently using two methods (RPC debug_traceTransaction + block explorer internal txs)
- Profit calculation verified by comparing attacker balance before and after
- All contract addresses, function signatures, and parameter values cross-referenced with source code
- Timeline block numbers checked on the actual chain (not just from incident announcements)
- Mitigation recommendations validated against the specific vulnerability, not generic advice

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "The contract was audited by a top firm, it must be safe" | Audits find known patterns, not novel compositions. Many exploited protocols had multiple audits. |
| "It was just a flash loan attack, nothing to learn" | Each flash loan attack teaches something about capital efficiency and protocol composition risks. |
| "The oracle is battle-tested, it can't be manipulated" | Any oracle that can be moved by a single swap in a low-liquidity pool is manipulable. |
| "The exploit was too complex to understand" | DeFi attacks decompose into a few fundamental primitives — flash loans, swaps, and balance computations. |
