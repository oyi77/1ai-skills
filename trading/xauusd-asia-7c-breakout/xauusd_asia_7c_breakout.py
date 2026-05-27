# XAUUSD Asia 7-Candle Breakout Strategy
# Complete implementation with full statistics

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

class Asia7CBreakout:
    def __init__(self, config=None):
        self.config = {
            'symbol': 'XAUUSD',
            'pair': 'XAUUSD',
            'min_range_pips': 5,
            'rr_ratio': 2.0,
            'lot_size': 0.01,  # Mini lot
            'pip_value': 0.01,  # $0.10 per point for 0.01 lot
        }
        if config:
            self.config.update(config)
    
    def download_data(self, start_date, end_date):
        print(f"Downloading {self.config['symbol']} data...")
        ticker = yf.Ticker("GC=F")
        df = ticker.history(start=start_date, end=end_date, interval="1h")
        print(f"Downloaded {len(df)} bars")
        return df
    
    def run_backtest(self, start_date, end_date):
        df = self.download_data(start_date, end_date)
        
        if len(df) < 7:
            return {'error': 'Insufficient data'}
        
        # Remove timezone
        if df.index.tz is not None:
            df = df.tz_localize(None)
        
        df = df.copy()
        df['hour'] = df.index.hour
        
        # Asia session: 00:00-08:00 UTC (07:00-15:00 Jakarta)
        asia_mask = (df['hour'] >= 0) & (df['hour'] < 8)
        asia_df = df[asia_mask].copy()
        asia_df['date'] = asia_df.index.normalize()
        
        # Get COA (first candle of Asia session each day)
        coa_times = asia_df.groupby('date').first()
        
        trades = []
        
        for date, row in coa_times.iterrows():
            coa_datetime = pd.Timestamp(date)
            
            # Find COA in full dataframe
            try:
                idx = df.index.get_indexer([coa_datetime], method='nearest')[0]
            except:
                continue
            
            # Get 7-candle window
            start_idx = max(0, idx)
            end_idx = min(len(df), idx + 7)
            window = df.iloc[start_idx:end_idx]
            
            if len(window) < 7:
                continue
            
            # Calculate HH, LL, R
            hh = window['High'].max()
            ll = window['Low'].min()
            r = window.iloc[-1]['High'] - window.iloc[-1]['Low']
            
            if r < self.config['min_range_pips'] / 100:
                continue
            
            rr = self.config['rr_ratio']
            
            # SL/TP levels
            buy_entry = hh
            buy_sl = hh - r
            buy_tp = hh + (r * rr)
            
            sell_entry = ll
            sell_sl = ll + r
            sell_tp = ll - (r * rr)
            
            # Check next candles for trigger
            post = df.iloc[idx + 7:]
            bought, sold = False, False
            
            for ts, candle in post.iterrows():
                high = candle['High']
                low = candle['Low']
                close = candle['Close']
                
                # Buy Stop triggered
                if not bought and high >= buy_entry:
                    if close >= buy_tp:
                        pnl = r * rr
                    elif close <= buy_sl:
                        pnl = -r
                    else:
                        continue
                    trades.append({
                        'date': str(date.date()), 
                        'type': 'BUY', 
                        'pnl': pnl,
                        'pnl_usd': round(pnl * self.config['pip_value'] * 10, 2)  # Convert to USD
                    })
                    bought = True
                    
                # Sell Stop triggered
                if not sold and low <= sell_entry:
                    if close <= sell_tp:
                        pnl = r * rr
                    elif close >= sell_sl:
                        pnl = -r
                    else:
                        continue
                    trades.append({
                        'date': str(date.date()), 
                        'type': 'SELL', 
                        'pnl': pnl,
                        'pnl_usd': round(pnl * self.config['pip_value'] * 10, 2)
                    })
                    sold = True
                
                if bought and sold:
                    break
        
        # Calculate full statistics
        total = len(trades)
        wins = [t for t in trades if t['pnl'] > 0]
        losses = [t for t in trades if t['pnl'] < 0]
        
        gross_profit = sum(t['pnl'] for t in wins)
        gross_loss = abs(sum(t['pnl'] for t in losses))
        net_pnl = sum(t['pnl'] for t in trades)
        
        gross_profit_usd = sum(t['pnl_usd'] for t in wins)
        gross_loss_usd = abs(sum(t['pnl_usd'] for t in losses))
        net_pnl_usd = sum(t['pnl_usd'] for t in trades)
        
        win_rate = len(wins) / total * 100 if total > 0 else 0
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
        profit_factor_usd = gross_profit_usd / gross_loss_usd if gross_loss_usd > 0 else 0
        
        avg_win = gross_profit / len(wins) if wins else 0
        avg_loss = gross_loss / len(losses) if losses else 0
        avg_win_usd = gross_profit_usd / len(wins) if wins else 0
        avg_loss_usd = gross_loss_usd / len(losses) if losses else 0
        
        return {
            'pair': self.config['pair'],
            'period': f"{start_date} to {end_date}",
            'total_trades': total,
            'wins': len(wins),
            'losses': len(losses),
            'win_rate': round(win_rate, 1),
            'profit_factor': round(profit_factor, 2),
            'pnl': {
                'points': round(net_pnl, 2),
                'usd': round(net_pnl_usd, 2),
            },
            'avg_win': {
                'points': round(avg_win, 2),
                'usd': round(avg_win_usd, 2),
            },
            'avg_loss': {
                'points': round(avg_loss, 2),
                'usd': round(avg_loss_usd, 2),
            },
            'gross_profit': round(gross_profit, 2),
            'gross_loss': round(gross_loss, 2),
            'max_consecutive_wins': self._calc_consecutive(trades, is_win=True),
            'max_consecutive_losses': self._calc_consecutive(trades, is_win=False),
        }
    
    def _calc_consecutive(self, trades, is_win=True):
        """Calculate max consecutive wins or losses from full trades list"""
        if not trades:
            return 0
        max_seq = current = 0
        for t in trades:
            is_winning = t['pnl'] > 0
            if is_win and is_winning:
                current += 1
                max_seq = max(max_seq, current)
            elif not is_win and not is_winning:
                current += 1
                max_seq = max(max_seq, current)
            else:
                current = 0
        return max_seq
    
    def get_today_signal(self):
        """Get signal for today"""
        end = datetime.now()
        start = end - timedelta(days=10)
        
        df = self.download_data(start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))
        
        if len(df) < 7:
            return {'error': 'Insufficient data'}
        
        if df.index.tz is not None:
            df = df.tz_localize(None)
        
        df = df.copy()
        df['hour'] = df.index.hour
        df['date'] = df.index.normalize()
        
        today = df[df['date'] == datetime.now().date()]
        
        if len(today) == 0:
            return {'error': 'No data for today'}
        
        asia_mask = (today['hour'] >= 0) & (today['hour'] < 8)
        asia_today = today[asia_mask]
        
        if len(asia_today) == 0:
            return {'error': 'Asia session not started yet'}
        
        coa_time = asia_today.index[0]
        
        try:
            coa_idx = df.index.get_indexer([coa_time], method='nearest')[0]
        except:
            return {'error': 'Could not find COA index'}
        
        window = df.iloc[coa_idx:coa_idx+7]
        
        if len(window) < 7:
            return {'error': 'Incomplete 7-candle window'}
        
        hh = window['High'].max()
        ll = window['Low'].min()
        r = window.iloc[-1]['High'] - window.iloc[-1]['Low']
        
        rr = self.config['rr_ratio']
        
        return {
            'pair': self.config['pair'],
            'date': datetime.now().strftime('%Y-%m-%d'),
            'status': 'WAITING',
            'levels': {
                'hh': round(hh, 2),
                'll': round(ll, 2),
                'r': round(r, 2),
                'buy_stop': round(hh, 2),
                'buy_sl': round(hh - r, 2),
                'buy_tp': round(hh + (r * rr), 2),
                'sell_stop': round(ll, 2),
                'sell_sl': round(ll + r, 2),
                'sell_tp': round(ll - (r * rr), 2),
            }
        }


if __name__ == "__main__":
    import sys
    
    strategy = Asia7CBreakout()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'signal':
            result = strategy.get_today_signal()
            print(json.dumps(result, indent=2))
        
        elif command == 'backtest':
            if len(sys.argv) >= 4:
                result = strategy.run_backtest(sys.argv[2], sys.argv[3])
                print(json.dumps(result, indent=2))
            else:
                print("Usage: python xauusd_asia_7c_breakout.py backtest 2024-01-01 2024-12-31")
        else:
            print("Unknown command")
    else:
        print("Usage: python xauusd_asia_7c_breakout.py <command> [args]")
        print("Commands: signal, backtest")
