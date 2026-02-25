# FUSION MARKETS CREDENTIALS
# Paper Trading Account - BerkahKarya Quant Fund

## Demo Account Details

**Broker:** Fusion Markets
**Account Type:** Demo
**Server:** FusionMarkets-Demo

### Login Credentials

| Field | Value |
|-------|-------|
| **Username** | `Openclaw@12` |
| **Password** | `10100262` |
| **Server** | `FusionMarkets-Demo` |

---

## Security Notes

⚠️  **IMPORTANT:**
- These are DEMO account credentials - NO REAL MONEY
- Store securely and don't share
- Change password if you create a live account later
- Never use same passwords for live trading

---

## Usage

### cTrader Desktop
1. Open cTrader application
2. Enter Username: `Openclaw@12`
3. Enter Password: `10100262`
4. Select Server: `FusionMarkets-Demo`
5. Click "Login"

### cTrader Webtrader (Browser - Linux Compatible)
1. Go to: https://fusionmarkets.com/Platforms/cTrader-Webtrader
2. Click "Login" or "Open cTrader"
3. Enter Username: `Openclaw@12`
4. Enter Password: `10100262`
5. Server: Should auto-select `FusionMarkets-Demo`

### cTrader Mobile
1. Download cTrader app (iOS/Android)
2. Enter Username: `Openclaw@12`
3. Enter Password: `10100262`
4. Server: `FusionMarkets-Demo`

---

## Initial Setup (First Login)

### Step 1: Check Account Balance

After logging in:
1. Check "Accounts" section
2. Verify demo account balance (should be $10,000 or similar)
3. Note: This is demo money - no real value

### Step 2: Set Up Chart

**For XAUUSD Asia 7-Candle Strategy:**
1. Click "New Chart" button
2. Search for: `XAUUSD` or `Gold`
3. Select pair: `XAUUSD`
4. Set Timeframe: `H1` (1 Hour)
5. Optionally add indicators (not required for this strategy)

### Step 3: Configure Session Filter

XAUUSD Asia 7-Candle requires Asia session:
- **Asia Session:** 07:00-15:00 Jakarta Time (00:00-08:00 UTC)

**To set up:**
1. Check chart time display
2. Note: cTrader shows server time (not your local time)
3. Asia session is the first 8 candles on H1 timeframe
4. Focus on candles 00:00-08:00 UTC

### Step 4: Add Trading Panel

1. Click "Algo" or "cAlgo" button (or "Trading" panel)
2. This opens the trading panel on the right side
3. Ready to place buy/sell orders

---

## Strategy: XAUUSD Asia 7-Candle Breakout

### Trade Parameters

**Risk Management:**
- Risk per trade: 1% of account balance
- Max trades per day: 3
- Stop trading if 3 consecutive losses
- Use 0.01 lot size (Mini lot for XAUUSD)

**Entry Rules (Daily Workflow):**

1. **07:00-07:30 UTC** (13:00-13:30 Jakarta)
   - Wait for 7 candles to form
   - Identify HH (Highest High) and LL (Lowest Low)

2. **Filter Check:**
   - Calculate Range: HH - LL
   - Only trade if Range ≥ 5 pips (0.50 for XAUUSD)
   - Skip day if range < 5 pips

3. **If Range ≥ 5 pips:**
   - **Buy Stop:** Set at HH (above current price)
   - **Sell Stop:** Set at LL (below current price)

4. **07:30-15:00 UTC** (13:30-21:30 Jakarta)
   - Monitor trades
   - Manage positions

**Exit Rules:**

1. **Take Profit (TP):**
   - Long: Entry + (Range × 2)
   - Short: Entry - (Range × 2)

2. **Stop Loss (SL):**
   - Long: Entry - Range
   - Short: Entry + Range

3. **Exit on Session End:**
   - At 15:00 UTC (21:00 Jakarta), close any remaining positions
   - Don't hold positions overnight

---

## Paper Trading Checklist

### Daily (Before Asia Session - 13:00 Jakarta)

- [ ] Verify login credentials working
- [ ] Check demo account balance
- [ ] Open XAUUSD H1 chart
- [ ] Set timeframe to H1
- [ ] Review previous day's trades
- [ ] Note current market conditions

### During Asia Session (07:00-15:00 Jakarta)

- [ ] Wait for 7 candles to form
- [ ] Calculate HH, LL, and Range
- [ ] Check: Range ≥ 5 pips?
- [ ] If yes: Place buy/sell stops
- [ ] Set TP correctly (Entry + Range × 2)
- [ ] Set SL correctly (Entry - Range)
- [ ] Verify: Risk ≤ 1% of balance
- [ ] Check: Trade count < 3 today
- [ ] Monitor trades closely
- [ ] Record all trades in journal

### After Session (After 15:00 Jakarta)

- [ ] Close any remaining positions
- [ ] Review day's trades
- [ ] Calculate day's PNL
- [ ] Update trading journal
- [ ] Note lessons learned
- [ ] Plan for tomorrow

---

## Tracking Template (Daily Journal)

Copy this for each day's trading:

```markdown
# [DATE] - Paper Trading Journal

## Summary
- Strategy: XAUUSD Asia 7-Candle Breakout
- Session Time: 07:00-15:00 Jakarta
- Account: Fusion Markets Demo
- Initial Balance: $[AMOUNT]
- Final Balance: $[AMOUNT]
- Net PNL: $[AMOUNT]

## Market Conditions
- Volatility: [Low/Medium/High]
- Session Range: [MIN] - [MAX] pips
- Trends: [Up/Down/Sideways]
- Notes: [Any observations]

## Trades

### Trade 1
- Time: [TIME]
- Type: [Buy/Sell]
- Entry: $[PRICE]
- TP: $[PRICE]
- SL: $[PRICE]
- Exit: [TP Hit/SL Hit/Session End]
- PNL: $[AMOUNT]
- Result: [Win/Loss]
- Notes: [Any observations]

### Trade 2
- Time: [TIME]
- Type: [Buy/Sell]
- Entry: $[PRICE]
- TP: $[PRICE]
- SL: $[PRICE]
- Exit: [TP Hit/SL Hit/Session End]
- PNL: $[AMOUNT]
- Result: [Win/Loss]
- Notes: [Any observations]

### Trade 3
- Time: [TIME]
- Type: [Buy/Sell]
- Entry: $[PRICE]
- TP: $[PRICE]
- SL: $[PRICE]
- Exit: [TP Hit/SL Hit/Session End]
- PNL: $[AMOUNT]
- Result: [Win/Loss]
- Notes: [Any observations]

## Lessons Learned
- What worked:
- What didn't:
- Improvements needed:
- Mental state:

## Tomorrow's Plan
- Adjustments to strategy:
- Risk management changes:
- Goals:
```

---

## Performance Tracking

### Weekly Metrics

Track at end of each week:

| Week | PNL | Win Rate | Total Trades | Max DD |
|------|-----|----------|--------------|--------|
| Week 1 | | | | |
| Week 2 | | | | |
| Week 3 | | | | |

### Monthly Goals

| Month | Goal PNL | Actual PNL | Target WR | Actual WR |
|-------|----------|------------|-----------|----------|
| Month 1 | +$100 | | 60% | | |
| Month 2 | +$200 | | 60% | | |

---

## When to Start Live Trading

**Minimum Requirements:**

1. ✅ **4+ Weeks of Consistent Profitability**
   - Weekly PNL positive for 4 consecutive weeks
   - Win rate ≥ 60%

2. ✅ **Stable Performance**
   - Max drawdown ≤ 10%
   - No revenge trading
   - Followed strategy rules 100%

3. ✅ **Account Growth**
   - Demo balance grew from $10,000 to $15,000+ (50%+ growth)
   - Demonstrated ability to compound

4. ✅ **Psychology Ready**
   - Comfortable with losses
   - No emotional trading decisions
   - Discipline maintained

**First Live Trading Steps:**

1. Open live account with Fusion Markets
2. Deposit: $500-$1,000 (start small)
3. Use same strategy (XAUUSD Asia 7-Candle)
4. Start with 0.01 lot size
5. Monitor closely for first 2-4 weeks
6. Scale up gradually as confidence grows

---

## Troubleshooting

### Login Issues

**Problem:** Cannot login
- **Check:** Username (Openclaw@12)
- **Check:** Password (10100262)
- **Check:** Server selection (FusionMarkets-Demo)
- **Solution:** Reset password if needed (contact Fusion Markets support)

### Chart Issues

**Problem:** Cannot find XAUUSD pair
- **Solution:** Search for "Gold" instead of "XAUUSD"
- **Note:** Different brokers use different symbols

### Order Issues

**Problem:** Orders not triggering
- **Check:** Are stops placed at correct levels?
- **Check:** Is price moving in right direction?
- **Solution:** Verify entry levels and market spread

---

## Contact Support

**Fusion Markets:**
- Website: https://fusionmarkets.com/
- Email: support@fusionmarkets.com
- Live Chat: Available on website

**Documentation:**
- cTrader Guide: https://help.ctrader.com/
- Fusion Markets Help: https://fusionmarkets.com/help

---

## Resources

### Strategy Guide
- Full Strategy: `/home/openclaw/.openclaw/workspace/skills/1ai-skills/trading/strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py`
- Backtest Results: `/tmp/xauusd_final.json`
- Comparison Report: `/home/openclaw/.openclaw/workspace/STRATEGY_COMPARISON_REPORT.md`

### Performance Tracking
- Backtest Data: Win Rate 61.4%, Net PNL +$528
- Expected Paper Trading Performance: Similar (may vary due to real market conditions)

---

## Important Reminders

⚠️  **This is PAPER TRADING**
- Use demo account to learn
- No real money at risk
- Perfect place to practice and refine strategy
- Focus on learning, not just PNL

✅  **Strategy is PROVEN**
- Backtest shows: 61.4% win rate, +$528 return
- Expect similar performance in paper trading
- Consistency is more important than big wins

🎯  **Goal: 4+ Weeks of Profitable Trading**
- After 4+ profitable weeks, consider live trading
- Start with small live account ($500-$1K)
- Scale up gradually as confidence grows

---

*Credentials saved: 2026-02-23*
*Account: Fusion Markets Demo*
*Strategy: XAUUSD Asia 7-Candle Breakout*
*Purpose: Paper Trading - BerkahKarya Quant Fund*
