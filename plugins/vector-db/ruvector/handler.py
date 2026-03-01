# Vector DB Plugin - Ruvector Handler
# OpenClaw integration for Ruvector engine (multilingual)

from shared.engine import smart_chunk
from ruvector.engine import RuvectorEngine
import json

def handler(args: dict) -> dict:
    """Main handler for OpenClaw tool calls"""
    action = args.get('action', 'search')
    
    if action == 'search':
        query = args.get('query', '')
        top_k = args.get('top_k', 5)
        
        config = {'enabled': True, 'model': 'paraphrase-multilingual-mpnet-base-v2'}
        engine = RuvectorEngine(config)
        results = engine.search(query, top_k)
        
        return {
            'success': True,
            'results': [
                {
                    'content': r.content,
                    'score': r.score,
                    'metadata': r.metadata,
                    'language': r.metadata.get('language', 'unknown'),
                    'source': r.source
                }
                for r in results
            ],
            'engine': 'ruvector',
            'count': len(results),
            'query_language': engine.detect_language(query)
        }
    
    elif action == 'search_indonesian':
        query = args.get('query', '')
        top_k = args.get('top_k', 5)
        
        config = {'enabled': True, 'model': 'paraphrase-multilingual-mpnet-base-v2'}
        engine = RuvectorEngine(config)
        results = engine.search_by_language(query, 'id', top_k)
        
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
            'engine': 'ruvector',
            'count': len(results),
            'language_filter': 'id (Indonesian)'
        }
    
    elif action == 'index':
        content = args.get('content', '')
        doc_id = args.get('doc_id')
        title = args.get('title', '')
        source = args.get('source', '')
        
        chunks = smart_chunk(content)
        doc_id = doc_id or f"doc_{hash(content) % 100000}"
        
        config = {'enabled': True, 'model': 'paraphrase-multilingual-mpnet-base-v2'}
        engine = RuvectorEngine(config)
        
        engine.index_chunks(chunks, doc_id, {'title': title, 'source': source})
        
        # Get language distribution
        languages = {}
        for chunk in chunks:
            lang = engine.detect_language(chunk)
            languages[lang] = languages.get(lang, 0) + 1
        
        return {
            'success': True,
            'doc_id': doc_id,
            'chunks_indexed': len(chunks),
            'languages': languages,
            'engine': 'ruvector'
        }
    
    elif action == 'stats':
        config = {'enabled': True, 'model': 'paraphrase-multilingual-mpnet-base-v2'}
        engine = RuvectorEngine(config)
        stats = engine.get_stats()
        
        return {
            'success': True,
            'engine': 'ruvector',
            **stats
        }
    
    elif action == 'detect_language':
        text = args.get('text', '')
        config = {'enabled': True, 'model': 'paraphrase-multilingual-mpnet-base-v2'}
        engine = RuvectorEngine(config)
        lang = engine.detect_language(text)
        
        lang_names = {
            'id': 'Indonesian',
            'en': 'English',
            'mixed': 'Mixed/Multilingual'
        }
        
        return {
            'success': True,
            'detected_language': lang,
            'language_name': lang_names.get(lang, lang),
            'engine': 'ruvector'
        }
    
    else:
        return {
            'success': False,
            'error': f'Unknown action: {action}'
        }

# OpenClaw tool definitions
TOOLS = {
    'ruvector_search': {
        'description': 'Search Ruvector (multilingual, optimized for Indonesian)',
        'parameters': {
            'query': {'type': 'string', 'required': True},
            'top_k': {'type': 'integer', 'default': 5}
        },
        'handler': lambda args: handler({**args, 'action': 'search'})
    },
    'ruvector_search_indonesian': {
        'description': 'Search specifically for Indonesian content',
        'parameters': {
            'query': {'type': 'string', 'required': True},
            'top_k': {'type': 'integer', 'default': 5}
        },
        'handler': lambda args: handler({**args, 'action': 'search_indonesian'})
    },
    'ruvector_index': {
        'description': 'Index content to Ruvector with language detection',
        'parameters': {
            'content': {'type': 'string', 'required': True},
            'doc_id': {'type': 'string', 'optional': True},
            'title': {'type': 'string', 'optional': True},
            'source': {'type': 'string', 'optional': True}
        },
        'handler': lambda args: handler({**args, 'action': 'index'})
    },
    'ruvector_stats': {
        'description': 'Get Ruvector statistics (document count, language distribution)',
        'parameters': {},
        'handler': lambda args: handler({'action': 'stats'})
    },
    'ruvector_detect_language': {
        'description': 'Detect language of text',
        'parameters': {
            'text': {'type': 'string', 'required': True}
        },
        'handler': lambda args: handler({**args, 'action': 'detect_language'})
    }
}