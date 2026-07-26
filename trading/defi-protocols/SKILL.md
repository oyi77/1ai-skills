---
name: defi-protocols
description: 'Skill: defi-protocols. See SKILL.md body for details. Use when this domain is relevant.'
domain: trading
tags:
- algorithms
- defi
- markets
- protocols
- trading
version: 1.0.0
---
## Overview

DeFi protocol patterns for Automated Market Makers (AMMs), lending pools, flash loans, yield farming, order-book DEXs, cross-chain bridges, and oracle integrations. Covers the mathematical foundations, Solidity implementations, Hardhat fork-testing patterns, and Web3.py/Ethers.js interaction code for each primitive. Security invariants (reentrancy, price manipulation, MEV) are treated as first-class design constraints, not afterthoughts.

Each section provides the economic invariant, the Solidity implementation pattern, a concrete test or interaction script, and the attack surface specific to that primitive.

## When to Use

**Trigger phrases:**
- "build DEX or AMM"
- "create lending protocol"
- "yield aggregation strategies"
- "flash loan arbitrage"
- "oracle integration"
- "cross-chain bridge"
- "liquidity pool math"
- "DeFi security audit"

**Matching signal:** The task involves implementing, auditing, extending, or interacting with any of the core DeFi primitives below. The skill covers both the math and the production Solidity with tests.

## When NOT to Use

- Task is about portfolio management, not protocol implementation (use portfolio-manager)
- Task is about low-level smart contract development unrelated to DeFi (use smart-contract-dev)
- Task is about NFT marketplace implementation (use nft-marketplace)
- Task is about wallet key management or gas estimation (use crypto-wallet)
- Task requires financial advice or trading strategy (use trading-strategist)
- You need on-chain forensic investigation (use onchain-transaction-forensics)

## AMM Core: Constant Product (x * y = k)

### Formula

The Uniswap V2 invariant: `reserve0 * reserve1 = k`. A trade that adds `dx` of token0 and receives `dy` of token1 must satisfy:

`(reserve0 + dx * 0.997) * (reserve1 - dy) = reserve0 * reserve1`

The 0.3% fee is extracted before the trade reaches the curve. The output formula:

`dy = (dx * 997 * reserve1) / (reserve0 * 1000 + dx * 997)`

### Solidity

```solidity
// Uniswap V2-style pair swap
function swap(uint256 amountIn, address tokenIn, address tokenOut, uint256 minOut) external {
    (uint256 rIn, uint256 rOut) = getReserves(tokenIn, tokenOut);

    // amountOut = amountIn * 997 * rOut / (rIn * 1000 + amountIn * 997)
    uint256 amountOut = (amountIn * 997 * rOut) / (rIn * 1000 + amountIn * 997);

    require(amountOut >= minOut, "slippage");
    require(amountOut < rOut, "insufficient liquidity");

    // transfer in
    IERC20(tokenIn).safeTransferFrom(msg.sender, address(this), amountIn);
    // transfer out
    IERC20(tokenOut).safeTransfer(msg.sender, amountOut);

    // update reserves
    _update(afterBalance(token0), afterBalance(token1));
}

function getReserves(address t0, address t1) internal view returns (uint256, uint256) {
    return t0 < t1
        ? (reserve0, reserve1)
        : (reserve1, reserve0);
}
```

### Price Calculation

Spot price from reserves: `P = reserve1 / reserve0` (price of token0 in terms of token1). Executing a trade shifts the price proportionally to trade size. After selling `dx`, the new spot price:

`P_new = reserve1 / (reserve0 + dx * 0.997) = reserve1 / (newReserve0)`

### JavaScript (ethers.js) - Query Pool Price

```javascript
async function getPoolPrice(pairAddress, provider) {
    const pair = new ethers.Contract(pairAddress, PAIR_ABI, provider);
    const [r0, r1] = await pair.getReserves();
    const token0 = await pair.token0();
    const price = token0.toLowerCase() < someToken.toLowerCase()
        ? Number(r1) / Number(r0)
        : Number(r0) / Number(r1);
    return price;
}
```

### Python (web3.py) - Simulate Swap

```python
from web3 import Web3

def simulate_swap(amount_in_wei: int, reserve_in: int, reserve_out: int) -> int:
    """Calculate output for a Uniswap V2 swap (0.3% fee)."""
    amount_in_with_fee = amount_in_wei * 997
    numerator = amount_in_with_fee * reserve_out
    denominator = reserve_in * 1000 + amount_in_with_fee
    return numerator // denominator

# Example: swap 1000 USDC (6 decimals) into ETH
usdc_in = 1000 * 10**6
r_usdc = 5_000_000 * 10**6   # 5M USDC in pool
r_eth  = 2_500 * 10**18       # 2500 ETH in pool

eth_out = simulate_swap(usdc_in, r_usdc, r_eth)
print(f"Output: {eth_out / 10**18:.6f} ETH")
```

## AMM Variants

### Weighted Pools (Balancer)

Balancer generalizes constant product to `n` tokens with weights `w_i`:

`prod(reserve_i ^ w_i) = k`

For a two-token pool with weights 80/20:

`r0 ^ 0.8 * r1 ^ 0.2 = k`

Spot price with weights: `P = (r0 * w1) / (r1 * w0)`

Trading one token for another changes the price differently than a 50/50 pool. Weighted pools allow LPs to concentrate risk exposure while still earning fees.

### Stable Swap (Curve)

Curve combines constant product and constant sum for correlated assets (USDC/USDT):

`x * y * (x^2 + y^2) = k`  (simplified two-peg)

More generally: `A * n^n * sum(x_i) + D = A * D * n^n + D^(n+1) / (n^n * prod(x_i))`

Where `A` is the amplification coefficient — higher `A` means flatter curve near peg, less slippage for stable pairs. The D invariant converges to total liquidity when all tokens are at peg, and to constant product when far from peg.

### Concentrated Liquidity (Uniswap V3)

LPs provide liquidity within discrete price ranges `[p_a, p_b]`. L = sqrt(k). The virtual reserves adjust so liquidity only depletes when price exits the range.

```solidity
// V3 tick math
function sqrtPriceX96ToPrice(uint160 sqrtPriceX96, uint256 decimals0, uint256 decimals1)
    internal pure returns (uint256)
{
    // sqrt(P) is stored as Q64.96: sqrtPriceX96 = sqrt(P) * 2^96
    uint256 sqrtPrice = uint256(sqrtPriceX96);
    uint256 priceX192 = sqrtPrice * sqrtPrice;
    return priceX192 * 10**decimals0 / (2**192 * 10**decimals1);
}
```

Position value within a range:

`amount0 = L * (1 / sqrt(p_low) - 1 / sqrt(p_high))`
`amount1 = L * (sqrt(p_high) - sqrt(p_low))`

Impermanent loss is concentrated: if price exits the range, the position becomes fully denomimated in the cheaper token.

## Impermanent Loss

IL occurs when LP return diverges from HODL return. For a price change factor `r = P_new / P_old` in a constant-product pool:

`IL(r) = (2 * sqrt(r)) / (1 + r) - 1`

| Price Change | IL |
|---|---|
| 1.25x (25% up) | -0.6% |
| 1.5x (50% up) | -2.0% |
| 2x (100% up) | -5.7% |
| 3x (200% up) | -13.4% |
| 4x (300% up) | -20.0% |

```python
def impermanent_loss(price_ratio: float) -> float:
    """IL as fraction of HODL value. r = new_price / old_price."""
    return (2 * (price_ratio ** 0.5)) / (1 + price_ratio) - 1
```

IL is symmetric: a 50% drop (-50%) has the same IL as a 100% gain (+100%). Fee income offsets IL over time; the breakeven period depends on pool volume and fee tier.

## Slippage Calculation

```solidity
// Given pool reserves and trade size, compute price impact
function priceImpact(uint256 amountIn, uint256 reserveIn, uint256 reserveOut)
    internal pure returns (uint256 bp)
{
    // returns basis points of price impact
    uint256 kPrev = reserveIn * reserveOut;
    uint256 newReserveIn = reserveIn + amountIn;
    uint256 newReserveOut = (kPrev * 1000) / (newReserveIn * 997); // approximate
    uint256 realizedPrice = (amountIn * 1e18) / (reserveOut - newReserveOut);
    uint256 spotPrice = (reserveIn * 1e18) / reserveOut;
    bp = (realizedPrice * 10000) / spotPrice - 10000;
}
```

## TWAP Oracles from AMM Reserves

### Uniswap V2 TWAP

Accumulate `price * elapsed` at the first transaction of each block:

```solidity
// In _update()
(uint112 r0, uint112 r1, ) = getReserves();
blockTimestampLast = blockTimestamp;
price0CumulativeLast += r1 * elapsed / r0;  // price of token0 in token1
price1CumulativeLast += r0 * elapsed / r1;

// Consumer computes TWAP over a window
function consult(address token, uint256 amountIn, uint256 window)
    external view returns (uint256 amountOut)
{
    uint256 elapsed = blockTimestamp - observationTimestamp;
    uint256 priceCumulative = price0CumulativeLast - price0Cumulative;
    uint256 twap = priceCumulative / elapsed;
    amountOut = amountIn * twap / 1e18;  // assuming 18-decimal tokens
}
```

### Uniswap V3 TWAP

V3 stores an array of observations (tick, timestamp) per pool. Each observation is a `tickCumulative` accumulator. Oracle subgraph queries fetch two observations and compute average tick:

```typescript
// ethers.js — get V3 TWAP
async function getV3Twap(pool: string, windowSeconds: number, provider: Provider) {
    const contract = new ethers.Contract(pool, V3_POOL_ABI, provider);
    const obs = await contract.observations(await contract.slot0());
    // simplified: observe() returns (tickCumulatives, secondsPerLiquidity)
    const [tickCumulatives] = await contract.observe([0, windowSeconds]);
    const avgTick = Number(tickCumulatives[0] - tickCumulatives[1]) / windowSeconds;
    return 1.0001 ** avgTick;
}
```

**Never use spot price from a single pool as an oracle. Always use TWAP over >= 30 minutes.**

## Lending Protocols

### Overcollateralized Lending (Aave-style)

Borrowers deposit collateral (e.g., ETH), then borrow up to a loan-to-value (LTV) ratio. The core state:

```solidity
// Simplified lending pool
contract LendingPool {
    mapping(address => mapping(address => uint256)) public deposits;  // user => asset => amount
    mapping(address => mapping(address => uint256)) public borrows;   // user => asset => amount
    mapping(address => uint256) public totalLiquidity;                // asset => total supplied
    mapping(address => uint256) public totalBorrows;                  // asset => total borrowed

    uint256 constant LTV = 7500;         // 75% in basis points
    uint256 constant LIQUIDATION_THRESHOLD = 8250;  // 82.5%
    uint256 constant LIQUIDATION_BONUS = 500;       // 5%

    function deposit(address asset, uint256 amount) external {
        IERC20(asset).safeTransferFrom(msg.sender, address(this), amount);
        deposits[msg.sender][asset] += amount;
        totalLiquidity[asset] += amount;
    }

    function borrow(address asset, uint256 amount, address collateral) external {
        uint256 collateralValue = getOraclePrice(collateral) * deposits[msg.sender][collateral];
        uint256 borrowValue = getOraclePrice(asset) * (borrows[msg.sender][asset] + amount);
        require(borrowValue * 10000 <= collateralValue * LTV, "over LTV");

        borrows[msg.sender][asset] += amount;
        totalBorrows[asset] += amount;
        IERC20(asset).safeTransfer(msg.sender, amount);
    }
}
```

### Health Factor

`healthFactor = (collateralValue * liquidationThreshold) / (borrowValue * 10000)`

When `healthFactor < 1.0`, the position is liquidatable.

```solidity
function getHealthFactor(address user) public view returns (uint256) {
    (uint256 totalCollateralETH, uint256 totalDebtETH) = getUserAccountData(user);
    if (totalDebtETH == 0) return type(uint256).max;
    return (totalCollateralETH * LIQUIDATION_THRESHOLD) / (totalDebtETH * 10000);
}

function liquidationCall(
    address collateral, address debt, address user, uint256 debtToCover, bool receiveAToken
) external {
    uint256 healthFactor = getHealthFactor(user);
    require(healthFactor < 1e18, "healthy");

    // Liquidator repays debt, receives collateral at a discount
    uint256 collateralAmount = debtToCover * getOraclePrice(debt) * (10000 + LIQUIDATION_BONUS)
        / (getOraclePrice(collateral) * 10000);

    IERC20(debt).safeTransferFrom(msg.sender, address(this), debtToCover);
    IERC20(collateral).safeTransfer(msg.sender, collateralAmount);

    // update state
    deposits[user][collateral] -= collateralAmount;
    borrows[user][debt] -= debtToCover;
}
```

### Interest Rate Models

**Linear model:** `borrowRate = baseRate + slope * utilization`

**Jump rate (Aave V2):** Below the optimal utilization `U_opt`, the slope is moderate. Above `U_opt`, the slope spikes to incentivize new deposits and penalize further borrowing.

```solidity
// Jump rate model
function calculateBorrowRate(uint256 utilization) public pure returns (uint256) {
    uint256 U_OPTIMAL = 8000;   // 80%
    uint256 BASE_RATE = 0;       // 0%
    uint256 SLOPE1 = 400;        // 4% APR
    uint256 SLOPE2 = 30000 * 1e9;  // 300% APR at U_max

    if (utilization <= U_OPTIMAL) {
        return BASE_RATE + (SLOPE1 * utilization) / U_OPTIMAL;
    } else {
        uint256 excess = utilization - U_OPTIMAL;
        return BASE_RATE + SLOPE1
            + (SLOPE2 * excess) / (1e4 - U_OPTIMAL);
    }
}

function utilizationRate(uint256 totalBorrows, uint256 totalLiquidity)
    internal pure returns (uint256)
{
    if (totalLiquidity == 0) return 0;
    return totalBorrows * 10_000 / totalLiquidity;
}
```

## Flash Loans

Flash loans allow uncollateralized borrowing within a single transaction. The borrowed amount must be returned (plus fee) before the transaction ends, or it reverts.

### Aave V3 Flash Loan

```solidity
// Receiver contract
contract FlashLoanReceiver is IFlashLoanSimpleReceiver {
    address constant POOL = 0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2;  // Aave V3 on Mainnet
    uint256 public constant FLASHLOAN_FEE = 5;  // 0.05% in basis points

    function executeOperation(
        address asset, uint256 amount, uint256 premium,
        address initiator, bytes calldata /* params */
    ) external override returns (bool) {
        require(msg.sender == POOL, "unauthorized");
        require(initiator == address(this), "wrong initiator");

        // --- arbitrage logic here ---

        // Approve repayment with premium
        IERC20(asset).approve(POOL, amount + premium);
        return true;
    }

    function initiateFlashLoan(
        address tokenBorrow, uint256 amount, bytes calldata params
    ) external {
        IPool(POOL).flashLoanSimple(
            address(this), tokenBorrow, amount, params, 0
        );
    }
}
```

### Uniswap V3 Flash Swap

Uniswap V3 allows any swap to borrow tokens as long as the callbacks deposit the equivalent amount. No separate flash loan contract needed.

```solidity
// Uniswap V3 flash swap — borrow token1, repay with token0
function uniswapV3SwapCallback(
    int256 amount0Delta, int256 amount1Delta, bytes calldata /* data */
) external override {
    // amount0Delta > 0 means we owe token0; amount1Delta > 0 means we received token1
    require(amount0Delta > 0, "only token0 flash");

    // use borrowed token1 here...

    // repay token0
    IERC20(token0).safeTransfer(pool, uint256(amount0Delta));
}

function initiateFlashSwap(address pool, uint256 amountIn, uint256 amountOutMin) external {
    // amountSpecified < 0 means exactOutput (borrow output)
    ISwapRouter.ExactInputSingleParams memory params = ISwapRouter.ExactInputSingleParams({
        tokenIn: token0,
        tokenOut: token1,
        fee: 3000,
        recipient: address(this),
        deadline: block.timestamp,
        amountIn: amountIn,
        amountOutMinimum: amountOutMin,
        sqrtPriceLimitX96: 0
    });
    ISwapRouter(ROUTER).exactInputSingle(params);
}
```

### dYdX Style (deprecated pattern, legacy reference)

```solidity
// dYdX SoloMargin flash loan (simplified)
function callFunction(
    address sender, Account.Info memory account,
    bytes memory data
) external {
    // borrowed funds available here

    // repay happens implicitly — SoloMargin checks balance difference
}
```

## Yield Farming

### LP Token Staking

A staking contract accepts LP tokens and distributes rewards proportionally.

```solidity
contract StakingRewards {
    IERC20 public stakingToken;
    IERC20 public rewardsToken;

    uint256 public rewardRate;          // reward tokens per second
    uint256 public lastUpdateTime;
    uint256 public rewardPerTokenStored;
    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;
    mapping(address => uint256) public userRewardPerTokenPaid;
    mapping(address => uint256) public rewards;

    modifier updateReward(address account) {
        rewardPerTokenStored = rewardPerToken();
        lastUpdateTime = block.timestamp;
        if (account != address(0)) {
            rewards[account] = earned(account);
            userRewardPerTokenPaid[account] = rewardPerTokenStored;
        }
        _;
    }

    function rewardPerToken() public view returns (uint256) {
        if (totalSupply == 0) return rewardPerTokenStored;
        return rewardPerTokenStored
            + (block.timestamp - lastUpdateTime) * rewardRate * 1e18 / totalSupply;
    }

    function earned(address account) public view returns (uint256) {
        return balanceOf[account] * (rewardPerTokenStored - userRewardPerTokenPaid[account]) / 1e18
            + rewards[account];
    }

    function stake(uint256 amount) external updateReward(msg.sender) {
        totalSupply += amount;
        balanceOf[msg.sender] += amount;
        stakingToken.safeTransferFrom(msg.sender, address(this), amount);
    }

    function withdraw(uint256 amount) external updateReward(msg.sender) {
        totalSupply -= amount;
        balanceOf[msg.sender] -= amount;
        stakingToken.safeTransfer(msg.sender, amount);
    }

    function getReward() external updateReward(msg.sender) {
        uint256 reward = rewards[msg.sender];
        if (reward > 0) {
            rewards[msg.sender] = 0;
            rewardsToken.safeTransfer(msg.sender, reward);
        }
    }
}
```

### Vesting Schedules

Distribute rewards linearly over a duration:

```solidity
contract Vesting {
    struct Schedule {
        uint256 totalAmount;
        uint256 startTime;
        uint256 duration;
        uint256 claimed;
    }

    mapping(address => Schedule) public schedules;

    function claimable(address user) public view returns (uint256) {
        Schedule storage s = schedules[user];
        if (block.timestamp < s.startTime) return 0;
        uint256 elapsed = block.timestamp - s.startTime;
        uint256 vested = s.totalAmount * Math.min(elapsed, s.duration) / s.duration;
        return vested - s.claimed;
    }

    function claim() external {
        uint256 amount = claimable(msg.sender);
        require(amount > 0, "nothing to claim");
        schedules[msg.sender].claimed += amount;
        token.safeTransfer(msg.sender, amount);
    }
}
```

## Order Book DEX

### 0x Protocol (Off-Chain Order Relay)

Orders are signed off-chain and submitted on-chain by a taker. The protocol matches orders via a settlement contract.

```solidity
// 0x limit order (simplified)
struct Order {
    address makerToken;
    address takerToken;
    uint256 makerAmount;
    uint256 takerAmount;
    address maker;
    uint256 expiry;
    uint256 salt;
}

function fillOrder(Order calldata order, bytes calldata signature) external {
    require(block.timestamp <= order.expiry, "expired");
    require(
        ECDSA.recover(keccak256(abi.encode(order)), signature) == order.maker,
        "bad sig"
    );

    IERC20(order.takerToken).safeTransferFrom(msg.sender, order.maker, order.takerAmount);
    IERC20(order.makerToken).safeTransferFrom(order.maker, msg.sender, order.makerAmount);
}
```

### RFQ-Based Matching (Request-for-Quote)

Used by 0x API, Matcha, 1inch — market makers quote prices via off-chain API, then the taker submits the quote on-chain. The quote includes a signature that binds the maker to the price.

## Cross-Chain Bridges

### Lock/Mint Pattern

```solidity
// Chain A — lock tokens, emit event for relayer
contract BridgeLock {
    mapping(address => uint256) public totalLocked;

    event Locked(address indexed token, address indexed sender, uint256 amount, bytes32 indexed destChain);

    function lock(address token, uint256 amount, bytes32 destChain, bytes calldata recipient) external {
        IERC20(token).safeTransferFrom(msg.sender, address(this), amount);
        totalLocked[token] += amount;
        emit Locked(token, msg.sender, amount, destChain);
    }

    function unlock(address token, uint256 amount, bytes calldata proof) external {
        require(verifyBurnProof(token, amount, proof), "invalid proof");
        IERC20(token).safeTransfer(msg.sender, amount);
        totalLocked[token] -= amount;
    }
}
```

```solidity
// Chain B — mint tokens when locked on Chain A
contract BridgeMint {
    mapping(address => address) public wrappedTokens;  // original token => wrapped

    event Minted(address indexed wrapped, address indexed recipient, uint256 amount);

    function mint(bytes calldata proof) external {
        (address originalToken, address recipient, uint256 amount) = parseLockProof(proof);
        address wrapped = wrappedTokens[originalToken];
        require(wrapped != address(0), "unsupported token");

        _mint(wrapped, recipient, amount);
        emit Minted(wrapped, recipient, amount);
    }

    // burn/redeem
    function burn(address wrapped, uint256 amount, bytes32 destChain, bytes calldata recipient) external {
        _burn(wrapped, msg.sender, amount);
        emit Burned(wrapped, msg.sender, amount, destChain, recipient);
    }
}
```

### Liquidity Network Bridges

Two pools hold the same asset on both chains. Users deposit on chain A and receive from the pool on chain B. The operator rebalances periodically. No wrapped tokens needed, but liquidity is fragmented.

### Light Client Verification

Advanced bridges (LayerZero, IBC) validate headers from chain A on chain B using light clients. The Solidity contract stores block headers and verifies state proofs:

```solidity
// Simplified header relay
contract LightClientBridge {
    struct BlockHeader {
        uint256 number;
        bytes32 stateRoot;
        bytes32 txRoot;
        uint256 timestamp;
    }

    mapping(uint256 => BlockHeader) public headers;

    function submitHeader(BlockHeader calldata header, bytes calldata attestation) external {
        require(verifyAttestation(header, attestation), "invalid attestation");
        headers[header.number] = header;
    }

    function verifyProof(bytes32 leaf, bytes32[] calldata proof, uint256 blockNumber)
        external view returns (bool)
    {
        bytes32 computedRoot = computeMerkleRoot(leaf, proof);
        return computedRoot == headers[blockNumber].stateRoot;
    }
}
```

## Oracle Integration

### Chainlink Price Feeds

```solidity
contract PriceConsumer {
    AggregatorV3Interface internal priceFeed;

    constructor(address feed) {
        priceFeed = AggregatorV3Interface(feed);
    }

    function getLatestPrice() public view returns (int256) {
        (, int256 price, , uint256 updatedAt, ) = priceFeed.latestRoundData();
        require(block.timestamp - updatedAt <= 1 hours, "stale price");
        require(price > 0, "invalid price");
        return price;
    }
}

// ETH/USD feed on Mainnet: 0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419
// BTC/USD feed on Mainnet: 0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c
```

```javascript
// ethers.js — read Chainlink price
async function getChainlinkPrice(feedAddress, provider) {
    const aggregator = new ethers.Contract(feedAddress, [
        "function latestRoundData() view returns (uint80,int256,uint256,uint256,uint80)",
        "function decimals() view returns (uint8)"
    ], provider);
    const [, price, , updatedAt] = await aggregator.latestRoundData();
    const decimals = await aggregator.decimals();
    return { price: Number(price) / 10 ** decimals, updatedAt: Number(updatedAt) };
}
```

### Uniswap V2 TWAP Oracle

Already covered above — accumulate `price * elapsed` at each update, compute over a window. Deploy as a separate oracle contract that reads a pair's cumulative price.

### MakerDAO Oracles

Maker's Medianizer aggregates prices from multiple feeds, publishes the median, and includes a delay before use. The `DSValue` and `DSMedianizer` contracts are legacy.

### Oracle Security Patterns

```solidity
// Multi-source validation
function validatePrice(uint256 priceCL, uint256 twap) internal pure returns (uint256) {
    uint256 deviation = priceCL > twap
        ? (priceCL - twap) * 10000 / twap
        : (twap - priceCL) * 10000 / priceCL;
    require(deviation < 500, "oracle divergence");  // max 5% divergence
    // return weighted average or min
    return priceCL < twap ? priceCL : twap;
}
```

## Security

### Reentrancy

The Checks-Effects-Interactions pattern plus OpenZeppelin's ReentrancyGuard:

```solidity
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract SecureLending is ReentrancyGuard {
    function withdraw(uint256 amount) external nonReentrant {
        require(balances[msg.sender] >= amount, "insufficient");
        balances[msg.sender] -= amount;             // effect
        IERC20(token).safeTransfer(msg.sender, amount);  // interaction
    }
}
```

### Price Manipulation (Oracle Attacks)

**The example of failure:** Aave V2 EURS depeg incident — attacker manipulated a low-liquidity Uniswap pair to get a false spot price, then liquidated positions in Aave.

```solidity
// VULNERABLE — spot price from a single AMM
function getPriceLiquid(address pair) external view returns (uint256) {
    (uint256 r0, uint256 r1,) = IUniswapV2Pair(pair).getReserves();
    return r1 * 1e18 / r0;  // manipulatable with a single swap
}

// SAFER — TWAP from multiple sources
function getPriceSafe(address pair) external view returns (uint256) {
    uint256 twap = IUniswapV2TWAP(pair).consult(someToken, 1e18, 30 minutes);
    uint256 chainlink = aggregator.latestAnswer();
    // Take the lower of two (or the average, or revert on divergence > 5%)
    return (twap + chainlink) / 2;
}
```

### Sandwich Attacks

MEV bots front-run and back-run user swaps:

1. Attacker sees user's pending swap transaction
2. Attacker buys before (front-run) — pushes price up
3. User buys at worse price
4. Attacker sells after (back-run) — profits from inflated price

**Mitigation:**
- Use a private mempool (Flashbots, MEV-Share)
- Set tight slippage bounds (minAmountOut)
- Use batch auctions (CowSwap) instead of direct DEX swaps
- Price-limit orders (e.g., maker orders settled at a target price)

### MEV Protection Patterns

```solidity
// Slippage sandwich protection — require exact output
function swapExactTokensForTokens(
    uint256 amountIn, uint256 amountOutMin,
    address[] calldata path, address to
) external returns (uint256[] memory amounts) {
    amounts = UniswapV2Library.getAmountsOut(factory, amountIn, path);
    require(amounts[amounts.length - 1] >= amountOutMin, "slippage");
    // ...transfer and swap
}

// Deadline protection — prevents long-pending transactions
function swapExactTokensForTokens(
    // ...
    uint256 deadline
) external {
    require(block.timestamp <= deadline, "expired");
    // ...
}
```

## Hardhat Fork Tests

```typescript
import { ethers } from "hardhat";

describe("AMM Integration", function () {
    it("should execute a flash loan arbitrage on mainnet fork", async function () {
        // Fork mainnet at a specific block
        await network.provider.request({
            method: "hardhat_reset",
            params: [{
                forking: {
                    jsonRpcUrl: `https://eth-mainnet.g.alchemy.com/v2/${process.env.ALCHEMY_KEY}`,
                    blockNumber: 18000000,
                }
            }]
        });

        // Impersonate a whale
        const whale = "0x...";
        await network.provider.request({
            method: "hardhat_impersonateAccount",
            params: [whale],
        });
        const signer = await ethers.getSigner(whale);

        // Execute the arbitrage
        const arb = await (await ethers.getContractFactory("FlashArb")).deploy();
        const tx = await arb.connect(signer).execute(amount, { gasLimit: 5000000 });
        const receipt = await tx.wait();

        expect(receipt.status).to.equal(1);
        const profit = await arb.profit();
        expect(profit).to.be.gt(0);
    });
});
```

## Common Patterns

- **Slippage protection:** Always compare `amountOut >= minAmountOut` or `amountIn <= maxAmountIn`
- **Deadline checks:** Reject stale transactions with `require(block.timestamp <= deadline)`
- **Emergency pause:** OpenZeppelin's `Pausable` — halt all state-changing functions during incidents
- **Fee tiers:** Uniswap V3 uses 0.01%, 0.05%, 0.30%, 1.00% for different volatility pairs
- **Pull over push:** Let users withdraw (pull) instead of contract sending (push), avoiding DoS vectors
- **Initialization protection:** Use OpenZeppelin's `Initializable` for upgradeable contracts
- **Access control:** OpenZeppelin's `AccessControl` for role-based admin functions
- **Fee-on-transfer tokens:** Check balance before and after transfer; never assume `amountIn == received`

```solidity
// Fee-on-transfer safe pattern
function deposit(address token, uint256 amount) external {
    uint256 before = IERC20(token).balanceOf(address(this));
    IERC20(token).safeTransferFrom(msg.sender, address(this), amount);
    uint256 received = IERC20(token).balanceOf(address(this)) - before;
    shares[msg.sender] += received;  // use received, not amount
}
```

## Red Flags

- **Spot price oracle from a single pool** — trivial to manipulate with a single swap.
- **Single-sided liquidity** — a pool with only one token provisioned is a honeypot.
- **Uncapped withdrawal fees** — can drain users on withdrawal; there should be a ceiling.
- **Flash loan fee set to zero without economic reason** — invites griefing attacks.
- **No minimum borrow amount** — attackers can create dust positions to grief liquidations.
- **Slippage tolerance set too high** — excessive price impact accepted, MEV sandwich bait.
- **Missing `safeTransfer`** — non-standard tokens (USDT) cause transfers to silently fail.
- **Incorrect fee ordering** — fee deducted after swap math instead of before (V2 style).
- **No deadline parameter** — transactions can be held and executed later at unfavorable prices.
- **ERC20 `approve` race condition** — Uniswap V2 pattern uses `safeIncreaseAllowance` instead.
- **Inflation attack on ERC-4626 vaults** — first depositor can manipulate share price. Mitigate with minimum initial mint or virtual shares.
- **Reentrancy in token callback** — ERC-777 callbacks re-enter the protocol during transfer.
- **Missing invariant check** — no `k`-value check after V2 swap (Uniswap enforces `k * 1000 >= kLast` for fee harvesting).

## Verification

After completing DeFi protocol implementation, confirm:

- [ ] AMM swap formula matches `x * y = k` with correct fee deduction (0.3% taken before curve)
- [ ] Flash loan repaid in full (plus premium) within the same transaction
- [ ] Slippage protection enforced via `minAmountOut` or `maxAmountIn`
- [ ] Deadline parameter guards stale transactions
- [ ] Oracle integration uses TWAP or multiple sources, never single-pool spot price
- [ ] ReentrancyGuard applied to all state-changing external calls
- [ ] Liquidation health factor computed correctly with oracle prices
- [ ] `safeTransfer` and `safeTransferFrom` used for all token transfers
- [ ] Fee-on-transfer tokens handled with pre/post balance checks
- [ ] Hardhat fork test executes the full flow against real mainnet state
- [ ] Emergency pause mechanism can stop critical functions

## Process

1. **Identify the primitive** — AMM, lending, flash loan, staking, bridge, or oracle. Each has different invariants and attack surfaces.
2. **Write the invariant first** — Express the core constraint as a formula (e.g., `x*y = k`, `healthFactor >= 1.0`). All other code enforces this invariant.
3. **Implement the core logic** — The swap, borrow, stake, or mint function. Keep reading external state only. Avoid loops over unbounded arrays.
4. **Add fee math** — Determine where fees are extracted (before curve for AMM, after interest accrual for lending). Apply fee basis points correctly.
5. **Apply security patterns** — ReentrancyGuard, Checks-Effects-Interactions, access control, pause control.
6. **Wire oracles** — Chainlink for LTV/liquidation, TWAP for internal pricing decisions. Add staleness checks and multi-source validation.
7. **Test with Hardhat fork** — Deploy against a mainnet fork, impersonate whales, validate the full economic flow.
8. **Invariant test** — Write fuzz tests (Foundry) that assert the core invariant holds after any sequence of operations.
9. **Audit for known attacks** — Reentrancy, sandwich, price manipulation, donation attacks on vaults, flash loan re-deposit.
10. **Document failure modes** — What happens when oracle goes stale, when utilization spikes, when a pool gets drained. Document the circuit breakers.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "TWAP adds complexity I don't need; spot price works fine for my use case" | Spot price from a single pool is manipulatable for ~$100k on most pairs. TWAP over 30 min costs nothing in gas (one extra read) and prevents oracle attacks. |
| "I can skip the deadline parameter to simplify the interface" | Without a deadline, a user's transaction can be held by a validator and executed hours later at manipulated prices. |
| "AMMs replace order books entirely" | AMMs excel at passive liquidity but have worse price discovery for large orders and suffer from MEV. Order books with RFQ matching are superior for institutional flows. |
| "Flash loans are free capital — no risk" | Flash loan callbacks can re-enter the lending protocol to drain it. The Aave V2 codebase requires receiver contracts to be non-reentrant relative to the pool. |
| "I can use the same interest rate model for all pools" | Stable assets (USDC/DAI) can tolerate higher utilization before spike. Volatile assets need jump-rate models with a lower `U_opt` (~60%) to keep liquidity available. |
| "Concentrated liquidity is always better than V2" | Concentrated positions need active rebalancing. Passive LPs in V3 often earn less than V2 LPs after gas costs for position management. IL is concentrated, not eliminated. |
| "Bridges just lock and mint — simple" | Bridge security depends on the validator/threshold set, not the lock/mint logic. Wormhole's $320M hack was a signature verification bug, not a lock/mint flaw. Light client bridges are more secure but significantly more expensive to verify on-chain. |
| "Chainlink feeds are always reliable" | Chainlink feeds can go stale during extreme volatility (LUNA collapse). Always add a staleness check (`heartbeat`) and a fallback TWAP source with divergence checks. |
| "I'll add emergency pause after the audit" | Without a pause mechanism deployed from the start, a live exploit forces the team to coordinate a migration before the protocol can be stopped. Code pause + proxy admin = minutes to stop an exploit. |
