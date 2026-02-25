#!/usr/bin/env python3
"""
Universal Backtest Runner
Works with ALL strategies - framework templates and simplified scripts
"""

import sys
import os
import argparse
import json
import pandas as pd
from datetime import datetime

# Setup paths
TRADING_DIR = "/home/openclaw/.openclaw/workspace/skills/1ai-skills/trading"
sys.path.insert(0, TRADING_DIR)

# Import frameworks
try:
    from trading.brokers.base import OHLCV
    FRAMEWORK_AVAILABLE = True
except ImportError:
    FRAMEWORK_AVAILABLE = False
    print("⚠️  Trading framework not available")

# Import data source
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    print("❌ yfinance not available")

# Import framework strategies
framework_strategies = {}
if FRAMEWORK_AVAILABLE:
    try:
        from trading.strategy.tradfi.commodities.xauusd_asia_7c_breakout.xauusd_asia_7c_breakout import Asia7CBreakout
        framework_strategies['asia-7c'] = Asia7CBreakout
        print("✅ Asia 7-Candle imported")
    except Exception as e:
        print(f"⚠️  Asia 7-Candle import failed: {e}")

    try:
        from trading.strategy.templates.forex.holy_grail import HolyGrailStrategy
        framework_strategies['holy-grail'] = HolyGrailStrategy
        print("✅ Holy Grail imported")
    except Exception as e:
        print(f"⚠️  Holy Grail import failed: {e}")

    try:
        from trading.strategy.templates.forex.kumo_breakout import KumoBreakoutStrategy
        framework_strategies['kumo'] = KumoBreakoutStrategy
        print("✅ Kumo Breakout imported")
    except Exception as e:
        print(f"⚠️  Kumo Breakout import failed: {e}")

    try:
        from trading.strategy.templates.forex.momentum_elder import MomentumElderStrategy
        framework_strategies['momentum-elder'] = MomentumElderStrategy
        print("✅ Momentum Elder imported")
    except Exception as e:
        print(f"⚠️  Momentum Elder import failed: {e}")

    try:
        from trading.strategy.templates.crypto.volume_momentum import VolumeMomentumStrategy
        framework_strategies['volume-momentum'] = VolumeMomentumStrategy
        print("✅ Volume Momentum imported")
    except Exception as e:
        print(f"⚠️  Volume Momentum import failed: {e}")

class UniversalBacktester:
    """Universal backtest engine for all strategies."""

    def __init__(self):
        self.results = []

    def download_data(self, symbol, start_date, end_date, interval="1d"):
        """Download OHLCV data using yfinance."""
        if not YFINANCE_AVAILABLE:
            raise ImportError("yfinance not available")

        # Convert symbol for yfinance
        if 'XAUUSD' in symbol:
            symbol_ticker = 'GC=F'
        elif 'USDJPY' in symbol:
            symbol_ticker = 'JPY=X'
        else:
            # Forex pairs: EUR/USD → EURUSD=X
            symbol_ticker = symbol.replace('/', '') + '=X'

        print(f"Downloading {symbol_ticker} data...")
        ticker = yf.Ticker(symbol_ticker)
        df = ticker.history(start=start_date, end=end_date, interval=interval)

        if df.empty:
            raise ValueError(f"No data for {symbol_ticker}")

        print(f"✅ Downloaded {len(df)} candles")

        # Remove timezone
        if df.index.tz is not None:
            df = df.tz_localize(None)

        return df

    def backtest_framework_strategy(self, strategy, start_date, end_date, initial_balance=100):
        """
        Backtest framework strategy.

        Strategy should have run_backtest() or backtest() method.
        """
        print(f"\nRunning backtest for {strategy.__class__.__name__}...")

        # Try to use run_backtest or backtest method
        if hasattr(strategy, 'run_backtest'):
            print(f"  Using {strategy.__class__.__name__}.run_backtest()...")
            try:
                results = strategy.run_backtest(start_date, end_date)
            except Exception as e:
                print(f"  ❌ run_backtest() failed: {e}")
                return None
        elif hasattr(strategy, 'backtest'):
            print(f"  Using {strategy.__class__.__name__}.backtest()...")
            try:
                # Try to parse dates
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                end_dt = datetime.strptime(end_date, '%Y-%m-%d')
                results = strategy.backtest(start_dt, end_dt, initial_balance)
            except Exception as e:
                print(f"  ❌ backtest() failed: {e}")
                return None
        else:
            print(f"  ⚠️  {strategy.__class__.__name__} has no backtest method")
            return None

        return results

    def backtest_simple_strategy(self, strategy_file, start_date, end_date, symbol, initial_balance=100):
        """Backtest simplified strategy script."""
        print(f"\nRunning backtest for {strategy_file}...")

        # Run the script
        import subprocess

        cmd = [
            '/home/openclaw/.trading-venv/bin/python',
            strategy_file,
            'backtest',
            start_date,
            end_date,
            '--initial-balance', str(initial_balance)
        ]

        if symbol:
            cmd.append('--symbol')
            cmd.append(symbol)

        result = subprocess.run(cmd, capture_output=True, text=True)

        print(result.stdout)
        if result.stderr:
            print(result.stderr)

        if result.returncode != 0:
            print(f"❌ Strategy failed with return code {result.returncode}")
            return None

        # Try to parse results from output
        # Look for "Net PNL:" line
        lines = result.stdout.split('\n')
        net_pnl = None
        win_rate = None
        total_trades = None

        for line in lines:
            if 'Net PNL:' in line:
                parts = line.split(':')
                if len(parts) > 1:
                    net_pnl = parts[1].strip().replace('$', '')
            elif 'Win Rate:' in line:
                parts = line.split(':')
                if len(parts) > 1:
                    win_rate = parts[1].strip().replace('%', '')
            elif 'Total Trades:' in line:
                parts = line.split(':')
                if len(parts) > 1:
                    total_trades = parts[1].strip()

        return {
            'strategy': strategy_file,
            'net_pnl': float(net_pnl) if net_pnl else 0,
            'win_rate': float(win_rate) if win_rate else 0,
            'total_trades': int(total_trades) if total_trades else 0,
            'raw_output': result.stdout
        }

    def compare_all_strategies(self, start_date, end_date, initial_balance=100):
        """Compare all strategies."""
        print("="*80)
        print("UNIVERSAL BACKTEST - ALL STRATEGIES")
        print("="*80)
        print(f"Period: {start_date} to {end_date}")
        print(f"Initial Balance: ${initial_balance}")
        print("="*80)
        print()

        all_results = []

        # Test framework strategies
        if framework_strategies:
            print("Testing Framework Strategies:")
            print("-"*80)
            print()

            for strategy_key, strategy_class in framework_strategies.items():
                print(f"\nStrategy: {strategy_key}")
                print("-"*80)

                results = self.backtest_framework_strategy(strategy_class, start_date, end_date, initial_balance)

                if results:
                    # Extract metrics
                    if isinstance(results, dict):
                        if 'win_rate' in results:
                            win_rate = results['win_rate']
                        elif 'pnl' in results:
                            # Asia 7-Candle has nested PNL
                            win_rate = results.get('win_rate', 0)

                        # Get PNL
                        if 'net_pnl' in results:
                            net_pnl = results['net_pnl']
                        elif 'pnl' in results:
                            if isinstance(results['pnl'], dict):
                                net_pnl = results['pnl'].get('usd', 0)
                            else:
                                net_pnl = results['pnl']

                        total_trades = results.get('total_trades', 0)

                    all_results.append({
                        'strategy': strategy_key,
                        'type': 'Framework',
                        'win_rate': win_rate if 'win_rate' in locals() else 0,
                        'net_pnl': net_pnl if 'net_pnl' in locals() else 0,
                        'total_trades': total_trades,
                        'status': 'Completed'
                    })

        # Test simplified strategies
        print()
        print("Testing Simplified Strategies:")
        print("-"*80)
        print()

        simple_strategies = [
            {
                'file': f"{TRADING_DIR}/simple_holy_grail_v2.py",
                'key': 'Holy Grail (GBPUSD)',
                'symbol': 'GBPUSD=X'
            },
            {
                'file': f"{TRADING_DIR}/simple_kumo_breakout.py",
                'key': 'Kumo Breakout (XAUUSD)',
                'symbol': 'GC=F'
            },
            {
                'file': f"{TRADING_DIR}/simple_momentum_elder.py",
                'key': 'Momentum Elder (XAUUSD)',
                'symbol': 'GC=F'
            },
            {
                'file': f"{TRADING_DIR}/simple_volume_momentum.py",
                'key': 'Volume Momentum (XAUUSD)',
                'symbol': 'GC=F'
            }
        ]

        for strategy_info in simple_strategies:
            print(f"\nStrategy: {strategy_info['key']}")
            print("-"*80)

            results = self.backtest_simple_strategy(
                strategy_info['file'],
                start_date,
                end_date,
                strategy_info.get('symbol'),
                initial_balance
            )

            if results:
                all_results.append({
                    'strategy': strategy_info['key'],
                    'type': 'Simplified',
                    'win_rate': results['win_rate'],
                    'net_pnl': results['net_pnl'],
                    'total_trades': results['total_trades'],
                    'status': 'Completed'
                })

        # Generate comparison report
        print()
        print("="*80)
        print("COMPARISON REPORT")
        print("="*80)
        print()

        # Sort by win rate
        sorted_results = sorted(all_results, key=lambda x: x['win_rate'], reverse=True)

        print(f"{'Strategy':<30} {'Type':<12} {'WR':<7} {'PNL':<10} {'Trades':<10}")
        print("-"*80)

        for i, r in enumerate(sorted_results, 1):
            pnl_str = f"${r['net_pnl']:+.2f}" if r['net_pnl'] != 0 else "$0.00"
            wr_str = f"{r['win_rate']:.1f}%"
            print(f"{i}. {r['strategy']:<28} {r['type']:<12} {wr_str:<7} {pnl_str:<10} {r['total_trades']:>10}")

        print()
        print("="*80)
        print("WINNERS (WR ≥ 55% and PNL > 0)")
        print("="*80)

        winners = [r for r in sorted_results if r['win_rate'] >= 55 and r['net_pnl'] > 0]

        if winners:
            for r in winners:
                print(f"✅ {r['strategy']}: WR {r['win_rate']:.1f}%, PNL ${r['net_pnl']:+.2f}")
        else:
            print("❌ No strategies met the criteria (WR ≥ 55% and PNL > 0)")

        # Save full results
        output_file = "/tmp/strategy_comparison.json"
        with open(output_file, 'w') as f:
            json.dump({
                'test_period': {'start': start_date, 'end': end_date},
                'initial_balance': initial_balance,
                'all_results': all_results,
                'winners': winners,
                'generated_at': datetime.now().isoformat()
            }, f, indent=2)

        print()
        print(f"✅ Full results saved to: {output_file}")

        return all_results

def main():
    parser = argparse.ArgumentParser(description='Universal Backtest Runner')

    parser.add_argument('action', choices=['backtest', 'compare'], help='Action')
    parser.add_argument('--strategy', help='Strategy name (asia-7c, holy-grail, kumo, momentum-elder, volume-momentum)')
    parser.add_argument('--symbol', help='Trading symbol (e.g., GC=F for XAUUSD)')
    parser.add_argument('--start-date', default='2025-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', default='2025-12-31', help='End date (YYYY-MM-DD)')
    parser.add_argument('--initial-balance', type=float, default=100, help='Initial balance')

    args = parser.parse_args()

    # Initialize backtester
    backtester = UniversalBacktester()

    if args.action == 'backtest':
        # Run single strategy backtest
        if not args.strategy:
            print("❌ --strategy is required for backtest")
            print("Available strategies: asia-7c, holy-grail, kumo, momentum-elder, volume-momentum")
            sys.exit(1)

        # Check if framework or simplified
        if args.strategy in framework_strategies:
            print(f"Testing framework strategy: {args.strategy}")
            results = backtester.backtest_framework_strategy(
                framework_strategies[args.strategy],
                args.start_date,
                args.end_date,
                args.initial_balance
            )
        else:
            # Find simplified strategy file
            strategy_files = {
                'holy-grail': f"{TRADING_DIR}/simple_holy_grail_v2.py",
                'kumo': f"{TRADING_DIR}/simple_kumo_breakout.py",
                'momentum-elder': f"{TRADING_DIR}/simple_momentum_elder.py",
                'volume-momentum': f"{TRADING_DIR}/simple_volume_momentum.py"
            }

            if args.strategy not in strategy_files:
                print(f"❌ Unknown strategy: {args.strategy}")
                sys.exit(1)

            print(f"Testing simplified strategy: {args.strategy}")
            results = backtester.backtest_simple_strategy(
                strategy_files[args.strategy],
                args.start_date,
                args.end_date,
                args.symbol,
                args.initial_balance
            )

        if results:
            print()
            print("="*80)
            print("BACKTEST RESULTS")
            print("="*80)

            if isinstance(results, dict):
                # Framework results
                for key, value in results.items():
                    if key != 'raw_output':
                        print(f"{key}: {value}")
            elif isinstance(results, dict):
                # Simplified results
                print(f"Strategy: {results['strategy']}")
                print(f"Win Rate: {results['win_rate']:.1f}%")
                print(f"Net PNL: ${results['net_pnl']:+.2f}")
                print(f"Total Trades: {results['total_trades']}")
            else:
                print(f"Results: {results}")

            print()
            print("="*80)
            print("COMPLETE")
            print("="*80)

    elif args.action == 'compare':
        # Compare all strategies
        all_results = backtester.compare_all_strategies(
            args.start_date,
            args.end_date,
            args.initial_balance
        )

if __name__ == "__main__":
    main()
