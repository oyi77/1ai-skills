# Vector DB Plugin
# Main plugin initialization for OpenClaw

__version__ = '1.0.0'
__author__ = 'Vilona AI'

from shared.engine import VectorEngine, smart_chunk, memory_search, index_document, semantic_similarity

def initialize(config: dict = None):
    """Initialize the plugin"""
    print("🔌 Initializing Vector DB Plugin...")
    
    engine = VectorEngine()
    available = list(engine.engines.keys())
    
    print(f"✅ Vector DB Plugin loaded")
    print(f"   Available engines: {', '.join(available)}")
    
    return {
        'engine': engine,
        'available_engines': available,
        'default_engine': engine.active_engine
    }

# Export main tools
__all__ = [
    'VectorEngine',
    'smart_chunk',
    'memory_search',
    'index_document',
    'semantic_similarity',
    'initialize'
]