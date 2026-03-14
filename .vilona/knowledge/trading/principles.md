# Vilona Trading Knowledge Base

## Core Principles (Nuno's Wisdom)

### 1. Risk Management First
- Max 1-2% risk per trade
- Never risk more than 6% total account on any session
- Stop loss is mandatory, no exceptions

### 2. Strategy Validation
- Backtest minimum 6-12 months
- Paper trade minimum 1-2 months
- Live trade only after proven profitability
- ONE proven strategy > 10 unproven

### 3. BerkahKarya Trading Stack

**Asia 7-Candle Breakout**
- Win Rate: 61.4%
- Net PNL: $528 (+528% on $100)
- Profit Factor: 4.1
- Max Drawdown: 0.5%

**Session:** 07:00-15:00 Jakarta (Asia)
**Entry:** Buy stop at HH, Sell stop at LL (7-candle)
**Filter:** Only if range ≥ 5 pips
**Exit:** TP = Entry + (Range × 2), SL = Entry - Range
**Risk:** 1% per trade, max 3/day

### 4. Broker Priorities
1. **Ostium** - Decentralized, self-custody, XAUUSD available
2. MT5 - Proven track record
3. cTrader - Pending setup

### 5. Daily Trading Routine

**07:00** - Prepare 7-candle range
**11:00** - Asia session midpoint check
**15:00** - Session close analysis
**18:00** - P&L review, journal
**22:00** - Next day prep

### 6. Common Mistakes to Avoid
- Overtrading (max 3/day rule)
- Moving stop loss
- Revenge trading
- Trading without stop loss
- Ignoring session times

### 7. Learning Resources
- Price Action: Lance Beggs (YTC)
- Risk Management: Van Tharp
- Psychology: Mark Douglas
- Systems: Van K. Tharp

---

## Weekend Protocol C: Sunday Trading Prep

### Protocol Overview

**Purpose:** Weekly Sunday execution of Asia 7-Candle Breakout strategy
**Session:** Asia 07:00-15:00 UTC+7
**Entry Window:** 14:50-15:05 UTC+7 (7-candle range calculation + order entry)

### Protocol Execution Workflow

**Phase 1: Candle Watching (07:00-14:00) - Passive**
- Observe 15-minute candles form
- Track high/low of each candle
- No action required until 14:50

**Phase 2: Range Calculation (14:50-15:00)**
- Collect 7 candle highs and lows (from 07:00-14:45 windows)
- Calculate range: Highest High - Lowest Low
- Apply filter: Only proceed if range ≥ 5 pips
- Generate entry decision:
  - Buy Stop: Highest High
  - Sell Stop: Lowest Low
  - Stop Loss: Entry ± Range
  - Take Profit: Entry ± (Range × 2)

**Phase 3: Order Entry (15:00-15:05)**
- Monitor price at 15:00 UTC+7
- Place buy stop at Highest High if price breaks upward
- Place sell stop at Lowest Low if price breaks downward
- Risk: 1% of account (adjust position size based on range)
- Max risk per session: 3%

**Phase 4: Position Monitoring (16:00-23:00)**
- Monitor hourly if order triggered
- Do not adjust stop loss or take profit
- Record hourly P&L in journal
- 23:00: Final P&L, close if still open, journal entry

### Decision Matrix (Auto-Applied)

| Range (pips) | Qualification | Action |
|--------------|---------------|--------|
| < 5 pips | ❌ Too small | NO ENTRY |
| ≥ 5 pips | ✅ Qualified | ENTRY READY |

### Sunday Trading Automation Suite (Created March 8)

**1. Candle Tracker Script** ✅
- File: `scripts/sunday_candle_tracker.py`
- Purpose: Automated 7-candle tracking from 07:00-14:00 UTC+7
- Features: Tracks 15-minute candles, queries price APIs, auto-calculates range
- Note: Live API unreliable, manual input fallback preferred

**2. Decision Generator Script** ✅
- File: `scripts/sunday_decision_generator.py`
- Purpose: Takes candle data and generates entry decision
- Workflow:
  ```bash
  # At 14:50 UTC+7:
  python3 scripts/sunday_decision_generator.py
  # Enter 7 highs and 7 lows
  # Script auto-calculates range and outputs decision
  # Decision saved: temp/sunday-decision-YYYY-MM-DD-final.md
  ```
- Tested: March 8 - Range 17.00 pips → ENTRY QUALIFIED ✅

**3. Decision Template** ✅
- File: `temp/sunday-decision-template-YYYY-MM-DD.md`
- Purpose: Ready-to-fill template for manual data entry
- Contains: 7 high/low input fields, decision matrix reference, execution checklist

### Protocol C Status History

**Sunday, March 8, 2026:**
- Status: ✅ FRAMEWORK READY, ✅ NOT EXECUTED
- Deliverable: `temp/sunday-trading-prep-2026-03-08.md` (complete worksheet)
- Automation: Candle tracker + decision generator scripts created and tested
- Reason: Strategic deprioritization - crisis mode active (cashflow blind)
- Next execution: Sunday March 15 (after runway confirmed)

---

## Active Positions Tracker

| Date | Symbol | Direction | Entry | SL | TP | Size | P&L | Status |
|------|--------|-----------|-------|-----|-----|------|-----|--------|
| - | - | - | - | - | - | - | - | - |

---

## Protocol C Execution Log

| Date | Range (pips) | Qualified? | Entry Direction | Entry Price | SL | TP | P&L | Status |
|------|--------------|------------|-----------------|-------------|----|----|-----|--------|
| 2026-03-08 | Framework ready only | - | - | - | - | - | - | NOT EXECUTED (crisis mode) |

---

## Performance Log

| Period | Trades | Wins | Losses | Win% | P&L | Drawdown |
|--------|--------|------|--------|------|-----|----------|
| Backtest | 427 | 262 | 165 | 61.4% | +$528 | 0.5% |
| Paper 1 | - | - | - | 0% | $0 | 0% |
| Live | - | - | - | 0% | $0 | 0% |

---

## Current Status (2026-03-09)

### Readiness Assessment

| Phase | Status | Notes |
|-------|--------|-------|
| Backtest | ✅ COMPLETE | 61.4% win rate, 4.1 PF, 0.5% DD |
| Sunday Automation | ✅ FRAMEWORK READY | Scripts created (candle tracker, decision generator) |
| Paper Trading | ❌ NOT STARTED | Blocked by crisis mode (cashflow blind, revenue emergency) |
| Live Trading | ❌ NOT STARTED | Pending paper validation (1-2 months) |
| Full Automation | ⏳ TOOLS CREATED | Sunday scripts ready, trading_monitor.py still needed |

### Blockers

1. **CRITICAL**: Crisis mode - trading deprioritized
   - Cashflow blind (48+ hours) - runway unknown
   - Revenue gap EMERGENCY (24+ hours)
   - Priority: Cashflow visibility > trading setup

2. **DEFERRED**: Ostium broker paper trading not configured
   - Need to set up XAUUSD paper account
   - Requires API credentials
   - Priority: MEDIUM (execute after runway confirmed)

3. **DEFERRED**: trading_monitor.py missing
   - Cannot track positions automatically
   - Manual monitoring not scalable
   - Priority: MEDIUM (execute before live trading)

### Strategic Deprioritization (March 8)

**Decision:** Trading setup deferred until crisis resolved
**Reasoning:**
- Marketing revenue path: 24-48 hours after upload (clear, shorter horizon)
- Trading revenue path: 1-2 weeks (paper → live transition, longer horizon)
- Cashflow visibility unknown - cannot prioritize longer horizon without runway data

**Execution Plan:**
1. Resolve cashflow emergency (March 9)
2. Execute marketing revenue path (March 9-10)
3. Confirm runway with actual data
4. Reassess trading timeline based on runway:
   - Runway < 1 month: Defer trading, focus on marketing-only
   - Runway ≥ 1 month: Resume trading setup (paper → live)

### Next Steps (After Crisis Resolved)

1. **This Week (post-crisis):**
   - Create trading_monitor.py (4-6 hours)
   - Set up Ostium paper trading (1-2 hours)
   - Record first paper trade data

2. **This Month:**
   - Complete 1-2 months paper trading
   - Validate strategy live performance
   - Prepare for live trading activation

---

## Crisis Context (March 9, 2026)

**Current Situation:**
- BerkahKarya in CRISIS MODE (near bankruptcy)
- Revenue gap: 24+ hours EMERGENCY
- Cashflow: BLIND 48+ hours (runway unknown)
- Marketing revenue path: Blocked by PostBridge API failure
- Trading: Frameworks ready but DEPRIORITIZED until crisis resolved

**Strategic Decision:**
- Execute marketing path FIRST (revenue in 24-48h)
- Execute trading path SECOND (revenue in 1-2 weeks)
- Cashflow visibility NOW (blocks all strategic decisions)

**Trading Timeline:**
- March 9-10: Resolve cashflow emergency
- March 10-12: Execute marketing uploads (PostBridge recovery)
- March 12-14: Analyze runway with ACTUAL data
- March 15+: Resume trading setup IF runway ≥ 1 month
- April-May: Paper trading (1-2 months)
- June+: Live trading activation

---

### Knowledge Updated

- 2026-03-05: Learning rotation - Trading track review
  - Identified gap: Paper trading should have started immediately after backtest
- 2026-03-08: Sunday Protocol C automation suite created
  - Created candle tracker, decision generator, and template scripts
  - Tested decision generator: Range 17.00 pips → ENTRY QUALIFIED ✅
  - Documented execution workflow (4 phases: watching → calculation → entry → monitoring)
- 2026-03-09: Learning rotation - Monday track review (this update)
  - Updated current status with Sunday automation suite
  - Added Protocol C section with execution workflow and decision matrix
  - Added Protocol C execution log and status history
  - Documented strategic deprioritization due to crisis mode
  - Reorganized file structure for clarity

---

*Last updated: 2026-03-09*
*Next review: Daily at 18:00*
*Learning rotation: Monday = Trading track*
*Crisis status: Trading DEPRIORITIZED until cashflow emergency resolved*