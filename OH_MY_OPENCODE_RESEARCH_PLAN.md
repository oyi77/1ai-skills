# COMPREHENSIVE RESEARCH PLAN
# Optimasi Strategi Holy Grail, Kumo, Momentum Elder, Volume Momentum
# Menggunakan oh-my-opencode untuk multi-agent research

## Masalah Utama

### Current Performance (Tidak Profitable)

| Strategy | WR | PNL | Issues |
|----------|-----|-----|--------|
| **XAUUSD Asia 7-Candle** | **61.4%** | **+$528** | ✅ **PROFITABLE** |
| Holy Grail (GBPUSD) | 33.3% | -$0.39 | ❌ Entry timing salah |
| Kumo Breakout (XAUUSD) | 0.0% | $0.00 | ❌ Tidak ada trade |
| Momentum Elder (XAUUSD) | 22.2% | -$6.52 | ❌ Signal noise terlalu banyak |
| Volume Momentum (XAUUSD) | 0.0% | -$1.00 | ❌ Hanya 1 trade |

### Root Cause Analysis

**Holy Grail (WR 33.3%):**
- EMA(20) mungkin terlalu lambat re-aksi
- ADX threshold 30 terlalu tinggi untuk pair GBPUSD
- RSI zones 40-60 terlalu lebar, tidak cukup spesifik
- "Rollback" entry mungkin tidak terjadi di market ini
- Exit based pada ADX reversal terlalu late

**Kumo Breakout (0.0% Trades):**
- Cloud filter mungkin terlalu ketat (prev candle inside cloud)
- Range filter mungkin tidak ada/tidak terpasang
- XAUUSD trend mungkin tidak menghasilkan cloud breakout yang valid
- Ichimoku calculation mungkin salah

**Momentum Elder (WR 22.2%):**
- Bull/Bear power threshold mungkin terlalu kecil
- Elder Ray tidak cukup trend-following untuk pair ini
- Momentum filter menangkap terlalu banyak noise
- 1:1 R/R terlalu kecil (entry pun close ke SL)

**Volume Momentum (0.0% Trades):**
- Volume ratio threshold 1.5 terlalu tinggi
- Hanya ada 1 trade sepanjang tahun - tidak cukup data
- Momentum filter menangkap event langka
- Market mungkin tidak punya volume spikes yang significant

---

## Research Approach with oh-my-opencode

### Agent Roles

**1. Oracle (High-IQ)**
- **Tugas:** System design, arsitektur strategi, debugging complex
- **Prompt:** Analisis root cause masing-masing strategi dan desain ulang dari nol
- **Fokus:** Fundamental strategy design - apa yang membuat strategi profitable?

**2. Hephaestus (Deep Worker)**
- **Tugas:** Deep research, exploration parameter space, extensive backtesting
- **Prompt:** Test berbagai kombinasi parameter untuk setiap strategi
- **Fokus:** Parameter optimization - EMA period, ADX threshold, RSI zones, dll

**3. Librarian (Documentation & Research)**
- **Tugas:** Research existing profitable strategies, best practices, academic papers
- **Prompt:** Cari referensi strategi profitable (bollinger, MACD, price action, dll)
- **Fokus:** Evidence-based approach - apa yang bekerja di market lain?

**4. Explore (Fast Exploration)**
- **Tugas:** Codebase analysis, pattern discovery, quick backtest runs
- **Prompt:** Analisis code existing strategies, cari pattern, quick backtest
- **Fokus:** Fast iteration - test ide-ide cepat

---

## Research Plan per Strategy

### Strategy 1: Holy Grail (GBPUSD) - Fix & Optimize

**Current Issues:**
- EMA(20) terlalu slow, tidak catch reversal
- ADX threshold 30 terlalu high
- Entry timing tidak akurat

**Oracle Task: Redesign Entry Logic**
```python
# Target: Improve entry timing and filtering
Research Questions:
1. Bagaimana mendeteksi "valid rollback" ke EMA?
   - Price crosses below EMA kemudian re-cross di atas?
   - Gunakan confirmation candle setelah rollback?

2. Apa filter tambahan yang bisa digunakan?
   - Previous candle trend direction?
   - Volume spike saat entry?
   - Time-of-day filter (avoid news)?

3. Bagaimana mengoptimalkan exit?
   - TP based pada ATR (dynamic)?
   - SL based pada structure?
   - Early exit bila trend berubah?

Output: Desain ulang entry/exit logic dengan filter tambahan
```

**Hephaestus Task: Parameter Optimization**
```python
# Parameter space to explore:
- EMA period: 5, 10, 15, 20, 25
- ADX period: 7, 14, 21, 28
- ADX threshold: 15, 20, 25, 30, 35
- RSI period: 7, 14, 21
- RSI buy zone: 30-40, 35-45, 40-50
- RSI sell zone: 30-40, 35-45, 40-50
- Timeframe: H1, H4, D1

# Optimize with:
- Grid search pada parameter space
- Backtest 2025-01-01 to 2025-12-31
- Target: WR ≥ 55%, PNL positive
- Constraint: Max drawdown ≤ 15%

Output: Kombinasi parameter terbaik
```

**Librarian Task: Research Profitable EMA Strategies**
```python
# Research topics:
1. EMA Crossover + ADX combo strategies
2. RSI + EMA trend following
3. Bollinger Band breakout with EMA filter
4. Multi-timeframe confirmation (H1 + H4)

Sources:
- TradingView strategy ideas
- ForexFactory forum discussions
- Academic papers on EMA-based systems

Output: Daftar teknik yang sudah terbukti profitable, untuk diterapkan
```

**Explore Task: Quick Backtests**
```python
# Quick wins to test:
1. EMA(10) + ADX(20) + RSI(14)
2. EMA(15) + ADX(14) + RSI(14)
3. Multi-timeframe confirmation
4. Add volume filter

Target: Find "quick win" yang menaikkan WR ke 50%+

Output: Parameter yang menaikkan performa secara cepat
```

### Strategy 2: Kumo Breakout (XAUUSD) - Fix Cloud Filter

**Current Issues:**
- 0.0% trades - cloud filter terlalu ketat
- Mungkin prev candle harus TIDAK di cloud (outside cloud breakout)

**Oracle Task: Redesign Cloud Breakout Logic**
```python
# Alternative entry conditions:
1. Price breaks above cloud upper AND previous close above cloud?
2. Price breaks above cloud upper AND cloud is expanding (A above B)?
3. Price breaks above cloud upper AND volume spike?
4. Price breaks above cloud upper AND multiple candles confirm trend?

Research Questions:
- Bagaimana mendefinisikan "valid breakout" dari cloud?
- Apa peran volume dalam konfirmasi breakout?
- Bagaimana menghindari false breakout saat market choppy?

Output: Redesigned entry condition dengan multiple confirmation
```

**Hephaestus Task: Cloud Filter Optimization**
```python
# Parameter space:
- Tenkan period: 9, 18, 26 (default), 34
- Kijun period: 26 (default), 52
- Senkou Span B: 26 (default), 52
- Cloud thickness filter: Minimum 10 pips?
- Cloud expansion check: Enable/Disable
- Previous candle filter: Inside/outside cloud?

# Optimize for XAUUSD:
- Timeframes: H1, H4, D1
- Test combinations
- Target: At least 100 trades/year, WR ≥ 50%

Output: Kombinasi parameter yang menghasilkan trades valid
```

**Librarian Task: Ichimoku Strategies Research**
```python
# Research topics:
1. Profitable Ichimoku strategies (cloud breakouts, TK crosses)
2. Best Ichimoku settings for XAUUSD
3. Ichimoku + other indicators (RSI, MACD, ADX)
4. Time-of-day filters for XAUUSD

Output: Ichimoku best practices dan parameter yang sudah teruji
```

### Strategy 3: Momentum Elder (XAUUSD) - Reduce Noise

**Current Issues:**
- WR 22.2% - terlalu banyak false signals
- Bull/Bear power noise
- 1:1 R/R terlalu riski

**Oracle Task: Redesign Momentum Filter**
```python
# Alternative momentum indicators:
1. Elder Ray + ADX confirmation (ADX > 25 for trend)
2. Elder Ray + Volume confirmation (volume > average)
3. Elder Ray + MACD confirmation (MACD histogram)
4. Elder Ray + Multi-timeframe (H1 + H4 agree)

Research Questions:
- Bagaimana mengurangi false signals?
- Apa threshold optimal untuk Bull/Bear power?
- Apa confirmation terbaik untuk XAUUSD?

Output: Momentum filter dengan confirmation layer
```

**Hephaestus Task: Risk/Reward Optimization**
```python
# Current issue: 1:1 R/R (entry pun close to SL)

# R/R options to test:
1. 1.5:1 (slower TP, lebih room for SL)
2. 2:1 (default, tapi mungkin perlu ATR-based)
3. 2.5:1 (aggressive TP)
4. 3:1 (very aggressive)

# Stop Loss options:
1. ATR-based SL (dynamic SL)
2. Structure-based (previous low)
3. Percentage-based (1% of balance)
4. Fixed pip SL (10 pips for XAUUSD)

# Optimize for maximum profitability:
- Target: PF ≥ 1.5, WR ≥ 50%
- Constraint: Max drawdown ≤ 20%

Output: R/R ratio optimal
```

**Explore Task: Quick Backtests**
```python
# Test momentum combinations:
1. Elder + ADX only (no RSI)
2. Elder + Volume only (no RSI)
3. Elder + Multi-timeframe
4. Different timeframes (H4 better for momentum?)

Target: Naikkan WR dari 22.2% ke minimal 45%

Output: Momentum filter terbaik
```

### Strategy 4: Volume Momentum (XAUUSD) - Increase Trade Frequency

**Current Issues:**
- 0.0% WR tapi hanya 1 trade - tidak cukup data
- Volume ratio threshold 1.5 terlalu tinggi
- XAUUSD mungkin tidak punya volume spikes yang significant

**Oracle Task: Analyze XAUUSD Volume Characteristics**
```python
# Research questions:
1. Apakah volume distribution XAUUSD punya spikes?
2. Apakah ada daily/weekly volume patterns?
3. Apakah volume correlation dengan news?
4. Apakah time-of-day affects volume?

# Data analysis needed:
- Download XAUUSD data dengan volume (yfinance punya)
- Analisis volume distribution
- Cari volume outliers (spikes)
- Hitung rata-rata, median, percentiles

Output: Karakteristik volume XAUUSD dan threshold yang realistis
```

**Hephaestus Task: Redesign Volume Strategy**
```python
# Alternative approaches:
1. Volume-based session filter (trade hanya saat volume rata-rata)
2. Volume spike entry (entries pada volume tinggi, tapi bukan extreme)
3. Volume-weighted position sizing (large volume = larger position)
4. Volume-based exit (exit saat volume menurun/dry up)

# Parameter space:
- Volume ratio: 0.8, 1.0, 1.2, 1.5
- Volume average period: 10, 20, 50 candles
- Volume spike multiplier: 2x, 3x, 5x
- Minimum absolute volume: Filter volume rendah

# Target:
- Trade frequency: 50-200 trades/year
- WR ≥ 50%
- Positive PNL

Output: Volume strategy yang menghasilkan lebih banyak trade
```

---

## Phase 1: Quick Wins (1-2 Days)

### Oracle + Hephaestus: Holy Grail Quick Optimization

**Target:** Naikkan WR dari 33.3% ke 45%+ dalam 1-2 hari

**Langkah:**
1. Oracle desain ulang entry logic dengan:
   - Previous candle trend filter
   - Multi-timeframe confirmation (H1 + H4)
   - Volume confirmation filter

2. Hephaestus parameter optimization:
   - Test 10-20 kombinasi parameter
   - Focus pada EMA period dan ADX threshold
   - Target: WR ≥ 45%

3. Explore quick backtest:
   - Test 5-10 parameter variants
   - Pilih yang terbaik

**Expected Outcome:**
- Holy Grail dengan WR 45-55%
- PNL mendekati atau positive

---

## Phase 2: Medium-Term Research (3-5 Days)

### All Strategies Deep Research

**Target:** Semua strategi dengan WR ≥ 50%

**Parallel Research:**

**Holy Grail:** Hephaestus + Librarian
- Full parameter optimization
- Research profitable EMA strategies
- Implement multi-timeframe confirmation

**Kumo:** Oracle + Hephaestus + Librarian
- Redesign cloud breakout logic
- Ichimoku best practices research
- Filter optimization

**Momentum Elder:** Oracle + Hephaestus + Explore
- Momentum filter redesign
- R/R optimization
- Noise reduction techniques

**Volume Momentum:** Oracle + Librarian
- XAUUSD volume characteristics analysis
- Alternative volume-based approaches
- Trade frequency optimization

**Expected Outcome:**
- Semua 4 strategi dengan WR ≥ 50%
- PNL positive atau mendekati break-even
- Setidaknya 1 strategi baru untuk selain XAUUSD Asia 7-Candle

---

## Phase 3: Automated Paper Trading System

### Fusion Markets Integration

**Components:**
1. **Trading Engine:**
   - Execute XAUUSD Asia 7-Candle (PROVEN)
   - Execute Holy Grail (optimized)
   - Execute Kumo (optimized)
   - Execute Momentum Elder (optimized)
   - Execute Volume Momentum (optimized)

2. **Risk Management:**
   - 1% risk per trade
   - Max 3 trades/day per strategy
   - Stop trading after 3 consecutive losses
   - Daily PNL limit (-5% dari equity)

3. **Signal Generation:**
   - Real-time OHLCV data dari Fusion Markets cTrader
   - Calculate indicators untuk setiap strategy
   - Generate buy/sell signals
   - Filter signals (time, volatility, news)

4. **Order Execution:**
   - Place market/stop orders via Fusion Markets API
   - Set TP/SL
   - Monitor positions
   - Close positions sesuai rules

5. **Journaling:**
   - Log semua trades
   - Hitung PNL harian
   - Hitung metrics (WR, PF, DD)
   - Generate daily/weekly reports

---

## Expected Final Outcome

**After Research (5-7 days):**
- ✅ XAUUSD Asia 7-Candle: Tetap WR ~60%, PNL ~+$500
- ✅ Holy Grail: WR ≥ 50%, PNL ≥ $100
- ✅ Kumo: WR ≥ 50%, PNL ≥ $50
- ✅ Momentum Elder: WR ≥ 50%, PNL ≥ $50
- ✅ Volume Momentum: WR ≥ 50%, PNL ≥ $50

**After Automated Paper Trading (4-8 weeks):**
- ✅ Semua strategies running in paper trading
- ✅ Konsisten profit selama 4-8 minggu
- ✅ Risk management teruji
- ✅ Sistem siap untuk live trading

---

## Execution Plan with oh-my-opencode

### Step 1: Initialize (0.5 jam)
```bash
cd /home/openclaw/.openclaw/workspace/skills/1ai-skills/trading
opencode
# Wait for TUI to load
# Verify agents loaded
# Set working directory
```

### Step 2: Phase 1 Quick Wins (1-2 hari)
```bash
# Holy Grail Quick Optimization
opencode run --agent Oracle "Desain ulang entry logic untuk Holy Grail. Tambahkan: previous candle trend filter, multi-timeframe confirmation (H1+H4), volume confirmation filter. Target: WR ≥ 45%."

opencode run --agent Hephaestus "Optimasi parameter Holy Grail. EMA period: [5,10,15,20,25], ADX threshold: [15,20,25,30,35], RSI period: [7,14,21]. Backtest 2025-01-01 to 2025-12-31. Pilih kombinasi dengan WR ≥ 45%."

opencode run --agent Explore "Analisis code Holy Grail strategy. Cari pattern yang mungkin menyebabkan false signals. Test 5-10 quick parameter variants. Target: naikkan WR dari 33.3% ke 45%+."
```

### Step 3: Phase 2 Deep Research (3-5 hari)
```bash
# Parallel research semua strategies

opencode run --agent Oracle "Analisis root cause semua strategi yang tidak profitable. Desain ulang masing-masing: Holy Grail (EMA timing), Kumo (cloud filter), Momentum Elder (noise), Volume Momentum (trade frequency). Output: detailed analysis dan desain baru."

opencode run --agent Hephaestus "Optimasi parameter untuk Holy Grail. Full grid search pada parameter space. EMA: [5,10,15,20,25], ADX: [7,14,21,28], ADX threshold: [15,20,25,30,35], RSI: [7,14,21], timeframe: [H1,H4,D1]. Target: WR ≥ 55%."

opencode run --agent Hephaestus "Optimasi parameter untuk Kumo Breakout. Tenkan: [9,18,26,34], Kijun: [26,52], Senkou B: [26,52], Cloud thickness filter: [5,10,15 pips], Prev candle filter: [inside,outside,none]. Timeframe: [H1,H4,D1]. Target: ≥ 100 trades/year, WR ≥ 50%."

opencode run --agent Hephaestus "Optimasi parameter untuk Momentum Elder. Elder power threshold: [0.001,0.002,0.003,0.004], ADX confirmation: [≥20,≥25,≥30], Multi-timeframe: [yes,no], R/R: [1.5,2.0,2.5,3.0]. Timeframe: [H1,H4]. Target: WR ≥ 50%."

opencode run --agent Librarian "Research profitable strategies untuk: (1) EMA-based trend following, (2) Ichimoku cloud breakouts, (3) Momentum systems, (4) Volume-based trading. Sumber: TradingView, ForexFactory, academic papers. Output: daftar teknik terbukti profitable dengan parameter kira-kira."

opencode run --agent Librarian "Research XAUUSD volume characteristics. Sumber: yfinance data dengan volume. Analisis: volume distribution, outliers, daily/weekly patterns, time-of-day effects. Output: threshold volume yang realistis untuk XAUUSD (bukan 1.5 yang terlalu tinggi)."

opencode run --agent Explore "Quick backtest untuk setiap strategi dengan 5-10 parameter variants. Target: temukan 'quick win' yang menaikkan performa. Holy Grail: EMA [10,15,20] quick tests. Kumo: Tenkan [18,26,34] quick tests. Momentum Elder: Elder power threshold quick tests."
```

### Step 4: Review & Select (0.5 hari)
```bash
# Analyze semua hasil
# Pilih parameter terbaik untuk setiap strategi
# Generate optimized strategy files
# Validasi backtest results

opencode run --agent Oracle "Review semua hasil dari Hephaestus, Librarian, dan Explore. Pilih parameter terbaik untuk setiap strategi berdasarkan: WR ≥ 50%, PNL positive, Max DD ≤ 20%. Generate Python scripts untuk setiap strategy dengan parameter terbaik. Output: optimized_holy_grail.py, optimized_kumo.py, optimized_momentum_elder.py, optimized_volume_momentum.py."
```

### Step 5: Automated Paper Trading System (3-5 hari)
```bash
# Buat Fusion Markets automated trading system

opencode run --agent Oracle "Desain sistem automated paper trading untuk Fusion Markets. Components: (1) Trading Engine untuk XAUUSD Asia 7-Candle + 4 strategies optimized, (2) Risk Management (1% per trade, max 3 trades/day, stop after 3 consecutive losses, daily PNL limit -5%), (3) Signal Generation (real-time OHLCV, indicator calculation, signal generation, filtering), (4) Order Execution (market/stop orders, TP/SL, position monitoring), (5) Journaling (trade log, PNL calculation, metrics, daily/weekly reports). Output: fusion_paper_trading.py"

opencode run --agent Hephaestus "Implement Fusion Markets API integration untuk automated paper trading. Features: (1) Connect ke demo account, (2) Subscribe XAUUSD quotes, (3) Implement strategy classes, (4) Risk management logic, (5) Order placement dengan TP/SL, (6) Position monitoring, (7) Journal ke file, (8) Generate daily PNL report. Output: working fusion paper trading system."

opencode run --agent Librarian "Document Fusion Markets cTrader API untuk automated trading. Sumber: Fusion Markets API docs, cTrader Automated API documentation. Output: API examples dan best practices."
```

---

## Success Metrics

### Phase 1 (Quick Wins)
- [ ] Holy Grail: WR ≥ 45%, PNL ≥ $100
- [ ] Time to complete: ≤ 2 days

### Phase 2 (Deep Research)
- [ ] Holy Grail: WR ≥ 55%, PNL ≥ $100
- [ ] Kumo: WR ≥ 50%, PNL ≥ $50
- [ ] Momentum Elder: WR ≥ 50%, PNL ≥ $50
- [ ] Volume Momentum: WR ≥ 50%, PNL ≥ $50
- [ ] Time to complete: ≤ 5 days

### Phase 3 (Automated Paper Trading)
- [ ] Fusion Markets API integration working
- [ ] 5 strategies running in automated mode
- [ ] Risk management implemented
- [ ] Journaling working
- [ ] Daily/weekly reports generating
- [ ] Time to complete: ≤ 5 days

---

## Backup Plan

Jika oh-my-opencode tidak bekerja atau tidak menghasilkan profit:

### Alternative: Manual Optimization dengan Python
```bash
# Gunakan grid search manual
# Cek parameter space secara sistematis
# Validasi hasil dengan backtest
```

### Alternative: Copy Proven Strategies
```bash
# Copy XAUUSD Asia 7-Candle ke pair lain (GBPUSD, EURUSD, USDJPY)
# Timeframe testing: H1, H4, D1
# Parameter optimization: Min range filter, R/R ratio
```

### Alternative: Hybrid Strategies
```bash
# Combine Holy Grail dengan Asia session filter
# Combine Kumo dengan volume confirmation
# Combine Momentum Elder dengan ADX filter
```

---

*Research Plan Created: 2026-02-23*
*Using: oh-my-opencode with multi-agent research*
*Goal: Optimize all strategies to WR ≥ 50%, PNL positive*
*Phase 1: Quick Wins (1-2 days)*
*Phase 2: Deep Research (3-5 days)*
*Phase 3: Automated Paper Trading (3-5 days)*
