# Trading Checklist

Shared reference for trading-related skills. Load this when doing trading/finance work.

## Strategy Validation
- [ ] Strategy has clear entry criteria (specific, measurable, testable)
- [ ] Strategy has clear exit criteria (take profit, stop loss defined)
- [ ] Risk per trade defined (max 1-2% of account)
- [ ] Backtested: minimum 3 months of historical data
- [ ] Out-of-sample test: strategy works on unseen data
- [ ] Sharpe ratio > 1.0 (risk-adjusted returns)
- [ ] Maximum drawdown < 20% of account

## Technical Analysis
- [ ] Multiple timeframes analyzed (trend + entry timeframe)
- [ ] Support/resistance levels identified
- [ ] Volume confirmation: price move supported by volume
- [ ] No trading against major trend without strong signal
- [ ] Indicators: maximum 3-4 (avoid indicator overload)
- [ ] Divergences noted (price vs. RSI/MACD)

## Risk Management
- [ ] Position size calculated: (Account × Risk%) / (Entry - Stop)
- [ ] Stop loss set before entry (never move stop against position)
- [ ] Take profit set: minimum 1.5x risk:reward ratio
- [ ] No revenge trading after a loss
- [ ] Daily loss limit: stop trading after 3% account loss
- [ ] Correlation check: no more than 2 trades in same asset class
- [ ] Leverage: maximum 5x for crypto, 2x for stocks

## Fundamental Analysis (if applicable)
- [ ] Earnings date checked (avoid holding through earnings)
- [ ] News sentiment: no major negative news pending
- [ ] Sector performance: trade in strong sectors
- [ ] Economic calendar checked (Fed meetings, CPI, NFP)
- [ ] Options flow: unusual activity noted

## Execution
- [ ] Order type correct (market/limit/stop chosen intentionally)
- [ ] Slippage acceptable (< 0.1% for liquid assets)
- [ ] Fees calculated: impact on profitability (especially scalping)
- [ ] Time of day appropriate (avoid low volume hours)
- [ ] Partial fills handled (scale in/out if needed)

## Portfolio Management
- [ ] Maximum 5% of account in single position
- [ ] Diversification: no more than 20% in one sector
- [ ] Cash reserve: minimum 30% for opportunities
- [ ] Correlation matrix: positions not all moving same direction
- [ ] Rebalancing schedule: quarterly minimum

## Record Keeping
- [ ] Trade journal: entry reason, exit reason, emotions, lessons
- [ ] Screenshot taken at entry and exit
- [ ] Win rate tracked (target: > 50% for day/swing trading)
- [ ] Average win > average loss (target: 1.5x+)
- [ ] Monthly P&L statement generated

## Crypto-Specific
- [ ] Exchange reputation checked (no FTX/FTX-style risks)
- [ ] Wallet security: hardware wallet for long-term holds
- [ ] Gas fees considered (Ethereum mainnet expensive for small trades)
- [ ] Stablecoin risk: USDT/USDC depeg monitoring
- [ ] Bridge risks: minimize cross-chain transfers
- [ ] Slippage tolerance set (0.5% default, 1% max)

## Options-Specific
- [ ] Implied volatility: avoid buying at 52-week highs
- [ ] Time decay (theta): don't hold through expiration week
- [ ] Open interest: > 100 contracts (liquidity check)
- [ ] Bid-ask spread: < 5% of option price
- [ ] Assignment risk understood (short options)

## Common Red Flags
- Trading without a stop loss ("it'll come back")
- Revenge trading after a loss
- Over-leveraging (account can't absorb drawdown)
- Chasing pumps (buying after 20%+ move)
- Holding through major news events
- Ignoring correlation (all positions move same direction)
- Trading with rent money (emotional decisions)
- No journal/tracking (can't learn from mistakes)

## Related Skills

For deeper analysis frameworks, use these companion skills:
- **financial/all-in-one-finance** — 16-module suite: equity fundamental/technical, crypto onchain/forensic, macro liquidity, sentiment, forex, commodities, fixed income, options, risk guardian, algo execution, report orchestrator
- **financial/wolf-finance** — 22-module institutional suite: all 16 above plus corporate finance, private markets, wealth management, quant strategies, macro geopolitical, compliance/KYC
- **trading/black-edge** — Alternative data synthesis, dark pool signatures, options flow anomalies
- **trading/alphaear-strategy** — Multi-signal: news aggregation + sentiment + options flow + Kronos prediction
- **trading/value-investing** — Warren Buffett capital allocation framework
- **financial/model-builder** — DCF, LBO, 3-statement Excel models with live data connections
- **financial/risk-guardian** — Position sizing, Kelly, VaR, drawdown limits, correlation checks
