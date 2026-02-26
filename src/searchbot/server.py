#
# HTTP Server for search bot (provides configuration to user)
# 
from http import server
from os import path

class RequestHandler(server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory = 'dist', **kwargs)
    
    def do_GET(self):
        super().do_GET()

class Server:
    def __init__(self, port: int = 8000):
        self.httpd = server.ThreadingHTTPServer(('', port), RequestHandler)
        self.httpd.serve_forever()
