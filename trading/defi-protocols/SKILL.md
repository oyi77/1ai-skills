---
name: defi-protocols
description: DeFi protocol development — AMMs, lending, staking, yield farming. Uniswap, Aave patterns
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

## Pseudo Code

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
