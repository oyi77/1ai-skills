---
name: smart-contract-dev
description: 'Skill: smart-contract-dev. See SKILL.md body for details. Use when this domain is relevant.'
domain: trading
tags:
- algorithms
- contract
- dev
- markets
- smart
- trading
version: 1.0.0
---

## Overview

Smart contract development for EVM-compatible chains (Ethereum, Polygon, Arbitrum, Optimism, Base) using Solidity 0.8.x. Covers the full lifecycle: architecting, implementing, testing, deploying, and upgrading production-grade contracts. Hardhat and Foundry are the primary toolchains.

The EVM is a single-threaded 256-bit state machine. Storage is persistent; every write costs gas proportional to the number of storage slots touched. Understanding gas economics, proxy storage layouts, and the Solidity compiler's optimization passes separates production contracts from playground code.

## When to Use

**Trigger phrases:**
- "smart contract dev"
- "DeFi protocols (DEX, lending, staking)"
- "NFT collections and marketplaces"
- "DAOs and governance"

**Applicable scenarios:**
- Token contract design and deployment (ERC-20, ERC-721, ERC-1155, ERC-4626)
- DEX AMMs, lending pools, staking protocols, and yield aggregators
- NFT collections with mint, reveal, royalty mechanics
- Upgradeable proxy architecture (UUPS, Transparent, Beacon, Diamond)
- On-chain governance systems (token voting, timelocks, multisig)
- Cross-chain bridge and messaging patterns
- Security audits and vulnerability remediation

## When NOT to Use

- Task is about portfolio management, not trading (use portfolio skills)
- Task is about financial analysis (use analysis skills)
- You need to analyze trade results (use analytics skills)
- Task is about risk management (use risk skills)
- You don't have trading capital
- Task requires financial advice (consult advisors)
- Pure off-chain infrastructure (use backend skills)
- Financial modeling or strategy design (use relevant domain skills)

## Development Toolchains

### Foundry (forge, cast, anvil)

Foundry is the dominant toolchain for Solidity-first development. It compiles with solc directly, runs tests in the Solidity VM (no JavaScript middleware), and provides cheatcodes for EVM manipulation.

```solidity
// Foundry test — forge test -vvvv
contract CounterTest is Test {
    Counter public counter;

    function setUp() public {
        counter = new Counter();
        counter.setNumber(0);
    }

    function testIncrement() public {
        counter.increment();
        assertEq(counter.number(), 1);
    }

    function testFuzzIncrement(uint256 x) public {
        vm.assume(x > 0 && x < type(uint128).max);
        counter.increment(x);
        assertEq(counter.number(), x);
    }

    function testFail_CallByEOA() public {
        // Only contract callers allowed — vm.prank sets msg.sender
        vm.prank(address(0));
        counter.restrictedFn();
    }
}
```

Key Foundry cheatcodes:

```solidity
vm.prank(address)          // set msg.sender for next call
vm.startPrank(address)     // persist msg.sender across calls
vm.deal(address, uint)     // set ether balance
vm.roll(uint256)           // set block number
vm.warp(uint256)           // set block timestamp
vm.store(address,bytes32,bytes32) // write arbitrary storage
vm.load(address,bytes32)   // read arbitrary storage
vm.expectRevert(bytes)     // assert next call reverts
vm.assume(bool)            // filter fuzz inputs
vm.createSelectFork(url)   // fork from a live chain
vm.broadcast()             // sign and send as current msg.sender
vm.sign(uint256,bytes32)   // raw ECDSA signing
```

```bash
# Foundry CLI workflow
forge build                  # compile
forge test -vvvv             # run tests with traces
forge test --match-test testFuzz -vvv  # filter by name
forge coverage --report lcov # line+branch coverage
forge snapshot               # gas report
cast send $TOKEN "transfer(address,uint256)" $TO $AMT --rpc-url $RPC --private-key $PK
cast call $TOKEN "balanceOf(address)" $USER --rpc-url $RPC
cast sig "transfer(address,uint256)"  # compute 4-byte selector
anvil                        # local dev node (port 8545)
```

### Hardhat

Hardhat is the JavaScript-centric framework. It provides the `hardhat-network` forked-node EVM, plugins for Ethers.js, and the `console.sol` debugging library. Preferred when the team is JS-heavy or when complex deployment scripting is needed.

```javascript
// hardhat.config.js
require("@nomicfoundation/hardhat-toolbox");
require("@openzeppelin/hardhat-upgrades");

module.exports = {
  solidity: {
    version: "0.8.24",
    settings: { optimizer: { enabled: true, runs: 200 } },
  },
  networks: {
    sepolia: { url: process.env.RPC_URL, accounts: [process.env.PK] },
  },
  etherscan: { apiKey: process.env.ETHERSCAN_KEY },
};
```

```javascript
// Hardhat test — npx hardhat test
const { expect } = require("chai");
const { ethers, upgrades } = require("hardhat");

describe("Token", function () {
  it("deploys and mints", async () => {
    const [owner] = await ethers.getSigners();
    const Token = await ethers.getContractFactory("MyToken");
    const token = await Token.deploy("My", "MTK", owner.address);
    await token.waitForDeployment();

    expect(await token.balanceOf(owner.address)).to.equal(ethers.parseEther("1000000"));
  });

  it("reverts on insufficient balance", async () => {
    const [owner, user] = await ethers.getSigners();
    const token = await ethers.deployContract("MyToken", ["My", "MTK", owner.address]);
    const errorName = "ERC20Insufficient" + "Balance";

    await expect(
      token.connect(user).transfer(owner.address, 1)
    ).to.be.revertedWithCustomError(token, errorName);
  });
});
### When to Use Which

|Consideration|Foundry|Hardhat|
|---|---|---|
|Test speed|~10x faster (native Solidity)|Slower (JS EVM)|
|Fuzz + invariant|Native forge fuzz|Via plugin|
|Fork testing|`vm.createSelectFork()`|`network.forking` config|
|Deployment scripts|Solidity scripts + broadcast|ethers.js + upgrades plugin|
|Debugging|`forge test -vvvv` traces|console.sol + stack traces|
|Team language|Solidity-first|JS/TS-first|
|Ecosystem plugins|Minimal|Rich (hardhat-upgrades, tenderly, solidity-coverage)|

**Recommendation:** Use Foundry as primary for testing and development. Use Hardhat for upgradeable deployments (hardhat-upgrades plugin) and complex multi-step deployment orchestration. Many teams use both in the same repo.

## Solidity Deep Dive

### Data Locations

```solidity
// storage — persists on-chain, costs gas on read/write
// memory — temporary, scoped to function execution
// calldata — read-only function input, cheapest for external calls

contract DataLocations {
    struct User {
        address addr;
        uint256 balance;
        uint32 lastActive;  // packed
    }

    User[] public users;

    // storage ref — points into state, modifications persist
    function _loadUser(uint256 id) internal view returns (User storage u) {
        u = users[id];
    }

    // memory copy — snapshot, gas-intensive for large structs
    function getUser(uint256 id) external view returns (User memory) {
        return users[id];
    }

    // calldata — zero-copy, external functions only
    function batchProcess(User calldata u) external pure returns (uint256) {
        // u is read-only, no copy cost
        return u.balance;
    }
}
```

### Struct Packing

EVM storage slots are 32 bytes. Solidity packs adjacent elementary types smaller than 256 bits into one slot when they fit. Declaration order matters — pack tightly or waste gas.

```solidity
// BAD — 4 slots, 3 wasted bytes each slot
struct Loose {
    uint256 id;       // slot 0
    uint128 amount;   // slot 1 (16 bytes, 16 wasted)
    uint64  count;    // slot 2 (8 bytes, 24 wasted)
    uint32  version;  // slot 3 (4 bytes, 28 wasted)
}

// GOOD — 2 slots, everything packed
struct Tight {
    uint64  count;    // \_ packed into slot 0
    uint128 amount;   // /
    uint32  version;  // -- slot 0 tail
    uint256 id;       // slot 1
}
```

Rules: references (address, bytes32, uint256) start new slots. Smaller types after them waste space. Sort descending by size, or group same-sized types.

### Custom Errors

Solidity 0.8.4+ supports `error` types. They are cheaper than revert strings (no ABI-encoded string) and carry parameters.

```solidity
error Unauthorized(address caller);
error InsufficientBalance(uint256 available, uint256 required);
error ZeroAddress();

contract ErrorDemo {
    function withdraw(uint256 amount) external {
        if (amount > balances[msg.sender]) {
            revert InsufficientBalance(balances[msg.sender], amount);
        }

        // Foundry test asserts:
        // vm.expectRevert(abi.encodeWithSelector(InsufficientBalance.selector, 0, 100));
    }
}
```

```javascript
// Hardhat/ethers.js
await expect(contract.withdraw(100)).to.be.revertedWithCustomError(
  contract,
  "InsufficientBalance"
);
```

### Events and Topics

Events are indexed (up to 3 indexed parameters) and their topics enable efficient off-chain filtering. The first topic is always the event signature hash.

```solidity
event Transfer(address indexed from, address indexed to, uint256 value);
event Staked(address indexed user, uint256 amount, uint256 unlockTime);

// Emit as struct for cleaner code
event OrderCreated(Order order);
```

```javascript
// Off-chain — ethers.js
contract.on("Staked", (user, amount, unlockTime, event) => {
  console.log(`${user} staked ${amount} until ${unlockTime}`);
});

// Filter by indexed param
const filter = contract.filters.Staked(address);  // null = any
contract.queryFilter(filter, 0, "latest");
```

## Testing

### Unit Tests

```solidity
// Foundry
function testDeposit() public {
    vm.prank(alice);
    vault.deposit{value: 1 ether}();
    assertEq(vault.balanceOf(alice), 1 ether);
    assertEq(address(vault).balance, 1 ether);
}

function testRevert_ZeroDeposit() public {
    vm.prank(alice);
    vm.expectRevert(Vault__ZeroDeposit.selector);
    vault.deposit{value: 0}();
}
```

### Fork Tests

```solidity
// Test against mainnet state without deploying everything
function testFork_UniswapSwap() public {
    string memory rpc = vm.envString("MAINNET_RPC_URL");
    vm.createSelectFork(rpc, 19_500_000);  // block number

    // Use real Uniswap V3 pool
    IUniswapV3Pool pool = IUniswapV3Pool(0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640);
    assertGt(pool.liquidity(), 0);
}
```

### Fuzz Tests

```solidity
// forge test — runs 256 random inputs by default (configurable)
function testFuzz_MintTotalSupply(uint256 amount) public {
    vm.assume(amount > 0 && amount <= MAX_SUPPLY);
    token.mint(address(1), amount);
    assertEq(token.totalSupply(), amount);
}

// With handler — forge test with --fuzz-runs 10000
}
```

Foundry fuzzer config in `foundry.toml`:

```toml
[fuzz]
runs = 10000
max_test_rejects = 65536
dictionary_weight = 40
```

### Invariant Tests

Invariant tests run random sequences of function calls and verify properties never break. Requires a handler contract.

```solidity
// Invariant A: totalSupply = sum of all balances
contract VaultInvariants is Test {
    VaultHarness harness;

    function setUp() public {
        harness = new VaultHarness();
        targetContract(address(harness));
    }

    function invariant_totalSupply_eq_sumBalances() public {
        uint256 totalBal;
        for (uint256 i; i < harness.users(); i++) {
            totalBal += harness.balanceOf(harness.userAt(i));
        }
        assertEq(harness.totalSupply(), totalBal);
    }

    function invariant_noNegativeBalance() public {
        // forge invariant runs hundreds of random call sequences
        assertGe(harness.minBalance(), 0);
    }
}
```

Run: `forge test --inv-runs 1000 --fail-on-revert`

### Differential Testing

Compare Solidity output against a reference implementation (e.g., a Python model):

```solidity
function testFuzz_AMM_math(uint256 x, uint256 y) public {
    vm.assume(x > 1e6 && y > 1e6 && x < 1e30 && y < 1e30);
    uint256 k = x * y;
    uint256 dy = amm.getOutput(x, y, x / 10);

    // Compare: python model gives the same result?
    // Off-chain: run forge snapshot, diff with python script
    assertTrue(dy > 0);
    assertLt(dy, y);  // invariant: can't drain pool
}
```

## Upgradeable Patterns

### UUPS (Universal Upgradeable Proxy Standard)

Storage lives in the proxy; logic contract holds implementation. Upgrades call `upgradeTo()` on the proxy through the implementation's `_authorizeUpgrade`.

```solidity
// Proxy (deployed once): delegates all calls to implementation via delegatecall
// Implementation (upgraded): must inherit UUPSUpgradeable

contract VaultV1 is UUPSUpgradeable, OwnableUpgradeable {
    uint256 public value;

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();  // prevent implementation self-destruct
    }

    function initialize(uint256 _value) external initializer {
        __Ownable_init(msg.sender);
        __UUPSUpgradeable_init();
        value = _value;
    }

    function _authorizeUpgrade(address newImpl) internal override onlyOwner {}
}

contract VaultV2 is VaultV1 {
    function increment() external {
        value++;
    }
}
```

Upgrade script:

```javascript
// hardhat-upgrades
const { upgrades } = require("hardhat");

const v1 = await upgrades.deployProxy(
  await ethers.getContractFactory("VaultV1"),
  [100], { kind: "uups" }
);
await v1.waitForDeployment();

const v2 = await upgrades.upgradeProxy(
  await v1.getAddress(),
  await ethers.getContractFactory("VaultV2")
);
```

### Transparent Proxy

Proxy admin is a separate address (only admin can upgrade). Users call through the same proxy but never hit upgrade functions. More expensive per call (SLOAD for admin check) but simpler.

```solidity
// OpenZeppelin TransparentUpgradeableProxy
// Admin address gets admin functions; everyone else gets implementation

// Deployment hardhat-upgrades: { kind: "transparent" }
```

### Beacon Proxy

Multiple proxies point to a single beacon contract that stores the implementation address. Update once — all proxies upgrade.

```solidity
// Deploy beacon, then deploy proxies from beacon
// forge script
function run() external {
    vm.startBroadcast(deployerPK);
    UpgradeableBeacon beacon = new UpgradeableBeacon(address(v1), deployer);
    BeaconProxy proxyA = new BeaconProxy(address(beacon), initData);
    BeaconProxy proxyB = new BeaconProxy(address(beacon), initData);
    // Upgrade both proxies atomically:
    beacon.upgradeTo(address(v2));
    vm.stopBroadcast();
}
```

### Diamond Proxy (EIP-2535)

Multi-facet upgradeable proxy where each function is routed to a facet contract. Enables upgrading individual functions instead of whole contracts. Storage is managed via diamond-2 storage pattern (typed mapping-based storage).

```solidity
// Facet: implements a slice of the total API
contract DiamondLoupeFacet {
    // diamond storage — avoids storage collision
    bytes32 constant DIAMOND_STORAGE_POSITION = keccak256("diamond.standard.diamond.storage");

    struct DiamondStorage {
        mapping(bytes4 => FacetAddressAndSelectorPosition) selectorToFacet;
    }

    function ds() internal pure returns (DiamondStorage storage s) {
        bytes32 pos = DIAMOND_STORAGE_POSITION;
        assembly { s.slot := pos }
    }
}
```

**Use UUPS for most projects.** It's the cheapest per-call. Use Transparent only when the proxy admin role must be separated from the owner. Use Beacon for many identical copies (clone-like with upgradeability). Use Diamond only when the contract exceeds the 24KB contract size limit.

### Storage Gap Convention

Reserve unused storage slots in upgradeable base contracts so future versions can add state without corrupting existing storage:

```solidity
contract BaseV1 {
    uint256 public value;
    uint256[49] __gap;  // reserve 49 slots
}

contract V2 is BaseV1 {
    uint256 public newValue; // uses slot 1 (the first gap slot)
    uint256[48] __gap;
}
```

## Access Control

### Ownable2Step

Replaces deprecated `Ownable` — the new owner must accept, preventing accidental transfers to an uncontrolled address.

```solidity
import "@openzeppelin/contracts/access/Ownable2Step.sol";

contract MyContract is Ownable2Step {
    constructor(address owner) Ownable2Step(owner) {}

    function adminMint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }
}
```

### AccessControl (RBAC)

```solidity
import "@openzeppelin/contracts/access/AccessControl.sol";

contract DAOContract is AccessControl {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");

    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
    }

    function mint(address to, uint256 amount) external onlyRole(MINTER_ROLE) {
        _mint(to, amount);
    }
}
```

Foundry test for roles:

```solidity
function test_RevertIf_NotMinter() public {
    vm.prank(alice);  // alice has no MINTER_ROLE
    vm.expectRevert(abi.encodeWithSelector(AccessControlUnauthorizedAccount.selector, alice, MINTER_ROLE));
    dao.mint(bob, 100);
}
```

### Timelock Controller

```solidity
// OpenZeppelin TimelockController — queued, delayed execution
// Deploy with admin, proposers, executors
TimelockController timelock = new TimelockController(
    MIN_DELAY,     // 2 days
    proposers,     // multisig address
    executors,     // multisig address
    admin          // deployer (revoked after setup)
);
```

Pattern: make the timelock the `onlyOwner` of the protocol contract. Proposals go through: propose → wait for delay → execute. This gives users time to exit if a malicious upgrade is proposed.

### Multisig (Gnosis Safe)

For production admin operations, use a Gnosis Safe (now Safe) with N-of-M signing. Typical: 2-of-3 or 3-of-5. The Safe address owns protocol admin roles.

Deployment via Safe{Wallet} app at https://app.safe.global. Programmatic interaction via `@safe-global/safe-core-sdk`.

## Gas Optimization

### SSTORE Rules

Writing to storage is the most expensive EVM operation. Key costs:

|Operation|Cost (London)|Notes|
|---|---|---|
|SSTORE zero → non-zero|20,000 gas|First write to slot|
|SSTORE non-zero → non-zero|5,000 gas|Overwrite existing value|
|SSTORE non-zero → zero|2,900 gas + 15,000 refund|But refund capped at 50% of gas used|
|SLOAD (warm)|100 gas|Already accessed this tx|
|SLOAD (cold)|2,100 gas|First access this tx|

```solidity
// Batch storage writes to save gas
function batchMint(address[] calldata to, uint256[] calldata amounts) external {
    for (uint256 i; i < to.length; i++) {
        _mint(to[i], amounts[i]);  // each _mint does multiple SSTOREs
    }
}
```

### Calldata vs Memory

```solidity
// BAD — copies array to memory (extra 3 gas per element + expansion)
function process(uint256[] memory data) external { }

// GOOD — reads directly from calldata (zero copy)
function process(uint256[] calldata data) external {
    for (uint256 i; i < data.length; i++) {
        // data[i] reads from calldata directly
    }
}
```

### Unchecked Blocks

Solidity 0.8+ has built-in overflow checks that revert on overflow. When overflow is mathematically impossible (bounded by previous checks), wrap in `unchecked`:

```solidity
// BAD — overflow check every iteration
for (uint256 i = 0; i < n; i++) { ... }

// GOOD — unchecked when i < n is guaranteed to not overflow
for (uint256 i = 0; i < n; ) {
    ...
    unchecked { i++; }
}
```

### ERC-20 Gas Efficient Patterns

```solidity
// Use ERC20Burnable instead of separate burn()
// Use ERC20FlashMint for flash loans (built-in)

// Pack balances in mapping(uint256 => uint256) for multi-account ops
// where lower 128 bits = balance, upper 128 bits = allowance
```

## Assembly (Yul)

### delegatecall

```solidity
address target = logicContract;
(bool success, bytes memory data) = target.delegatecall(
    abi.encodeWithSignature("execute(bytes)", payload)
);
require(success, "DelegateCallFailed");
```

### Error Handling

```solidity
// Encode custom error in Yul
assembly {
    // revert with selector + params
    mstore(0x00, 0xb8e2f161)  // Unauthorized.selector
    mstore(0x04, caller())
    revert(0x00, 0x24)
}

// Safe encoded revert
assembly {
    let ptr := mload(0x40)
    mstore(ptr, 0x08c379a0)  // Error(string) selector
    mstore(add(ptr, 0x20), 0x20)
    mstore(add(ptr, 0x40), 26)
    mstore(add(ptr, 0x60), "Insufficient balance!!!")
    revert(ptr, 0x80)
}
```

### Precompile Calls

```solidity
// ecrecover — address 0x01
function recoverSigner(bytes32 hash, uint8 v, bytes32 r, bytes32 s) internal pure returns (address) {
    address signer;
    assembly {
        let ptr := mload(0x40)
        mstore(ptr, hash)
        mstore(add(ptr, 0x20), v)
        mstore(add(ptr, 0x40), r)
        mstore(add(ptr, 0x60), s)
        let success := staticcall(gas(), 0x01, ptr, 0x80, ptr, 0x20)
        if success { signer := mload(ptr) }
    }
    return signer;
}

// sha256 — address 0x02
function hashSha256(bytes memory data) internal view returns (bytes32) {
    bytes32 result;
    assembly {
        let ptr := mload(0x40)
        let len := mload(data)
        let dataPtr := add(data, 0x20)
        let success := staticcall(gas(), 0x02, dataPtr, len, ptr, 0x20)
        if success { result := mload(ptr) }
    }
    return result;
}

// modexp — address 0x05 (EIP-198)
```

## Security

### Reentrancy

```solidity
// WRONG — external call before state update
function withdraw(uint256 amount) external {
    require(balances[msg.sender] >= amount);
    (bool ok, ) = msg.sender.call{value: amount}("");
    require(ok);
    balances[msg.sender] -= amount;  // reentrancy: attacker calls withdraw again
}

// CORRECT — Checks-Effects-Interactions
function withdraw(uint256 amount) external nonReentrant {
    require(balances[msg.sender] >= amount, "insufficient");
    balances[msg.sender] -= amount;              // effects first
    (bool ok, ) = msg.sender.call{value: amount}(""); // then interaction
    require(ok);
}

// ReentrancyGuard (OpenZeppelin)
// Use _reentrancyGuardEntered() check in modifiers
```

### Checks-Effects-Interactions (CEI)

Always: validate (checks) → update state (effects) → call external (interactions). This prevents reentrancy by construction.

```solidity
function claimReward() external {
    // Check
    require(block.timestamp >= rewards[msg.sender].unlockTime);
    // Effect
    uint256 amount = rewards[msg.sender].amount;
    rewards[msg.sender].amount = 0;
    // Interaction
    (bool ok, ) = msg.sender.call{value: amount}("");
    require(ok);
}
```

### Pull Over Push

Never push Ether/ tokens to users in a loop — one recipient reverts and the whole tx fails. Instead, let users withdraw their share:

```solidity
// BAD — push
function distribute() external {
    for (uint256 i; i < users.length; i++) {
        (bool ok, ) = users[i].call{value: amounts[i]}("");  // one revert = all fail
        require(ok);
    }
}

// GOOD — pull
mapping(address => uint256) public pendingWithdrawals;

function withdraw() external {
    uint256 amount = pendingWithdrawals[msg.sender];
    pendingWithdrawals[msg.sender] = 0;
    (bool ok, ) = msg.sender.call{value: amount}("");
    require(ok);
}
```

### Oracle Manipulation

```solidity
// WRONG — single-slot price
uint256 price = pool.sqrtPriceX96();  // flash loan can manipulate

// BETTER — TWAP (time-weighted average price)
// Uniswap V3 Oracle:
uint32[] memory secondsAgos = new uint32[](2);
secondsAgos[0] = 1800;  // 30 min ago
secondsAgos[1] = 0;
(int56[] memory tickCumulatives, ) = pool.observe(secondsAgos);
uint160 twapPrice = TickMath.getSqrtRatioAtTick(
    int24((tickCumulatives[1] - tickCumulatives[0]) / 1800)
);

// BEST — Chainlink price feed for critical prices
// (AggregatorV3Interface with freshness check)
function getPrice() external view returns (uint256) {
    (, int256 answer, , uint256 updatedAt, ) = feed.latestRoundData();
    require(block.timestamp - updatedAt < 1 hours, "stale price");
    require(answer > 0, "invalid price");
    return uint256(answer);
}
```

### MEV Protection

```solidity
// Slippage protection
function swap(uint256 amountIn, uint256 minAmountOut) external {
    uint256 amountOut = getAmountOut(amountIn);
    require(amountOut >= minAmountOut, "slippage");
}

// Deadline
function swap(uint256 amountIn, uint256 amountOutMin, uint256 deadline) external {
    require(block.timestamp <= deadline, "expired");
}

// Commit-reveal (for preventing frontrunning)
// submit hash, then reveal
```

## DeFi Patterns

### AMM Exact Math (Uniswap V2-style)

```solidity
// Constant product: x * y = k
function getAmountOut(uint256 amountIn, uint256 reserveIn, uint256 reserveOut)
    internal pure returns (uint256)
{
    require(amountIn > 0, "zero in");
    require(reserveIn > 0 && reserveOut > 0, "zero reserve");
    uint256 amountInWithFee = amountIn * 997;  // 0.3% fee
    uint256 numerator = amountInWithFee * reserveOut;
    uint256 denominator = reserveIn * 1000 + amountInWithFee;
    return numerator / denominator;
}
```

### Lending Pool Accounting

```solidity
// Interest rate model: utilization-based
contract LendingPool {
    uint256 public totalDeposits;
    uint256 public totalBorrows;

    uint256 public constant BASE_RATE = 0.05 ether;  // 5% base
    uint256 public constant SLOPE_1 = 0.10 ether;    // up to optimal
    uint256 public constant SLOPE_2 = 1.0 ether;     // above optimal
    uint256 public constant OPTIMAL_UTIL = 0.80 ether;

    mapping(address => uint256) public depositIndex;  // scaled balance

    function getBorrowRate() public view returns (uint256) {
        if (totalDeposits == 0) return 0;
        uint256 util = totalBorrows * 1e18 / totalDeposits;
        if (util <= OPTIMAL_UTIL) {
            return BASE_RATE + (util * SLOPE_1 / OPTIMAL_UTIL);
        } else {
            uint256 excess = util - OPTIMAL_UTIL;
            return BASE_RATE + SLOPE_1 + (excess * SLOPE_2 / (1e18 - OPTIMAL_UTIL));
        }
    }
}
```

### Compounding Strategy

```solidity
// Yearn-style: vault deposits earn yield, shares appreciate
contract Vault {
    IERC20 public asset;
    uint256 public totalAssets;

    function deposit(uint256 amount) external returns (uint256 shares) {
        shares = convertToShares(amount);
        _mint(msg.sender, shares);
        totalAssets += amount;
        asset.transferFrom(msg.sender, address(this), amount);
    }

    function convertToShares(uint256 assets) public view returns (uint256) {
        uint256 supply = totalSupply();
        return supply == 0 ? assets : assets * supply / totalAssets;
    }

    function convertToAssets(uint256 shares) public view returns (uint256) {
        uint256 supply = totalSupply();
        return supply == 0 ? shares : shares * totalAssets / supply;
    }
}
```

## Token Standards

### ERC-20 with Permit (EIP-2612)

Gasless approvals via off-chain signature:

```solidity
// Inherent in OpenZeppelin's ERC20Permit
contract MyToken is ERC20, ERC20Permit {
    constructor() ERC20("My", "MTK") ERC20Permit("My") {}

    // permit() allows approvals via signed message (no tx from user)
    // delegate the approve tx cost to a relayer
}
```

```javascript
// Off-chain permit signing
const { signature } = await signPermit(
  token, owner, spender, amount,
  await token.nonces(owner.address), deadline, owner
);
await token.permit(owner.address, spender, amount, deadline, v, r, s);
```

### ERC-721 with Enumerable

```solidity
// OpenZeppelin ERC721Enumerable adds tokenOfOwnerByIndex, totalSupply
contract MyNFT is ERC721Enumerable, Ownable {
    using Strings for uint256;

    string public baseURI;

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        require(_ownerOf(tokenId) != address(0), "nonexistent");
        return string.concat(baseURI, tokenId.toString());
    }

    function safeMint(address to) external onlyOwner {
        uint256 tokenId = totalSupply() + 1;
        _safeMint(to, tokenId);
    }
}
```

### ERC-1155 (Multi-Token)

```solidity
contract My1155 is ERC1155 {
    function mintBatch(address to, uint256[] memory ids, uint256[] memory amounts) external {
        _mintBatch(to, ids, amounts, "");
    }
}
```

### ERC-4626 (Tokenized Vaults)

Standardized yield-bearing vault interface. Compatible with ERC-20.

```solidity
contract YieldVault is ERC4626, Ownable {
    constructor(IERC20 _asset)
        ERC4626(_asset)
        ERC20("Yield Vault", "yVLT")
    {}

    function totalAssets() public view override returns (uint256) {
        return asset.balanceOf(address(this));
    }

    // Override _deposit to deploy capital into strategies
    function _deposit(address caller, address receiver, uint256 assets, uint256 shares)
        internal override
    {
        super._deposit(caller, receiver, assets, shares);
        _deployToStrategy(assets);
    }
}
```

## Important EIPs

|EIP|Purpose|Key Detail|
|---|---|---|
|EIP-1967|Proxy storage slots|Standardized storage slot for proxy admin (`0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103`), implementation slot (`0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc`), beacon slot|
|EIP-712|Typed structured data signing|Domain separator + struct hash for human-readable signatures. Used by EIP-2612 permits, meta-transactions|
|EIP-2612|ERC-20 Permit|Gasless approvals via EIP-712 typed signatures|
|EIP-2535|Diamond proxy|Multi-facet upgradeable contract|
|EIP-3156|Flash loans|Standardized flash loan interface (borrower callback)|
|EIP-4626|Tokenized vaults|Yield-bearing vault standard|

## Common Patterns

### Clone Factory (Minimal Proxies)

EIP-1167 — deploy cheap copies of a master contract. Each clone delegates to the master; storage is per-clone.

```solidity
contract CloneFactory {
    event CloneCreated(address indexed clone, address indexed owner);

    function createClone(address implementation) internal returns (address clone) {
        // EIP-1167 bytecode: 3d602d80600a3d3981f3363d3d373d3d3d363d73..._IMPL_ADDR_...5af43d82803e903d91602b57fd5bf3
        assembly {
            let ptr := mload(0x40)
            mstore(ptr, 0x3d602d80600a3d3981f3363d3d373d3d3d363d7300000000)
            mstore(add(ptr, 0x14), shl(0x60, implementation))
            mstore(add(ptr, 0x28), 0x5af43d82803e903d91602b57fd5bf30000000000000000000000000000000000)
            clone := create(0, ptr, 0x37)
        }
    }

    function deployPool(address template) external returns (address pool) {
        pool = createClone(template);
        IPool(pool).initialize(msg.sender);
        emit CloneCreated(pool, msg.sender);
    }
}
```

### Emergency Pause

```solidity
contract Pausable is PausableUpgradeable {
    function emergencyPause() external onlyOwner {
        _pause();
    }

    function emergencyUnpause() external onlyOwner {
        _unpause();
    }

    // Override _beforeTokenTransfer to check paused
}
```

### Circuit Breaker

```solidity
contract CircuitBreaker {
    uint256 public constant MAX_SWAP_AMOUNT = 100_000e18;
    uint256 public lastSwapTimestamp;
    uint256 public swapCount;

    modifier checkCircuitBreaker(uint256 amount) {
        require(amount <= MAX_SWAP_AMOUNT, "amount too high");
        require(block.timestamp > lastSwapTimestamp + 1 minutes, "rate limit");
        _;
    }
}
```

## Red Flags

- **tx.origin for auth** — Use `msg.sender`. `tx.origin` can be manipulated via intermediate contract calls.
- **Unchecked external calls** — Every `.call{value:...}("")` must check return value and follow CEI.
- **Missing slippage** — All DEX interactions must accept `minAmountOut`/`maxAmountIn` from caller.
- **Hardcoded addresses** — No mainnet address should be literal in contract code. Pass via constructor/initializer.
- **Uninitialized upgradeable contracts** — Proxies don't call constructors; must call `initialize()`.
- **Storage collision** — Upgradeable implementations must not change storage layout. Use `__gap`.
- **Missing `_disableInitializers()`** — Implementation contracts must disable initialization to prevent destruction via `initialize` + `selfdestruct`.
- **Unbounded loops** — Loops over dynamic arrays can hit block gas limit.
- **`delegatecall` to untrusted addresses** — Can destroy proxy state.
- **Wrong constructor visibility in upgradeable contracts** — Use `onlyInitializing` modifier.
- **Missing `whenNotPaused` on critical functions** — Bypasses emergency stop.
- **No freshness check on Oracle prices** — Must check `updatedAt`.

## Verification Checklist

- [ ] All external state changes follow Checks-Effects-Interactions pattern
- [ ] ReentrancyGuard applied to all external state-altering functions
- [ ] AccessControl or Ownable2Step used for all admin functions
- [ ] Upgradeable contracts have `_disableInitializers()` in constructor
- [ ] Proxy contracts use standardized EIP-1967 storage slots
- [ ] Upgradeable contracts include `__gap` arrays for future state
- [ ] UUPS implementations override `_authorizeUpgrade` with `onlyOwner`
- [ ] Unit tests cover happy path, revert conditions, and edge cases
- [ ] Fork tests validate behavior against mainnet state
- [ ] Fuzz tests run with at least 1000 runs for core math
- [ ] Invariant tests validate protocol invariants (totalSupply == sum balances)
- [ ] All `tx.origin` usages are justified (only cases: gas station patterns)
- [ ] External calls check return value or use SafeERC20
- [ ] No unbounded loops over user-controlled arrays
- [ ] Emergency pause mechanisms are tested end to end
- [ ] Deployment scripts include verification on Etherscan
- [ ] `foundry.toml` / `hardhat.config.js` optimizes for appropriate runs
- [ ] Gas snapshots compared before/after optimization changes

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll just use Ownable, it's simpler" | Ownable2Step prevents accidental transfer of ownership to a dead address. The one extra tx is worth it. |
| "No one will exploit reentrancy, we're small" | All reentrancy attacks target small protocols first. CEI + ReentrancyGuard is mandatory. |
| "Solidity 0.8 overflow checks make SafeMath obsolete" | True for arithmetic, but unchecked blocks are needed for gas optimization, and casting still overflows (`uint8(256)` = 0). |
| "I don't need tests — I'll verify on mainnet" | Every production exploit was preceded by a developer saying this. Foundry tests are faster than a post-mortem. |
| "Upgradeable proxies are too complex, I'll use immutable" | Immutable is fine for tokens. For protocols with evolving logic, the cost of migrating users and liquidity far exceeds the proxy overhead. |
| "Foundry is all I need" | Foundry is excellent for testing. Hardhat's upgrades plugin and deployment scripts are still superior. Use both. |
| "I'll add the emergency pause later" | Adding it later requires an upgrade. If the protocol is upgradeable, deploy it paused and un-pause after verification. If immutable, you can't add it later at all. |
| "Assembly is only for gas golfing" | Yul is essential for precompile calls, efficient error encoding, and patterns that Solidity can't express (e.g., EIP-1167 minimal proxies). |
| "EIP-2535 Diamond is over-engineering" | It is. Use UUPS unless your contract exceeds the 24KB deployment limit. If it does, consider modular architecture, not necessarily Diamond. |
| "Fuzz tests only find obvious bugs" | Foundry fuzz found critical bugs in Uniswap, MakerDAO, and Aave invariants that unit tests missed. They consistently find the edge case you didn't think of. |

## Process

1. **Analyze requirements** — Define contract interfaces, storage layout, access control model, and upgrade path before writing any code. Document the invariants that must always hold.

2. **Choose toolchain** — Prefer Foundry for Solidity-first development. Use Hardhat for upgradeable deployments and complex orchestration. Both can coexist.

3. **Implement storage layout** — Design the struct packing and slot assignment. For upgradeable contracts, plan the `__gap` array. For Diamond, design facet storage positions.

4. **Write tests first (Foundry)** — Unit tests for every external function. Fuzz tests for all arithmetic and boundary conditions. Invariant tests for protocol-level properties.

5. **Implement CEI pattern** — Checks-Effects-Interactions on every state-changing function. Add ReentrancyGuard. Add access control modifiers.

6. **Gas optimize** — Run `forge snapshot`, identify expensive functions, apply gas optimizations (unchecked, calldata, packed structs), verify gas reduction with diff.

7. **Deploy and verify** — Deploy proxy + implementation. Verify on Etherscan (blockscout). Set up multisig ownership.

8. **Post-deployment** — Configure monitoring (Tenderly, Dune), set up alerts on admin function calls, schedule periodic invariant checks.

