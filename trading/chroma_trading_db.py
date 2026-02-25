#!/usr/bin/env python3
"""
VILONA CHROMA INTEGRATION - Trading System Vector Database
Menyimpan strategi, backtest results, dan trade patterns untuk semantic search
"""

import sys
import os
import argparse
import json
import hashlib
import numpy as np
from datetime import datetime
import yfinance as yf
import pandas as pd

# Chroma import
try:
    import chromadb
    from chromadb.config import Settings
    from chromadb.utils import embedding_functions
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
    print("⚠️  ChromaDB not installed. Install with: pip install chromadb")

# Sentence transformers for embeddings
try:
    from sentence_transformers import SentenceTransformer
    EMBEDDING_AVAILABLE = True
except ImportError:
    EMBEDDING_AVAILABLE = False
    print("⚠️  Sentence transformers not installed. Install with: pip install sentence-transformers")

class ChromaTradingDB:
    """ChromaDB untuk trading system."""

    def __init__(self, db_path="./chroma_trading_db"):
        self.db_path = db_path

        if CHROMA_AVAILABLE:
            # Initialize Chroma
            chroma_settings = Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )

            self.client = chromadb.Client(
                settings=chroma_settings,
                path=db_path
            )

            # Collections
            self.backtests_col = self.client.get_or_create_collection(
                name="backtests",
                metadata={"hnsw:space": "l2"}
            )

            self.strategies_col = self.client.get_or_create_collection(
                name="strategies",
                metadata={"hnsw:space": "l2"}
            )

            self.trade_journal_col = self.client.get_or_create_collection(
                name="trade_journal",
                metadata={"hnsw:space": "l2"}
            )

            self.best_practices_col = self.client.get_or_create_collection(
                name="best_practices",
                metadata={"hnsw:space": "l2"}
            )

            # Embedding model
            if EMBEDDING_AVAILABLE:
                self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            else:
                self.embedding_model = None
                print("⚠️  Using dummy embeddings (sentence-transformers not installed)")

            print(f"✅ ChromaDB initialized at {db_path}")

    def _embed_text(self, text):
        """Convert text ke vector embedding."""
        if self.embedding_model is not None:
            embedding = self.embedding_model.encode(text).tolist()
            return embedding
        else:
            # Dummy hash-based embedding
            hash_obj = hashlib.md5(text.encode())
            hash_hex = hash_obj.hexdigest()
            np.random.seed(int(hash_hex[:8], 16))
            return np.random.rand(384).astype(np.float32).tolist()

    def insert_backtest(self, pair, timeframe, strategy, config, metrics, notes=""):
        """Simpan hasil backtest."""
        if not CHROMA_AVAILABLE:
            return {"error": "ChromaDB not available"}

        # Create text for embedding
        text = f"""
        {pair} {timeframe} {strategy}
        Config: {json.dumps(config, separators=(',', ':'))}
        Metrics: WR {metrics.get('win_rate', 0)}% PNL {metrics.get('pnl', {}).get('usd', 0)}
        Notes: {notes}
        """

        # Create embedding
        embedding = self._embed_text(text)

        # Insert to Chroma
        try:
            self.backtests_col.add(
                documents=[text],
                embeddings=[embedding],
                metadatas=[{
                    "pair": pair,
                    "timeframe": timeframe,
                    "strategy": strategy,
                    "config": config,
                    "win_rate": metrics.get('win_rate', 0),
                    "pnl_usd": metrics.get('pnl', {}).get('usd', 0),
                    "profit_factor": metrics.get('profit_factor', 0),
                    "total_trades": metrics.get('total_trades', 0),
                    "max_drawdown": metrics.get('max_drawdown', 0),
                    "timestamp": datetime.now().isoformat()
                }],
                ids=[f"backtest_{pair}_{timeframe}_{strategy}_{datetime.now().isoformat()}"]
            )

            print(f"✅ Backtest inserted: {pair} {timeframe} {strategy}")

            return {"status": "success", "id": f"backtest_{pair}_{timeframe}_{strategy}"}

        except Exception as e:
            return {"error": f"Failed to insert backtest: {str(e)}"}

    def search_best_strategies(self, pair, min_win_rate=55, min_profit_factor=2.0, n_results=5):
        """Cari strategi terbaik untuk pair."""
        if not CHROMA_AVAILABLE:
            return []

        # Query text for semantic search
        query_text = f"Best performing strategies for {pair} with high win rate and profit factor"

        query_embedding = self._embed_text(query_text)

        # Query Chroma with filters
        results = self.backtests_col.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where={
                "pair": pair,
                "win_rate": {"$gte": min_win_rate},
                "profit_factor": {"$gte": min_profit_factor}
            }
        )

        print(f"🔍 Found {len(results['ids'])} strategies for {pair}")

        return results

    def insert_strategy_code(self, name, category, code, description, tags=[]):
        """Simpan strategy code."""
        if not CHROMA_AVAILABLE:
            return {"error": "ChromaDB not available"}

        # Create text
        text = f"""
        {name}
        Category: {category}
        Description: {description}
        Tags: {', '.join(tags)}
        Code: {code[:500]}...
        """

        embedding = self._embed_text(text)

        self.strategies_col.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[{
                "name": name,
                "category": category,
                "description": description,
                "tags": tags,
                "timestamp": datetime.now().isoformat()
            }],
            ids=[f"strategy_{name}_{datetime.now().isoformat()}"]
        )

        print(f"✅ Strategy code inserted: {name}")

    def search_strategy_code(self, query, category=None):
        """Cari strategy code."""
        if not CHROMA_AVAILABLE:
            return []

        query_embedding = self._embed_text(query)

        if category:
            results = self.strategies_col.query(
                query_embeddings=[query_embedding],
                n_results=10,
                where={"category": category}
            )
        else:
            results = self.strategies_col.query(
                query_embeddings=[query_embedding],
                n_results=10
            )

        return results

    def insert_trade_journal(self, pair, entry_price, exit_price, pnl, emotion, notes, strategy, trade_type="buy"):
        """Simpan jurnal trading."""
        if not CHROMA_AVAILABLE:
            return {"error": "ChromaDB not available"}

        # Create text
        text = f"""
        {pair} Trade {strategy}
        Type: {trade_type}
        Entry: {entry_price} Exit: {exit_price}
        PNL: {pnl} Emotion: {emotion}
        Notes: {notes}
        """

        embedding = self._embed_text(text)

        self.trade_journal_col.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[{
                "pair": pair,
                "entry_price": entry_price,
                "exit_price": exit_price,
                "pnl": pnl,
                "emotion": emotion,
                "notes": notes,
                "strategy": strategy,
                "trade_type": trade_type,
                "timestamp": datetime.now().isoformat()
            }],
            ids=[f"trade_{pair}_{datetime.now().isoformat()}"]
        )

        print(f"✅ Trade journal inserted: {pair}")

    def search_similar_trades(self, pair, current_conditions, n_results=10):
        """Cari trade historis yang mirip."""
        if not CHROMA_AVAILABLE:
            return []

        query_text = f"""
        {pair} {current_conditions}
        Similar historical trades
        """

        query_embedding = self._embed_text(query_text)

        results = self.trade_journal_col.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where={"pair": pair}
        )

        return results

    def insert_best_practice(self, category, title, content, tags=[]):
        """Simpan best practice."""
        if not CHROMA_AVAILABLE:
            return {"error": "ChromaDB not available"}

        text = f"""
        {title}
        Category: {category}
        Content: {content}
        Tags: {', '.join(tags)}
        """

        embedding = self._embed_text(text)

        self.best_practices_col.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[{
                "category": category,
                "title": title,
                "tags": tags,
                "timestamp": datetime.now().isoformat()
            }],
            ids=[f"bp_{category}_{title}_{datetime.now().isoformat()}"]
        )

        print(f"✅ Best practice inserted: {title}")

    def search_best_practices(self, query, category=None):
        """Cari best practice."""
        if not CHROMA_AVAILABLE:
            return []

        query_embedding = self._embed_text(query)

        if category:
            results = self.best_practices_col.query(
                query_embeddings=[query_embedding],
                n_results=10,
                where={"category": category}
            )
        else:
            results = self.best_practices_col.query(
                query_embeddings=[query_embedding],
                n_results=10
            )

        return results

def main():
    parser = argparse.ArgumentParser(description='Vilona Chroma Trading DB Integration')
    parser.add_argument('action', choices=[
        'insert-backtest', 'search-best', 'insert-strategy',
        'search-strategy', 'insert-journal', 'search-similar',
        'insert-best-practice', 'search-best-practices'
    ], help='Action')
    parser.add_argument('--pair', default='XAUUSD', help='Trading pair')
    parser.add_argument('--timeframe', default='H1', help='Timeframe')
    parser.add_argument('--strategy', help='Strategy name')
    parser.add_argument('--notes', default='', help='Additional notes')
    parser.add_argument('--top-k', type=int, default=5, help='Top K results')
    parser.add_argument('--query', help='Search query')

    args = parser.parse_args()

    # Initialize DB
    db = ChromaTradingDB()

    print("="*80)
    print("VILONA CHROMA TRADING DB")
    print("="*80)
    print(f"Action: {args.action}")
    print(f"Pair: {args.pair}")
    print(f"ChromaDB Available: {CHROMA_AVAILABLE}")
    print(f"Embedding Available: {EMBEDDING_AVAILABLE}")
    print("="*80)
    print()

    # Execute action
    if args.action == 'insert-backtest':
        # Import XAUUSD backtest result
        result_path = "/tmp/xauusd_final.json"

        if os.path.exists(result_path):
            with open(result_path, 'r') as f:
                data = json.load(f)

            config = {
                'min_range_pips': 5,
                'rr_ratio': 2.0,
                'lot_size': 0.01,
                'pip_value': 0.10,
            }

            result = db.insert_backtest(
                pair=data['pair'],
                timeframe=args.timeframe,
                strategy="Asia 7-Candle Breakout",
                config=config,
                metrics=data,
                notes=args.notes
            )

            print(json.dumps(result, indent=2))
        else:
            print(f"❌ Backtest file not found: {result_path}")

    elif args.action == 'search-best':
        results = db.search_best_strategies(
            pair=args.pair,
            min_win_rate=55,
            min_profit_factor=2.0,
            n_results=args.top_k
        )

        print("\nTop Strategies:")
        print("-"*80)
        for i, r in enumerate(results['ids'], 1):
            print(f"{i}. {r}")

    elif args.action == 'insert-journal':
        # Sample trade
        db.insert_trade_journal(
            pair=args.pair,
            entry_price=2024.50,
            exit_price=2025.20,
            pnl=20.70,
            emotion="Confident",
            notes="Followed Asia 7-Candle breakout",
            strategy="Asia 7-Candle Breakout",
            trade_type="buy"
        )

    elif args.action == 'search-similar':
        results = db.search_similar_trades(
            pair=args.pair,
            current_conditions="Asia session low volatility",
            n_results=args.top_k
        )

        print("\nSimilar Historical Trades:")
        print("-"*80)
        for i, r in enumerate(results['ids'], 1):
            print(f"{i}. {r}")

    elif args.action == 'insert-best-practice':
        db.insert_best_practice(
            category="risk_management",
            title="Max 1% Risk Per Trade",
            content="Never risk more than 1% of account balance on a single trade. Use 2:1 reward-to-risk ratio for XAUUSD Asia 7-Candle Breakout strategy.",
            tags=["risk", "position_sizing", "money_management"]
        )

    elif args.action == 'search-best-practices':
        results = db.search_best_practices(
            query="risk management strategies for trading"
        )

        print("\nBest Practices:")
        print("-"*80)
        for i, r in enumerate(results['ids'], 1):
            print(f"{i}. {r}")

    else:
        print(f"❌ Unknown action: {args.action}")

    print()
    print("="*80)
    print("COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
