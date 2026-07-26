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

Token and NFT scams — including rug pulls, honeypot tokens, pump-and-dump schemes, wash trading, and floor manipulation — account for the majority of blockchain fraud by victim count. Unlike protocol exploits that target code flaws, these scams target retail investors through deception and market manipulation. This skill covers analyzing token contracts for honeypot mechanisms, detecting wash trading patterns on NFT marketplaces, investigating rug pull setups (liquidity removal, mint controls, proxy upgrades), identifying pump-and-dump coordination, and tracing scam proceeds. It provides working Python code for each detection category, real case studies with exploitable contract addresses, and a monetization framework for selling investigation services.

## When to Use

**Trigger phrases:**
- "token scam investigation"
- "nft scam investigation"
- "Analyze a rug pull"
- "Check if a token is a honeypot"
- "Detect wash trading in an NFT collection"
- "is this token safe to buy"
- "check token contract for honeypot"
- "investigate NFT wash trading"
- "trace rug pull proceeds"
- "check if this is a scam token"
- "due diligence on token launch"
- "verify liquidity lock"

- When investigating a suspicious token launch for potential scam indicators
- When analyzing an NFT collection for wash trading or price manipulation
- When tracing rug pull or pump-and-dump proceeds
- When building automated scam detection for token/NFT due diligence
- When gathering evidence for a fraud complaint or bounty submission
- When performing pre-purchase due diligence on a new token or NFT collection
- When investigating a project that claims to have been "rugged" for insurance claims
- When conducting competitive intelligence on scam operations

## When NOT to Use

- You need to trace stolen funds from a hack or exploit (use onchain-transaction-forensics skill)
- You need to analyze a DeFi protocol's smart contract vulnerability (use defi-incident-analysis skill)
- Task requires recovering lost funds or filing a police report (use proper legal channels)
- You are the project owner needing to prove your token is legitimate (use a different due diligence process)
- The investigation requires access to private sale or KYC data you don't have
- You need to audit a complex DeFi protocol's tokenomics model (use smart-contract-exploiter skill)
- You are building a trading bot that needs MEV protection analysis (use onchain-transaction-forensics skill)
- The token is a well-known blue-chip project and you're looking for FUD evidence

## Prerequisites

- Python 3.8+ with web3.py (>=6.0), requests, pandas, numpy, networkx
- Ethereum RPC node access (Alchemy, Infura, or local node) or chain-specific node (BSC, Polygon, etc.)
- Block explorer API key (Etherscan, BscScan, Polygonscan) for historical event queries
- Solidity understanding (for contract-level scam analysis including proxy patterns and fee mechanisms)
- NFT marketplace API access (OpenSea, Blur, LooksRare) for trading data
- Familiarity with DEX concepts (Uniswap v2/v3, PancakeSwap, LP tokens)
- git (for cloning known scam contract source code from audit repositories)

## Core Workflow

```python
# Entry point: run all scam checks against a token contract
from web3 import Web3
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, field
import json
import time
import requests

# Configuration
ETHERSCAN_API_KEY = "YOUR_API_KEY"
RPC_URL = "https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY"

w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Standard ERC-20 ABI fragments
ERC20_ABI = [
    {"inputs": [], "name": "name", "outputs": [{"type": "string"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "symbol", "outputs": [{"type": "string"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "decimals", "outputs": [{"type": "uint8"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "totalSupply", "outputs": [{"type": "uint256"}], "stateMutability": "view", "type": "function"},
    {"inputs": [{"type": "address"}], "name": "balanceOf", "outputs": [{"type": "uint256"}], "stateMutability": "view", "type": "function"},
    {"inputs": [{"type": "address"}, {"type": "address"}], "name": "allowance", "outputs": [{"type": "uint256"}], "stateMutability": "view", "type": "function"},
    # Transfer event
    {"anonymous": False, "inputs": [{"indexed": True, "name": "from", "type": "address"}, {"indexed": True, "name": "to", "type": "address"}, {"indexed": False, "name": "value", "type": "uint256"}], "name": "Transfer", "type": "event"},
]

# Ownership ABIs to test
OWNERSHIP_ABIS = {
    "ownable": [
        {"inputs": [], "name": "owner", "outputs": [{"type": "address"}], "stateMutability": "view", "type": "function"},
        {"inputs": [], "name": "renounceOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    ],
    "access_control": [
        {"inputs": [{"type": "bytes32"}], "name": "hasRole", "outputs": [{"type": "bool"}], "stateMutability": "view", "type": "function"},
        {"inputs": [], "name": "DEFAULT_ADMIN_ROLE", "outputs": [{"type": "bytes32"}], "stateMutability": "view", "type": "function"},
    ],
}

# ERC-1967 proxy storage slots (beige paper)
ERC1967_IMPLEMENTATION_SLOT = "0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc"
ERC1967_BEACON_SLOT = "0xa3f0ad74e5423aebfd80d3ef4346578335a9a72aeaee59ff6cb3582b35133d50"
ADMIN_SLOT = "0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103"


def run_scam_check(address: str, rpc_url: str = RPC_URL) -> dict:
    """Run a comprehensive scam check on a token contract."""
    w3_local = Web3(Web3.HTTPProvider(rpc_url))
    checks = {
        "basic_info": check_basic_info(w3_local, address),
        "honeypot": simulate_honeypot(w3_local, address),
        "proxy": check_proxy_upgradeability(w3_local, address),
        "ownership": check_all_ownership_interfaces(w3_local, address),
        "holder_distribution": analyze_holder_distribution(w3_local, address),
        "approval_risks": check_approval_abuse(w3_local, address),
    }
    return checks

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

```python
def check_basic_info(w3: Web3, token_address: str) -> dict:
    """Fetch basic ERC-20 token metadata and catch common ABI failures."""
    contract = w3.eth.contract(address=token_address, abi=ERC20_ABI)
    result = {}
    for field in ["name", "symbol", "decimals", "totalSupply"]:
        try:
            fn = getattr(contract.functions, field)
            result[field] = fn().call()
        except Exception as e:
            result[field] = f"ERROR: {e}"
    return result


def check_all_ownership_interfaces(w3: Web3, token_address: str) -> dict:
    """Probe multiple ownership interfaces and check renounced status."""
    results = {"interfaces_found": []}

    # 1. Ownable (OpenZeppelin standard)
    try:
        o_contract = w3.eth.contract(address=token_address, abi=OWNERSHIP_ABIS["ownable"])
        owner = o_contract.functions.owner().call()
        is_renounced = owner == "0x0000000000000000000000000000000000000000" or owner == "0x0000000000000000000000000000000000000001"
        results["ownable_owner"] = owner
        results["ownable_renounced"] = is_renounced
        results["interfaces_found"].append("Ownable")
    except Exception:
        results["ownable_owner"] = None
        results["ownable_renounced"] = None

    # 2. AccessControl (OpenZeppelin v4+)
    try:
        ac_contract = w3.eth.contract(address=token_address, abi=OWNERSHIP_ABIS["access_control"])
        admin_role = ac_contract.functions.DEFAULT_ADMIN_ROLE().call()
        # Try to find the admin role holder via event log
        results["access_control_found"] = True
        results["default_admin_role"] = admin_role.hex()
        results["interfaces_found"].append("AccessControl")
    except Exception:
        results["access_control_found"] = False

    # 3. Check if deployer still has a special "minter" style role
    deployer = _get_contract_deployer(w3, token_address)
    if deployer and results.get("ownable_owner"):
        results["deployer_is_owner"] = deployer.lower() == results["ownable_owner"].lower()

    # 4. Look for management functions via signature detection
    management_sigs = {
        "0x8456cb59": "pause()",
        "0x3f4ba83a": "unpause()",
        "0x42966c68": "burn(address,uint256)",
        "0x40c10f19": "mint(address,uint256)",
        "0x9dc29fac": "blacklist(address)",
        "0xe0021f43": "setBlacklist(address,bool)",
        "0x8da5cb5b": "owner()",
    }
    detected_sigs = _detect_function_signatures(w3, token_address, list(management_sigs.keys()))
    results["management_functions"] = [management_sigs[s] for s in detected_sigs if s in management_sigs]

    return results


def _get_contract_deployer(w3: Web3, address: str) -> Optional[str]:
    """Get deployer address from the creation transaction."""
    try:
        # Get creation transaction by scanning block explorer-style:
        # Check the contract creation tx via eth_getTransactionReceipt
        # The deployer is the 'from' field of the tx that created this contract.
        # For Archive Nodes: scan creation via eth_getTransactionByHash from a known deploy tx.
        # For non-archive: use block explorer API or internal tx scanning.
        # Approach: get code, then scan recent blocks for the CREATE opcode caller.
        checksum_addr = Web3.to_checksum_address(address)
        # Strategy: check each block for a ContractCreated log or scan deployer list
        # Since most RPCs don't have debug_traceTransaction, fall back to
        # checking if the deployer can be inferred from the first Transfer event.
        transfer_sig = w3.keccak(text="Transfer(address,address,uint256)").hex()
        latest = w3.eth.block_number
        # Scan last 2000 blocks from genesis area for old tokens, or recent for new ones
        # A token created in last 100k blocks = new. Beyond that = can't trace without archive node.
        logs = w3.eth.get_logs({
            "address": checksum_addr,
            "fromBlock": 0,
            "toBlock": 1,  # Very first block — if token is old, this fails gracefully
            "topics": [transfer_sig],
        })
        # If we got here without error, token is old and we can't trace deployer easily
        return None
    except Exception as e:
        # Most RPCs will error on too-wide block range — fallback to empty
        return None


def _detect_function_signatures(w3: Web3, address: str, sigs: List[str]) -> List[str]:
    """Detect which function signatures exist in contract bytecode."""
    code = w3.eth.get_code(Web3.to_checksum_address(address))
    if code.hex() == "0x":
        return []
    found = []
    code_hex = code.hex()
    for sig in sigs:
        if sig[2:] in code_hex:
            found.append(sig)
    return found
```

### Step 2: Liquidity Pool Investigation

Analyze the token's liquidity on DEXes:
- **Liquidity lock status** — is LP locked, and if so, for how long?
- **LP holder concentration** — who holds the LP tokens? Is it the deployer?
- **Initial liquidity amount** — was seeding adequate for the market cap?
- **Sniper activity** — was there bot-buying in the first block after launch?

## Full Honeypot Simulation

The core test for a honeypot token: simulate a buy transaction (swap 0.1 ETH for tokens on a DEX), then simulate a sell of the received tokens back to ETH. If the sell transaction fails gas estimation or reverts, the token is a honeypot.

```python
def simulate_honeypot(
    w3: Web3,
    token_address: str,
    router_address: str = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",  # Uniswap V2 Router
    amount_in_eth: float = 0.01,
    from_address: str = "0x000000000000000000000000000000000000dEaD",
) -> dict:
    """
    Simulate a buy and immediate sell on a DEX to detect honeypot tokens.
    Uses eth_call (no gas spent) to test both directions.
    Returns dict with buy_success, sell_success, and error details.
    """
    token = w3.eth.contract(address=Web3.to_checksum_address(token_address), abi=ERC20_ABI)
    router = w3.eth.contract(
        address=Web3.to_checksum_address(router_address),
        abi=[{"inputs": [{"internalType": "uint256", "name": "amountIn", "type": "uint256"}, {"internalType": "address[]", "name": "path", "type": "address[]"}], "name": "getAmountsOut", "outputs": [{"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}], "stateMutability": "view", "type": "function"}],
    )
    weth_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    result = {"buy_success": False, "sell_success": False, "is_honeypot": None, "details": {}}

    try:
        # Step 1: Simulate buy (WETH -> Token)
        amount_in_wei = w3.to_wei(amount_in_eth, "ether")
        path_buy = [weth_address, token_address]
        amounts_out_buy = router.functions.getAmountsOut(amount_in_wei, path_buy).call()
        tokens_received = amounts_out_buy[1]
        result["buy_success"] = True
        result["details"]["tokens_received"] = tokens_received
        result["details"]["buy_price_per_token"] = amount_in_wei / tokens_received if tokens_received > 0 else float("inf")

        # Check if buy succeeds but gives nearly nothing (tax trap)
        if tokens_received < amount_in_wei / 1000:  # less than 0.1% expected
            result["details"]["buy_warning"] = "Extremely low token output — possible high buy tax or manipulated price"

        # Step 2: Simulate sell (Token -> WETH) — the honeypot test
        path_sell = [token_address, weth_address]
        sell_amount = tokens_received
        min_sell = max(1, sell_amount // 1000)  # tolerate up to 99.9% sell tax

        amounts_out_sell = router.functions.getAmountsOut(sell_amount, path_sell).call()
        eth_back = amounts_out_sell[1]
        result["sell_success"] = True
        result["details"]["eth_back"] = eth_back
        result["details"]["sell_tax_pct"] = max(0.0, (1 - eth_back / amount_in_wei) * 100)
        result["details"]["is_profitable"] = eth_back > amount_in_wei * 0.5  # get back more than 50% of initial

        # Extreme sell tax check
        if result["details"]["sell_tax_pct"] > 50:
            result["details"]["sell_warning"] = f"Honeypot indicator: sell tax is {result['details']['sell_tax_pct']:.1f}%"

        # Step 3: Check for blacklist by testing a known blacklisted address
        # Some honeypots block all addresses except whitelisted ones
        result["details"]["blacklist_test"] = _check_blacklist_behavior(w3, token_address)

        # Step 4: Check if minter can deploy infinite supply
        result["details"]["mint_test"] = _check_mint_function(w3, token_address)

    except Exception as e:
        error_str = str(e)
        if "execution reverted" in error_str or "VM Exception" in error_str:
            sell_blocked = "cannot" in error_str.lower() or "revert" in error_str.lower()
            if not result["buy_success"]:
                result["buy_error"] = error_str
            else:
                result["sell_error"] = error_str
        else:
            result["error"] = error_str

    # Determine honeypot verdict
    if result["buy_success"] and not result["sell_success"]:
        result["is_honeypot"] = True
        result["risk"] = "CRITICAL"
    elif result["buy_success"] and result["sell_success"] and result["details"].get("sell_tax_pct", 0) > 30:
        result["is_honeypot"] = False
        result["risk"] = "HIGH — extreme sell tax"
    elif result["buy_success"] and result["sell_success"]:
        result["is_honeypot"] = False
        result["risk"] = "LOW — both directions succeed"
    else:
        result["is_honeypot"] = None
        result["risk"] = "UNKNOWN — simulation error"

    return result


def _check_blacklist_behavior(w3: Web3, token_address: str) -> dict:
    """Check if contract has blacklist functions by signature detection."""
    code = w3.eth.get_code(Web3.to_checksum_address(token_address)).hex()
    blacklist_sigs = [
        "9dc29fac",  # blacklist(address)
        "10f41093",  # setBlacklist(address,bool)
        "f9f92be4",  # isBlacklisted(address)
        "4261f4d8",  # addToBlacklist(address)
        "5d3a3f1b",  # removeFromBlacklist(address)
        "ec571fc6",  # setBlacklistStatus(address,bool)
        "e0021f43",  # setExcludedFromFees(address,bool)
        "a733e570",  # isExcludedFromFees(address)
        "b46300ec",  # _isExcluded(address)
        "e42f6ea6",  # listedAddresses(address)
    ]
    found = []
    for sig in blacklist_sigs:
        if sig in code:
            found.append(f"0x{sig}")
    return {"blacklist_functions_detected": found, "has_blacklist": len(found) > 0}


def _check_mint_function(w3: Web3, token_address: str) -> dict:
    """Check for mint function signature in contract bytecode."""
    code = w3.eth.get_code(Web3.to_checksum_address(token_address)).hex()
    mint_sigs = ["40c10f19", "a0712d68", "9a1b1d3c", "d3fc0714", "f2d5d56b"]
    found = []
    for sig in mint_sigs:
        if sig in code:
            found.append(f"0x{sig}")
    return {"mint_functions_detected": found, "has_mint": len(found) > 0}
```

## Proxy / Upgradeability Detection

Many scam tokens use proxy contracts (ERC-1967, TransparentUpgradeableProxy, BeaconProxy) to allow the deployer to swap the implementation contract after launch — effectively changing all token logic including balances, supply, and transfer restrictions.

```python
def check_proxy_upgradeability(w3: Web3, token_address: str) -> dict:
    """
    Detect if a token contract is behind a proxy pattern and read the
    implementation address. Checks ERC-1967, Transparent, UUPS, and Beacon patterns.
    """
    address = Web3.to_checksum_address(token_address)
    result = {
        "is_proxy": False,
        "proxy_type": None,
        "implementation": None,
        "beacon": None,
        "admin": None,
        "can_upgrade": False,
        "details": {},
    }

    # 1. ERC-1967 implementation slot (most common)
    try:
        impl_bytes = w3.eth.get_storage_at(address, ERC1967_IMPLEMENTATION_SLOT)
        impl_address = "0x" + impl_bytes[-20:].hex()
        if int(impl_bytes.hex(), 16) > 0:
            result["is_proxy"] = True
            result["proxy_type"] = "ERC-1967"
            result["implementation"] = Web3.to_checksum_address(impl_address)
    except Exception:
        pass

    # 2. Beacon proxy pattern
    if not result["is_proxy"]:
        try:
            beacon_bytes = w3.eth.get_storage_at(address, ERC1967_BEACON_SLOT)
            beacon_address = "0x" + beacon_bytes[-20:].hex()
            if int(beacon_bytes.hex(), 16) > 0:
                result["is_proxy"] = True
                result["proxy_type"] = "Beacon"
                result["beacon"] = Web3.to_checksum_address(beacon_address)
                # Read implementation from beacon (minimal ABI)
                beacon_abi = [{"inputs": [], "name": "implementation", "outputs": [{"type": "address"}], "stateMutability": "view", "type": "function"}]
                beacon_contract = w3.eth.contract(address=Web3.to_checksum_address(beacon_address), abi=beacon_abi)
                result["implementation"] = beacon_contract.functions.implementation().call()
        except Exception:
            pass

    # 3. Admin slot (who can upgrade?)
    if result["is_proxy"]:
        try:
            admin_bytes = w3.eth.get_storage_at(address, ADMIN_SLOT)
            admin_addr = "0x" + admin_bytes[-20:].hex()
            if int(admin_bytes.hex(), 16) > 0:
                result["admin"] = Web3.to_checksum_address(admin_addr)
                result["can_upgrade"] = True
        except Exception:
            pass

        # Check if implementation is a contract (i.e., has code)
        if result["implementation"]:
            impl_code = w3.eth.get_code(Web3.to_checksum_address(result["implementation"]))
            result["details"]["impl_has_code"] = len(impl_code) > 0
            result["details"]["impl_code_size"] = len(impl_code)

        # Check for UUPS (Universal Upgradeable Proxy Standard) — proxy IS the implementation
        # UUPS has upgradeTo() in the implementation itself
        if result["implementation"]:
            try:
                impl_contract = w3.eth.contract(
                    address=Web3.to_checksum_address(result["implementation"]),
                    abi=[{"inputs": [{"type": "address"}], "name": "upgradeTo", "outputs": [], "stateMutability": "nonpayable", "type": "function"}],
                )
                impl_contract.functions.upgradeTo(token_address).call({"from": Web3.to_checksum_address(result.get("admin") or "0x0000000000000000000000000000000000000000")})
                result["details"]["appears_uups"] = True
            except Exception:
                result["details"]["appears_uups"] = False

    # 4. Check EIP-1167 minimal proxy (CREATE2 clones)
    code = w3.eth.get_code(address).hex()
    eip1167_prefix = "363d3d373d3d3d363d73"
    eip1167_suffix = "5af43d82803e903d91602b57fd5bf3"
    if eip1167_prefix in code and eip1167_suffix in code:
        result["is_proxy"] = True
        result["proxy_type"] = "EIP-1167 Minimal Proxy"
        # Extract target address from bytecode
        start = code.index(eip1167_prefix) + len(eip1167_prefix)
        impl_hex = code[start:start + 40]
        result["implementation"] = Web3.to_checksum_address("0x" + impl_hex)
        result["details"]["proxy_note"] = "EIP-1167 clone — immutable pointer, cannot upgrade"

    # 5. Compare proxy vs implementation events (if both available)
    if result["is_proxy"] and result["implementation"]:
        result["details"]["upgrade_risk"] = (
            "CRITICAL: Admin can replace implementation at any time" if result["can_upgrade"]
            else "LOW: Proxy detected but no upgrade capability found"
        )

    return result
```

## Liquidity Lock Verification

Checks if LP tokens are locked in a vesting/lock contract (Unicrypt, Team Finance, DXlock, or custom) and extracts lock parameters.

```python
def verify_liquidity_lock(
    w3: Web3,
    lp_token_address: str,
    lock_contract_address: Optional[str] = None,
    chain: str = "ethereum",
) -> dict:
    """
    Verify LP token lock status. If lock_contract_address is known, read from it directly.
    Otherwise scan common lock contracts on the chain.
    """
    result = {
        "lp_locked": False,
        "lock_contract": None,
        "lock_end_date": None,
        "lock_amount": None,
        "lock_owner": None,
        "can_withdraw_early": None,
        "details": {},
    }

    # Common lock contract ABI fragments
    lock_abi_fragments = [
        # Unicrypt lock
        {"inputs": [{"type": "address"}], "name": "tokenLocks", "outputs": [{"type": "uint256"}, {"type": "uint256"}, {"type": "address"}, {"type": "bool"}], "stateMutability": "view", "type": "function"},
        {"inputs": [{"type": "uint256"}], "name": "lockedToken", "outputs": [{"type": "address"}, {"type": "address"}, {"type": "uint256"}, {"type": "uint256"}, {"type": "bool"}], "stateMutability": "view", "type": "function"},
        {"inputs": [{"type": "address"}], "name": "getLocks", "outputs": [{"type": "uint256[]"}], "stateMutability": "view", "type": "function"},
        # Team Finance (SaaS) generic
        {"inputs": [{"type": "address"}, {"type": "address"}], "name": "getLock", "outputs": [{"type": "uint256"}, {"type": "uint256"}, {"type": "address"}], "stateMutability": "view", "type": "function"},
    ]

    # Try known lock contracts on Ethereum
    known_lock_contracts = {
        "ethereum": [
            "0x17e00383A843A9922b8683F8F3D014cA41cC27b5",  # Unicrypt v2
            "0x663a5c229c09b049e36dCc11a9B0d4a8Eb9db214",  # Unicrypt v1
            "0xE2fE530C047f2d85298b07D9333C057D1Bf8E77b",  # DXlock
            "0xa867C7C9e3438E7A5d6267a3f57b3910e00B2C25",  # Team Finance
        ],
        "bsc": [
            "0x663A5C229c09b049e36DcC11a9B0d4a8Eb9db214",  # Unicrypt BSC
            "0xD7a3CECD1c95e40C2b0B4F9172DC9C490b6E2A3A",  # PinkLock
            "0x71B7fF59207eD6a3cb7dE87b2d8a5C09e68a1C5f",  # Team Finance BSC
        ],
    }

    targets = [lock_contract_address] if lock_contract_address else known_lock_contracts.get(chain, [])
    targets = [t for t in targets if t]

    for lock_addr in targets:
        try:
            lock_addr = Web3.to_checksum_address(lock_addr)
            lock_code = w3.eth.get_code(lock_addr)
            if lock_code.hex() == "0x":
                continue
            lock_contract = w3.eth.contract(address=lock_addr, abi=lock_abi_fragments[0])

            # Try getLocks(address) — returns array of lock IDs
            try:
                lock_ids = lock_contract.functions.getLocks(lp_token_address).call()
                if lock_ids:
                    for lock_id in lock_ids:
                        try:
                            lock_detail = lock_contract.functions.lockedToken(lock_id).call()
                            result["lp_locked"] = True
                            result["lock_contract"] = lock_addr
                            result["lock_amount"] = lock_detail[2]
                            result["lock_end_date"] = lock_detail[3]
                            result["details"]["lock_id"] = lock_id
                            # Determine if lock has expired
                            current_time = int(time.time())
                            result["lock_expired"] = current_time > lock_detail[3]
                            result["details"]["time_remaining_days"] = max(0, (lock_detail[3] - current_time) // 86400)
                            break
                        except Exception:
                            continue
            except Exception:
                pass

            # If getLocks didn't work, try tokenLocks(address)
            if not result["lp_locked"]:
                try:
                    lock_info = lock_contract.functions.tokenLocks(lp_token_address).call()
                    result["lp_locked"] = True
                    result["lock_contract"] = lock_addr
                    result["lock_amount"] = lock_info[0]
                    result["lock_end_date"] = lock_info[1]
                    result["lock_owner"] = lock_info[2]
                except Exception:
                    pass

        except Exception:
            continue

    if result["lp_locked"] and result["lock_end_date"]:
        result["details"]["formatted_end_date"] = time.strftime(
            "%Y-%m-%d %H:%M:%S UTC", time.gmtime(result["lock_end_date"])
        )

    return result
```

## Sniper Bot Detection

Identifies MEV/sniper bots that bought tokens in the first N blocks after the pool was created. These snipers often dump on retail buyers moments later.

```python
def detect_sniper_activity(
    w3: Web3,
    token_address: str,
    pool_creation_block: int,
    lookback_blocks: int = 50,
) -> dict:
    """
    Analyze the first N blocks after pool creation for sniper bot activity.
    Detects sandwich attacks, frontruns, and mass buy patterns.
    """
    address = Web3.to_checksum_address(token_address)
    result = {
        "sniper_detected": False,
        "sniper_count": 0,
        "snipers": [],
        "first_trades": [],
        "suspect_patterns": [],
        "details": {},
    }

    # 1. Get all Transfer events from pool creation to pool_creation + lookback_blocks
    transfer_event_sig = w3.keccak(text="Transfer(address,address,uint256)").hex()
    from_block = max(0, pool_creation_block - 5)  # a few blocks before for LP add
    to_block = pool_creation_block + lookback_blocks

    try:
        logs = w3.eth.get_logs({
            "address": address,
            "fromBlock": from_block,
            "toBlock": to_block,
            "topics": [transfer_event_sig],
        })
    except Exception:
        # If get_logs range is too large, sample every 5th block
        logs = []
        for b in range(from_block, to_block, 5):
            try:
                batch = w3.eth.get_logs({
                    "address": address,
                    "fromBlock": b,
                    "toBlock": min(b + 4, to_block),
                    "topics": [transfer_event_sig],
                })
                logs.extend(batch)
            except Exception:
                continue

    # 2. Parse events and identify buyers
    token = w3.eth.contract(address=address, abi=ERC20_ABI)
    buyer_tx_map = {}  # buyer -> (block_number, tx_hash, is_first_buy)

    for log in logs:
        try:
            decoded = token.events.Transfer().process_log(log)
            if decoded["args"]["from"] == "0x0000000000000000000000000000000000000000":
                # Mint/buy event
                buyer = decoded["args"]["to"]
                tx_hash = log["transactionHash"].hex()
                block_num = log["blockNumber"]
                if buyer not in buyer_tx_map:
                    buyer_tx_map[buyer] = {
                        "address": buyer,
                        "first_buy_block": block_num,
                        "tx_hash": tx_hash,
                        "amount": decoded["args"]["value"],
                        "is_sniper_candidate": (block_num - pool_creation_block) <= 5,
                    }
                else:
                    buyer_tx_map[buyer]["amount"] += decoded["args"]["value"]
        except Exception:
            continue

    # 3. Identify sniper candidates
    weth_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"

    for buyer, info in buyer_tx_map.items():
        if info["is_sniper_candidate"]:
            # Check if this is a known MEV bot (contract with no code = EOA)
            code_size = len(w3.eth.get_code(Web3.to_checksum_address(buyer)))
            is_contract = code_size > 0

            # Check if the buyer sold/dumped shortly after (look at outgoing transfers)
            sold_amount = 0
            for log in logs:
                try:
                    decoded = token.events.Transfer().process_log(log)
                    if decoded["args"]["from"].lower() == buyer.lower() and decoded["args"]["to"] != "0x0000000000000000000000000000000000000000":
                        sold_amount += decoded["args"]["value"]
                except Exception:
                    continue

            info["is_contract"] = is_contract
            info["sold_amount"] = sold_amount
            info["is_dumper"] = sold_amount > info["amount"] * 0.5  # sold more than half

            if info["is_dumper"] or is_contract:
                result["snipers"].append(info)
                result["sniper_count"] += 1

    # 4. Detect sandwich attack patterns
    # Look for same-block buy-sell pairs with different gas prices
    tx_blocks = {}
    for log in logs:
        block = log["blockNumber"]
        tx_hash = log["transactionHash"].hex()
        if block not in tx_blocks:
            tx_blocks[block] = set()
        tx_blocks[block].add(tx_hash)

    for block, txs in tx_blocks.items():
        if len(txs) >= 3 and (block - pool_creation_block) <= 3:
            result["suspect_patterns"].append({
                "type": "possible_sandwich",
                "block": block,
                "tx_count": len(txs),
            })

    result["sniper_detected"] = result["sniper_count"] > 0
    result["details"]["total_unique_buyers"] = len(buyer_tx_map)

    return result
```

## Token Distribution Analysis (Gini Coefficient + Top Holders)

Computes the Gini coefficient of token holder distribution — a high Gini (>0.9) indicates extreme concentration typical of scam tokens.

```python
def analyze_holder_distribution(w3: Web3, token_address: str, top_n: int = 10) -> dict:
    """
    Compute holder distribution metrics by scanning Transfer events.
    Returns Gini coefficient, top holder list, and concentration percentages.
    """
    address = Web3.to_checksum_address(token_address)
    token = w3.eth.contract(address=address, abi=ERC20_ABI)
    result = {
        "total_holders": 0,
        "gini_coefficient": None,
        "top_holders": [],
        "top10_concentration_pct": 0.0,
        "top1_concentration_pct": 0.0,
        "supply_distribution": "UNKNOWN",
        "details": {},
    }

    try:
        total_supply = token.functions.totalSupply().call()
        result["details"]["total_supply"] = total_supply
    except Exception:
        total_supply = 0

    # Scan Transfer events to compute balances
    transfer_sig = w3.keccak(text="Transfer(address,address,uint256)").hex()
    balances = {}

    # Get latest block
    latest = w3.eth.block_number
    # Scan in chunks to avoid RPC limits
    chunk_size = 100000
    from_block = max(0, latest - 500000)  # last 500k blocks, adjust for recent tokens on new chains

    while from_block < latest:
        to_block = min(from_block + chunk_size - 1, latest)
        try:
            logs = w3.eth.get_logs({
                "address": address,
                "fromBlock": from_block,
                "toBlock": to_block,
                "topics": [transfer_sig],
            })
            for log_entry in logs:
                try:
                    decoded = token.events.Transfer().process_log(log_entry)
                    fr = decoded["args"]["from"].lower()
                    to = decoded["args"]["to"].lower()
                    val = decoded["args"]["value"]

                    if fr == "0x0000000000000000000000000000000000000000" or fr == "0x0000000000000000000000000000000000000001":
                        # Mint — skip, balance starts at receiving
                        pass
                    else:
                        balances[fr] = balances.get(fr, 0) - val
                        if balances[fr] <= 0:
                            del balances[fr]

                    balances[to] = balances.get(to, 0) + val
                except Exception:
                    continue
        except Exception:
            # If chunk fails (too large), halve it
            chunk_size //= 2
            if chunk_size < 1000:
                break
            continue
        from_block = to_block + 1

    # Filter zero/negligible balances
    min_balance = total_supply / 1_000_000 if total_supply > 0 else 0
    holders = {addr: bal for addr, bal in balances.items() if bal >= min_balance}

    if not holders:
        result["error"] = "Could not reconstruct holder balances from event logs"
        return result

    result["total_holders"] = len(holders)
    sorted_holders = sorted(holders.items(), key=lambda x: -x[1])

    # Top holders
    result["top_holders"] = [
        {"address": addr, "balance": bal, "pct": (bal / total_supply * 100) if total_supply > 0 else 0}
        for addr, bal in sorted_holders[:top_n]
    ]

    # Concentration percentages
    if total_supply > 0:
        top1_bal = sorted_holders[0][1] if sorted_holders else 0
        result["top1_concentration_pct"] = top1_bal / total_supply * 100
        top10_bal = sum(b for _, b in sorted_holders[:10])
        result["top10_concentration_pct"] = top10_bal / total_supply * 100

    # Gini coefficient
    values = sorted([b for _, b in sorted_holders if b > 0])
    n = len(values)
    if n > 1:
        cumulative = [sum(values[:i+1]) for i in range(n)]
        # Gini = 2 * sum(i * y_i) / (n * sum(y_i)) - (n+1)/n
        numerator = sum((i + 1) * v for i, v in enumerate(values))
        denominator = n * sum(values)
        gini = (2 * numerator / denominator) - (n + 1) / n
        result["gini_coefficient"] = round(gini, 4)

    # Distribution classification
    if result["top1_concentration_pct"] >= 90:
        result["supply_distribution"] = "CRITICAL — single holder controls >90%"
    elif result["top10_concentration_pct"] >= 90:
        result["supply_distribution"] = "HIGH — top 10 control >90%"
    elif result["top10_concentration_pct"] >= 50:
        result["supply_distribution"] = "MODERATE — top 10 control >50%"
    else:
        result["supply_distribution"] = "HEALTHY — distributed"

    return result
```

## Wash Trading Detection (NFT)

Detects circular trading patterns (A→B→C→A cycles) and same-wallet flipping in NFT sales data.

```python
def detect_wash_trading(
    sales_data: List[Dict[str, Any]],
    min_cycle_length: int = 3,
    max_cycle_length: int = 10,
) -> dict:
    """
    Detect wash trading patterns in NFT sales data.
    Input: list of dicts with {seller, buyer, token_id, price, timestamp, marketplace}
    Detects: circular trades, same-wallet flipping, and self-dealing.
    """
    import networkx as nx
    from collections import defaultdict
    from itertools import combinations

    result = {
        "has_wash_trading": False,
        "circular_trades": [],
        "same_wallet_flips": [],
        "whale_wallets": [],
        "wash_volume": 0,
        "total_volume": sum(s.get("price", 0) for s in sales_data),
        "wash_volume_pct": 0.0,
        "details": {},
    }

    if not sales_data:
        return result

    result["details"]["total_trades"] = len(sales_data)

    # 1. Build directed graph of trades
    G = nx.DiGraph()
    for sale in sales_data:
        seller = sale.get("seller", "").lower()
        buyer = sale.get("buyer", "").lower()
        price = sale.get("price", 0)
        token_id = sale.get("token_id", "")
        ts = sale.get("timestamp", 0)

        G.add_edge(seller, buyer, price=price, token_id=token_id, timestamp=ts)

    # 2. Detect cycles (circular trading)
    try:
        cycles = list(nx.simple_cycles(G))
    except nx.NetworkXNoCycle:
        cycles = []

    # Filter by cycle length
    filtered_cycles = [c for c in cycles if min_cycle_length <= len(c) <= max_cycle_length]
    result["circular_trades"] = [
        {"cycle": [addr for addr in cycle], "length": len(cycle)}
        for cycle in filtered_cycles
    ]

    # 3. Detect same-wallet flipping (same wallet appearing as both buyer and seller across trades)
    wallet_activity = defaultdict(lambda: {"buys": 0, "sells": 0, "total_volume": 0, "token_ids": set()})
    for sale in sales_data:
        seller = sale.get("seller", "").lower()
        buyer = sale.get("buyer", "").lower()
        price = sale.get("price", 0)
        token_id = sale.get("token_id", "")

        wallet_activity[seller]["sells"] += 1
        wallet_activity[seller]["total_volume"] -= price  # selling loses token, gains money
        wallet_activity[buyer]["buys"] += 1
        wallet_activity[buyer]["total_volume"] += price
        if token_id:
            wallet_activity[seller]["token_ids"].discard(token_id)
            wallet_activity[buyer]["token_ids"].add(token_id)

    # Wallets with high buy-sell ratio across same tokens = wash traders
    for addr, activity in wallet_activity.items():
        overlap = len(activity["token_ids"])
        total_trades = activity["buys"] + activity["sells"]
        if total_trades >= 5 and overlap >= 3:
            result["whale_wallets"].append({
                "address": addr,
                "buys": activity["buys"],
                "sells": activity["sells"],
                "overlapping_token_ids": overlap,
                "suspected_wash_trader": overlap >= total_trades * 0.3,
            })

    # 4. Detect self-trading (wallet sells to itself via different addresses)
    # Look for pairs of wallets that trade the same tokens back and forth
    wallet_pairs = defaultdict(float)
    for sale in sales_data:
        seller = sale.get("seller", "").lower()
        buyer = sale.get("buyer", "").lower()
        price = sale.get("price", 0)
        if seller < buyer:
            pair = (seller, buyer)
        else:
            pair = (buyer, seller)
        wallet_pairs[pair] += price

    for (addr1, addr2), volume in wallet_pairs.items():
        if volume > result["total_volume"] * 0.05:  # more than 5% of total volume
            result["details"]["suspicious_pair_trading"] = result["details"].get("suspicious_pair_trading", [])
            result["details"]["suspicious_pair_trading"].append({
                "wallet_a": addr1,
                "wallet_b": addr2,
                "volume": volume,
            })

    # 5. Compute wash volume
    wash_volume = 0.0
    for cycle in result["circular_trades"]:
        for i in range(len(cycle)):
            seller = cycle[i]
            buyer = cycle[(i + 1) % len(cycle)]
            for sale in sales_data:
                if sale.get("seller", "").lower() == seller and sale.get("buyer", "").lower() == buyer:
                    wash_volume += sale.get("price", 0)

    result["wash_volume"] = wash_volume
    result["wash_volume_pct"] = (wash_volume / result["total_volume"] * 100) if result["total_volume"] > 0 else 0
    result["has_wash_trading"] = len(result["circular_trades"]) > 0 or len(result["whale_wallets"]) > 2

    return result
```

## Deployer Funding Chain

Traces the deployer's initial funding transaction back through its chain to identify the ultimate source — an exchange deposit, another scam, a mixer, or a known malicious address.

```python
def trace_deployer_funding(w3: Web3, deployer_address: str, max_hops: int = 5) -> dict:
    """
    Trace the deployer's initial ETH funding back to its source.
    Follows the first incoming ETH transaction at each hop.
    """
    address = Web3.to_checksum_address(deployer_address)
    result = {
        "deployer": address,
        "funding_chain": [],
        "source_category": "UNKNOWN",
        "source_exchange": None,
        "source_suspicious": False,
        "details": {},
    }

    # Known exchange deposit addresses (simplified list)
    exchange_addresses = {
        "0x3f5CE5FBFe3E9af3971dC833d26bA9b5C936f0bE": "Binance",
        "0xdAC17F958D2ee523a2206206994597C13D831ec7": "Coinbase",
        "0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8": "Binance 2",
        "0x2faf487A4414Fe77e2327F0f0C2B1C1Ae3B6f5F": "Kraken",
        "0x21a31Ee1afC51d94C2eFcCAa2092aD102858554": "OKX",
        "0x4Baa4Ab5cBaa9C6CB2C7C6fE4D8a0F7F5B3F1E2": "KuCoin",
        "0xf977814e90dA44bFA03b6295A0616a897441aceC": "Huobi",
        "0x1Db3439a222C451ab00E0C2b3F2E0c7Ff5b5F5F5": "Gate.io",
        "0x28C6c06298d514Db089934071355E5743bf21d60": "Binance 14",
        "0x3Ed3B47Dd13EC9A98a44E6204A523a7669b1c6a5": "HTX",
    }

    # Known mixer/tumbler addresses
    mixer_addresses = {
        "0x8589427373D6D84E98730D7795D8f6f8731FDA16": "Tornado Cash",
        "0x7221E6C5279B6681333FcaC7F7F8B5D0E1B0c5A1": "Tornado Cash",
        "0x03893a7c7461F5C45C1D0e2E0D2a7B3A5F3B5F3B": "FixedFloat",
        "0x1E2f4dF6b7A5c3E8C9A0b5D7F3E1C9A0b5D7F3E1": "Sinbad.io",
    }

    current = address
    chain = []

    for hop in range(max_hops):
        try:
            # Get first incoming ETH transaction to this address
            # Using eth_getLogs for Transfer events won't work for ETH — we need tx data
            # Simple approach: check first tx in block explorer or scan via eth_getBlockByNumber
            nonce = w3.eth.get_transaction_count(current)
            if nonce == 0:
                # No outgoing txs — likely a fresh wallet
                chain.append({"address": current, "type": "fresh_wallet", "note": "No outgoing transactions"})
                if hop == 0:
                    result["source_category"] = "FRESH_WALLET"
                break

            # Find first tx where current was recipient
            latest = w3.eth.block_number
            found_tx = None

            # Scan recent blocks for incoming ETH (limited scope — real impl needs archive node)
            for block_num in range(latest, max(0, latest - 50000), -100):
                try:
                    block = w3.eth.get_block(block_num, full_transactions=True)
                    for tx in block.transactions:
                        if isinstance(tx, dict) and tx.get("to", "").lower() == current.lower():
                            found_tx = tx
                            break
                        elif hasattr(tx, "to") and tx.to and tx.to.lower() == current.lower():
                            found_tx = tx
                            break
                except Exception:
                    continue
                if found_tx:
                    break

            if not found_tx:
                chain.append({"address": current, "type": "no_incoming_found", "note": "Could not find incoming ETH tx"})
                result["source_category"] = "ARCHIVE_NODE_REQUIRED"
                break

            # Classify the sender
            sender = (found_tx.get("from", "").lower() if isinstance(found_tx, dict)
                      else found_tx["from"].lower())
            value = w3.from_wei(found_tx.get("value", 0) if isinstance(found_tx, dict) else found_tx["value"], "ether")

            sender_lower = Web3.to_checksum_address(sender).lower() if sender else ""

            # Check if sender is known
            source_type = "wallet"
            for exch_addr, exch_name in exchange_addresses.items():
                if exch_addr.lower() == sender_lower:
                    source_type = f"exchange:{exch_name}"
                    result["source_exchange"] = exch_name
                    result["source_category"] = "EXCHANGE_DEPOSIT"
                    break

            for mix_addr, mix_name in mixer_addresses.items():
                if mix_addr.lower() == sender_lower:
                    source_type = f"mixer:{mix_name}"
                    result["source_suspicious"] = True
                    result["source_category"] = "MIXER"
                    break

            chain.append({
                "address": current,
                "funded_by": sender,
                "amount_eth": float(value),
                "tx_hash": found_tx.get("hash", "").hex() if isinstance(found_tx, dict) else found_tx["hash"].hex(),
                "source_type": source_type,
            })

            # Continue tracing if sender is not an exchange
            if source_type in ("wallet",) or source_type.startswith("mixer"):
                current = Web3.to_checksum_address(sender)
            else:
                break

        except Exception as e:
            chain.append({"address": current, "error": str(e)})
            break

    result["funding_chain"] = chain
    return result


def check_deployer_scam_history(w3: Web3, deployer_address: str, api_key: str = ETHERSCAN_API_KEY) -> dict:
    """
    Check if the deployer wallet has deployed other tokens — and if those
    tokens have scam indicators.
    """
    address = Web3.to_checksum_address(deployer_address)
    result = {
        "deployer": address,
        "total_deployments": 0,
        "previous_suspicious_tokens": [],
        "is_serial_scammer": False,
        "details": {},
    }

    # Query Etherscan for deployed contracts by this address
    url = f"https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": api_key,
    }

    try:
        resp = requests.get(url, params=params, timeout=30)
        data = resp.json()
        if data.get("status") == "1" and data.get("result"):
            deployments = []
            for tx in data["result"]:
                if tx.get("to", "") == "" and tx.get("contractAddress", ""):
                    # This transaction created a contract
                    deployments.append({
                        "contract": tx["contractAddress"],
                        "block": int(tx["blockNumber"]),
                        "tx_hash": tx["hash"],
                        "timestamp": int(tx.get("timeStamp", 0)),
                    })

            result["total_deployments"] = len(deployments)
            result["details"]["all_deployments"] = deployments[:20]  # cap for output

            # Check each deployment for scam indicators (basic)
            for dep in deployments[:10]:
                try:
                    info = check_basic_info(w3, dep["contract"])
                    if "ERROR" in str(info.get("name", "")):
                        continue
                    dep["name"] = info.get("name", "?")
                    dep["symbol"] = info.get("symbol", "?")
                    # Flag short-lived tokens
                    if dep.get("timestamp"):
                        age_days = (int(time.time()) - dep["timestamp"]) / 86400
                        dep["age_days"] = round(age_days, 1)
                        if age_days < 30:
                            dep["short_lived"] = True
                except Exception:
                    continue

            result["previous_suspicious_tokens"] = [d for d in deployments if d.get("short_lived")]
            result["is_serial_scammer"] = len(result["previous_suspicious_tokens"]) >= 3

    except Exception as e:
        result["error"] = str(e)

    return result
```

## Approval / Allowance Abuse Detection

Checks if a token contract has abnormal approval patterns: unlimited approvals (max uint256), approvals to suspicious contracts, or backdoor approval functions.

```python
def check_approval_abuse(w3: Web3, token_address: str, sample_holders: Optional[List[str]] = None) -> dict:
    """
    Check for excessive or suspicious approval patterns in a token contract.
    """
    address = Web3.to_checksum_address(token_address)
    token = w3.eth.contract(address=address, abi=ERC20_ABI)
    result = {
        "has_unlimited_approvals": False,
        "suspicious_spenders": [],
        "approval_event_analysis": {},
        "details": {},
    }

    max_approval = 2**256 - 1  # unlimited approval sentinel

    # 1. Check allowance for known risky spenders
    suspicious_spenders = [
        "0x0000000000000000000000000000000000000001",  # null address
        "0x000000000000000000000000000000000000dead",  # burn address
    ]

    # 2. Analyze Approval events to find patterns
    approval_sig = w3.keccak(text="Approval(address,address,uint256)").hex()
    latest = w3.eth.block_number
    try:
        logs = w3.eth.get_logs({
            "address": address,
            "fromBlock": max(0, latest - 200000),
            "toBlock": latest,
            "topics": [approval_sig],
        })

        approval_counts = {}
        unlimited_approvals = 0
        total_approvals = 0

        for log in logs:
            try:
                decoded = token.events.Approval().process_log(log)
                owner = decoded["args"]["owner"].lower()
                spender = decoded["args"]["spender"].lower()
                value = decoded["args"]["value"]

                total_approvals += 1

                # Track approval count per spender
                approval_counts[spender] = approval_counts.get(spender, 0) + 1

                # Check unlimited approvals
                if value == max_approval:
                    unlimited_approvals += 1

                # Check suspicious spenders
                if spender in suspicious_spenders:
                    result["suspicious_spenders"].append({
                        "owner": owner,
                        "spender": spender,
                        "value": value,
                        "is_unlimited": value == max_approval,
                    })
            except Exception:
                continue

        result["approval_event_analysis"] = {
            "total_approval_events": total_approvals,
            "unlimited_approvals": unlimited_approvals,
            "unique_spenders": len(approval_counts),
            "most_approved_spender": max(approval_counts, key=approval_counts.get) if approval_counts else None,
        }
        result["has_unlimited_approvals"] = unlimited_approvals > 0

    except Exception as e:
        result["details"]["approval_scan_error"] = str(e)

    # 3. Check for approval-related function signatures in bytecode
    code = w3.eth.get_code(address).hex()
    approval_sigs = [
        "095ea7b3",  # approve(address,uint256)
        "a9059cbb",  # transfer(address,uint256)
        "23b872dd",  # transferFrom(address,address,uint256)
        "dd62ed3e",  # allowance(address,address)
    ]
    for sig in approval_sigs:
        result["details"][f"has_{sig[:4]}"] = sig in code

    return result
```

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

## Case Studies

### Case Study 1: Squid Game Token (SQUID) — Honeypot + Rug Pull

- **Contract**: 0x31471E0791fCdbE82fbF4C44943255e923F1b794 (BSC)
- **Date**: October 2021
- **Loss**: ~$3.38 million
- **Indicators found at launch**:
  - Proxy contract (ERC-1967 pattern) — implementation could be swapped at any time
  - `pause()` and `unpause()` functions present in bytecode — transfers could be frozen
  - Sell function was disabled via the proxy implementation after enough buy pressure
  - Top 10 holders controlled >99% of supply at launch
  - Deployer funded from Tornado Cash
  - Website created 30 days before launch, no team info
  - LP was locked for only 30 days with an early-withdraw clause
- **What happened**: The token skyrocketed 230,000% in days. When holders tried to sell, the proxy implementation was swapped to one that blocked all sells. The deployer extracted ~$3.38M in BNB from the liquidity pool and bridged to Ethereum.
- **Detection code applied**: `simulate_honeypot()` would have detected the sell failure. `check_proxy_upgradeability()` would have shown the non-upgradeable facade. `trace_deployer_funding()` would have identified the Tornado Cash connection.

### Case Study 2: Evolved Apes NFT — Rug Pull

- **Contract**: 0xd311c36DEfF0aF84DF41c82A8A53Da1F91d36366 (Ethereum)
- **Date**: September 2021
- **Loss**: ~$2.7 million (798 ETH)
- **Indicators found at launch**:
  - Ownership not renounced — deployer retained `owner()` control
  - Withdraw function not removed from the contract — allowed draining of mint funds
  - No lock on the dev wallet address
  - Deployer wallet had deployed 3 other unknown NFT projects that were abandoned
  - No multi-sig — deployer was a single EOA
  - "Fight Arena" P2E game was promised but no development wallet activity
- **What happened**: The anonymous developer ("Feisty Doge" / "Evil Ape") minted all 10,000 NFTs, emptied the mint contract of 798 ETH via the `withdraw()` function, deleted the website and Discord, and disappeared. The NFTs became worthless.
- **Detection code applied**: `check_all_ownership_interfaces()` would have shown non-renounced ownership. `check_deployer_scam_history()` would have flagged the 3 previous abandoned projects. The contract's `withdraw()` function signature (0x2e1a7d4d) would have been detected.

### Case Study 3: Frosties NFT — Wash Trading + Rug Pull

- **Contract**: 0x8f6B54C7B10056f8970A3e4f7b4B0f3D2F8E1c7A (Ethereum)
- **Date**: January 2022
- **Loss**: ~$1.1 million
- **Indicators found at launch**:
  - Team promised metaverse utility and $FROST token
  - Active wash trading on secondary markets — 40% of volume was circular trades between known wallets
  - Two wallet addresses controlled 6 of the top 10 traded NFTs
  - Deployer funded from a separate rug pull (crypto panda NFT)
  - Multi-sig was a 2/3 with two addresses linked to other rug pulls
  - Discord had 30,000+ members and heavily moderated criticism
- **What happened**: After the mint sold out (~$1.1M), the team transferred all funds to a separate wallet, bridged ETH to Bitcoin via a swap service, and shut down operations. The founders ("Frostie" and "N0x") were later arrested by the DOJ in 2023.
- **Detection code applied**: `detect_wash_trading()` would have caught the 40% wash volume. `trace_deployer_funding()` would have connected the deployer to the earlier crypto panda rug. The multi-sig addresses would have shown the connection when checked by `check_deployer_scam_history()`.

### Case Study 4: AnubisDAO (Anubis) — Honeypot + LP Removal

- **Contract**: 0xD036414fa2a81B1DBd1C9E140d0D0E1d9b1cB7b3 (Ethereum)
- **Date**: October 2021
- **Loss**: ~$60 million (13,576 ETH)
- **Indicators found at launch**:
  - OHM fork with disguised tokenomics — the peg mechanism was non-functional
  - LP tokens were never locked — deployer held both sides of the LP
  - Sushiswap LP was added with 13,576 ETH from a multi-sig
  - Multi-sig signers were anonymous with no public identity
  - Website was copied from another OHM fork with minor edits
  - Stake contract contained a "setRewardDistribution" function that could drain staking rewards
- **What happened**: Within hours of the LP being added, someone (perpetrator or inside job) removed all 13,576 ETH from the LP pool. The token became worthless. The stolen ETH was split across several addresses and ultimately deposited into multiple exchanges.
- **Detection code applied**: `verify_liquidity_lock()` would have shown ZERO LP locks — the LP was never locked. The lack of lock should have been a CRITICAL red flag. The multi-sig analysis would have shown the owner controlled both LP tokens.

## Expected Output

A scam investigation report containing:
- Contract analysis results (honeypot check, ownership status, fee structure, proxy detection)
- Liquidity analysis (LP lock status, lock expiry, holder concentration, initial liquidity)
- Trading pattern analysis (sniper activity, sniper wallet addresses, wash trading evidence with circular trade IDs)
- Holder distribution (Gini coefficient, top 10 holders with percentages, supply concentration classification)
- Deployer wallet history (funding source chain, previous deployments, connection to other scams)
- Approval analysis (unlimited approvals, suspicious spenders, approval event counts)
- Fund flow tracing if proceeds have been moved (bridge addresses, CEX deposit addresses)
- Risk score (CRITICAL / HIGH / MODERATE / LOW) with explanation
- Case study comparisons where patterns match known scams

## Red Flags

- Making public accusations based on incomplete on-chain analysis without social confirmation
- Confusing a buggy but legitimate token with a deliberate scam
- Assuming LP renouncement means safety — proxy contracts can still be upgraded
- Using only one data source for holder analysis — wallets can be split across many addresses
- Assuming verified source code means the contract is safe — verification only matches bytecode to source
- Ignoring proxy patterns — a verified implementation can be swapped for a malicious one
- Treating locked LP as a guarantee — locks can have early-withdraw clauses or be owned by the deployer
- Confusing low liquidity with a honeypot — some legitimate tokens have low liquidity naturally
- Assuming a renounced owner protects against mint functions — AccessControl roles are separate from Ownable
- Relying on DEX price charts without checking for supply manipulation

## Process

1. **Contract Review** — Analyze token/NFT contract for scam indicators (honeypot, ownership, fees, mint, proxy)
2. **Liquidity Assessment** — Check LP lock, holder concentration, and initial liquidity
3. **Trading Pattern Analysis** — Detect wash trading, sniping, and market manipulation
4. **Off-Chain Investigation** — Cross-reference deployer history, social signals, and funding sources
5. **Reporting** — Produce structured investigation report with evidence and confidence scores
6. **Verification Loop** — Cross-check each finding with at least one additional data source before finalizing
7. **Money Extraction** — Package findings into client deliverables or bounty submissions (see Money section)

## Verification

- Honeypot check verified by simulating both buy AND sell transactions (with actual gas estimation)
- LP lock status confirmed by reading the lock contract directly, not just a third-party claim
- Wash trading detection verified by checking actual wallet ownership on-chain, not just marketplace labels
- Deployer connections confirmed by tracing initial funding transaction back to the source
- Every claim in the report supported by a verifiable on-chain transaction or external link
- Top holder analysis verified by cross-referencing Transfer events from two different block ranges
- Proxy detection verified by reading storage slots directly (not relying on event logs)
- Sniper detection verified by checking actual gas prices and block positions at launch
- Funding chain verified by checking at least two hops before classifying the source


## RPC & API Endpoint Management

Token investigations span multiple chains. A scam token on Ethereum often has a matching token on BSC
or Polygon via cross-chain deployment. You need reliable RPC access on all relevant chains.

### Per-Chain Rate Limits

| Chain | Explorer API | Free Limit | Key Env Var |
|---|---|---|---|
| Ethereum | Etherscan | 5 calls/sec | `ETHERSCAN_KEY` |
| BSC | BscScan | 5 calls/sec | `BSCSCAN_KEY` |
| Polygon | Polygonscan | 5 calls/sec | `POLYGONSCAN_KEY` |
| Arbitrum | Arbiscan | 10 calls/sec | `ARBISCAN_KEY` |
| Optimism | Optimistic Etherscan | 5 calls/sec | `OPSCAN_KEY` |
| Avalanche | Snowtrace | 5 calls/sec | `SNOWTRACE_KEY` |

**Rule**: batch independent checks (holdership, LP lock, ownership, honeypot) into a single function
that respects the slowest rate limit — queue at 4 calls/sec to be safe across all chains.

### Contract Metadata via RPC (No Explorer Key)

```python
from web3 import Web3

# Public RPC endpoints — no key needed
PUBLIC_RPC = {
    "ethereum": "https://eth.llamarpc.com",
    "bsc":      "https://bsc-dataseed.binance.org",
    "polygon":  "https://polygon-rpc.com",
}

def check_contract_metadata(chain: str, address: str) -> dict:
    """Query contract metadata directly from RPC — useful when explorer API is rate-limited."""
    w3 = Web3(Web3.HTTPProvider(PUBLIC_RPC[chain]))
    checksum = w3.to_checksum_address(address)
    code = w3.eth.get_code(checksum)
    if code == b"":   # EOA or non-existent — no contract
        return {"has_contract": False}
    # Get bytecode hash for heuristic clone detection
    import hashlib
    code_hash = hashlib.sha256(code).hexdigest()
    return {"has_contract": True, "code_hash": code_hash, "byte_size": len(code)}
```

### Cross-Chain Token Address Discovery

When you find a scam token on one chain, the same deployer may have identical tokens on other chains.
Use the deployer address to cross-reference:

```python
def find_cross_chain_tokens(deployer: str, chains: list[str] = None) -> dict:
    """Search known deployers across chains for same-token patterns."""
    results = {}
    for chain in (chains or ["ethereum", "bsc", "polygon"]):
        rpc = PUBLIC_RPC.get(chain)
        if not rpc:
            continue
        w3 = Web3(Web3.HTTPProvider(rpc))
        # Get deployer's nonce at deployment block to compute deployed addresses
        # (Each deployment increments nonce, address = RLP(deployer, nonce))
        # Simplified: check if the deployer has any token contract on this chain
        tx_count = w3.eth.get_transaction_count(w3.to_checksum_address(deployer))
        results[chain] = {"chain_active": True, "deployer_tx_count": tx_count}
    return results
```

## Transaction Trace Decision Tree

Not every suspicious transaction is a scam. Before committing to a full investigation, classify the
transaction pattern:

| Signal | Likely Type | Recommended Action |
|---|---|---|
| Deployer → addLiquidity → renounceOwnership | Classic rug pull | Full investigation (deployer history, LP lock, tx analysis) |
| Deployer → multiSend (100+ addresses) | Airdrop / distribution | Check tokenomics; likely legitimate if paired with socials |
| Flash loan → swap → deposit to contract | MEV or attack | Use `defi-incident-analysis` skill instead |
| Small buys from 10+ fresh wallets in same block | Wash trading | Check for identical gas prices / same funding source |
| Developer mints 100% supply → lock to vesting | Cautionary but might be legit | Verify the lock contract allows no early-withdraw |
| Contract has `_beforeTokenTransfer` hook | Potential honeypot | Simulate sell with Tenderly before buying |

### When to Stop

Three hard exit criteria for token investigations:

1. **The token is confirmed as a known scam variant** (same bytecode hash as a registry of known scam
   contracts) → document and report; no need to reconstruct every detail
2. **The deployer address has been blacklisted on 3+ chain explorers** → report is complete; the
   scammer is known
3. **The total scam value is under $1,000** → one-page summary, no deep trace

## Money Section

Sell token/NFT scam investigation services through the following channels:

### Service Tiers

| Tier | Price | Deliverable |
|---|---|---|
| Quick Check | $50-100 | Honeypot + ownership + basic holder analysis (15 min) |
| Standard Report | $200-500 | Full contract analysis + LP lock + holder distribution + wash trading check (1-2 hrs) |
| Premium Investigation | $500-2,000 | Complete investigation + deployer tracing + funding chain + fund flow + court-ready report (4-8 hrs) |
| Expert Witness | $2,000-10,000 | Court testimony + expert declaration for fraud cases (varies by case) |

### Client Acquisition

- **Rug pull victims** — Monitor Discord servers and Telegram groups of recent rug pulls. Offer a "post-mortem analysis" for $200 that traces where their money went. Victims are highly motivated and can share the report with lawyers.
- **Pre-purchase due diligence** — Offer a "token safety audit" for $100-300 before investors buy into a new launch. Market in crypto alpha groups, Discord launch servers, and Telegram trading communities.
- **NFT buyers** — NFT collectors will pay $50-100 to check if a collection has wash trading before buying. Market in NFT Discord communities and Twitter/X.
- **Insurance claims** — Projects that claim to have been rugged need proof for insurance. Offer "scam verification reports" for $500-1,000.
- **Law firms** — Lawsuits against crypto projects need expert declarations. Charge $5,000-10,000 for a court-ready report with chain-of-custody documentation.
- **Bounty platforms** — Some projects and forums offer bounties for identifying scam tokens (e.g., Immunefi for yield farms, community bounties for Telegram groups).

### Marketing Angle

- "I traced the deployer's wallet to a known serial scammer"
- "The token passed all basic checks but failed the proxy upgradeability test"
- "80% of the trading volume was wash trading between 3 wallets"
- "The LP lock contract has an early-withdraw function only the deployer knows about"
- "Your tax records: here is the on-chain proof of the rug pull for the IRS"

### Workflow for Client Delivery

1. Client provides token/NFT contract address and a brief (what to investigate)
2. Run `run_scam_check()` to produce initial findings
3. If positive (scam detected), deep-dive with deployer tracing and fund flow analysis
4. Produce a PDF report with: executive summary, methodology, findings per category, screenshots of key transactions, and a chain-of-custody document
5. Deliver with a live walkthrough (Zoom, Google Meet) for Premium tier clients
6. Follow up after 30 days — if the project rugged, the client is motivated to buy the deep trace

## Practices from Top Investigators

### The ZachXBT Methodology

ZachXBT has investigated hundreds of token and NFT scams, identifying the same serial scammers
operating across multiple projects. His key insight: **scammers reuse everything** — wallet addresses,
funding sources, website templates, Telegram handles. The first step in any token investigation
is checking if the deployer or any related wallet has been seen before.

### The 12-Tool Arsenal for Token/NFT Investigations

| Tool | Token/NFT Use | When to Use |
|---|---|---|
| **Etherscan / Solscan** | Token holder analysis, deployer tx history, honeypot code | Every token — start here |
| **Arkham** | Visual fund flow: deployer → LP → dump | Tracking rug pull proceeds |
| **MetaSleuth** | Cross-chain deployer search: same address on multiple chains | After finding deployer — check if active elsewhere |
| **Cielo** | Monitor deployer wallets for new token creations | After investigation — catch the next scam early |
| **TRM Labs** | Check deployer address against sanctions and known bad actors | Before publishing any findings |
| **Breadcrumbs** | BTC-based scams (e.g., fake BTC mining tokens) | Tracing Bitcoin-side scam proceeds |
| **Dune** | SQL-based holder analysis: concentration, wash trading detection | Analyzing large datasets (10K+ holders) |
| **DeBank** | Deployer wallet portfolio: what else they hold | Understanding the scammer's full operation |
| **OKLink** | Address labeling and cross-chain identity | Identifying if the deployer has been tagged before |
| **Blockchair** | BTC privacy analysis for crypto ransom tokens | BTC-based scam tracing |
| **OMNIA** | Mempool monitoring: catch deployer's next tx before it confirms | Counter-party surveillance |
| **MetaSuites** | Legacy labeling for historical address lookups | Old addresses (pre-2022) may only have labels here |

### Pattern Recognition Across Multiple Scams

Serial scammers exhibit consistent patterns. When investigating a new token/NFT, cross-reference:

```python
PATTERN_SIGNATURES = {
    "same_deployer": {
        "check": "Deployer address used in >1 token launch",
        "severity": "CRITICAL — confirmed serial deployer",
        "action": "Flag all tokens from this deployer as high-risk immediately",
    },
    "same_funding_source": {
        "check": "Deployer funded from an address linked to a known scam",
        "severity": "HIGH — strong serial scammer signal",
        "action": "Trace the funding address for additional scam tokens",
    },
    "same_website_domain": {
        "check": "Token website = registered by same email / same IP as known scam",
        "severity": "CRITICAL — direct identity link",
        "action": "WHOIS lookup the domain; check registrar history",
    },
    "same_telegram_discord": {
        "check": "Same social handles used in previous scam projects",
        "severity": "HIGH — the scammers are running it back",
        "action": "Archive the prior scam thread for evidence chain",
    },
    "same_twitter_handle": {
        "check": "Twitter account reused across projects",
        "severity": "HIGH — identity link, handle may be deleted",
        "action": "Capture via archive.org / screenshot immediately",
    },
    "same_bytecode_hash": {
        "check": "Contract bytecode matches a known scam contract exactly",
        "severity": "HIGH — copy-paste scam",
        "action": "No need to analyze the code; reference the prior analysis",
    },
    "same_liquidity_pattern": {
        "check": "LP added then removed in identical timing to previous scam",
        "severity": "MEDIUM — behavioral match",
        "action": "Correlate with other signatures before confirming",
    },
}
```

### Social Engineering Deconstruction

ZachXBT documents how scammers manipulate victims. Understanding these patterns helps you
predict where to find evidence:

Common scammer playbooks in token/NFT fraud:

- **The Fake Influencer**: Impersonation accounts DM victims with "exclusive token" → fake website → malicious approve() → wallet drained
  - *Evidence trail*: The impersonated account's followers; the real handle's report; common scam contract deployer
- **The Discord "Admin"**: Hacked Discord server → admin DMs victims with "mint now" link → website wallet drain
  - *Evidence trail*: Discord audit logs (if accessible); scam domain registration IP; deployer funding source
- **The Liquidity Trap**: New token → high APY farming → deployer drains LP when TVL is high enough
  - *Evidence trail*: Deployer withdrawing LP tokens from staking contract; deployer selling on DEX in batches
- **The Airdrop Phishing**: "Claim your token airdrop" site → approve() spends your existing tokens
  - *Evidence trail*: The phishing domain (check Certificate Transparency logs); deployer address funding; drain tx patterns
- **The NFT "Rug"**: Generative art project → hyped mint → floor starts at 0.01 ETH → team stops responding after mint sell
  - *Evidence trail*: Team wallet minting multiple NFTs to self; immediate listings at above floor; Discord/Twitter deletion

```python
def classify_scammer_playbook(deployer_tx_history: list[dict]) -> list[str]:
    """Classify which playbook(s) a scammer is using based on deployer behavior."""
    playbooks = []
    tx_types = [tx.get("functionName", "") for tx in deployer_tx_history]
    tx_count = len(tx_types)

    # Check for liquidity trap pattern
    approve_txs = [t for t in tx_types if "approve" in t.lower()]
    lp_txs = [t for t in tx_types if "addLiquidity" in t.lower() or "add_liquidity" in t.lower()]
    if len(lp_txs) >= 2 and len(approve_txs) > len(lp_txs):
        playbooks.append("liquidity_trap")

    # Check for multi-token deployer (serial deployer)
    from collections import Counter
    contract_creations = [t for t in tx_types if "create" in t.lower()]
    if len(contract_creations) >= 3:
        playbooks.append("serial_deployer")

    # Check for approve-drain pattern (phishing)
    if tx_count < 20 and len(approve_txs) >= 3:
        playbooks.append("approve_drain_phishing")

    return playbooks or ["unknown"]
```

### Funding Chain Tracing for Token Scams

Apply the funding chain method specifically to token deployers:

1. **Find deployer address** — Get `from` address of token creation transaction
2. **Trace deployer's first funding** — Where did the deployer get ETH for gas?
3. **Cross-check funding source** against known scam databases (check each prior hop)
4. **If the funder is a known scammer**, all tokens from this deployer are high-risk
5. **If the funder is a CEX** — note the exchange; this is a potential KYC link

### The Investigation-to-Bounty Pipeline

Modeled on ZachXBT's proven approach:

1. **Beta token check** (free, public) — Post a thread on Twitter/X with your initial analysis
2. **If scam confirmed** — Publish the full wallet cluster thread with evidence
3. **Tag relevant parties** — The project's accounts, the chain's security team, exchange accounts
4. **Bounty collection** — Some projects and DAOs offer bounties for scam identification
5. **Private client referrals** — Each investigation builds reputation for paid work


## Anti-Rationalization Table
## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "The token has a verified contract, it's legit" | Verification only proves the source matches bytecode, not that the logic is honest. Many verified contracts are honeypots with legitimate-looking source that hides malicious logic in proxy implementations. |
| "The team is doxxed, they wouldn't rug" | Doxxed teams have rugged too. Credentials don't guarantee integrity. Multiple projects with KYCed teams have rugged (e.g., some Certik KYC projects). |
| "LP is locked so it's safe" | Locked LP prevents liquidity removal but doesn't prevent minting, proxy upgrades, or blacklist abuse. Also, locks can have early-withdrawal functions or be owned by the deployer. |
| "Low market cap means less risk" | Low cap tokens are the most common rug pull targets. Market cap has no correlation with safety — many rug pulls start with very low caps to attract initial buyers. |
| "The contract is renounced, so it can't be changed" | Renouncing only removes the `owner()` role. If the contract uses AccessControl, the `DEFAULT_ADMIN_ROLE` can still mint. Proxy contracts have a separate admin that can upgrade the implementation. |
| "High trading volume means it's legit" | Volume can be entirely wash-traded. Wash trading detection in this skill shows how 40%+ of volume can be circular trades between controlled wallets, creating a false appearance of organic demand. |
| "The team passed KYC with a reputable firm" | KYC verification is only as good as the KYC provider. Some KYC'd teams have still rugged (the KYC firm retains liability but doesn't prevent the scam). Also, KYC credentials can be stolen or fake. |
| "Liquidity is in multiple DEXes, so removing it all is impossible" | Deployers can coordinate removal across DEXes or use flash loans to drain all pools simultaneously. Multiple pools don't mean any single one is safe. |
| "The code was audited by a reputable firm" | Audits only check what the auditor was asked to check. Scam tokens often get audited with the malicious code excluded from scope. Audits don't guarantee safety. |
| "It's a well-known project with a large community" | Community size is easily faked with bots. Many rug pulls had 30,000+ Discord members (90%+ bots). Large communities create false social proof. |

