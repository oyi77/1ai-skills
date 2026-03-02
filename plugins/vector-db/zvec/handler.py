# Vector DB Plugin - ZVec Handler
# OpenClaw integration for ZVec engine

from shared.engine import VectorEngine, smart_chunk
from zvec.engine import ZVecEngine
import json

def handler(args: dict) -> dict:
    """Main handler for OpenClaw tool calls"""
    action = args.get('action', 'search')
    
    if action == 'search':
        query = args.get('query', '')
        top_k = args.get('top_k', 5)
        
        config = {'enabled': True, 'model': 'BAAI/bge-m3'}
        engine = ZVecEngine(config)
        results = engine.search(query, top_k)
        
        return {
            'success': True,
            'results': [
                {
                    'content': r.content,
                    'score': r.score,
                    'metadata': r.metadata,
                    'source': r.source
                }
                for r in results
            ],
            'engine': 'zvec',
            'count': len(results)
        }
    
    elif action == 'index':
        content = args.get('content', '')
        doc_id = args.get('doc_id')
        title = args.get('title', '')
        source = args.get('source', '')
        
        chunks = smart_chunk(content)
        doc_id = doc_id or f"doc_{hash(content) % 100000}"
        
        config = {'enabled': True, 'model': 'BAAI/bge-m3'}
        engine = ZVecEngine(config)
        engine.index_chunks(chunks, doc_id, {'title': title, 'source': source})
        
        return {
            'success': True,
            'doc_id': doc_id,
            'chunks_indexed': len(chunks),
            'engine': 'zvec'
        }
    
    elif action == 'status':
        config = {'enabled': True, 'model': 'BAAI/bge-m3'}
        engine = ZVecEngine(config)
        count = engine.collection.count() if hasattr(engine, 'collection') else 0
        
        return {
            'success': True,
            'engine': 'zvec',
            'documents_indexed': count,
            'model': 'BAAI/bge-m3',
            'status': 'active' if engine else 'inactive'
        }
    
    else:
        return {
            'success': False,
            'error': f'Unknown action: {action}'
        }

# OpenClaw tool definitions
TOOLS = {
    'zvec_search': {
        'description': 'Search ZVec vector database for semantic similarity',
        'parameters': {
            'query': {'type': 'string', 'required': True},
            'top_k': {'type': 'integer', 'default': 5}
        },
        'handler': lambda args: handler({**args, 'action': 'search'})
    },
    'zvec_index': {
        'description': 'Index content to ZVec vector database',
        'parameters': {
            'content': {'type': 'string', 'required': True},
            'doc_id': {'type': 'string', 'optional': True},
            'title': {'type': 'string', 'optional': True},
            'source': {'type': 'string', 'optional': True}
        },
        'handler': lambda args: handler({**args, 'action': 'index'})
    },
    'zvec_status': {
        'description': 'Check ZVec engine status',
        'parameters': {},
        'handler': lambda args: handler({'action': 'status'})
    }
}