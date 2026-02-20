# Multi-Market Trading Strategies Implementation Plan

## TL;DR

> **Quick Summary**: Implement profitable trading strategies for FOREX, CRYPTO, STOCKS, and COMMODITIES based on research from authoritative sources (ForexTester, Amberdata, QuantInsti, Brenndoerfer). Includes new indicators, market-specific strategy templates, risk management frameworks, and integration with existing trading system.

> **Deliverables**:
> - New indicators: ADX, Stochastic, ATR, Ichimoku
> - FOREX strategies: Holy Grail, Momentum Elder, Kumo Breakout
> - CRYPTO strategies: Funding Rate Reversal, Volume Momentum, On-Chain Flow
> - STOCKS strategies: Golden Cross Screener, RSI Divergence
> - COMMODITY strategies: Gold-Silver Ratio, Seasonal Pattern
> - Market-specific risk management modules
> - Backtest modules for each strategy

> **Estimated Effort**: Large (50+ tasks across all markets)
> **Parallel Execution**: YES - Multiple waves with indicator foundation first
> **Critical Path**: Indicators → FOREX → CRYPTO → STOCKS → COMMODITIES → Integration

---

## Context

### Original Request
Research and implement profitable trading strategies for all market types:
- FOREX (currency pairs)
- CRYPTO (BTC, ETH, altcoins)
- STOCKS (equities)
- COMMODITIES (gold, oil, silver)

### Research Findings Summary

#### FOREX Strategies (from bg_9fc163dd)
- **Holy Grail**: EMA(20) + ADX(14) + RSI(14), H4+ timeframe
- **Momentum Elder**: EMA(19) + Momentum(18), H1+ timeframe
- **Two Groups of SMA**: Multi-SMA alignment, H4+ timeframe
- **Kumo Breakout**: Ichimoku (8,29,34) + AO, M15+ timeframe
- **Yen Crosses**: EMA(8) + SMA(21) + ADX, H1-H4 timeframe
- **Risk**: 1-2% per trade, R-multiple system (1:2 minimum)

#### CRYPTO Strategies (from bg_caeb85a1)
- **Trend Continuation**: EMA(20/50/200) + VWAP, 4H-Daily timeframe
- **Pullback Buying**: Fibonacci 38-61% + Volume, 1H-4H timeframe
- **Mean Reversion**: VWAP + Bollinger Bands + RSI, 15M-1H timeframe
- **Funding Rate Reversal**: Persistent funding >14 days = reversal signal, Daily-Weekly timeframe
- **Momentum Scalping**: MACD(12,26,9) + RSI(60-80), 5M-15M timeframe
- **Crypto-Specific**: On-chain metrics (exchange flows, whale transactions, MVRV), funding rates, 150-200% volume confirmation

#### STOCKS Strategies (from bg_ac00a07d)
- **CAN SLIM**: C=Current earnings, A=Annual earnings, N=New products, S=Supply/demand, L=Leader, I=Institutional, M=Market
- **Golden Cross**: 50/200 SMA crossover, Daily-Weekly timeframe
- **RSI Divergence**: RSI(14) extremes, Daily timeframe
- **Momentum Factor**: 6-12 month returns, Weekly timeframe
- **Risk**: 1-2% per trade, max 5-10% per stock

#### COMMODITY Strategies (from bg_3342d8c6)
- **Gold-Silver Ratio**: Pair trade between XAUUSD and XAGUSD
- **Seasonal Pattern**: Monthly/quarterly recurring patterns
- **USD Correlation Reversal**: Inverse USD pair movements
- **Supply/Demand**: Commodity-specific fundamentals

### Existing Codebase (from bg_ca7af3da)

**Already Implemented**:
- Strategy base classes: `Strategy`, `StrategyTemplate`
- Indicators: RSI, SMA, EMA, WMA, MACD, Bollinger Bands
- Strategy templates: TrendFollowing, Scalping, MeanReversion, Breakout
- XAUUSD 7-Candle Breakout strategy
- Broker connectors: MT5, CCXT

**Missing (from research)**:
- Indicators: ADX, Stochastic, ATR, Ichimoku
- Strategy templates: FOREX-specific, CRYPTO-specific, STOCKS-specific, COMMODITY-specific
- Market-specific risk management
- On-chain data integration (for crypto)

---

## Work Objectives

### Core Objective
Build a comprehensive multi-market trading strategy system that enables:
1. Profitable strategies across FOREX, CRYPTO, STOCKS, and COMMODITIES
2. Market-specific indicators and risk management
3. Backtesting and paper trading for all strategies
4. Seamless integration with existing MT5/CCXT brokers

### Concrete Deliverables

1. **New Indicators**:
   - `trading/indicators/adx.py` - Average Directional Index
   - `trading/indicators/stochastic.py` - Stochastic Oscillator
   - `trading/indicators/atr.py` - Average True Range
   - `trading/indicators/ichimoku.py` - Ichimoku Kinko Hyo

2. **FOREX Strategies**:
   - `trading/strategy/templates/forex/holy_grail.py`
   - `trading/strategy/templates/forex/momentum_elder.py`
   - `trading/strategy/templates/forex/kumo_breakout.py`

3. **CRYPTO Strategies**:
   - `trading/strategy/templates/crypto/funding_reversal.py`
   - `trading/strategy/templates/crypto/volume_momentum.py`
   - `trading/strategy/templates/crypto/onchain_flow.py`

4. **STOCKS Strategies**:
   - `trading/strategy/templates/stocks/golden_cross.py`
   - `trading/strategy/templates/stocks/rsi_divergence.py`

5. **COMMODITY Strategies**:
   - `trading/strategy/templates/commodities/gold_silver_ratio.py`
   - `trading/strategy/templates/commodities/seasonal.py`

6. **Risk Management**:
   - `trading/risk/forex_manager.py` - FOREX-specific risk
   - `trading/risk/crypto_manager.py` - CRYPTO-specific risk
   - `trading/risk/stock_manager.py` - STOCKS-specific risk
   - `trading/risk/commodity_manager.py` - COMMODITY-specific risk

7. **Backtest Modules**:
   - `trading/backtest/forex_engine.py`
   - `trading/backtest/crypto_engine.py`
   - `trading/backtest/stock_engine.py`
   - `trading/backtest/commodity_engine.py`

8. **Data Integration**:
   - `trading/data/onchain.py` - On-chain data for crypto
   - `trading/data/funding.py` - Funding rate data

### Definition of Done
- [ ] All indicators implement base class correctly
- [ ] All strategies produce signals in expected format
- [ ] Backtest engines calculate metrics correctly
- [ ] Risk managers apply market-specific rules
- [ ] Integration tests pass with existing brokers

### Must Have
- ADX, Stochastic, ATR, Ichimoku indicators
- 1 strategy per market type (4 total)
- Market-specific risk management
- Backtest capability for each strategy
- Integration with existing broker connectors

### Must NOT Have
- Hard-coded credentials
- Real money execution without confirmation
- Strategies without backtesting validation

---

## Verification Strategy

### Test Decision
- **Infrastructure exists**: YES - pytest framework
- **Automated tests**: YES (TDD)
- **Framework**: pytest
- **TDD Approach**: Test-first for indicators and strategies
- **Agent-Executed QA**: Mandatory for all tasks

### QA Policy
Every task includes agent-executed QA scenarios verifying:
- Indicator calculations against known values
- Strategy signals match expected patterns
- Backtest metrics accuracy
- Risk calculations match formulas

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Indicators - Start Immediately):
├── Task 1: ADX indicator implementation [quick]
├── Task 2: Stochastic indicator implementation [quick]
├── Task 3: ATR indicator implementation [quick]
├── Task 4: Ichimoku indicator implementation [deep]
├── Task 5: Indicator test suite [quick]
└── Task 6: Indicator base class update [quick]

Wave 2 (FOREX Strategies - After Wave 1):
├── Task 7: Holy Grail strategy [deep]
├── Task 8: Momentum Elder strategy [deep]
├── Task 9: Kumo Breakout strategy [deep]
├── Task 10: FOREX risk manager [quick]
└── Task 11: FOREX backtest engine [deep]

Wave 3 (CRYPTO Strategies - After Wave 2):
├── Task 12: On-chain data module [deep]
├── Task 13: Funding rate data module [quick]
├── Task 14: Funding Rate Reversal strategy [deep]
├── Task 15: Volume Momentum strategy [deep]
├── Task 16: CRYPTO risk manager [quick]
└── Task 17: CRYPTO backtest engine [deep]

Wave 4 (STOCKS Strategies - After Wave 3):
├── Task 18: Golden Cross screener [deep]
├── Task 19: RSI Divergence detector [deep]
├── Task 20: STOCKS risk manager [quick]
└── Task 21: STOCKS backtest engine [deep]

Wave 5 (COMMODITY Strategies - After Wave 4):
├── Task 22: Gold-Silver Ratio strategy [deep]
├── Task 23: Seasonal Pattern strategy [deep]
├── Task 24: COMMODITY risk manager [quick]
└── Task 25: COMMODITY backtest engine [deep]

Wave 6 (Integration & Documentation):
├── Task 26: Strategy registry [quick]
├── Task 27: Update main SKILL.md [quick]
├── Task 28: Update SKILL_INDEX.json [quick]
├── Task 29: Create strategy README [quick]
└── Task 30: Integration tests [deep]
```

### Dependency Matrix

| Task | Depends On | Blocks | Wave |
|------|------------|--------|------|
| 1-6 | — | 7-11 | 1 |
| 7-11 | 1-6 | 12-17 | 2 |
| 12-17 | 7-11 | 18-21 | 3 |
| 18-21 | 12-17 | 22-25 | 4 |
| 22-25 | 18-21 | 26-30 | 5 |
| 26-30 | 22-25 | — | 6 |

---

## TODOs

### Wave 1: Indicators

- [ ] 1. ADX Indicator Implementation

  **What to do**:
  - Create `trading/indicators/adx.py`
  - Implement ADX calculation (14-period default)
  - Implement +DI and -DI calculation
  - Support trend strength levels (15=weak, 25=strong, 50=very strong)
  - Follow Indicator base class pattern

  **Must NOT do**:
  - Don't hardcode period (make configurable)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Indicator implementation is straightforward following existing patterns
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1-6)
  - **Blocks**: Tasks 7-11
  - **Blocked By**: None

  **References**:
  - `trading/indicators/rsi.py` - Pattern to follow
  - `trading/indicators/base.py` - Base class interface
  - Research: Holy Grail strategy requires ADX(14) with level 25 filtering

  **Acceptance Criteria**:
  - [ ] ADX class inherits from Indicator
  - [ ] calculate() returns (adx, plus_di, minus_di)
  - [ ] Period configurable (default 14)
  - [ ] Trend strength levels correct

  **QA Scenarios**:

  ```
  Scenario: ADX calculation with known values
    Tool: Bash
    Preconditions: Python with indicator framework
    Steps:
      1. Create test data with known trends
      2. Run ADX calculation
      3. Verify ADX rises during strong trends
      4. Verify +DI/-DI direction matches trend
    Expected Result: ADX increases when trend strengthens
    Evidence: .sisyphus/evidence/task-1-adx-test.txt
  ```

  **Commit**: YES
  - Message: `feat(indicators): add ADX indicator`
  - Files: trading/indicators/adx.py

---

- [ ] 2. Stochastic Indicator Implementation

  **What to do**:
  - Create `trading/indicators/stochastic.py`
  - Implement Stochastic Oscillator (%K and %D lines)
  - Default parameters: (14, 3, 3) - periods for %K, %D, slowing
  - Support oversold (<20) and overbought (>80) zones

  **Must NOT do**:
  - Don't use fixed periods (make configurable)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Standard indicator implementation
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1-6)

  **References**:
  - `trading/indicators/rsi.py` - Pattern to follow
  - Research: Mean reversion strategy uses Stochastic for confirmation

  **Acceptance Criteria**:
  - [ ] Stochastic class inherits from Indicator
  - [ ] calculate() returns (%K, %D)
  - [ ] Oversold/overbought levels correct (20/80)
  - [ ] Smoothed %D line calculated correctly

  **QA Scenarios**:

  ```
  Scenario: Stochastic oversold/overbought detection
    Tool: Bash
    Preconditions: Python with indicator framework
    Steps:
      1. Create test data with price at lows
      2. Run Stochastic calculation
      3. Verify %K < 20 (oversold)
      4. Create test data with price at highs
      5. Verify %K > 80 (overbought)
    Expected Result: Correct identification of oversold/overbought
    Evidence: .sisyphus/evidence/task-2-stoch-test.txt
  ```

  **Commit**: YES
  - Message: `feat(indicators): add Stochastic indicator`
  - Files: trading/indicators/stochastic.py

---

- [ ] 3. ATR Indicator Implementation

  **What to do**:
  - Create `trading/indicators/atr.py`
  - Implement Average True Range calculation
  - Wilder's smoothing method (default 14-period)
  - Support volatility-based stop loss calculation

  **Must NOT do**:
  - Don't use simple average (must use Wilder's smoothing)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Standard indicator implementation
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1-6)

  **References**:
  - `trading/indicators/moving_averages.py` - EMA implementation reference
  - Research: All strategies need ATR for stop loss calibration

  **Acceptance Criteria**:
  - [ ] ATR class inherits from Indicator
  - [ ] calculate() returns atr value
  - [ ] Wilder's smoothing implemented correctly
  - [ ] Period configurable (default 14)

  **QA Scenarios**:

  ```
  Scenario: ATR volatility measurement
    Tool: Bash
    Preconditions: Python with indicator framework
    Steps:
      1. Create test data with known ranges
      2. Run ATR calculation
      3. Verify ATR reflects true range average
      4. Test with different period values
    Expected Result: ATR increases with larger ranges
    Evidence: .sisyphus/evidence/task-3-atr-test.txt
  ```

  **Commit**: YES
  - Message: `feat(indicators): add ATR indicator`
  - Files: trading/indicators/atr.py

---

- [ ] 4. Ichimoku Indicator Implementation

  **What to do**:
  - Create `trading/indicators/ichimoku.py`
  - Implement all 5 Ichimoku components:
    - Tenkan-shi (Conversion Line) - 9-period
    - Kijun-shi (Base Line) - 26-period
    - Senkou Span A (Leading Span A) - (Tenkan + Kijun) / 2
    - Senkou Span B (Leading Span B) - 52-period
    - Chikou Span (Lagging Span) - 26-period back
  - Implement Kumo (cloud) calculation
  - Support optimized parameters for forex: (8, 29, 34)

  **Must NOT do**:
  - Don't use standard (9, 26, 52) without forex optimization option

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Complex multi-component indicator
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1-6)

  **References**:
  - Research: Kumo Breakout strategy uses Ichimoku (8, 29, 34) + AO
  - `trading/indicators/base.py` - Base class interface

  **Acceptance Criteria**:
  - [ ] Ichimoku class inherits from Indicator
  - [ ] calculate() returns (tenkan, kijun, senkou_a, senkou_b, chikou)
  - [ ] Kumo (cloud) regions calculated correctly
  - [ ] Both standard (9,26,52) and forex (8,29,34) parameters supported

  **QA Scenarios**:

  ```
  Scenario: Ichimoku Kumo identification
    Tool: Bash
    Preconditions: Python with indicator framework
    Steps:
      1. Create test data with trending price
      2. Run Ichimoku calculation with forex params (8,29,34)
      3. Verify Kumo cloud is bullish (senkou_a > senkou_b)
      4. Verify price breaks above/below Kumo
    Expected Result: Kumo signals match price action
    Evidence: .sisyphus/evidence/task-4-ichimoku-test.txt
  ```

  **Commit**: YES
  - Message: `feat(indicators): add Ichimoku indicator`
  - Files: trading/indicators/ichimoku.py

---

- [ ] 5. Indicator Test Suite

  **What to do**:
  - Create `trading/tests/test_indicators/test_new_indicators.py`
  - Test all new indicators (ADX, Stochastic, ATR, Ichimoku)
  - Verify calculations against known values
  - Test edge cases (insufficient data, flat markets)

  **Must NOT do**:
  - Don't skip edge case testing

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Test implementation following existing patterns
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1-6)

  **References**:
  - `trading/tests/test_indicators/rsi_test.py` - Pattern to follow
  - `trading/tests/conftest.py` - Test configuration

  **Acceptance Criteria**:
  - [ ] All 4 indicators tested
  - [ ] pytest runs successfully
  - [ ] Coverage > 80%

  **Commit**: YES
  - Message: `test(indicators): add tests for ADX, Stochastic, ATR, Ichimoku`
  - Files: trading/tests/test_indicators/test_new_indicators.py

---

- [ ] 6. Update Indicators __init__.py

  **What to do**:
  - Update `trading/indicators/__init__.py`
  - Export all new indicators
  - Verify all indicators import correctly

  **Must NOT do**:
  - Don't modify existing exports

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Simple export update
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1-6)

  **References**:
  - `trading/indicators/__init__.py` - Current exports

  **Acceptance Criteria**:
  - [ ] All indicators import from trading.indicators
  - [ ] No import errors

  **Commit**: YES
  - Message: `feat(indicators): export new indicators`
  - Files: trading/indicators/__init__.py

---

### Wave 2: FOREX Strategies

- [ ] 7. Holy Grail Strategy Implementation

  **What to do**:
  - Create `trading/strategy/templates/forex/holy_grail.py`
  - Implement strategy based on research:
    - Indicators: EMA(20), ADX(14), RSI(14)
    - Entry BUY: Uptrend by EMA; ADX rises above 30; breakdown of EMA with rollback
    - Entry SELL: Bearish trend by EMA; ADX grows above 30; breakdown from bottom up with rollback
    - Exit: ADX line reversal down from upper zone
  - Timeframe: H4 minimum
  - Support major pairs: EUR/USD, GBP/USD, USD/JPY

  **Must NOT do**:
  - Don't hardcode symbols (make configurable)

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Complex multi-indicator strategy
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 7-11)
  - **Blocks**: Task 12
  - **Blocked By**: Tasks 1-4

  **References**:
  - Research: Holy Grail strategy from ForexTester
  - `trading/strategy/templates/trend_following.py` - Pattern to follow

  **Acceptance Criteria**:
  - [ ] HolyGrailStrategy class inherits from StrategyTemplate
  - [ ] entry_conditions() implements all 3 conditions
  - [ ] exit_conditions() handles ADX reversal
  - [ ] Configuration supports all parameters

  **QA Scenarios**:

  ```
  Scenario: Holy Grail signal generation
    Tool: Bash
    Preconditions: Python with strategy framework
    Steps:
      1. Create test OHLCV data with uptrend
      2. Add ADX rising above 30
      3. Add EMA alignment
      4. Run strategy.get_signals()
      5. Verify BUY signal generated
    Expected Result: BUY signal with correct levels
    Evidence: .sisyphus/evidence/task-7-holygrail-test.txt
  ```

  **Commit**: YES
  - Message: `feat(strategy): add Holy Grail FOREX strategy`
  - Files: trading/strategy/templates/forex/holy_grail.py

---

- [ ] 8. Momentum Elder Strategy Implementation

  **What to do**:
  - Create `trading/strategy/templates/forex/momentum_elder.py`
  - Implement strategy based on research:
    - Indicators: EMA(19), Momentum(18, close, 100)
    - Entry BUY: Closing above EMA(19), Momentum crosses 100 from bottom up
    - Entry SELL: Closing below EMA(19), Momentum crosses 100 from top to bottom
  - Timeframe: H1 minimum

  **Must NOT do**:
  - Don't use wrong Momentum parameters

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Momentum-based strategy
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 7-11)

  **References**:
  - Research: Momentum Elder strategy from ForexTester
  - `trading/strategy/templates/trend_following.py` - Pattern reference

  **Acceptance Criteria**:
  - [ ] MomentumElderStrategy class inherits from StrategyTemplate
  - [ ] EMA(19) and Momentum(18) calculated correctly
  - [ ] Crossover detection works
  - [ ] Signals match expected format

  **QA Scenarios**:

  ```
  Scenario: Momentum Elder crossover detection
    Tool: Bash
    Preconditions: Python with strategy framework
    Steps:
      1. Create test data with Momentum crossing 100 up
      2. Price closes above EMA(19)
      3. Run strategy.get_signals()
      4. Verify BUY signal
      5. Test opposite case (SELL)
    Expected Result: Correct signals for both directions
    Evidence: .sisyphus/evidence/task-8-momentum-test.txt
  ```

  **Commit**: YES
  - Message: `feat(strategy): add Momentum Elder FOREX strategy`
  - Files: trading/strategy/templates/forex/momentum_elder.py

---

- [ ] 9. Kumo Breakout Strategy Implementation

  **What to do**:
  - Create `trading/strategy/templates/forex/kumo_breakout.py`
  - Implement strategy based on research:
    - Indicators: Ichimoku (8, 29, 34) - Kumo zone only, Awesome Oscillator
    - Timeframe: M15 for entry, H1+ for tracking
    - Entry BUY: Breakdown of upper Kumo boundary; AO histogram reversal from bottom up
    - Entry SELL: Breakdown of lower Kumo boundary; AO histogram reversal from top to bottom

  **Must NOT do**:
  - Don't use standard Ichimoku params without forex optimization

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Ichimoku-based strategy
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 7-11)

  **References**:
  - Research: Kumo Breakout strategy from ForexTester
  - Task 4: Ichimoku indicator

  **Acceptance Criteria**:
  - [ ] KumoBreakoutStrategy class inherits from StrategyTemplate
  - [ ] Kumo boundary detection works
  - [ ] AO confirmation integrated
  - [ ] Forex-optimized parameters (8,29,34) used

  **QA Scenarios**:

  ```
  Scenario: Kumo Breakout signal generation
    Tool: Bash
    Preconditions: Python with strategy framework
    Steps:
      1. Create test data with price below Kumo
      2. Price breaks above upper Kumo boundary
      3. Add AO histogram reversal
      4. Run strategy.get_signals()
      5. Verify BUY signal
    Expected Result: BUY signal at Kumo breakout
    Evidence: .sisyphus/evidence/task-9-kumo-test.txt
  ```

  **Commit**: YES
  - Message: `feat(strategy): add Kumo Breakout FOREX strategy`
  - Files: trading/strategy/templates/forex/kumo_breakout.py

---

- [ ] 10. FOREX Risk Manager

  **What to do**:
  - Create `trading/risk/forex_manager.py`
  - Implement FOREX-specific risk management:
    - Pip-based position sizing
    - Correlation risk (e.g., EUR/USD, GBP/USD exposure)
    - Spread check before entry
    - Maximum daily/weekly loss limits
    - Leverage warnings

  **Must NOT do**:
  - Don't use stock-based position sizing

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Risk management following existing patterns
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 7-11)

  **References**:
  - `trading/risk/manager.py` - Existing risk manager
  - Research: 1-2% per trade risk rule

  **Acceptance Criteria**:
  - [ ] FOREXRiskManager class
  - [ ] calculate_position_size() works with pips
  - [ ] correlation_check() implemented
  - [ ] spread_check() implemented

  **QA Scenarios**:

  ```
  Scenario: FOREX position sizing
    Tool: Bash
    Preconditions: Python with risk framework
    Steps:
      1. Create FOREXRiskManager instance
      2. Test position size calculation with pips
      3. Verify correlation check works
      4. Verify spread check works
    Expected Result: Correct position sizes for FOREX
    Evidence: .sisyphus/evidence/task-10-forex-risk-test.txt
  ```

  **Commit**: YES
  - Message: `feat(risk): add FOREX risk manager`
  - Files: trading/risk/forex_manager.py

---

- [ ] 11. FOREX Backtest Engine

  **What to do**:
  - Create `trading/backtest/forex_engine.py`
  - Adapt BacktestEngine for FOREX:
    - Support multiple timeframes (H1, H4, D1)
    - FOREX-specific metrics (pips, spread cost)
    - Correlation-adjusted returns
    - Support major pairs

  **Must NOT do**:
  - Don't break existing BacktestEngine interface

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Backtest engine specialization
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 7-11)
  - **Blocks**: Task 12

  **References**:
  - `trading/backtest/engine.py` - Existing engine
  - Research: FOREX-specific metrics requirements

  **Acceptance Criteria**:
  - [ ] ForexBacktestEngine class
  - [ ] run() method works with FOREX strategies
  - [ ] Metrics include pips, spread-adjusted returns
  - [ ] Integration with broker connectors

  **QA Scenarios**:

  ```
  Scenario: FOREX backtest execution
    Tool: Bash
    Preconditions: Python with backtest framework
    Steps:
      1. Create ForexBacktestEngine instance
      2. Load historical OHLCV data
      3. Run backtest for Holy Grail strategy
      4. Verify metrics output (pips, win rate)
    Expected Result: Complete backtest with FOREX metrics
    Evidence: .sisyphus/evidence/task-11-forex-backtest-test.txt
  ```

  **Commit**: YES
  - Message: `feat(backtest): add FOREX backtest engine`
  - Files: trading/backtest/forex_engine.py

---

### Wave 3: CRYPTO Strategies

- [ ] 12. On-Chain Data Module

  **What to do**:
  - Create `trading/data/onchain.py`
  - Implement on-chain data fetching:
    - Exchange inflows/outflows
    - Whale transactions
    - MVRV ratio calculation
    - Network value to transactions (NVT)
  - Support APIs: Glassnode, CryptoQuant (mock for now)

  **Must NOT do**:
  - Don't make real API calls without credentials

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: New data domain for crypto
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 12-17)
  - **Blocks**: Task 14
  - **Blocked By**: Tasks 7-11

  **References**:
  - Research: On-chain metrics for crypto strategies
  - `trading/data/yahoo.py` - Data module pattern

  **Acceptance Criteria**:
  - [ ] OnChainData class
  - [ ] Exchange flow methods
  - [ ] Whale transaction detection
  - [ ] MVRV calculation

  **Commit**: YES
  - Message: `feat(data): add on-chain data module`
  - Files: trading/data/onchain.py

---

- [ ] 13. Funding Rate Data Module

  **What to do**:
  - Create `trading/data/funding.py`
  - Implement funding rate data:
    - Fetch funding rates from exchanges
    - Calculate persistence (consecutive days elevated)
    - Identify crowded positioning signals
    - Support major pairs: BTC/USD, ETH/USD

  **Must NOT do**:
  - Don't hardcode funding rates

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Data module implementation
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 12-17)

  **References**:
  - Research: 14+ consecutive days elevated = warning signal
  - `trading/data/storage.py` - Data storage pattern

  **Acceptance Criteria**:
  - [ ] FundingRateData class
  - [ ] fetch_funding_rates() method
  - [ ] calculate_persistence() method
  - [ ] Warning threshold detection (14 days)

  **Commit**: YES
  - Message: `feat(data): add funding rate data module`
  - Files: trading/data/funding.py

---

- [ ] 14. Funding Rate Reversal Strategy

  **What to do**:
  - Create `trading/strategy/templates/crypto/funding_reversal.py`
  - Implement strategy based on research:
    - Indicators: Funding rate persistence (>14 days = reversal signal)
    - Timeframe: Daily-Weekly
    - Entry: Short when funding persists elevated; Buy when funding negative persistence
    - Exit: Funding normalization or profit target

  **Must NOT do**:
  - Don't enter without funding confirmation

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Unique crypto-specific strategy
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 12-17)
  - **Blocks**: Task 16

  **References**:
  - Research: Funding rate persistence leads to reversals
  - Task 13: Funding rate data module

  **Acceptance Criteria**:
  - [ ] FundingReversalStrategy class
  - [ ] Persistent funding detection
  - [ ] Reversal signal generation
  - [ ] Integration with funding data

  **QA Scenarios**:

  ```
  Scenario: Funding reversal signal
    Tool: Bash
    Preconditions: Python with strategy framework
    Steps:
      1. Create test data with 14+ days elevated funding
      2. Run strategy.get_signals()
      3. Verify SHORT signal generated
    Expected Result: SHORT signal at funding reversal point
    Evidence: .sisyphus/evidence/task-14-funding-test.txt
  ```

  **Commit**: YES
  - Message: `feat(strategy): add Funding Rate Reversal CRYPTO strategy`
  - Files: trading/strategy/templates/crypto/funding_reversal.py

---

- [ ] 15. Volume Momentum Strategy

  **What to do**:
  - Create `trading/strategy/templates/crypto/volume_momentum.py`
  - Implement strategy based on research:
    - Indicators: MACD(12,26,9), RSI(60-80), Volume 150-200%+ of average
    - Timeframe: 5M-15M scalping
    - Entry: Volume surge + momentum confirmation
    - Exit: SL hit or TP hit

  **Must NOT do**:
  - Don't enter without volume confirmation

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: High-frequency crypto scalping
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 12-17)

  **References**:
  - Research: Volume confirmation mandatory for crypto
  - `trading/strategy/templates/scalping.py` - Scalping pattern

  **Acceptance Criteria**:
  - [ ] VolumeMomentumStrategy class
  - [ ] Volume surge detection (150-200%)
  - [ ] RSI momentum confirmation (60-80)
  - [ ] MACD alignment

  **QA Scenarios**:

  ```
  Scenario: Volume momentum signal
    Tool: Bash
    Preconditions: Python with strategy framework
    Steps:
      1. Create test data with volume spike (200%)
      2. Add RSI in momentum range (60-80)
      3. Run strategy.get_signals()
      4. Verify signal generated
    Expected Result: Signal with volume confirmation
    Evidence: .sisyphus/evidence/task-15-volume-test.txt
  ```

  **Commit**: YES
  - Message: `feat(strategy): add Volume Momentum CRYPTO strategy`
  - Files: trading/strategy/templates/crypto/volume_momentum.py

---

- [ ] 16. CRYPTO Risk Manager

  **What to do**:
  - Create `trading/risk/crypto_manager.py`
  - Implement CRYPTO-specific risk management:
    - Higher volatility position sizing (smaller sizes)
    - Wider stop losses (1.5-2x traditional)
    - Leverage limits per volatility regime
    - Liquidation prevention (max 50% leverage in high vol)
    - Daily/weekly loss limits (lower than FOREX)

  **Must NOT do**:
  - Don't use traditional stop widths for crypto

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Risk management following existing patterns
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 12-17)
  - **Blocks**: Task 17

  **References**:
  - Research: Crypto requires 1.5-2x wider stops
  - `trading/risk/forex_manager.py` - FOREX risk pattern

  **Acceptance Criteria**:
  - [ ] CRYPTORiskManager class
  - [ ] Volatility-adjusted position sizing
  - [ ] Wider stop implementation
  - [ ] Liquidation prevention

  **Commit**: YES
  - Message: `feat(risk): add CRYPTO risk manager`
  - Files: trading/risk/crypto_manager.py

---

- [ ] 17. CRYPTO Backtest Engine

  **What to do**:
  - Create `trading/backtest/crypto_engine.py`
  - Adapt BacktestEngine for CRYPTO:
    - Support 24/7 trading
    - CRYPTO-specific metrics (funding-adjusted returns)
    - Volatility-adjusted performance
    - Integration with CCXT broker

  **Must NOT do**:
  - Don't break existing BacktestEngine interface

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Backtest engine specialization
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 12-17)
  - **Blocks**: Task 18

  **References**:
  - `trading/backtest/forex_engine.py` - FOREX backtest pattern
  - `trading/brokers/ccxt/connector.py` - CCXT integration

  **Acceptance Criteria**:
  - [ ] CryptoBacktestEngine class
  - [ ] run() method works with CRYPTO strategies
  - [ ] Metrics include funding-adjusted returns
  - [ ] Integration with CCXT broker

  **Commit**: YES
  - Message: `feat(backtest): add CRYPTO backtest engine`
  - Files: trading/backtest/crypto_engine.py

---

### Wave 4: STOCKS Strategies ✅ COMPLETE

- [x] 18. Golden Cross Screener Strategy

  **What to do**:
  - Create `trading/strategy/templates/stocks/golden_cross.py`
  - Implement strategy based on research:
    - Indicators: 50/200 SMA crossover
    - Timeframe: Daily-Weekly
    - Entry BUY: 50 SMA crosses above 200 SMA (golden cross)
    - Entry SELL: 50 SMA crosses below 200 SMA (death cross)
    - Exit: Opposite crossover or trailing stop

  **Must NOT do**:
  - Don't use wrong SMA periods

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Classic stock strategy
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Tasks 18-21)
  - **Blocks**: Task 22

  **References**:
  - Research: Golden Cross is key stock signal
  - `trading/strategy/templates/trend_following.py` - Trend pattern

  **Acceptance Criteria**:
  - [ ] GoldenCrossStrategy class
  - [ ] 50/200 SMA crossover detection
  - [ ] Bullish/bearish signal generation
  - [ ] Support for multiple stocks

  **QA Scenarios**:

  ```
  Scenario: Golden Cross detection
    Tool: Bash
    Preconditions: Python with strategy framework
    Steps:
      1. Create test data with 50 SMA crossing above 200 SMA
      2. Run strategy.get_signals()
      3. Verify BUY signal
      4. Test opposite (death cross -> SELL)
    Expected Result: Correct signals for both crossovers
    Evidence: .sisyphus/evidence/task-18-golden-test.txt
  ```

  **Commit**: YES
  - Message: `feat(strategy): add Golden Cross STOCKS strategy`
  - Files: trading/strategy/templates/stocks/golden_cross.py

---

- [x] 19. RSI Divergence Detector Strategy

  **What to do**:
  - Create `trading/strategy/templates/stocks/rsi_divergence.py`
  - Implement strategy based on research:
    - Indicators: RSI(14) with divergence detection
    - Timeframe: Daily
    - Entry BUY: Price makes lower low, RSI makes higher low (bullish divergence)
    - Entry SELL: Price makes higher high, RSI makes lower high (bearish divergence)
    - Exit: RSI reaches 50 or opposite signal

  **Must NOT do**:
  - Don't confuse regular with hidden divergence

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Divergence detection is complex
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Tasks 18-21)
  - **Blocks**: Task 22

  **References**:
  - Research: RSI divergence is key mean reversion signal
  - `trading/indicators/rsi.py` - RSI implementation

  **Acceptance Criteria**:
  - [ ] RSIDivergenceStrategy class
  - [ ] Bullish divergence detection
  - [ ] Bearish divergence detection
  - [ ] RSI levels correctly identified

  **QA Scenarios**:

  ```
  Scenario: RSI divergence detection
    Tool: Bash
    Preconditions: Python with strategy framework
    Steps:
      1. Create test data with price lower low + RSI higher low
      2. Run strategy.get_signals()
      3. Verify BUY signal (bullish divergence)
      4. Test bearish case
    Expected Result: Correct divergence signals
    Evidence: .sisyphus/evidence/task-19-rsi-test.txt
  ```

  **Commit**: YES
  - Message: `feat(strategy): add RSI Divergence STOCKS strategy`
  - Files: trading/strategy/templates/stocks/rsi_divergence.py

---

- [x] 20. STOCKS Risk Manager

  **What to do**:
  - Create `trading/risk/stock_manager.py`
  - Implement STOCKS-specific risk management:
    - Position limits (max 5-10% per stock)
    - Sector exposure limits (max 25-30% per sector)
    - Earnings event risk management
    - Correlation risk (market beta)
    - Dividend/earnings calendar awareness

  **Must NOT do**:
  - Don't use FOREX-style position sizing

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Risk management following existing patterns
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Tasks 18-21)
  - **Blocks**: Task 21

  **References**:
  - Research: Max 5-10% per stock, 25-30% sector limit
  - `trading/risk/forex_manager.py` - FOREX risk pattern

  **Acceptance Criteria**:
  - [ ] STOCKSRiskManager class
  - [ ] Position limit enforcement
  - [ ] Sector exposure check
  - [ ] Correlation risk assessment

  **Commit**: YES
  - Message: `feat(risk): add STOCKS risk manager`
  - Files: trading/risk/stock_manager.py

---

- [x] 21. STOCKS Backtest Engine

  **What to do**:
  - Create `trading/backtest/stock_engine.py`
  - Adapt BacktestEngine for STOCKS:
    - Support daily/weekly timeframes
    - STOCKS-specific metrics (alpha, beta, Sharpe ratio)
    - Sector-adjusted returns
    - Support multiple stock screening

  **Must NOT do**:
  - Don't break existing BacktestEngine interface

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Backtest engine specialization
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Tasks 18-21)
  - **Blocks**: Task 22

  **References**:
  - `trading/backtest/forex_engine.py` - FOREX backtest pattern

  **Acceptance Criteria**:
  - [ ] StockBacktestEngine class
  - [ ] run() method works with STOCKS strategies
  - [ ] Metrics include alpha, beta, Sharpe
  - [ ] Sector-adjusted performance

  **Commit**: YES
  - Message: `feat(backtest): add STOCKS backtest engine`
  - Files: trading/backtest/stock_engine.py

---

### Wave 5: COMMODITY Strategies ✅ COMPLETE

- [x] 22. Gold-Silver Ratio Strategy

  **What to do**:
  - Create `trading/strategy/templates/commodities/gold_silver_ratio.py`
  - Implement strategy based on research:
    - Concept: Pair trade between XAUUSD and XAGUSD
    - Entry: Ratio extreme (above 80 = short gold/buy silver, below 70 = buy gold/short silver)
    - Exit: Ratio returns to mean (75)
    - Timeframe: Daily-Weekly

  **Must NOT do**:
  - Don't trade individual metals without ratio context

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Pair trade strategy
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 5 (with Tasks 22-25)
  - **Blocks**: Task 26
  - **Blocked By**: Tasks 18-21

  **References**:
  - Research: Gold-Silver ratio is key commodities signal
  - `trading/strategy/tradfi/commodities/xauusd_asia_7c_breakout/strategy.py` - Existing commodities pattern

  **Acceptance Criteria**:
  - [ ] GoldSilverRatioStrategy class
  - [ ] Ratio calculation (XAUUSD / XAGUSD)
  - [ ] Mean reversion signals
  - [ ] Pair trade execution

  **QA Scenarios**:

  ```
  Scenario: Gold-Silver ratio signal
    Tool: Bash
    Preconditions: Python with strategy framework
    Steps:
      1. Create test data with ratio > 80
      2. Run strategy.get_signals()
      3. Verify BUY SILVER / SHORT GOLD signal
      4. Test opposite case (ratio < 70)
    Expected Result: Correct pair trade signals
    Evidence: .sisyphus/evidence/task-22-ratio-test.txt
  ```

  **Commit**: YES
  - Message: `feat(strategy): add Gold-Silver Ratio COMMODITY strategy`
  - Files: trading/strategy/templates/commodities/gold_silver_ratio.py

---

- [x] 23. Seasonal Pattern Strategy

  **What to do**:
  - Create `trading/strategy/templates/commodities/seasonal.py`
  - Implement strategy based on research:
    - Concept: Monthly/quarterly recurring patterns
    - Indicators: Seasonal averages, historical performance
    - Examples: Gold historically strong in Jan/Sept, Oil in Q4
    - Timeframe: Weekly-Monthly

  **Must NOT do**:
  - Don't use seasonal without confirmation

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Seasonal analysis is specialized
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 5 (with Tasks 22-25)

  **References**:
  - Research: Seasonality affects commodities significantly
  - `trading/strategy/base.py` - Strategy pattern

  **Acceptance Criteria**:
  - [ ] SeasonalStrategy class
  - [ ] Seasonal pattern database
  - [ ] Signal generation based on seasonality
  - [ ] Confidence scoring

  **QA Scenarios**:

  ```
  Scenario: Seasonal pattern signal
    Tool: Bash
    Preconditions: Python with strategy framework
    Steps:
      1. Create test data for September
      2. Add historical September strength
      3. Run strategy.get_signals()
      4. Verify GOLD BUY signal (historical pattern)
    Expected Result: Seasonal signal matches pattern
    Evidence: .sisyphus/evidence/task-23-seasonal-test.txt
  ```

  **Commit**: YES
  - Message: `feat(strategy): add Seasonal Pattern COMMODITY strategy`
  - Files: trading/strategy/templates/commodities/seasonal.py

---

- [x] 24. COMMODITY Risk Manager

  **What to do**:
  - Create `trading/risk/commodity_manager.py`
  - Implement COMMODITY-specific risk management:
    - Contract-specific position limits
    - Contango/backwardation awareness (futures)
    - Seasonality risk (unusual patterns)
    - Supply/demand event risk
    - Currency exposure (commodities priced in USD)

  **Must NOT do**:
  - Don't ignore futures mechanics

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Risk management following existing patterns
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 5 (with Tasks 22-25)
  - **Blocks**: Task 25

  **References**:
  - Research: Contango/backwardation affects roll returns
  - `trading/risk/forex_manager.py` - FOREX risk pattern

  **Acceptance Criteria**:
  - [ ] COMMODITYRiskManager class
  - [ ] Contract size awareness
  - [ ] Contango impact assessment
  - [ ] Seasonal risk check

  **Commit**: YES
  - Message: `feat(risk): add COMMODITY risk manager`
  - Files: trading/risk/commodity_manager.py

---

- [x] 25. COMMODITY Backtest Engine

  **What to do**:
  - Create `trading/backtest/commodity_engine.py`
  - Adapt BacktestEngine for COMMODITIES:
    - Support futures contracts
    - COMMODITY-specific metrics (contango-adjusted returns)
    - Seasonality-adjusted performance
    - Integration with MT5 broker

  **Must NOT do**:
  - Don't break existing BacktestEngine interface

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Backtest engine specialization
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 5 (with Tasks 22-25)
  - **Blocks**: Task 26

  **References**:
  - `trading/backtest/forex_engine.py` - FOREX backtest pattern
  - `trading/brokers/mt5/connector.py` - MT5 integration

  **Acceptance Criteria**:
  - [ ] CommodityBacktestEngine class
  - [ ] run() method works with COMMODITY strategies
  - [ ] Metrics include contango-adjusted returns
  - [ ] Integration with MT5 broker

  **Commit**: YES
  - Message: `feat(backtest): add COMMODITY backtest engine`
  - Files: trading/backtest/commodity_engine.py

---

### Wave 6: Integration & Documentation ✅ COMPLETE

- [x] 26. Strategy Registry

  **What to do**:
  - Create `trading/strategy/registry.py`
  - Implement strategy registration system
  - Support strategy discovery by market type
  - Factory pattern for strategy creation

  **Must NOT do**:
  - Don't break existing strategy loading

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Registry implementation
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 6 (with Tasks 26-30)
  - **Blocked By**: Tasks 22-25

  **References**:
  - `trading/brokers/factory.py` - Factory pattern reference

  **Acceptance Criteria**:
  - [ ] StrategyRegistry class
  - [ ] Register/get methods
  - [ ] Market type filtering
  - [ ] All strategies discoverable

  **Commit**: YES
  - Message: `feat(strategy): add strategy registry`
  - Files: trading/strategy/registry.py

---

- [x] 27. Update Main SKILL.md

  **What to do**:
  - Update `trading/SKILL.md`
  - Document all new strategies
  - Include market type organization
  - Add command references

  **Must NOT do**:
  - Don't duplicate documentation

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Documentation update
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 6 (with Tasks 26-30)

  **References**:
  - `trading/SKILL.md` - Current documentation

  **Acceptance Criteria**:
  - [ ] All strategies documented
  - [ ] Commands for each strategy
  - [ ] Market type organization

  **Commit**: YES
  - Message: `docs(trading): update SKILL.md with new strategies`
  - Files: trading/SKILL.md

---

- [x] 28. Update SKILL_INDEX.json

  **What to do**:
  - Add all new skills to `SKILL_INDEX.json`
  - FOREX: holy-grail, momentum-elder, kumo-breakout
  - CRYPTO: funding-reversal, volume-momentum
  - STOCKS: golden-cross, rsi-divergence
  - COMMODITY: gold-silver-ratio, seasonal-pattern

  **Must NOT do**:
  - Don't miss any skill entries

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: JSON update
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 6 (with Tasks 26-30)

  **References**:
  - `SKILL_INDEX.json` - Current entries

  **Acceptance Criteria**:
  - [ ] All 10 new strategies in index
  - [ ] Correct paths and categories

  **Commit**: YES
  - Message: `feat(skills): add new strategy skills to index`
  - Files: SKILL_INDEX.json

---

- [x] 29. Create Strategy README

  **What to do**:
  - Create `trading/strategy/README.md`
  - Document all strategy templates
  - Include examples for each market
  - Add performance metrics summary

  **Must NOT do**:
  - Don't include credentials

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Documentation creation
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 6 (with Tasks 26-30)

  **References**:
  - `trading/README.md` - Documentation format

  **Acceptance Criteria**:
  - [ ] All strategies documented
  - [ ] Examples included
  - [ ] Clear structure

  **Commit**: YES
  - Message: `docs(strategy): create strategy README`
  - Files: trading/strategy/README.md

---

- [x] 30. Integration Tests

  **What to do**:
  - Create `trading/tests/test_integration/test_strategies.py`
  - Test all strategies with backtest engines
  - Verify broker integration works
  - Test risk management application

  **Must NOT do**:
  - Don't use real broker accounts

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Integration verification
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 6 (with Tasks 26-30)

  **References**:
  - `trading/tests/test_brokers/` - Broker tests

  **Acceptance Criteria**:
  - [ ] All strategies tested
  - [ ] Backtest engines verified
  - [ ] Risk managers tested
  - [ ] pytest runs successfully

  **Commit**: YES
  - Message: `test(integration): add strategy integration tests`
  - Files: trading/tests/test_integration/test_strategies.py

---

## Final Verification Wave

- [ ] F1. Plan Compliance Audit — `oracle`

  Read the plan end-to-end. For each "Must Have": verify implementation exists (read file, curl endpoint, run command). For each "Must NOT Have": search codebase for forbidden patterns — reject with file:line if found. Check evidence files exist in .sisyphus/evidence/. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [ ] F2. Code Quality Review — `unspecified-high`

  Run `tsc --noEmit` + linter + `bun test`. Review all changed files for: `as any`/`@ts-ignore`, empty catches, console.log in prod, commented-out code, unused imports. Check AI slop: excessive comments, over-abstraction, generic names (data/result/item/temp).
  Output: `Build [PASS/FAIL] | Lint [PASS/FAIL] | Tests [N pass/N fail] | Files [N clean/N issues] | VERDICT`

- [ ] F3. Real Manual QA — `unspecified-high` (+ `playwright` skill if UI)

  Start from clean state. Execute EVERY QA scenario from EVERY task — follow exact steps, capture evidence. Test cross-task integration (features working together, not isolation). Test edge cases: empty state, invalid input, rapid actions. Save to `.sisyphus/evidence/final-qa/`.
  Output: `Scenarios [N/N pass] | Integration [N/N] | Edge Cases [N tested] | VERDICT`

- [ ] F4. Scope Fidelity Check — `deep`

  For each task: read "What to do", read actual diff (git log/diff). Verify 1:1 — everything in spec was built (no missing), nothing beyond spec was built (no creep). Check "Must NOT do" compliance. Detect cross-task contamination: Task N touching Task M's files. Flag unaccounted changes.
  Output: `Tasks [N/N compliant] | Contamination [CLEAN/N issues] | Unaccounted [CLEAN/N files] | VERDICT`

---

## Commit Strategy

- **1-6**: `feat(indicators): add ADX, Stochastic, ATR, Ichimoku`
- **7-11**: `feat(strategy): add FOREX strategies (holy-grail, momentum-elder, kumo-breakout)`
- **12-17**: `feat(strategy): add CRYPTO strategies (funding-reversal, volume-momentum)`
- **18-21**: `feat(strategy): add STOCKS strategies (golden-cross, rsi-divergence)`
- **22-25**: `feat(strategy): add COMMODITY strategies (gold-silver-ratio, seasonal)`
- **26-30**: `feat(integration): add registry, docs, tests`

---

## Success Criteria

### Verification Commands
```bash
# Import all new indicators
python -c "from trading.indicators import ADX, Stochastic, ATR, Ichimoku; print('Indicators OK')"

# Import all new strategies
python -c "from trading.strategy.templates.forex import HolyGrailStrategy, MomentumElderStrategy, KumoBreakoutStrategy; from trading.strategy.templates.crypto import FundingReversalStrategy, VolumeMomentumStrategy; from trading.strategy.templates.stocks import GoldenCrossStrategy, RSIDivergenceStrategy; from trading.strategy.templates.commodities import GoldSilverRatioStrategy, SeasonalStrategy; print('Strategies OK')"

# Run tests
pytest trading/tests/test_indicators/ -v
pytest trading/tests/test_strategy/ -v
```

### Final Checklist
- [ ] All 30 tasks completed
- [ ] All strategies import and run
- [ ] All backtest engines functional
- [ ] All risk managers operational
- [ ] Documentation complete
- [ ] SKILL_INDEX updated
