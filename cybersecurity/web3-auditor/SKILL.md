---
name: web3-auditor
description: Smart contract and DeFi security auditing for maximum bounty payouts. Use when auditing Solidity/Vyper contracts, testing DeFi protocols, hunting web3 vulnerabilities, or preparing Immunefi submissions.
---

# Web3 Auditor

Smart contract security auditing targeting the highest-paying bounties in the industry. Web3 critical bugs pay $100k-$10M. This skill covers the most common and highest-impact vulnerability classes.

## When to Use

- Auditing smart contracts for bug bounty programs
- Testing DeFi protocols for economic exploits
- Hunting on Immunefi, HackenProof, Code4rena
- Reviewing token contracts for rug pull indicators
- Analyzing upgrade mechanisms and proxy patterns

## The Process

1. **Scope the task** — define objectives, boundaries, and success criteria
2. **Gather information** — collect all necessary data and context before proceeding
3. **Execute the core workflow** — follow the domain-specific steps methodically
4. **Validate results** — verify outputs against expected outcomes or baselines
5. **Document findings** — record results, anomalies, and recommendations
### 1. Target Reconnaissance

Before diving into code:

1. **Contract discovery** — Etherscan, Blockscout, deployment tx
2. **Source verification** — Is source code verified? Compiler version?
3. **Proxy detection** — Is it a proxy? What's the implementation?
4. **Dependency mapping** — What does it import? OpenZeppelin version?
5. **TVL assessment** — How much value is locked? Higher TVL = higher bounty
6. **Admin controls** — What can the owner/admin do? Multisig?

### 2. Vulnerability Classes (Ranked by Payout)

#### Critical ($100k-$10M)

**Reentrancy**
```solidity
// VULNERABLE: state update after external call
function withdraw() external {
    uint balance = balances[msg.sender];
    (bool success, ) = msg.sender.call{value: balance}("");
    require(success);
    balances[msg.sender] = 0; // TOO LATE
}

// FIX: checks-effects-interactions
function withdraw() external {
    uint balance = balances[msg.sender];
    balances[msg.sender] = 0; // State first
    (bool success, ) = msg.sender.call{value: balance}("");
    require(success);
}
```

**Flash Loan Attacks**
- Price oracle manipulation via flash loans
- Governance token flash loan → vote → drain treasury
- LP manipulation → skewed price → arbitrage

**Access Control**
```solidity
// VULNERABLE: missing access control
function setOwner(address newOwner) external {
    owner = newOwner; // Anyone can call!
}

// VULNERABLE: wrong visibility
function _authorizeUpgrade(address impl) internal {
    // Should be internal but is public
}
```

**Integer Overflow/Underflow**
```solidity
// Pre-0.8.0: silent overflow
uint8 x = 255;
x += 1; // Becomes 0, no revert

// Post-0.8.0: reverts by default
// But unchecked blocks still vulnerable
unchecked {
    uint8 x = 255;
    x += 1; // Becomes 0
}
```

#### High ($10k-$100k)

**Oracle Manipulation**
```solidity
// VULNERABLE: spot price from single DEX
function getPrice() returns (uint) {
    return token.balanceOf(address(pair)) * 1e18 / 
           otherToken.balanceOf(address(pair));
}
// Flash loan drains one side → price manipulation

// FIX: Use TWAP oracle (Chainlink, Uniswap TWAP)
```

**Accounting Desync**
- Deposit/withdrawal rounding errors
- Share price manipulation
- Fee calculation errors
- Precision loss in division

**Signature Replay**
```solidity
// VULNERABLE: no nonce, no chain ID check
function execute(address to, uint value, bytes memory data, bytes memory sig) {
    bytes32 hash = keccak256(abi.encodePacked(to, value, data));
    address signer = ECDSA.recover(hash, sig);
    require(signer == owner);
    // Same signature can be reused!
}

// FIX: Include nonce and chain ID
bytes32 hash = keccak256(abi.encodePacked(to, value, data, nonce, block.chainid));
```

**Proxy/Upgrade Vulnerabilities**
- Storage collision between proxy and implementation
- Uninitialized implementation (can be taken over)
- Malicious upgrade (if admin key compromised)
- Missing `disableInitializers()` in implementation

#### Medium ($1k-$10k)

**Denial of Service**
```solidity
// VULNERABLE: iterating over all users
function distributeRewards() external {
    for (uint i = 0; i < users.length; i++) {
        // If array grows too large, gas limit blocks execution
        users[i].transfer(reward);
    }
}

// VULNERABLE: griefing with small deposits
function claimReward() external {
    require(rewards[msg.sender] > 0);
    // Attacker deposits dust → rewards calculation fails
}
```

**Front-Running / MEV**
- Transaction ordering dependence
- Sandwich attacks on DEX trades
- Miner extractable value exploitation

**Centralization Risks**
- Owner can pause/freeze all funds
- Owner can change critical parameters
- No timelock on admin actions
- Single point of failure in multisig

### 3. Audit Methodology

#### Phase 1: Automated Analysis

```bash
# Static analysis
slither . --print human-summary
mythril analyze contract.sol --execution-timeout 90

# Check for known patterns
slither . --detect reentrancy-eth,reentrancy-no-eth
slither . --detect unchecked-transfer
slither . --detect arbitrary-send-eth

# Fuzzing
echidna-test . --contract TestContract --config echidna.yaml
```

#### Phase 2: Manual Review

Focus on:
1. **External calls** — Every `.call`, `.transfer`, `.send` is a potential reentrancy
2. **State changes** — Are they before or after external calls?
3. **Access control** — Who can call what? Are modifiers correct?
4. **Math** — Division before multiplication? Rounding? Precision?
5. **Upgrades** — Storage layout compatible? Initializers protected?
6. **Economic invariants** — Can flash loans break assumptions?

#### Phase 3: Economic Analysis

For DeFi protocols:
1. **Invariant testing** — What must always be true? Can it be broken?
2. **Edge cases** — What happens at zero? At max uint? With empty pools?
3. **Game theory** — What's the rational actor behavior? Can it be exploited?
4. **Composability** — How does it interact with other protocols?

### 4. Web3-Specific Red Flags

- `tx.origin` for authentication (phishing attack vector)
- Floating pragma (`pragma solidity ^0.8.0` instead of specific version)
- `selfdestruct` callable by anyone
- Unchecked return values from `.call()`
- Block timestamp dependence (miners can manipulate ±15s)
- Assembly blocks without comments
- Missing events for state changes
- No reentrancy guard on external calls with state changes

### 5. Report Format (Immunefi)

```
## Title
[Severity] Brief description of vulnerability

## Target
Contract: 0x...
Chain: Ethereum/Arbitrum/Polygon
TVL: $X

## Vulnerability Type
Reentrancy / Access Control / Oracle Manipulation / etc.

## Impact
- Funds at risk: $X
- Attack complexity: Low/Medium/High
- Prerequisites: Flash loan capital, specific conditions

## Proof of Concept
[Working Foundry/Hardhat test]

## Recommended Fix
[Specific code change]
```

## Revenue Potential

| Skill Level | Focus | Monthly Range |
|------------|-------|---------------|
| Beginner | Reentrancy, access control | $0-$5000 |
| Intermediate | Oracle manipulation, flash loans | $5000-$50000 |
| Advanced | Economic exploits, novel attack chains | $50000-$500000 |
| Elite | 0-day discovery, protocol-level bugs | $500000+ |

## Verification

- All findings have working Foundry/Hardhat test cases
- Economic impact is quantified (not just "could lose funds")
- No false positives from automated tools
- Reports follow Immunefi format
- Findings include specific code fixes

## Tools

| Purpose | Tools |
|---------|-------|
| Static analysis | Slither, Mythril |
| Fuzzing | Echidna, Foundry fuzz |
| Testing | Foundry (forge), Hardhat |
| Block explorer | Etherscan, Blockscout |
| DeFi data | DeFiLlama, Dune Analytics |
| MEV analysis | Flashbots Protect, MEV Blocker |

## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Treating compliance checklists as security guarantees rather than minimum baselines
- Failing to document exceptions and risk acceptance decisions
- Relying on point-in-time audits instead of continuous monitoring

## References

- Immunefi Bug Bounty Standard
- SWC Registry (Smart Contract Weakness Classification)
- Damn Vulnerable DeFi (practice)
- Ethernaut (practice)
- Trail of Bits: Not All Bugs Are Created Equal
