# PAPER TRADING SETUP GUIDE
## Fusion Markets cTrader - XAUUSD Asia 7-Candle Strategy

### Step 1: Create Demo Account

**Fusion Markets Demo Account:** https://fusionmarkets.com/

1. Go to https://fusionmarkets.com/
2. Click "Open Account"
3. Select "Demo Account"
4. Fill in registration:
   - Email
   - Password
   - Country
5. Verify email (if required)
6. Login to Client Hub
7. Navigate to "Accounts" section
8. Note down your:
   - **Account ID**
   - **Password**
   - **Server** (Fusion Markets Demo Server)

### Step 2: Access cTrader Platform

**Option A: cTrader Webtrader (Browser - Linux Compatible)**
- URL: https://fusionmarkets.com/Platforms/cTrader-Webtrader
- No download required
- Access via browser

**Option B: cTrader Desktop (Windows/Mac - Wine Compatible)**
- Download: https://fusionmarkets.com/Platforms/cTrader
- Run with Wine on Linux:
  ```bash
  wine cTrader.exe
  ```

**Option C: cTrader Mobile (iOS/Android)**
- Download from App Store/Play Store
- Login with demo credentials

### Step 3: Configure Trading Platform

**Login Details:**
```
Account ID: [From Step 1]
Password:   [From Step 1]
Server:     Fusion Markets Demo
```

**Platform Settings:**

1. **Chart Setup:**
   - Symbol: XAUUSD (Gold)
   - Timeframe: H1 (1 Hour)
   - Session Filter: 07:00-15:00 Jakarta Time

2. **Indicators (Optional):**
   - No indicators needed for Asia 7-Candle strategy
   - Price action only

3. **Order Settings:**
   - Lot Size: 0.01 (Mini lot)
   - Risk: 1% per trade
   - Max Trades: 3 per day

### Step 4: Asia 7-Candle Strategy Rules

**Entry Rules:**

1. **Identify Asia Session:**
   - Time: 07:00-15:00 Jakarta Time (00:00-08:00 UTC)
   - Look for 7 candles in this window

2. **Calculate 7-Candle Range:**
   - Find HH (Highest High) of 7 candles
   - Find LL (Lowest Low) of 7 candles
   - Calculate Range: HH - LL

3. **Filter:**
   - Only trade if Range ≥ 5 pips (0.50 for XAUUSD)

4. **Entry Points:**
   - Buy Stop: HH (above 7-candle high)
   - Sell Stop: LL (below 7-candle low)

**Exit Rules:**

1. **Take Profit (TP):**
   - Long: Entry + (Range × 2)
   - Short: Entry - (Range × 2)

2. **Stop Loss (SL):**
   - Long: Entry - Range
   - Short: Entry + Range

**Risk Management:**

1. **Risk per Trade:**
   - 1% of account balance
   - With $100 demo balance: $1 per trade max

2. **Position Sizing:**
   - Lot Size: 0.01 (Mini lot for XAUUSD)
   - Pip Value: ~$0.10 per pip for 0.01 lot

3. **Trade Limits:**
   - Max 3 trades per day
   - Stop trading if hit max consecutive losses (3-4)

### Step 5: Paper Trading Workflow

**Daily Workflow (Asia Session - Jakarta Time 07:00-15:00):**

1. **07:00-07:30:** Wait for 7 candles to form
2. **07:30:** Identify HH/LL of first 7 candles
3. **07:30:** Calculate range, set up buy/sell stops
4. **07:30-15:00:** Monitor trades, manage positions
5. **15:00+:** Close any remaining positions (optional)

**Daily Checklist:**

- [ ] 7 candles formed in Asia session?
- [ ] Range ≥ 5 pips?
- [ ] Entry orders placed (buy stop at HH, sell stop at LL)?
- [ ] TP and SL set correctly?
- [ ] Risk per trade ≤ 1%?
- [ ] No more than 3 trades today?
- [ ] Track results in trading journal

### Step 6: Performance Tracking

**Metrics to Track:**

1. **Daily:**
   - Number of trades
   - Wins / Losses
   - Net PNL
   - Max drawdown for the day

2. **Weekly:**
   - Total PNL
   - Win rate
   - Profit factor
   - Consecutive wins/losses

3. **Monthly:**
   - Consistency analysis
   - Best performing days
   - Areas for improvement

**Trading Journal Template:**

```markdown
# 2026-02-24 - Paper Trading Journal

## Summary
- Balance: $100.00
- Trades: 3
- Wins: 2
- Losses: 1
- Net PNL: +$2.50

## Trade 1
- Time: 08:15
- Type: Long (Buy Stop)
- Entry: 2024.50
- TP: 2025.50
- SL: 2023.50
- Exit: TP hit
- PNL: +$1.00

## Trade 2
- Time: 10:30
- Type: Short (Sell Stop)
- Entry: 2025.20
- TP: 2024.20
- SL: 2026.20
- Exit: SL hit
- PNL: -$0.50

## Trade 3
- Time: 12:45
- Type: Long (Buy Stop)
- Entry: 2026.00
- TP: 2027.00
- SL: 2025.00
- Exit: TP hit
- PNL: +$1.00

## Notes
- Volatility was lower than expected
- Range was only 4.5 pips on first setup
- Second trade had news event that spiked the market
- Overall good day, followed strategy rules

## Improvements
- Consider reducing range filter to 3 pips for low volatility days
- Track volatility conditions more closely
```

### Step 7: When to Start Live Trading

**Prerequisites:**

1. ✅ **Consistent Profitability:**
   - 4+ weeks of profitable paper trading
   - Win rate ≥ 55%
   - Positive net PNL

2. ✅ **Stable Performance:**
   - Max drawdown ≤ 10%
   - Consistent execution without mistakes
   - Followed strategy rules strictly

3. ✅ **Account Growth:**
   - Demo balance grew from $100 to $150+ (50%+ growth)
   - Demonstrated ability to compound

4. ✅ **Psychology:**
   - Comfortable with losses
   - No revenge trading
   - Discipline maintained

**Live Trading Setup:**

1. Open live account with Fusion Markets
2. Deposit initial capital: $500-$1,000
3. Start with smaller position size (0.01 lot)
4. Monitor first 2-4 weeks closely
5. Scale up gradually as confidence grows

### Step 8: Troubleshooting

**Issue: Orders not triggering**

- Check: Are entry orders set correctly (buy stop/sell stop)?
- Check: Is account balance sufficient?
- Check: Is market spread too wide?

**Issue: High number of losses**

- Review: Are you trading outside Asia session?
- Review: Is range filter being applied correctly?
- Review: Are you moving SL/TP after entry?

**Issue: Consistency issues**

- Review: Are you following strategy rules 100%?
- Review: Are you overtrading (more than 3 trades/day)?
- Review: Is your psychological state affecting decisions?

### Step 9: Resources

**Links:**
- Fusion Markets: https://fusionmarkets.com/
- cTrader Webtrader: https://fusionmarkets.com/Platforms/cTrader-Webtrader
- cTrader Documentation: https://help.ctrader.com/

**Strategy Parameters:**
- Session: 07:00-15:00 Jakarta Time
- Timeframe: H1
- Candles: 7
- Min Range: 5 pips (0.50 for XAUUSD)
- R/R Ratio: 2:1
- Risk: 1% per trade
- Max Trades: 3 per day

---

## Paper Trading Checklist

**Before Starting:**
- [ ] Demo account created
- [ ] cTrader platform accessed
- [ ] XAUUSD chart opened (H1)
- [ ] Session filter set (07:00-15:00 Jakarta)
- [ ] Trading journal prepared

**During Trading:**
- [ ] 7 candles formed
- [ ] HH/LL calculated correctly
- [ ] Range ≥ 5 pips
- [ ] Entry orders placed
- [ ] TP/SL set correctly
- [ ] Risk ≤ 1%
- [ ] Max 3 trades/day

**After Trading:**
- [ ] Results tracked in journal
- [ ] Lessons learned noted
- [ ] Strategy adherence reviewed
- [ ] Performance metrics calculated

---

*Created: 2026-02-23*
*Strategy: XAUUSD Asia 7-Candle Breakout*
*Platform: Fusion Markets cTrader*
