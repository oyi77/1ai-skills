#!/usr/bin/env python3
"""
Vector DB API Server
REST API for Vector DB operations
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys

sys.path.insert(0, '/home/openclaw/.openclaw/plugins')
sys.path.insert(0, '/home/openclaw/.openclaw/workspace/tools')

exec(open('/home/openclaw/.openclaw/workspace/vector_db_startup.py').read())

class VectorDBHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/status':
            status = vector_status()
            self._send_json(status)
        elif self.path == '/':
            self._send_html(
                "<h1>Vector DB API</h1>"
                "<p>Endpoints:</p>"
                "<ul>"
                "<li>/api/status - Check status</li>"
                "<li>/api/search - POST to search</li>"
                "<li>/api/index - POST to index</li>"
                "</ul>"
            )
        else:
            self._send_error(404, "Not found")
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            data = json.loads(body)
        except:
            self._send_error(400, "Invalid JSON")
            return
        
        if self.path == '/api/search':
            query = data.get('query', '')
            top_k = data.get('top_k', 5)
            results = vector_search(query, top_k=top_k)
            self._send_json({'results': results})
        elif self.path == '/api/index':
            content = data.get('content', '')
            title = data.get('title', '')
            source = data.get('source', '')
            doc_id = vector_index(content, title=title, source=source)
            self._send_json({'doc_id': doc_id})
        else:
            self._send_error(404, "Not found")
    
    def _send_json(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def _send_html(self, html):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def _send_error(self, code, message):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'error': message}).encode())

if __name__ == "__main__":
    PORT = 8765
    server = HTTPServer(('localhost', PORT), VectorDBHandler)
    print(f"🚀 Vector DB API running on http://localhost:{PORT}")
    server.serve_forever()