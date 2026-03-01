# Vector DB Plugin - PageIndex Handler
# OpenClaw integration for PageIndex engine

from shared.engine import smart_chunk
from pageindex.engine import PageIndexEngine
import json

def handler(args: dict) -> dict:
    """Main handler for OpenClaw tool calls"""
    action = args.get('action', 'search')
    
    if action == 'search':
        query = args.get('query', '')
        top_k = args.get('top_k', 5)
        
        config = {'enabled': True, 'useGoogleAuth': False}
        engine = PageIndexEngine(config)
        results = engine.search(query, top_k)
        
        return {
            'success': True,
            'results': [
                {
                    'content': r.content,
                    'score': r.score,
                    'metadata': r.metadata,
                    'page': r.metadata.get('page', 'unknown'),
                    'section': r.metadata.get('section', 'unknown'),
                    'source': r.source
                }
                for r in results
            ],
            'engine': 'pageindex',
            'count': len(results)
        }
    
    elif action == 'index_document':
        content = args.get('content', '')
        doc_id = args.get('doc_id')
        title = args.get('title', '')
        source_type = args.get('source_type', 'text')
        
        # Create page markers for long documents
        lines = content.split('\n')
        page_size = 50
        paged_content = ""
        
        for i, line in enumerate(lines):
            if i % page_size == 0:
                paged_content += f"\n---PAGE {(i // page_size) + 1}---\n"
            paged_content += line + "\n"
        
        config = {'enabled': True, 'useGoogleAuth': False}
        engine = PageIndexEngine(config)
        
        chunks = [paged_content]
        doc_id = doc_id or f"doc_{hash(content) % 100000}"
        
        engine.index_chunks(chunks, doc_id, {
            'title': title,
            'source_type': source_type
        })
        
        return {
            'success': True,
            'doc_id': doc_id,
            'pages_approx': len(lines) // page_size + 1,
            'engine': 'pageindex'
        }
    
    elif action == 'index_pdf':
        pdf_path = args.get('pdf_path', '')
        doc_id = args.get('doc_id')
        
        try:
            import PyPDF2
            
            doc_id = doc_id or f"pdf_{hash(pdf_path) % 100000}"
            
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for i, page in enumerate(reader.pages):
                    text += f"\n---PAGE {i+1}---\n"
                    text += page.extract_text()
            
            config = {'enabled': True, 'useGoogleAuth': False}
            engine = PageIndexEngine(config)
            
            chunks = text.split('\n\n')
            engine.index_chunks(chunks, doc_id, {'source': pdf_path})
            
            return {
                'success': True,
                'doc_id': doc_id,
                'pages': len(reader.pages),
                'engine': 'pageindex'
            }
            
        except ImportError:
            return {
                'success': False,
                'error': 'PyPDF2 not installed. Run: pip install PyPDF2'
            }
    
    elif action == 'status':
        return {
            'success': True,
            'engine': 'pageindex',
            'status': 'active',
            'features': [
                'hierarchical_chunking',
                'page_tracking',
                'section_awareness',
                'pdf_support'
            ]
        }
    
    else:
        return {
            'success': False,
            'error': f'Unknown action: {action}'
        }

# OpenClaw tool definitions
TOOLS = {
    'pageindex_search': {
        'description': 'Search PageIndex with document structure awareness',
        'parameters': {
            'query': {'type': 'string', 'required': True},
            'top_k': {'type': 'integer', 'default': 5}
        },
        'handler': lambda args: handler({**args, 'action': 'search'})
    },
    'pageindex_index_document': {
        'description': 'Index document to PageIndex with page tracking',
        'parameters': {
            'content': {'type': 'string', 'required': True},
            'doc_id': {'type': 'string', 'optional': True},
            'title': {'type': 'string', 'optional': True},
            'source_type': {'type': 'string', 'default': 'text'}
        },
        'handler': lambda args: handler({**args, 'action': 'index_document'})
    },
    'pageindex_index_pdf': {
        'description': 'Index PDF file to PageIndex',
        'parameters': {
            'pdf_path': {'type': 'string', 'required': True},
            'doc_id': {'type': 'string', 'optional': True}
        },
        'handler': lambda args: handler({**args, 'action': 'index_pdf'})
    },
    'pageindex_status': {
        'description': 'Check PageIndex engine status',
        'parameters': {},
        'handler': lambda args: handler({'action': 'status'})
    }
}