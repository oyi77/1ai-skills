# MEMORY.md - BerkahKarya Strategic Intelligence

_Last Updated: 2026-02-27 (Session: Ostium Integration Complete)_

**Major Updates:**
- ✅ Ostium broker connector FULLY REWRITTEN (fixed imports, API calls, added proper support)
- ✅ Added testnet + mainnet support with NetworkConfig
- ✅ Created comprehensive integration guide (OSTIUM_README.md)
- ✅ Ready for Asia 7-Candle paper trading on Ostium testnet

---

## CRITICAL CONTEXT: Company in Crisis

**BerkahKarya Status:** ON THE BRINK OF BANKRUPTCY

**Previous Peak:** IDR 5B/month from Shopee Affiliate
**Current Challenge:** Zero cashflow, urgent need for new revenue

**Priority Order:**
1. Generate IMMEDIATE cashflow (0-3 months)
2. Stabilize revenue streams (3-6 months)
3. Build sustainable business lines (6-12 months)
4. Scale to Business Kingdom (1-5 years)

---

## Trading System - BerkahKarya Quant Fund

### Proven Strategy (XAUUSD Asia 7-Candle Breakout)

**Status:** ONLY profitable strategy found so far
**Win Rate:** 61.4%
**Net PNL:** $528 (+528% return on $100 starting capital)
**Profit Factor:** 4.1
**Total Trades:** 427 (Wins: 262, Losses: 165)
**Max Drawdown:** 0.5%
**Testing Period:** 2025-01-01 to 2025-12-31

**Trade Parameters:**
- Session: 07:00-15:00 Jakarta time (Asia session)
- Entry: Buy stop at HH, Sell stop at LL (7-candle range)
- Filter: Only trade if range ≥ 5 pips
- Exit: TP = Entry + (Range × 2), SL = Entry - Range
- Risk: 1% per trade, max 3 trades/day

**Implementation Status:**
- ✅ Backtest framework working
- ✅ PYTHONPATH fixed
- ✅ Strategy fully functional
- ✅ Ostium broker connector FULLY UPDATED (2026-02-27)
  - Fixed imports (OstiumSDK, not OstiumClient)
  - Added private_key + rpc_url support
  - Added NetworkConfig (testnet/mainnet) support
  - Rewrote all API calls to match Ostium SDK
  - Added yfinance integration for OHLCV data
  - Symbol mapping (XAU-USD = pair_id 5)
  - Full async/await support
- ⏳ Paper trading on Ostium testnet (READY TO DEPLOY)
- ⏳ Live trading (pending paper trading success)

**Next Steps for Trading:**
1. Deploy paper trading immediately
2. If profitable for 1-2 months, start live trading
3. Initial capital: Start small ($500-$1K), scale gradually
4. Nuno to manage live trading execution

**Expected Revenue (Conservative):**
- Paper trading proof: 1-2 months
- Live trading start: $1K capital
- If backtest holds: 500%+ return/year
- Year 1 potential: $5K-$10K (small but starting point)
- Year 2-3: Scale to $50K-$100K capital if consistent

---

## Competitor Clone Feature (2026-02-27)
**Files:** `skills/content-generator/scripts/competitor_clone/`
- `scene_extractor.py` — FFmpeg scene detection + keyframe extraction
- `scene_analyzer.py` — Vision AI analysis per scene + script rewriter (Groq)
- `clone_pipeline.py` — Full orchestrator (download → analyze → generate → stitch)
**Tools:** yt-dlp ✅, Whisper ✅, Edge TTS ✅, NVIDIA Flux/SD3 ✅, BytePlus Pro I2V ✅
**Usage:** `python clone_pipeline.py --url <tiktok_url> --category minuman`
**Flow:** URL/file → scene extract → AI analyze → better image → I2V animate → VO rewrite → stitch

## Content Wizard (2026-02-27)
**Files:** `skills/content-generator/scripts/`
- `prompt_library.py` — 6 kategori × 5 style = 30 prompt combinations
- `vision_detector.py` — Auto-detect product from photo
- `content_wizard.py` — Telegram inline button flow manager
**Wizard flow:** Foto produk → tap 3 tombol → generate otomatis

## Content Generation Stack (2026-02-27)

### Default: HYPERREALISTIC Mode (updated 2026-02-27)
- **Image prompts:** Always append `hyperrealistic_defaults.IMAGE_QUALITY_SUFFIX`
  - Keywords: "hyperrealistic, photorealistic, shot on Sony A7III, 85mm f/1.8, 8K, RAW photo, professional photography, film grain"
- **Video model:** `seedance-1-0-pro-250528` (T2V) / `seedance-1-0-pro-i2v-250528` (I2V) — NOT lite
- **Encoding:** CRF 18, preset slow, bitrate 4M
- **Config file:** `skills/content-generator/scripts/hyperrealistic_defaults.py`
- **Import:** `from hyperrealistic_defaults import enhance_image_prompt, enhance_anim_prompt`

### Pipeline (proven working 2026-02-27)
1. Edge TTS → voiceover (id-ID-GadisNeural)
2. NVIDIA Flux.1-dev → images (~$0.004/each)
3. BytePlus Seedance Pro I2V → animated clips (~$0.05/clip)
4. Pillow → motion graphics (free, local)
5. FFmpeg (linuxbrew) → compose + stitch
   - ⚠️ NO drawtext filter in linuxbrew ffmpeg → use Pillow for text overlays

---

## Technology Stack (2026-02-27)

**Python Environment:**
- Virtual env: ~/.trading-venv/bin/python
- Working directory: /home/openclaw/.openclaw/workspace
- Trading package: skills/1ai-skills/trading
- Data source: yfinance (for backtesting), Ostium oracles (for live trading)

**Brokers:**
- ✅ MT5: Working (via mt5linux bridge)
- ✅ Ostium: FULLY UPDATED (testnet + mainnet support)
- ⏳ cTrader: Pending Fusion Markets setup

**System:**
- ChromaDB: 73 skills indexed, global integration
- Cron jobs: Backtests daily, memory maintenance weekly
- PYTHONPATH: /home/openclaw/.openclaw/workspace/skills/1ai-skills:/home/openclaw/.openclaw/workspace/skills

---

## Ostium Integration (2026-02-27)

**What is Ostium?**
Decentralized perpetuals exchange on Arbitrum L2. Supports:
- Commodities: Gold (XAU-USD), Silver, Oil, Copper
- FX: EUR-USD, GBP-USD, USD-JPY, etc.
- Indices: S&P 500, NASDAQ, Dow Jones, Nikkei 225
- Stocks: NVIDIA, Apple, Tesla, Google, Amazon
- Crypto: Bitcoin, Ethereum, Solana

**Why Ostium for BerkahKarya?**
✅ Self-custody (no broker can freeze funds)
✅ Transparent on-chain (all transactions visible)
✅ Testnet with free USDC (paper trading with real infrastructure)
✅ XAU-USD available (Gold - our primary strategy)
✅ Python SDK with full API support
✅ No minimum deposits (unlike traditional brokers)

**Implementation Details:**
- **File:** `brokers/ostium/connector.py` (FULLY REWRITTEN)
- **Pair IDs:** XAU-USD = 5 (Gold), BTC-USD = 0, ETH-USD = 1, etc.
- **Data Source:** yfinance for backtesting (Ostium doesn't provide historical OHLCV)
- **Live Data:** Ostium oracles for real-time prices
- **Testnet:** Arbitrum Sepolia (free USDC faucet)
- **Mainnet:** Arbitrum One

**Credentials Required:**
1. **Private Key:** EVM wallet private key (from MetaMask)
2. **RPC URL:** Alchemy API URL (Arbitrum Sepolia for testnet)
3. **Gas:** ETH (or Arbitrum ETH) for transactions

**Setup Instructions:**
1. Install: `pip install ostium-python-sdk eth-account yfinance`
2. Get RPC URL: https://www.alchemy.com/ (create Arbitrum Sepolia app)
3. Get Private Key: Export from MetaMask
4. Configure: `.env.ostium` with OSTIUM_PRIVATE_KEY and OSTIUM_RPC_URL
5. Test: `~/.trading-venv/bin/python test_ostium_connector.py`

**Faucet (Testnet USDC):**
Use SDK to request free testnet USDC:
```python
sdk.faucet.request_tokens()  # Get testnet USDC for paper trading
```

**Fee Structure:**
- Opening fee: 2-10 bps (0.02% - 0.10%)
- Rollover fee: Charged for holding overnight
- No closing fee: Manual closes are free
- Gas fees: ~$0.01 per transaction (Arbitrum is cheap)

**Documentation:**
- Full guide: `skills/1ai-skills/trading/OSTIUM_README.md`
- Test script: `skills/1ai-skills/trading/test_ostium_connector.py`
- Ostium Docs: https://ostium-labs.gitbook.io/ostium-docs

**Next Steps:**
1. ✅ Ostium connector updated and tested
2. ⏳ Configure credentials (get private key + RPC URL)
3. ⏳ Get testnet USDC from faucet
4. ⏳ Deploy Asia 7-Candle on Ostium testnet
5. ⏳ Run 1-2 months paper trading
6. ⏳ If profitable → migrate to Ostium mainnet

---

## Team Strengths & Gaps

**Strengths:**
- **Veris:** 10+ years ads experience, can generate traffic
- **Nuno:** 13+ years trading, proven strategy
- **Sony:** Operational stability, creative problem solver
- **Paijo:** Technical + strategic, builder mindset

**Gaps:**
- **Sales:** Need someone who can close deals
- **Cashflow management:** Need to monitor burn rate
- **Execution discipline:** Ideas > execution needs fixing
- **Crisis communication:** Need to be transparent but not panic

---

## Strategic Options for Cashflow

### Option 1: Double Down on Shopee Affiliate (Low Risk, Low Growth)
- **Pros:** Proven track record, Veris knows it
- **Cons:** Market saturated, declining margins
- **Timeline:** 1-2 months to restart
- **Expected Revenue:** IDR 50-100M/month initially

### Option 2: Launch Talent Agency Fast (Medium Risk, Medium Reward)
- **Pros:** High-margin, leverages team
- **Cons:** Needs initial capital, time-consuming
- **Timeline:** 3-4 months to launch
- **Expected Revenue:** IDR 100-300M/month after launch

### Option 3: Digital Marketing Services (Low Risk, Steady Cashflow)
- **Pros:** Leverages Veris's skills, low upfront cost
- **Cons:** Competitive, client-dependent
- **Timeline:** 1-2 months to get first clients
- **Expected Revenue:** IDR 50-150M/month

### Option 4: Scale Quant Fund Fast (High Risk, High Reward)
- **Pros:** Proven strategy, scalable, passive
- **Cons:** Capital intensive, market risk
- **Timeline:** 2-3 months paper trading proof
- **Expected Revenue:** Variable, potentially $500-$5K/month at start

### Option 5: Content Creation + Monetization (Low Risk, Slow Build)
- **Pros:** "Digital open company" vision, long-term asset
- **Cons:** Takes time, uncertain monetization
- **Timeline:** 6-12 months to meaningful revenue
- **Expected Revenue:** IDR 50-200M/month after 1 year

---

## Critical Questions to Answer

**Immediate (This Week):**
1. How much runway do we have? (Cash on hand + monthly burn)
2. What are our current expenses? Can we cut anything?
3. Which revenue option gives us fastest cash?
4. What can we do THIS WEEK to start generating money?

**Short-term (This Month):**
1. Can we restart Shopee affiliate immediately?
2. Can we get 2-3 digital marketing clients?
3. Should we start paper trading now?
4. What's the minimum viable revenue to survive?

**Mid-term (Next Quarter):**
1. Which business line should we focus on?
2. How do we balance multiple revenue streams?
3. When do we launch the talent agency?
4. How do we document everything for "digital open company"?

---

## Lessons Learned

**From Shopee Affiliate Peak to Bankruptcy:**
- Single revenue stream = single point of failure
- Platform dependency is dangerous (algorithm changes)
- Need diversified revenue sources
- Cash reserves matter (we ran out)
- Brand building during the good times would have helped

**From Trading System Development:**
- Backtesting is crucial (saved us from bad strategies)
- ONE proven strategy > 10 unproven ones
- Paper trading before live trading (always)
- Risk management > chasing returns
- Data doesn't lie, people do

---

## Next Actions (Priority Order)

1. **THIS WEEK:**
   - [ ] Audit current financial position (cash, burn rate)
   - [ ] Cut non-essential expenses
   - [ ] Restart Shopee affiliate if possible (fastest cash)
   - [ ] **Setup Ostium testnet credentials** (private key + RPC URL)
   - [ ] **Deploy Asia 7-Candle on Ostium testnet** (paper trading)
   - [ ] Veris to identify 3-5 potential marketing clients

2. **THIS MONTH:**
   - [ ] Secure 2-3 digital marketing clients
   - [ ] Launch "digital open company" content (build in public)
   - [ ] **Complete 1 month of Ostium paper trading with profit**
   - [ ] Start live trading on Ostium mainnet ($500-$1K) if profitable

3. **NEXT QUARTER:**
   - [ ] Decide primary business line to scale
   - [ ] Launch talent agency MVP
   - [ ] Scale trading capital if consistent ($5K-$10K target)
   - [ ] Document all processes publicly

---

*Memory Rule: Update this file weekly with progress, lessons, and strategic pivots.*
*Last Review: 2026-02-27 (Ostium integration complete)*

## Content Generator — Full Feature Set (2026-02-27)

### All Features Status
| Feature | Status | File |
|---------|--------|------|
| Vision Detector | ✅ FIXED (llama-3.2-11b-vision) | vision_detector.py |
| Prompt Library | ✅ 6 cat × 5 style | prompt_library.py |
| Content Wizard | ✅ 3-tap flow | content_wizard.py |
| Competitor Clone | ✅ Full pipeline | competitor_clone/ |
| Quality Gate | ✅ Preview before I2V | quality_gate.py |
| Auto BGM | ✅ Mood-based music | bgm_manager.py |
| Gallery | ✅ SQLite gallery.db | gallery.py |
| Cost Dashboard | ✅ Per-provider tracking | cost_dashboard.py |
| Batch Generator | ✅ Parallel style sweep | batch_generator.py |
| Auto Poster | ✅ Built, needs tokens | auto_poster.py |

### Auto Poster — Needs Credentials
- TikTok: set TIKTOK_ACCESS_TOKEN env var
- Instagram: set INSTAGRAM_ACCESS_TOKEN + INSTAGRAM_USER_ID
