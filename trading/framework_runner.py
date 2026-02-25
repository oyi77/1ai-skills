#!/usr/bin/env python3
"""
Framework Strategy Runner
Add CLI interface to framework strategies
"""

import sys
import os
import argparse
from datetime import datetime
import json

# Import trading framework
try:
    from trading import Strategy, BrokerType, OHLCV
    from trading.strategy.templates.forex.holy_grail import HolyGrailStrategy
    from trading.strategy.templates.forex.kumo_breakout import KumoBreakoutStrategy
    from trading.strategy.templates.forex.momentum_elder import MomentumElderStrategy
    from trading.strategy.templates.crypto.volume_momentum import VolumeMomentumStrategy
    from trading.strategy.tradfi.commodities.xauusd_asia_7c_breakout.xauusd_asia_7c_breakout import Asia7CBreakout
    TRADING_AVAILABLE = True
except ImportError as e:
    print(f"❌ Trading framework import failed: {e}")
    TRADING_AVAILABLE = False

# Import yfinance for data
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    print("❌ yfinance not installed")
    YFINANCE_AVAILABLE = False

def download_ohlcv(symbol, start_date, end_date, interval="1d"):
    """Download OHLCV data using yfinance."""
    if not YFINANCE_AVAILABLE:
        raise ImportError("yfinance not available")

    ticker = yf.Ticker(symbol)
    df = ticker.history(start=start_date, end=end_date, interval=interval)

    if df.empty:
        raise ValueError(f"No data for {symbol} from {start_date} to {end_date}")

    # Convert to OHLCV list
    ohlcv_list = []
    for idx, row in df.iterrows():
        ohlcv_list.append(
            OHLCV(
                timestamp=idx,
                open=row['Open'],
                high=row['High'],
                low=row['Low'],
                close=row['Close'],
                volume=row['Volume']
            )
        )

    return ohlcv_list

def run_backtest(strategy_class, symbol, start_date, end_date, interval="1d", initial_balance=100):
    """Run backtest for given strategy."""
    print("="*80)
    print(f"FRAMEWORK BACKTEST: {strategy_class.__name__}")
    print("="*80)
    print(f"Symbol: {symbol}")
    print(f"Period: {start_date} to {end_date}")
    print(f"Initial Balance: ${initial_balance}")
    print("="*80)
    print()

    # Download data
    print("Downloading OHLCV data...")
    try:
        ohlcv_data = download_ohlcv(symbol, start_date, end_date, interval)
        print(f"✅ Downloaded {len(ohlcv_data)} candles")
    except Exception as e:
        print(f"❌ Failed to download data: {e}")
        return

    # Initialize strategy
    print("\nInitializing strategy...")

    # Asia7CBreakout has special init with config parameter
    if strategy_class.__name__ == 'Asia7CBreakout':
        strategy = strategy_class(config={
            'symbol': symbol,
            'initial_balance': initial_balance
        })
    else:
        strategy = strategy_class(config={
            'symbol': symbol,
            'timeframe': interval,
            'initial_balance': initial_balance
        })

    # Run backtest
    print("Running backtest...")
    try:
        # Try to use run_backtest or backtest method
        if hasattr(strategy, 'run_backtest'):
            print(f"Using {strategy_class.__name__}.run_backtest() method...")
            results = strategy.run_backtest(
                start_date=start_date,
                end_date=end_date
            )
        elif hasattr(strategy, 'backtest'):
            results = strategy.backtest(
                start_date=start_date,
                end_date=end_date,
                initial_balance=initial_balance
            )
        else:
            # Manual backtest if no backtest method
            print(f"⚠️  {strategy_class.__name__} has no backtest method")
            print("Using manual backtest logic...")
            results = manual_backtest(strategy, ohlcv_data, initial_balance)
    except Exception as e:
        print(f"❌ Backtest failed: {e}")
        import traceback
        traceback.print_exc()
        return

    # Display results
    print()
    print("="*80)
    print("BACKTEST RESULTS")
    print("="*80)

    if isinstance(results, dict):
        for key, value in results.items():
            print(f"{key}: {value}")
    else:
        print(f"Results: {results}")

    print("="*80)
    print()

    # Save results
    output_file = f"/tmp/{strategy_class.__name__.lower()}_backtest.json"
    with open(output_file, 'w') as f:
        json.dump(results if isinstance(results, dict) else {'result': str(results)}, f, indent=2)

    print(f"✅ Results saved to: {output_file}")
    print()

def manual_backtest(strategy, ohlcv_data, initial_balance=100):
    """Manual backtest logic for framework strategies."""
    balance = initial_balance
    trades = []

    # Try to generate signals from strategy
    for i in range(1, len(ohlcv_data)):
        prev_ohlcv = ohlcv_data[i-1:i]
        current_ohlcv = ohlcv_data[i:i+1]

        if len(prev_ohlcv) == 0 or len(current_ohlcv) == 0:
            continue

        try:
            # Try to generate signals
            if hasattr(strategy, 'generate_signals'):
                signals = strategy.generate_signals(prev_ohlcv + current_ohlcv)
            elif hasattr(strategy, 'on_bar'):
                # Call on_bar for each candle
                for bar in current_ohlcv:
                    strategy.on_bar(bar)
            else:
                print("⚠️  Strategy has no signal generation method")
                break
        except Exception as e:
            print(f"⚠️  Signal generation failed: {e}")
            break

    # Return basic results
    return {
        'strategy': strategy.name,
        'initial_balance': initial_balance,
        'final_balance': balance,
        'net_pnl': balance - initial_balance,
        'total_trades': len(trades),
        'notes': 'Manual backtest - may not use full strategy logic'
    }

def main():
    parser = argparse.ArgumentParser(description='Framework Strategy Runner')

    parser.add_argument('action', choices=['backtest', 'list'], help='Action')
    parser.add_argument('--strategy', help='Strategy name (holy-grail, kumo, momentum-elder, volume-momentum, asia-7c)')
    parser.add_argument('--symbol', default='GC=F', help='Trading symbol')
    parser.add_argument('--start-date', default='2025-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', default='2025-12-31', help='End date (YYYY-MM-DD)')
    parser.add_argument('--interval', default='1d', help='Timeframe (1d, 1h, 4h)')
    parser.add_argument('--initial-balance', type=float, default=100, help='Initial balance')

    args = parser.parse_args()

    if not TRADING_AVAILABLE:
        print("❌ Trading framework not available!")
        sys.exit(1)

    if args.action == 'list':
        print("="*80)
        print("AVAILABLE FRAMEWORK STRATEGIES")
        print("="*80)
        print()
        print("1. holy-grail        - Holy Grail (Forex)")
        print("2. kumo               - Kumo Breakout (Forex)")
        print("3. momentum-elder     - Momentum Elder (Forex)")
        print("4. volume-momentum    - Volume Momentum (Crypto)")
        print("5. asia-7c            - Asia 7-Candle Breakout (TradFi - XAUUSD)")
        print()
        print("="*80)
        return

    if args.action == 'backtest':
        if not args.strategy:
            print("❌ --strategy is required for backtest")
            print("Use --list to see available strategies")
            sys.exit(1)

        # Map strategy names to classes
        strategy_map = {
            'holy-grail': HolyGrailStrategy,
            'kumo': KumoBreakoutStrategy,
            'momentum-elder': MomentumElderStrategy,
            'volume-momentum': VolumeMomentumStrategy,
            'asia-7c': Asia7CBreakout
        }

        strategy_class = strategy_map.get(args.strategy)

        if not strategy_class:
            print(f"❌ Unknown strategy: {args.strategy}")
            print("Use --list to see available strategies")
            sys.exit(1)

        # Run backtest
        run_backtest(
            strategy_class=strategy_class,
            symbol=args.symbol,
            start_date=args.start_date,
            end_date=args.end_date,
            interval=args.interval,
            initial_balance=args.initial_balance
        )

        print("="*80)
        print("COMPLETE")
        print("="*80)

if __name__ == "__main__":
    main()
