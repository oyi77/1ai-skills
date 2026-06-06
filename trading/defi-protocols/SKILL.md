---
name: defi-protocols
description: DeFi protocol development — AMMs, lending, staking, yield farming. Uniswap, Aave patterns

---
## Red Flags

- Slippage tolerance set too high (excessive price impact accepted)
- Flash loan repayment not verified before fund transfer
- Oracle price feed manipulation not mitigated (TWAP recommended)
- Reentrancy vulnerability in external calls to borrower contracts
- Fee-on-transfer tokens not handled in swap calculations
- Liquidity pool imbalance not checked before large swaps

## Verification

After completing DeFi protocol implementation, confirm:

- [ ] AMM swap formula matches x*y=k with correct fee deduction
- [ ] Flash loan repaid in full within same transaction
- [ ] Slippage protection enforced (minAmountOut check)
- [ ] Oracle integration uses TWAP, not spot price
- [ ] ReentrancyGuard applied to all state-changing external calls
- [ ] Test coverage includes edge cases (zero liquidity, max uint256)


## Red Flags

- Slippage tolerance set too high (excessive price impact accepted)
- Flash loan repayment not verified before fund transfer
- Oracle price feed manipulation not mitigated (TWAP recommended)
- Reentrancy vulnerability in external calls to borrower contracts
- Fee-on-transfer tokens not handled in swap calculations

## Verification

After completing DeFi protocol implementation, confirm:

- [ ] AMM swap formula matches x*y=k with correct fee deduction
- [ ] Flash loan repaid in full within same transaction
- [ ] Slippage protection enforced (minAmountOut check)
- [ ] Oracle integration uses TWAP, not spot price
- [ ] ReentrancyGuard applied to all state-changing external calls

---

## Overview

DeFi protocol patterns for AMMs, lending, staking, and yield farming. Covers Uniswap-style constant product AMMs, Aave-like lending pools, and flash loan mechanics.

## Capabilities

- AMM constant product formula (x*y=k)
- Liquidity pool management
- Lending/borrowing with collateral
- Flash loans
- Yield farming and staking
- Oracle integration (Chainlink)

## When to Use

- Building DEX or AMM
- Creating lending protocols
- Yield aggregation strategies
- Staking/reward systems

## When NOT to Use

- Task is about portfolio management, not trading (use portfolio skills)
- Task is about financial analysis (use analysis skills)
- You need to analyze trade results (use analytics skills)
- Task is about risk management (use risk skills)
- You don't have trading capital
- Task requires financial advice (consult advisors)


## Pseudo Code

Reference implementations for AMM swaps, flash loans, and liquidity pool management.


### AMM Swap (Uniswap V2 style)
```solidity
function swap(uint amountIn, address tokenIn, address tokenOut) external {
    (uint reserveIn, uint reserveOut) = getReserves(tokenIn, tokenOut);
    uint amountOut = (amountIn * 997 * reserveOut) / (reserveIn * 1000 + amountIn * 997);
    IERC20(tokenIn).transferFrom(msg.sender, address(this), amountIn);
    IERC20(tokenOut).transfer(msg.sender, amountOut);
}
```

### Flash Loan
```solidity
function flashLoan(uint amount, address token) external {
    uint balanceBefore = IERC20(token).balanceOf(address(this));
    IERC20(token).transfer(msg.sender, amount);
    require(IFlashBorrower(msg.sender).onFlashLoan(amount, token) == "OK");
    require(IERC20(token).balanceOf(address(this)) >= balanceBefore + fee);
}
```

## Common Patterns

- Slippage: require(amountOut >= minAmountOut)
- Deadline: require(block.timestamp <= deadline)
- Fee: 0.3% (Uniswap), configurable
- TWAP oracle for price feeds

## Red Flags

- Slippage tolerance set too high (excessive price impact accepted)
- Flash loan repayment not verified before fund transfer
- Oracle price feed manipulation not mitigated (TWAP recommended)
- Reentrancy vulnerability in external calls to borrower contracts
- Fee-on-transfer tokens not handled in swap calculations

## Verification

After completing DeFi protocol implementation, confirm:

- [ ] AMM swap formula matches x*y=k with correct fee deduction
- [ ] Flash loan repaid in full within same transaction
- [ ] Slippage protection enforced (minAmountOut check)
- [ ] Oracle integration uses TWAP, not spot price
- [ ] ReentrancyGuard applied to all state-changing external calls
