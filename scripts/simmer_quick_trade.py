#!/usr/bin/env python3
"""Quick Simmer SIM trader - finds and trades live markets.
Runs via cron every 5 min. Uses SIM venue (virtual money).
"""
import os, sys, json, time
from datetime import datetime, timezone

API_KEY = os.environ.get("SIMMER_API_KEY", "sk_live_269696a939dec0c28c8165da1e3ba2a7f0367a1362a2b1cd412db1b033c07f1e")
TRADE_AMOUNT = float(os.environ.get("SIM_TRADE_AMOUNT", "5.0"))
MAX_TRADES = int(os.environ.get("SIM_MAX_TRADES", "3"))

def get_btc_direction():
    """Get BTC direction from CoinGecko."""
    import urllib.request
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"
        resp = urllib.request.urlopen(url, timeout=10)
        data = json.loads(resp.read())
        price = data['bitcoin']['usd']
        change = data['bitcoin']['usd_24h_change']
        return {"price": price, "change": change, "direction": "up" if change > 0 else "down"}
    except Exception as e:
        print(f"  Price fetch error: {e}")
        return None

def main():
    from simmer_sdk import SimmerClient
    
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"\n[{ts}] Simmer Quick Trader")
    
    client = SimmerClient(api_key=API_KEY, venue="sim")
    
    # Portfolio check
    port = client.get_portfolio()
    balance = port["sim_balance"]
    pnl = port["sim_pnl"]
    print(f"  Balance: ${balance:,.2f} | PnL: ${pnl:,.2f}")
    
    if balance < TRADE_AMOUNT:
        print("  Insufficient balance, skipping")
        return
    
    # Get signal
    signal = get_btc_direction()
    if not signal:
        print("  No price signal, skipping")
        return
    print(f"  BTC: ${signal['price']:,.0f} ({signal['change']:+.2f}%) → {signal['direction']}")
    
    # Get markets (with timeout protection)
    try:
        markets = client.get_markets(limit=10)
    except Exception as e:
        print(f"  Markets API timeout/error: {e}")
        return
    
    # Get existing positions
    positions = client.get_positions()
    pos_ids = set()
    for p in positions:
        d = vars(p) if hasattr(p, '__dict__') else {}
        if 'market_id' in d:
            pos_ids.add(d['market_id'])
    
    # Find tradeable markets
    trades = 0
    for m in markets:
        if trades >= MAX_TRADES:
            break
        if m.id in pos_ids:
            continue
        if 'Up or Down' not in m.question:
            continue
        prob = m.current_probability
        if not (0.15 < prob < 0.85):
            continue
        
        # Decide side based on signal + market probability
        if 'Bitcoin' in m.question:
            side = 'yes' if signal['direction'] == 'up' else 'no'
        elif 'Solana' in m.question or 'XRP' in m.question:
            # Alts follow BTC
            side = 'yes' if signal['direction'] == 'up' else 'no'
        else:
            continue
        
        print(f"  Trading: {m.question[:55]}")
        print(f"    Prob: {prob:.3f} → {side.upper()} ${TRADE_AMOUNT}")
        
        try:
            result = client.trade(
                market_id=m.id,
                side=side,
                amount=TRADE_AMOUNT,
                action='buy'
            )
            if result.success:
                print(f"    ✅ {result.shares_bought:.1f} shares, cost ${result.cost:.2f}")
                trades += 1
                pos_ids.add(m.id)
            else:
                reason = result.skip_reason or result.error or "unknown"
                print(f"    ❌ {reason}")
        except Exception as e:
            print(f"    ❌ Error: {e}")
        
        time.sleep(1)  # Rate limit
    
    # Final portfolio
    port = client.get_portfolio()
    print(f"  Final: ${port['sim_balance']:,.2f} | PnL: ${port['sim_pnl']:,.2f} | Trades: {trades}")

if __name__ == "__main__":
    main()
