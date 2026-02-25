#!/usr/bin/env python3
"""
VILONA ZVEC INTEGRATION - Trading System
Menyimpan dan mencari strategi, backtest results, dan trade patterns
"""

import sys
import os
import json
import argparse
from datetime import datetime
import yfinance as yf
import pandas as pd
import numpy as np

# ZVEC import
try:
    import zvec
    ZVEC_AVAILABLE = True
except ImportError:
    ZVEC_AVAILABLE = False
    print("⚠️  ZVEC not installed. Install with: pip install zvec")

class ZvecTradingDB:
    """ZVEC database untuk trading system."""

    def __init__(self, db_path="./zvec_trading_db"):
        self.db_path = db_path

        if ZVEC_AVAILABLE:
            # Initialize schema
            self.schema = zvec.CollectionSchema(
                name="trading_system",
                vectors=zvec.VectorSchema(
                    "embedding",
                    zvec.DataType.VECTOR_FP32,
                    768  # Dimension (sesua dengan model)
                )
            )

            # Create database
            self.collection = zvec.create_and_open(db_path, schema=self.schema)
            print(f"✅ ZVEC database initialized at {db_path}")

    def insert_backtest(self, pair, timeframe, strategy, config, metrics):
        """Simpan hasil backtest."""
        if not ZVEC_AVAILABLE:
            return

        # Create embedding text
        text = f"""
        {pair} {timeframe} {strategy}
        Config: {json.dumps(config)}
        Metrics: WR {metrics.get('win_rate', 0)}% PNL {metrics.get('pnl', {}).get('usd', 0)}
        Profit Factor {metrics.get('profit_factor', 0)}
        """

        # Insert to ZVEC
        try:
            self.collection.insert(
                zvec.Doc(
                    id=f"backtest_{pair}_{timeframe}_{datetime.now().isoformat()}",
                    vectors=self._embed_text(text),
                    metadata={
                        "type": "backtest",
                        "pair": pair,
                        "timeframe": timeframe,
                        "strategy": strategy,
                        "config": config,
                        "metrics": metrics,
                        "win_rate": metrics.get('win_rate', 0),
                        "pnl_usd": metrics.get('pnl', {}).get('usd', 0),
                        "profit_factor": metrics.get('profit_factor', 0),
                        "max_drawdown": metrics.get('max_drawdown', 0),
                        "total_trades": metrics.get('total_trades', 0),
                        "timestamp": datetime.now().isoformat()
                    }
                )
            )
            print(f"✅ Backtest inserted: {pair} {timeframe} {strategy}")

        except Exception as e:
            print(f"❌ Failed to insert backtest: {e}")

    def search_best_strategies(self, pair, min_win_rate=55, min_profit_factor=2.0, top_k=5):
        """Cari strategi terbaik untuk pair."""
        if not ZVEC_AVAILABLE:
            return []

        # Create query vector for search
        query_text = f"{pair} high win rate high profit factor"
        query_vector = self._embed_text(query_text)

        # Query ZVEC
        results = self.collection.query(
            vectors=query_vector,
            filter=zvec.Filter(
                type="backtest",
                pair=pair,
                win_rate=zvec.GTE(min_win_rate),
                profit_factor=zvec.GTE(min_profit_factor)
            ),
            top_k=top_k
        )

        print(f"🔍 Found {len(results)} strategies for {pair}")
        return results

    def insert_strategy_code(self, name, category, code, description):
        """Simpan strategy code untuk code search."""
        if not ZVEC_AVAILABLE:
            return

        text = f"""
        {name}
        Category: {category}
        Description: {description}
        Code: {code[:500]}...
        """

        self.collection.insert(
            zvec.Doc(
                id=f"strategy_{name}_{datetime.now().isoformat()}",
                vectors=self._embed_text(text),
                metadata={
                    "type": "strategy_code",
                    "name": name,
                    "category": category,
                    "description": description,
                    "code": code,
                    "timestamp": datetime.now().isoformat()
                }
            )
        )

    def search_strategy_code(self, query, category=None):
        """Cari strategy code."""
        if not ZVEC_AVAILABLE:
            return []

        query_vector = self._embed_text(query)

        if category:
            results = self.collection.query(
                vectors=query_vector,
                filter=zvec.Filter(
                    type="strategy_code",
                    category=category
                ),
                top_k=10
            )
        else:
            results = self.collection.query(
                vectors=query_vector,
                filter=zvec.Filter(type="strategy_code"),
                top_k=10
            )

        return results

    def insert_trade_journal(self, pair, entry_price, exit_price, pnl, emotion, notes, strategy):
        """Simpan jurnal trading."""
        if not ZVEC_AVAILABLE:
            return

        text = f"""
        {pair} Trade {strategy}
        Entry: {entry_price} Exit: {exit_price} PNL: {pnl}
        Emotion: {emotion}
        Notes: {notes}
        """

        self.collection.insert(
            zvec.Doc(
                id=f"trade_{datetime.now().isoformat()}",
                vectors=self._embed_text(text),
                metadata={
                    "type": "trade_journal",
                    "pair": pair,
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "pnl": pnl,
                    "emotion": emotion,
                    "notes": notes,
                    "strategy": strategy,
                    "timestamp": datetime.now().isoformat()
                }
            )
        )

    def search_similar_trades(self, pair, current_market_conditions, top_k=10):
        """Cari trade historis yang mirip dengan kondisi sekarang."""
        if not ZVEC_AVAILABLE:
            return []

        query_text = f"""
        {pair} {current_market_conditions}
        Similar trades
        """

        results = self.collection.query(
            vectors=self._embed_text(query_text),
            filter=zvec.Filter(
                type="trade_journal",
                pair=pair
            ),
            top_k=top_k
        )

        return results

    def _embed_text(self, text):
        """Convert text ke vector embedding."""
        # Di production, ini akan menggunakan model embedding (OpenAI, sentence-transformers, dll.)
        # Untuk prototype, gunakan hash sederhana atau dummy vector
        import hashlib

        # Simple hash-based embedding (not optimal, but works for prototype)
        hash_obj = hashlib.md5(text.encode())
        hash_hex = hash_obj.hexdigest()

        # Convert hex ke float vector (768 dim)
        # Di production, ganti dengan: openai.Embedding.create(), sentence-transformers, dll.
        np.random.seed(int(hash_hex[:8], 16))
        embedding = np.random.rand(768).astype(np.float32)

        return embedding.tolist()

def main():
    parser = argparse.ArgumentParser(description='Vilona ZVEC Integration - Trading System')
    parser.add_argument('action', choices=['insert-backtest', 'search-best', 'insert-code', 'search-code', 'insert-journal', 'search-similar', 'import-xauusd'], help='Action')
    parser.add_argument('--db-path', default='./zvec_trading_db', help='Database path')
    parser.add_argument('--pair', default='XAUUSD', help='Trading pair')
    parser.add_argument('--timeframe', default='H1', help='Timeframe')
    parser.add_argument('--query', help='Search query')
    parser.add_argument('--top-k', type=int, default=5, help='Top K results')

    args = parser.parse_args()

    # Initialize DB
    db = ZvecTradingDB(args.db_path)

    print("="*80)
    print("VILONA ZVEC TRADING SYSTEM")
    print("="*80)
    print(f"Action: {args.action}")
    print(f"DB Path: {args.db_path}")
    print(f"ZVEC Available: {ZVEC_AVAILABLE}")
    print("="*80)
    print()

    # Execute action
    if args.action == 'import-xauusd':
        """Import XAUUSD Asia 7-Candle backtest results ke ZVEC."""
        result_path = "/tmp/xauusd_final.json"

        if os.path.exists(result_path):
            with open(result_path, 'r') as f:
                data = json.load(f)

            config = {
                'min_range_pips': 5,
                'rr_ratio': 2.0,
                'lot_size': 0.01
            }

            db.insert_backtest(
                pair=data['pair'],
                timeframe='H1',
                strategy='Asia 7-Candle Breakout',
                config=config,
                metrics=data
            )

            print("✅ XAUUSD Asia 7-Candle backtest imported to ZVEC")
        else:
            print(f"❌ Result file not found: {result_path}")

    elif args.action == 'search-best':
        """Cari strategi terbaik."""
        results = db.search_best_strategies(
            pair=args.pair,
            min_win_rate=55,
            min_profit_factor=2.0,
            top_k=args.top_k
        )

        print("\nTop Strategies:")
        print("-"*80)
        for i, r in enumerate(results, 1):
            print(f"{i}. {r.metadata['timeframe']} {r.metadata['strategy']}")
            print(f"   WR: {r.metadata['win_rate']}% PNL: ${r.metadata['pnl_usd']}")
            print(f"   PF: {r.metadata['profit_factor']} Trades: {r.metadata['total_trades']}")

    elif args.action == 'insert-code':
        """Insert strategy code."""
        db.insert_strategy_code(
            name="Asia 7-Candle Breakout",
            category="Breakout",
            description="Asia session 7-candle breakout strategy for XAUUSD",
            code="""
def backtest(start_date, end_date):
    # Download data
    ticker = yf.Ticker("GC=F")
    df = ticker.history(start=start_date, end=end_date, interval="1d")

    # Filter Asia session
    df = df.tz_localize(None)
    df['hour'] = df.index.hour
    asia_mask = (df['hour'] >= 0) & (df['hour'] < 8)
    asia_df = df[asia_mask]

    # Calculate 7-candle range
    for date, group in asia_df.groupby(asia_df.index.date):
        window = group.head(7)
        hh = window['High'].max()
        ll = window['Low'].min()
        r = window.iloc[-1]['High'] - window.iloc[-1]['Low']

        if r >= 5 / 100:  # 5 pips minimum
            # Entry signals
            buy_stop = hh
            sell_stop = ll
            target_long = hh + (r * 2)
            target_short = ll - (r * 2)
            stop_long = hh - r
            stop_short = ll + r

            # Simulate trades
            # ... (trading logic)
"""
        )
        print("✅ Strategy code inserted")

    elif args.action == 'search-code':
        """Cari strategy code."""
        results = db.search_strategy_code(
            query=args.query,
            category="Breakout"
        )

        print("\nSearch Results:")
        print("-"*80)
        for r in results:
            print(f"📄 {r.metadata['name']}")
            print(f"   Category: {r.metadata['category']}")
            print(f"   Description: {r.metadata['description']}")

    elif args.action == 'insert-journal':
        """Simpan contoh trade journal."""
        db.insert_trade_journal(
            pair=args.pair,
            entry_price=2024.50,
            exit_price=2025.20,
            pnl=20.70,
            emotion="Confident",
            notes="Followed Asia 7-Candle breakout",
            strategy="Asia 7-Candle Breakout"
        )
        print("✅ Trade journal inserted")

    elif args.action == 'search-similar':
        """Cari trade historis yang mirip."""
        results = db.search_similar_trades(
            pair=args.pair,
            current_market_conditions="Asia session low volatility",
            top_k=args.top_k
        )

        print("\nSimilar Historical Trades:")
        print("-"*80)
        for r in results:
            print(f"💰 PNL: {r.metadata['pnl']} Emotion: {r.metadata['emotion']}")
            print(f"   {r.metadata['notes']}")

    else:
        print(f"❌ Unknown action: {args.action}")

    print()
    print("="*80)
    print("COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
