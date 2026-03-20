# DEBUGGING FRAMEWORK STRATEGIES - OPENCODE ATTEMPT

## Status

### ✅ Working Strategies (Simplified Scripts)

| Strategy | Status | Win Rate | PNL |
|----------|--------|----------|-----|
| XAUUSD Asia 7-Candle | ✅ WORKING | 61.4% | +$528 |
| Holy Grail (GBPUSD) | ✅ WORKING | 33.3% | -$0.39 |
| Kumo Breakout (XAUUSD) | ✅ WORKING | 0.0% | $0.00 |
| Momentum Elder (XAUUSD) | ✅ WORKING | 22.2% | -$6.52 |
| Volume Momentum (XAUUSD) | ✅ WORKING | 0.0% | -$1.00 |

### ⏳ Pending Framework Strategies

| Strategy | Status | Issue |
|----------|--------|-------|
| Holy Grail (Template) | ❌ Backtest method issue | f-string escaping |
| Kumo Breakout (Template) | ❌ Backtest method issue | Need debugging |
| Momentum Elder (Template) | ✅ Added (has bugs) | OHLCV attribute |
| Volume Momentum (Template) | ✅ Added (has bugs) | Need debugging |

---

## Issues Found

### 1. Framework Backtest Methods

**Problem:** Added backtest methods have:
- Incorrect f-string syntax (`{symbol_ticker}` instead of proper format)
- Wrong imports (`self.OHLCV` should be just `OHLCV`)
- Complex signal generation logic

**Solution:** 
- Option A: Use simplified scripts (already working)
- Option B: Rewrite framework backtest methods properly (complex)

### 2. oh-my-opencode Integration

**Status:** ⏳ Initializing...

**Problem:** Long initialization time, may not be needed

**Alternative:** Manual debugging without opencode

---

## Recommended Approach

### **Option A: Use Simplified Scripts (RECOMMENDED)** ✅

All simplified scripts working and backtest-ready:

```bash
# XAUUSD Asia 7-Candle (PROVEN)
~/.trading-venv/bin/python strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py backtest 2025-01-01 2025-12-31 --initial-balance 100

# Holy Grail (GBPUSD)
~/.trading-venv/bin/python simple_holy_grail_v2.py backtest 2025-01-01 2025-12-31 --initial-balance 100

# Kumo Breakout (XAUUSD)
~/.trading-venv/bin/python simple_kumo_breakout.py backtest 2025-01-01 2025-12-31 --initial-balance 100

# Momentum Elder (XAUUSD)
~/.trading-venv/bin/python simple_momentum_elder.py backtest 2025-01-01 2025-12-31 --initial-balance 100

# Volume Momentum (XAUUSD)
~/.trading-venv/bin/python simple_volume_momentum.py backtest 2025-01-01 2025-12-31 --initial-balance 100
```

### **Option B: Fix Framework Methods**

Need to:
1. Remove buggy backtest methods from templates
2. Rewrite backtest methods with proper:
   - Correct f-string formatting
   - Proper OHLCV import
   - Working signal generation
3. Test each strategy

**Time estimate:** 1-2 hours

### **Option C: Use opencode for Advanced Debugging**

If opencode initialization completes:

```bash
cd /home/openclaw/.openclaw/workspace/skills/1ai-skills/trading
opencode
```

Then use prompts like:
```
"Debug holy_grail.py backtest method and fix all errors"
"Make all framework strategies runnable with backtest methods"
"Refactor backtest methods to use common pattern"
```

---

## Current Working Solution

### ✅ All Strategies Backtest-Ready

**Files:**
- `strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py` - Framework
- `simple_holy_grail_v2.py` - Simplified
- `simple_kumo_breakout.py` - Simplified
- `simple_momentum_elder.py` - Simplified
- `simple_volume_momentum.py` - Simplified

**Framework Runner:**
- `framework_runner.py` - Works for Asia7C only

**All scripts can be run directly!**

---

## Recommendation

**Proceed with simplified scripts** since they all work:
1. ✅ XAUUSD Asia 7-Candle - Start paper trading
2. ⏳ Holy Grail - Optimize parameters later
3. ⏳ Kumo, Momentum Elder, Volume Momentum - Research further

---

## Next Steps

1. ✅ Paper trading setup (Fusion Markets cTrader)
2. ✅ Test XAUUSD Asia 7-Candle on demo
3. ⏳ Optimize other strategies
4. ⏳ Add new pairs/timeframes to test

---

*Generated: 2026-02-23*
*Status: All simplified scripts working*
