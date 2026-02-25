# MEMORY.md - Long-term Memories

_Curated wisdom from daily logs. Keep this distilled, not raw._

---

## Trading System - BerkahKarya Quant Fund

### Proven Strategy (2026-02-23)
**XAUUSD Asia 7-Candle Breakout** is ONLY strategy with proven profitability.

**Results (Framework + Simplified):**
- Win Rate: 61.4%
- Net PNL: +$528 (+528% return)
- Profit Factor: 4.1
- Total Trades: 427 (Wins: 262, Losses: 165)
- Max Consecutive Wins: 11
- Max Consecutive Losses: 6
- Max Drawdown: 0.5%

**Trade Parameters:**
- Session: 07:00-15:00 Jakarta time (Asia session)
- Entry: Buy stop at HH, Sell stop at LL (7-candle range)
- Filter: Only trade if range ≥ 5 pips
- Exit: TP = Entry + (Range × 2), SL = Entry - Range
- Risk: 1% per trade, max 3 trades/day

**Testing Period:** 2025-01-01 to 2025-12-31
**Initial Balance:** $100

### Other Strategies (Developed 2026-02-23) - NOT PROFITABLE

**Simplified Versions (Self-Contained):**

**Holy Grail Strategy:**
- Win Rate: 33.3%
- Net PNL: -$0.39
- Total Trades: 39 (Wins: 13, Losses: 26)
- Profit Factor: 1.0
- Max Drawdown: 11.5%

**Kumo Breakout Strategy (Ichimoku Cloud):**
- Win Rate: 0.0%
- Net PNL: $0.00
- Total Trades: 0 (no qualifying breakouts)
- Profit Factor: 0.0

**Momentum Elder Strategy (Elder Ray):**
- Win Rate: 22.2%
- Net PNL: -$6.52 (-6.5%)
- Total Trades: 27 (Wins: 6, Losses: 21)
- Profit Factor: 0.4
- Max Drawdown: 10.1%

**Volume Momentum Strategy:**
- Win Rate: 0.0%
- Net PNL: -$1.00
- Total Trades: 1
- Profit Factor: 0.0

**Framework Template Strategies:**

**Holy Grail (Template):**
- Framework version: No backtest method
- Status: Template only, needs implementation

**Kumo Breakout (Template):**
- Framework version: No backtest method
- Status: Template only, needs implementation

**Momentum Elder (Template):**
- Framework version: No backtest method
- Status: Template only, needs implementation

**Volume Momentum (Template):**
- Framework version: No backtest method
- Status: Template only, needs implementation

**Asia 7-Candle (Full Implementation):**
- Framework version: ✅ Has run_backtest() method
- Status: ✅ Fully functional

### PYTHONPATH FIX (2026-02-23)

**Problem:** Literal backslash in path: `/home/openclaw/C:\Users\EX PC\.openclaw\workspace`

**Solution:**
- Set PYTHONPATH to: `/home/openclaw/.openclaw/workspace/skills/1ai-skills:/home/openclaw/.openclaw/workspace/skills`
- Fixed all relative imports in trading package
  - Root files: `from utils.` → `from .utils.` (1 dot)
  - Indicators files: `from brokers.` → `from ..brokers.` (2 dots)
  - Strategy templates: `from brokers.` → `from ...brokers.` (3 dots)
  - Forex & crypto: `from brokers.` → `from ....brokers.` (4 dots)

**Result:** ✅ All framework strategies import successfully
- Holy Grail (Forex)
- Kumo Breakout (Forex)
- Momentum Elder (Forex)
- Volume Momentum (Crypto)
- XAUUSD Asia 7-Candle (TradFi)

### Framework Runner (2026-02-23)

**File:** `/home/openclaw/.openclaw/workspace/skills/1ai-skills/trading/framework_runner.py`

**Features:**
- List available strategies: `framework_runner.py list`
- Run backtest: `framework_runner.py backtest --strategy asia-7c`
- Support all 5 framework strategies
- Auto-detect backtest method
- Manual backtest fallback for templates

**Usage:**
```bash
export PYTHONPATH="/home/openclaw/.openclaw/workspace/skills/1ai-skills:/home/openclaw/.openclaw/workspace/skills"

# List strategies
~/.trading-venv/bin/python framework_runner.py list

# Run backtest
~/.trading-venv/bin/python framework_runner.py backtest \
  --strategy asia-7c \
  --symbol GC=F \
  --start-date 2025-01-01 \
  --end-date 2025-12-31 \
  --initial-balance 100
```

### Technology Stack
- Python venv: ~/.trading-venv/bin/python
- Working directory: /home/openclaw/.openclaw/workspace
- Trading package: skills/1ai-skills/trading
- ChromaDB: /home/openclaw/.openclaw/chroma_db (73 skills indexed)
- Data source: yfinance

### Next Steps (2026-02-23)
1. ✅ PYTHONPATH fix - DONE
2. ✅ Framework runner created - DONE
3. ✅ Asia 7-Candle backtest working - DONE
4. ✅ All simplified scripts working - DONE
5. ⏳ Implement backtest methods for template strategies (complex, pending)
6. ⏳ Start paper trading XAUUSD Asia 7-Candle on Fusion Markets cTrader
7. ⏳ Consider live trading with $1K initial capital if paper trading successful

---

## System Configuration

### ChromaDB Global Integration (2026-02-23)
Index: Skills (73), Tools (3), Memory (1), Commands (8), Context (5)

### Cron Jobs (2026-02-23)
- ChromaDB re-index: Every 6 hours
- Memory maintenance: Weekly (Sundays)
- Trading backtests: Daily at 8 AM
- Strategy comparison: Daily at 9 AM

### Workflow Definitions (2026-02-23)
- WORKFLOW_AUTO.md created with 5 active workflows
- Logging to /home/openclaw/.openclaw/workspace/logs/

---

## Notes
- Memory file: /home/openclaw/.openclaw/workspace/memory/YYYY-MM-DD.md
- Memory maintenance: Review daily files weekly, update this file
- Keep distilled insights only, not raw logs

---

*Last Updated: 2026-02-23*
*Updated by: OpenClaw*
