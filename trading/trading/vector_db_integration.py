#!/usr/bin/env python3
"""
Vector DB Integration for Trading Skill
Enhanced trading analysis with semantic search
"""

import sys
sys.path.insert(0, '/home/openclaw/.openclaw/plugins')
sys.path.insert(0, '/home/openclaw/.openclaw/workspace/tools')

try:
    exec(open('/home/openclaw/.openclaw/workspace/vector_db_startup.py').read())
    VECTOR_DB_AVAILABLE = True
except:
    VECTOR_DB_AVAILABLE = False
    print("⚠️ Vector DB not available for trading")

def analyze_strategy(strategy_name: str):
    """
    Enhanced strategy analysis with Vector DB context
    
    Args:
        strategy_name: Trading strategy name
    
    Returns:
        Strategy analysis with historical context
    """
    if not VECTOR_DB_AVAILABLE:
        return None
    
    # Search for strategy info
    context = vector_search(strategy_name, top_k=5)
    
    # Filter high-relevance results
    relevant = [r for r in context if r['score'] > 0.5]
    
    return {
        'strategy': strategy_name,
        'context_found': len(context),
        'relevant_docs': len(relevant),
        'insights': [r['content'][:150] for r in relevant[:3]],
        'sources': [r.get('source') for r in relevant]
    }

def find_similar_setups(market_condition: str):
    """Find similar historical trading setups"""
    if not VECTOR_DB_AVAILABLE:
        return None
    
    results = vector_search(market_condition, top_k=5)
    
    return {
        'condition': market_condition,
        'similar_setups': results,
        'confidence_scores': [r['score'] for r in results]
    }

def verify_trade_setup(setup_description: str, min_confidence: float = 0.6):
    """Verify trade setup against historical data"""
    if not VECTOR_DB_AVAILABLE:
        return {'verified': False, 'reason': 'Vector DB unavailable'}
    
    results = vector_search(setup_description, top_k=3)
    
    if results and results[0]['score'] >= min_confidence:
        return {
            'verified': True,
            'confidence': results[0]['score'],
            'similar_setups': len(results),
            'reference': results[0]['content'][:100]
        }
    
    return {
        'verified': False,
        'highest_score': results[0]['score'] if results else 0
    }

__all__ = ['analyze_strategy', 'find_similar_setups', 'verify_trade_setup']

if __name__ == "__main__":
    if VECTOR_DB_AVAILABLE:
        result = analyze_strategy("Asia 7-Candle Breakout")
        print(f"Strategy analysis: {result['relevant_docs']} relevant docs")
    else:
        print("Vector DB not available")