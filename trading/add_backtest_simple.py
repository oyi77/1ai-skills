#!/usr/bin/env python3
"""
Add Backtest Methods to Template Strategies - Simplified Version
"""

import sys
import os

# Setup paths
TRADING_DIR = "/home/openclaw/.openclaw/workspace/skills/1ai-skills/trading"
sys.path.insert(0, TRADING_DIR)

BACKTEST_METHOD_CODE = '''
    def backtest(self, start_date, end_date, initial_balance=100):
        """
        Run backtest for {strategy_name} strategy.

        Args:
            start_date: Start date string (YYYY-MM-DD)
            end_date: End date string (YYYY-MM-DD)
            initial_balance: Starting balance (default: 100)

        Returns:
            Dictionary with backtest results
        """
        import yfinance as yf
        import pandas as pd
        from datetime import datetime
        import json

        # Download data
        symbol_ticker = self.symbol.replace('/', '-')
        if 'XAUUSD' in symbol_ticker:
            symbol_ticker = 'GC=F'
        elif 'USDJPY' in symbol_ticker:
            symbol_ticker = 'JPY=X'
        else:
            symbol_ticker += '=X'

        print(f"Downloading {{symbol_ticker}} data from {{start_date}} to {{end_date}}...")
        ticker = yf.Ticker(symbol_ticker)
        df = ticker.history(start=start_date, end=end_date, interval="1d")

        if df.empty:
            return {{'error': f'No data for {{symbol_ticker}}'}}

        print(f"Downloaded {{len(df)}} candles")

        # Remove timezone
        if df.index.tz is not None:
            df = df.tz_localize(None)

        # Initialize backtest
        balance = initial_balance
        trades = []
        signals = []

        # Calculate indicators
        print("Calculating indicators...")
        for i in range(len(df)):
            current_candle = df.iloc[i:i+1]
            timestamp = current_candle.index[0]
            ohlcv = self.OHLCV(
                timestamp=timestamp,
                open=current_candle['Open'].iloc[0],
                high=current_candle['High'].iloc[0],
                low=current_candle['Low'].iloc[0],
                close=current_candle['Close'].iloc[0],
                volume=current_candle['Volume'].iloc[0]
            )

            signals.append(ohlcv)

        # Generate trading signals
        print("Generating trading signals...")
        try:
            for i in range(len(signals)):
                if i < len(signals) - 1:
                    # Get signals for current candle
                    signal = self.generate_signals(signals[:i+1])

                    if signal:
                        # Simulate trade
                        entry = signals[i].close
                        sl = signals[i].low
                        tp = signals[i].high

                        # Simple 1:1 R/R for now
                        risk = entry - sl
                        if risk <= 0:
                            continue

                        if risk > 0:
                            # Long trade
                            tp_price = entry + abs(risk)
                            sl_price = sl
                        else:
                            # Short trade
                            tp_price = entry - abs(risk)
                            sl_price = signals[i].high

                        # Risk 1% of balance
                        risk_amount = balance * 0.01
                        lot_size = risk_amount / abs(risk)

                        # Simulate exit
                        pnl = 0
                        if i < len(signals) - 1:
                            next_candles = signals[i+1:min(i+10, len(signals))]

                            # Check if TP hit
                            for c in next_candles:
                                if risk > 0 and c.high >= tp_price:
                                    pnl = (tp_price - entry) * lot_size
                                    break
                                elif risk < 0 and c.low <= tp_price:
                                    pnl = (entry - tp_price) * lot_size
                                    break
                                elif risk > 0 and c.low <= sl_price:
                                    pnl = (sl_price - entry) * lot_size
                                    break
                                elif risk < 0 and c.high >= sl_price:
                                    pnl = (entry - sl_price) * lot_size
                                    break

                        balance += pnl
                        trades.append({{
                            'date': str(signals[i].timestamp),
                            'type': 'BUY' if risk > 0 else 'SELL',
                            'entry': entry,
                            'sl': sl_price,
                            'tp': tp_price,
                            'pnl': pnl,
                            'win': pnl > 0
                        }})

        except Exception as e:
            print(f"Signal generation error: {{e}}")
            return {{'error': str(e)}}

        # Calculate metrics
        wins = [t for t in trades if t['win']]
        losses = [t for t in trades if not t['win']]

        total_trades = len(trades)
        total_wins = len(wins)
        total_losses = len(losses)
        win_rate = (total_wins / total_trades * 100) if total_trades > 0 else 0

        net_pnl = balance - initial_balance

        total_profit = sum(t['pnl'] for t in wins)
        total_loss = abs(sum(t['pnl'] for t in losses))
        profit_factor = (total_profit / total_loss) if total_loss > 0 else 0

        avg_win = (total_profit / total_wins) if total_wins > 0 else 0
        avg_loss = (total_loss / total_losses) if total_losses > 0 else 0

        # Max drawdown
        peak = initial_balance
        trough = initial_balance
        for t in trades:
            balance_after = peak + sum(t['pnl'] for t in trades[:trades.index(t)+1])
            peak = max(peak, balance_after)
            trough = min(trough, balance_after)

        max_drawdown = ((peak - trough) / peak * 100) if peak > 0 else 0

        # Consecutive wins/losses
        max_consecutive_wins = 0
        max_consecutive_losses = 0
        current_consecutive_wins = 0
        current_consecutive_losses = 0

        for t in trades:
            if t['win']:
                current_consecutive_wins += 1
                current_consecutive_losses = 0
                max_consecutive_wins = max(max_consecutive_wins, current_consecutive_wins)
            else:
                current_consecutive_losses += 1
                current_consecutive_wins = 0
                max_consecutive_losses = max(max_consecutive_losses, current_consecutive_losses)

        return {{
            'pair': self.symbol,
            'strategy': '{strategy_name}',
            'initial_balance': initial_balance,
            'final_balance': balance,
            'net_pnl': net_pnl,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'total_trades': total_trades,
            'wins': total_wins,
            'losses': total_losses,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'max_consecutive_wins': max_consecutive_wins,
            'max_consecutive_losses': max_consecutive_losses,
            'max_drawdown': max_drawdown
        }}
'''

STRATEGIES = [
    {
        'file': f"{TRADING_DIR}/strategy/templates/forex/kumo_breakout.py",
        'strategy_name': 'Kumo Breakout'
    },
    {
        'file': f"{TRADING_DIR}/strategy/templates/crypto/volume_momentum.py",
        'strategy_name': 'Volume Momentum'
    }
]

def main():
    print("="*80)
    print("ADDING BACKTEST METHODS TO TEMPLATE STRATEGIES")
    print("="*80)
    print()

    for strategy_info in STRATEGIES:
        print(f"Processing: {strategy_info['strategy_name']}")
        print(f"File: {strategy_info['file']}")
        print()

        # Check if file exists
        if not os.path.exists(strategy_info['file']):
            print(f"⚠️  File not found: {strategy_info['file']}")
            print()
            continue

        # Check if backtest method already exists
        with open(strategy_info['file'], 'r') as f:
            content = f.read()

        if 'def backtest(' in content:
            print(f"⚠️  Backtest method already exists. Skipping.")
            print()
            continue

        # Add backtest method at the end of the file
        backtest_method = BACKTEST_METHOD_CODE.replace('{strategy_name}', strategy_info['strategy_name'])

        new_content = content + '\n' + backtest_method

        with open(strategy_info['file'], 'w') as f:
            f.write(new_content)

        print(f"✅ Backtest method added to {strategy_info['strategy_name']}")
        print()

    print("="*80)
    print("COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
