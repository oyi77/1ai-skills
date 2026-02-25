!/bin/bash
# OH-MY-OPENCODE INITIALIZATION - Trading Strategy Research

# Start oh-my-opencode in background if not already running
cd /home/openclaw/.openclaw/workspace/skills/1ai-skills/trading

# Check if opencode is running
if ! pgrep -x "opencode" > /dev/null; then
    echo "Starting oh-my-opencode..."
    # Run in background with logging
    /home/openclaw/.opencode/bin/opencode > /tmp/opencode.log 2>&1 &
    OPENCODE_PID=$!

    # Wait for initialization (10 seconds)
    sleep 10

    echo "oh-my-opencode started with PID: $OPENCODE_PID"
    echo "Logs: /tmp/opencode.log"
else
    echo "oh-my-opencode already running"
fi

# Create prompt file for strategy research
cat > /tmp/research_prompt.txt << 'EOF'
# MISSION: Optimize Trading Strategies for BerkahKarya Quant Fund

## Goal
Research and optimize 4 trading strategies to achieve:
- Win Rate ≥ 55%
- Net PNL Positive
- Max Drawdown ≤ 20%

## Strategies to Optimize

1. Holy Grail (GBPUSD)
   Current: WR 33.3%, PNL -$0.39
   Issues: Entry timing wrong, EMA too slow

2. Kumo Breakout (XAUUSD)
   Current: WR 0.0%, PNL $0.00 (0 trades)
   Issues: Cloud filter too restrictive, no valid breakouts

3. Momentum Elder (XAUUSD)
   Current: WR 22.2%, PNL -$6.52
   Issues: Too much noise, R/R too low (1:1)

4. Volume Momentum (XAUUSD)
   Current: WR 0.0%, PNL -$1.00 (only 1 trade)
   Issues: Volume filter too high, not enough trades

## Research Tasks

### Task 1: Holy Grail Optimization (HIGH PRIORITY)

Oracle - System Design:
- Analyze why current Holy Grail fails (33.3% WR)
- Design new entry logic that reduces false signals
- Consider: Previous candle trend, Multi-timeframe confirmation (H1+H4), Volume spike at entry

Hephaestus - Parameter Grid Search:
- Test EMA periods: [5, 10, 15, 20, 25, 30]
- Test ADX periods: [7, 14, 21, 28]
- Test ADX thresholds: [15, 20, 25, 30, 35, 40]
- Test Timeframes: [H1, H4]
- Backtest 2025-01-01 to 2025-12-31
- Target: Find configuration with WR ≥ 50%

Librarian - Research Profitable EMA Strategies:
- Search for proven EMA-based strategies (TradingView, ForexFactory)
- Focus on GBPUSD pairs (GBP/USD, GBP/JPY, GBP/EUR)
- Look for patterns: EMA crossover with trend confirmation
- Find documented parameters that work

Explore - Quick Backtest Script:
- Create simplified backtest script for Holy Grail
- Test 10-20 parameter combinations
- Use yfinance GBPUSD=X for data
- Output: WR and PNL for each configuration
- Goal: Find "quick win" with WR ≥ 45%

### Task 2: Kumo Breakout Fix (HIGH PRIORITY)

Oracle - Redesign Cloud Breakout Logic:
- Current: 0 trades - cloud filter too restrictive
- New approach: Require price breaks cloud AND previous close was outside cloud
- Alternative: Only trade when cloud is expanding (Senkou A > Senkou B)
- Consider: Volume confirmation (only trade if volume > average)

Hephaestus - Parameter Optimization:
- Test Tenkan periods: [9, 18, 26, 34, 52]
- Test Kijun periods: [26, 52, 78]
- Test Senkou B periods: [26, 52, 78]
- Test Cloud thickness filter: [5, 10, 15 pips minimum]
- Test Timeframes: [H1, H4, D1]
- Backtest 2025-01-01 to 2025-12-31
- Target: At least 100 trades, WR ≥ 50%

Librarian - Ichimoku Best Practices:
- Research successful Ichimoku strategies (TK Cross, Kumo Twists)
- Look for optimal settings for XAUUSD (gold is trending)
- Focus on breakout vs pullback strategies
- Find timeframes where Ichimoku works best

Explore - Data Analysis:
- Analyze XAUUSD 2025 price data
- Check Ichimoku cloud characteristics (thickness, slope)
- Find periods where cloud produces valid breakouts
- Visualize if possible (matplotlib charts)

### Task 3: Momentum Elder Noise Reduction (MEDIUM PRIORITY)

Oracle - Redesign Momentum Filter:
- Current: 22.2% WR - too much noise
- New approach: Add ADX trend filter (only trade if ADX > 25 trending)
- Alternative: Use Elder Ray + RSI (confirm with oversold/overbought zones)
- Consider: Multi-timeframe (H1 momentum must align with H4 trend)

Hephaestus - Risk/Reward Optimization:
- Current: 1:1 R/R (entry close to SL)
- Test R/R ratios: [1.5:1, 2:1, 2.5:1, 3:1]
- Test Stop Loss methods: Fixed pips, ATR-based, Structure-based (previous low)
- Target: PF ≥ 1.5 (more wins bigger than losses)

Librarian - Momentum System Research:
- Research Elder Ray optimization techniques
- Look for: Elder Force Index, Elder Impulse system
- Find how professionals trade with Elder Ray
- Look for combinations with ADX, RSI, MACD

Explore - Quick Backtests:
- Test Elder Ray + ADX(25) combinations
- Test different R/R ratios
- Test with/without trend filters
- Goal: Find configuration with WR ≥ 40%

### Task 4: Volume Momentum - Increase Trade Frequency (MEDIUM PRIORITY)

Oracle - Analyze XAUUSD Volume:
- Current: 0.0% WR but only 1 trade - not enough data
- Research: Does XAUUSD have significant volume spikes?
- Check: Volume distribution, daily/weekly patterns, time-of-day effects
- Alternative: Use volume as confirmation filter rather than entry trigger

Hephaestus - Parameter Optimization:
- Test Volume ratio thresholds: [0.8, 1.0, 1.2, 1.5]
- Test Volume average periods: [10, 20, 50, 100] candles
- Test Volume spike multipliers: [1.5, 2.0, 3.0, 5.0]
- Test Momentum lookback: [3, 5, 10, 15] bars
- Target: 50-200 trades per year, WR ≥ 50%

Librarian - Volume-Based Trading:
- Research: Volume Spread Analysis (VSA) techniques
- Look for: Volume breakout strategies, Volume exhaustion patterns
- Find: Volume-based entry filters that work for gold/XAUUSD
- Check: Wyckoff volume patterns (accumulation, distribution, markup)

Explore - Data Analysis & Backtest:
- Download XAUUSD data with volume (yfinance provides this)
- Analyze volume characteristics: mean, std, percentiles
- Test volume threshold combinations
- Backtest different strategies
- Goal: Find configuration that generates 50+ trades with WR ≥ 50%

## Deliverables

For each strategy, produce:

1. Optimized Strategy Script
   - File: strategy_name_optimized.py
   - Contains: backtest() method with optimal parameters
   - Can be run: python strategy_optimized.py backtest 2025-01-01 2025-12-31

2. Backtest Results
   - File: strategy_name_results.json
   - Contains: WR, PNL, PF, trades, max DD, etc.
   - Expected: WR ≥ 55%, PNL positive

3. Performance Report
   - Summary of optimization process
   - Comparison of tested configurations
   - Final selected parameters with reasoning

## Research Methodology

1. **Hypothesis Generation**
   - Oracle proposes entry/exit logic improvements
   - Based on market mechanics and strategy principles

2. **Parameter Exploration**
   - Hephaestus grid searches parameter space systematically
   - Uses backtest engine to evaluate each configuration
   - Finds optimal parameters for each hypothesis

3. **Knowledge Discovery**
   - Librarian researches existing profitable strategies
   - Find proven techniques and parameters
   - Adapt learnings to current strategies

4. **Rapid Iteration**
   - Explore tests quick hypotheses
   - Fast feedback loop (test in <1 min)
   - Quickly eliminates bad ideas
   - Focuses effort on promising approaches

## Success Criteria

Strategy is "PROFITABLE" when:
- Win Rate ≥ 55%
- Net PNL Positive
- Profit Factor ≥ 1.3
- Max Drawdown ≤ 20%
- Minimum 50 trades/year

Strategy is "READY FOR PAPER TRADING" when:
- Meets all PROFITABLE criteria
- Consistent performance over 2025
- Backtest results verified
- Strategy documented with rules

## Constraints

- Use yfinance for historical data (2025-01-01 to 2025-12-31)
- Risk: 1% per trade, max 3 trades/day
- Initial Balance: $100 for all backtests
- Timeframes: H1 preferred, test H4 and D1 for comparison
- No look-ahead bias (use only past candles for decisions)

## Output Format

For each completed strategy, generate:

```python
{
  "strategy": "Holy Grail Optimized",
  "symbol": "GBPUSD=X",
  "parameters": {
    "ema_period": 15,
    "adx_period": 21,
    "adx_threshold": 25,
    "rsi_period": 14,
    "rsi_buy_zone": 40,
    "rsi_sell_zone": 60,
    "timeframe": "H1"
  },
  "performance": {
    "win_rate": 58.3,
    "net_pnl": 156.42,
    "profit_factor": 1.8,
    "total_trades": 127,
    "max_drawdown": 12.5
  },
  "status": "PROFITABLE"
}
```

## Next Steps

1. Load this research plan into oh-my-opencode
2. Start with Task 1: Holy Grail Optimization (highest priority)
3. Use Oracle, Hephaestus, Librarian, Explore in parallel
4. Iterate quickly through tasks
5. Generate optimized strategies
6. Create Fusion Markets automated paper trading system

---
END OF PROMPT
EOF

echo "Research plan created: /tmp/research_prompt.txt"
echo ""
echo "To start research with oh-my-opencode, load the prompt:"
echo "  cat /tmp/research_prompt.txt | /home/openclaw/.opencode/bin/opencode run"
