# fin-crypto-onchain: Multi-Chain Intelligence Framework

**REQUIRED SUB-SKILL:** Load `risk-guardian.md` before any position sizing. Verify asset jurisdiction compliance.

## 20-Indicator Market Heat Score (0–100)

Two scoring bands with different refresh cadences. Multi-chain coverage: Bitcoin, Ethereum, Solana, BNB Chain, Arbitrum, Optimism, Base.

---

## Daily Pulse Score (32 points total)

| Indicator | Max Pts | Bearish (0 pts) | Neutral | Bullish (max pts) | Data Source |
|-----------|---------|----------------|---------|------------------|-------------|
| Spot ETF Net Flows (7d) | 8 | Outflow >$500M | ±$100M | Inflow >$500M | Farside/Glassnode |
| Perpetual Funding Rate | 8 | >0.05% (overheated) | 0.01–0.03% | Slightly negative | Coinglass |
| Fear & Greed Index | 8 | >85 Extreme Greed | 45–55 | <15 Extreme Fear | Alternative.me |
| Long/Short Ratio | 8 | >2.0 (too many longs) | 0.9–1.1 | <0.7 (shorts dominate) | Coinglass |
| OI Change (7d) | 4 | –20% open interest drop | Stable | +30% OI increase | Coinglass |
| Stablecoin Supply | 4 | Inflows to exchanges | Flat | Outflows (buying) | Glassnode |

**Daily Pulse**: <8 = capitulation; >24 = heat building; 16–20 = neutral zone.

---

## Weekly Structure Score (68 points total)

| Indicator | Max Pts | Bear Signal | Neutral | Bull Signal | Chain |
|-----------|---------|------------|---------|-------------|-------|
| LTH-MVRV Z-Score | 12 | >7 (top zone) | 2–4 | <0 (capitulation) | BTC/ETH |
| NUPL | 10 | >0.75 (euphoria) | 0.25–0.50 | <0 (capitulation) | BTC |
| LTH-SOPR | 10 | >1.05 (profit taking) | ~1.0 | <1.0 (LTH at loss) | BTC |
| STH-SOPR | 8 | >1.05 (new buyers up) | ~1.0 | <0.95 (underwater) | BTC/ETH |
| LTH Supply % | 8 | <60% (distribution) | 62–68% | >70% (accumulation) | BTC |
| Price vs 365d MA | 8 | >3.5× (overextension) | 1.0–1.5× | <1.0× (below MA) | All |
| Price vs 200w MA | 6 | >4× | 1.5–2.5× | <1× (historical buy) | BTC |
| Weekly RSI | 3 | >80 | 50–65 | <30 | All |
| Weekly Volume Change | 3 | –40% declining | Stable | +50% expanding | All |

---

## Multi-Chain DeFi Metrics

### Solana
- **TVL**: Total value locked (DefiLlama)
- **Daily active addresses**: >500K = healthy; <200K = contraction
- **DEX volume (7d)**: Jupiter, Raydium dominance check
- **Validator concentration**: Top 10 validators <33% = decentralized

### Ethereum L2s (Arbitrum, Optimism, Base)
- **TVL growth**: MoM change, bridge inflows
- **Daily transactions**: Gas fees impact (L2 <$0.10 = adoption)
- **Bridge risk**: Official bridge vs. third-party, audit status

### BNB Chain
- **DEX volume**: PancakeSwap dominance, centralization risk
- **Validator set**: 21 validators (centralized), Binance relationship
- **BSC ecosystem**: GameFi, NFT activity trends

---

## Exchange Flow Intelligence

### Inflow / Outflow Signals
- **Exchange inflows rising**: Potential selling pressure (hs=holders -> exchange)
- **Exchange outflows (BTC to cold storage)**: Accumulation / long-term holding
- **Stablecoin inflows to exchanges**: Dry powder ready to buy (USDT/USDC)
- **Stablecoin outflows**: Risk-off, moving to self-custody or fiat off-ramp

### Whale Tracking (Multi-Chain)
- **Bitcoin**: Wallets >1,000 BTC; 30-day net accumulation
- **Ethereum**: Wallets >10,000 ETH; validator queue length
- **Solana**: Wallets >100,000 SOL; staking yield trend
- **OTC desks**: Genesis, Cumberland inventory as institutional demand proxy

### Exchange Health Monitoring
- **Proof of Reserves**: Merkle tree verification, >95% solvency
- **Reserve ratios**: Bitcoin, Ethereum, USDT, USDC balances vs. liabilities
- **Withdrawal suspensions**: Past 90 days, user fund accessibility
- **Jurisdiction risk**: Binance (multiple), Coinbase (US regulated), Kraken (US)

---

## On-Chain Forensics & Network Health

### Network Activity
- **Daily active addresses**: Trend vs. price (divergence = warning)
- **Transaction count**: Payments vs. smart contract interactions
- **Fee revenue**: Burn mechanism (ETH EIP-1559), validator income
- **Hash rate (BTC)**: Difficulty adjustment, mining profitability

### Token Metrics
- **Circulating supply**: Inflation schedule, unlock schedules (vesting cliffs)
- **Staking yield**: Real yield (nominal – inflation), slash risk
- **Token distribution**: Top 10 holders %, foundation treasury
- **Vesting schedules**: Team, investors, ecosystem unlocks (check TokenTerminal)

### Smart Contract Risk (ERC-20, SPL, etc.)
- **Audit status**: CertiK, Trail of Bits, OpenZeppelin verification
- **TVL concentration**: >50% in single protocol = systemic risk
- **Contract upgradeability**: Proxy patterns, timelock, multisig admin
- **Exploit history**: Past hacks, bug bounties, insurance coverage

---

## Composite Market Heat Score Interpretation

| Score | Zone | Signal | Strategy | Position Size |
|-------|------|--------|----------|---------------|
| 0–15 | Extreme Fear / Capitulation | Strong Buy | Staged entry over 4–8 weeks | FULL (after gates) |
| 16–30 | Fear | Buy | Accumulate; DCA into weakness | REDUCED (75%) |
| 31–45 | Caution | Cautious Buy | Partial position; wait for confirmation | REDUCED (50%) |
| 46–55 | Neutral | Hold | No change; monitor for breakout | Maintain |
| 56–70 | Optimism | Trim | Start reducing; move stop to breakeven | REDUCED (50%) |
| 71–85 | Greed | Sell | Reduce 50–70%; hedge with puts | REDUCED (25%) |
| 86–100 | Extreme Greed / Euphoria | Strong Sell | Exit majority; deploy puts/shorts | CLOSE (keep 10%) |

---

## Key Data Sources (Prioritized)

| Source | Coverage | Use Case | Refresh |
|--------|----------|----------|--------|
| **Glassnode** | BTC/ETH LTH/STH, MVRV, NUPL, SOPR, flows | Weekly structure | Daily |
| **CryptoQuant** | Exchange flows, miner flows, funding rates | Daily pulse | Hourly |
| **Dune Analytics** | Custom queries, DeFi, NFT, L2 metrics | Custom analysis | Real-time |
| **DefiLlama** | TVL trends, protocol flows, chain comparison | DeFi health | Daily |
| **Coinglass** | Futures, long/short ratios, liquidation maps | Derivatives | Real-time |
| **TokenTerminal** | Fees, revenue, P/S ratios, unlock schedules | Valuation | Daily |
| **Etherscan/Blockchain.com** | Transaction-level forensics, address tracking | Forensic | Real-time |
| **The Block** | Institutional flow, VC investment, regulation | News/context | Daily |

---

## On-Chain Output Template

```
ASSET: [BTC / ETH / SOL / token]
DATE: [YYYY-MM-DD]
MARKET HEAT SCORE: [0–100] / Zone: [Extreme Fear → Extreme Greed]
BLOCKCHAIN: [Bitcoin / Ethereum / Solana / BNB / L2]

DAILY PULSE (/32): [score]
  ETF Flows (7d): $[amount] — [interpretation]
  Funding Rate: [%] — [longs paying/shorts paying]
  Fear & Greed: [score] — [zone]
  Long/Short: [ratio] — [who dominates]
  Open Interest Δ: [%] — [leverage building/unwinding]

WEEKLY STRUCTURE (/68): [score]
  LTH-MVRV Z: [value] — [capitulation/neutral/euphoria]
  NUPL: [value] — [zone]
  LTH-SOPR: [value] — [profit taking/holding]
  LTH Supply %: [%] — [accumulation/distribution]
  Price vs 365d MA: [×] — [below/above mean]
  Price vs 200w MA: [×] — [historical zone]

MULTI-CHAIN / DEFI:
  TVL: $[amount] ([±%] WoW) — [trend]
  Daily Active Addresses: [count] — [vs. 30d avg]
  DEX Volume (7d): $[amount] — [dominance]
  Staking Yield: [%] (real: [%]) — [inflation-adjusted]

EXCHANGE FLOWS:
  BTC to exchanges (7d): [amount] — [selling pressure]
  Stablecoin reserves: $[amount] — [dry powder]
  Exchange solvency: [%] — [verified via PoR]

WHALE ACTIVITY:
  >1k BTC wallets: [count] ([±] 30d) — [accumulation/distribution]
  Large transactions (>100btc): [count] — [institutional flow]

SIGNAL: [STRONG BUY / BUY / ACCUMULATE / HOLD / TRIM / SELL / STRONG SELL]
CONVICTION: [0.0–1.0] (T1:[%] T2:[%] T3:[%])
POSITION SIZE: [X%] portfolio | GATE STATUS: [FULL/REDUCED/SKIP]
```

---

## Red Flags — STOP and Verify

- Heat score >85 but no profit-taking plan
- LTH supply <55% but thesis is "institutional adoption"
- Funding rate >0.1% sustained but recommending "buy the dip"
- Exchange inflows >5k BTC/day but claiming "supply shock"
- Tether (USDT) depeg <$0.98 → systemic stablecoin risk
- Major exchange withdrawal suspension → liquidity trap
- Smart contract upgrade without timelock → rug risk

**All of these mean: Re-run risk gates. Reduce size or SKIP.**
