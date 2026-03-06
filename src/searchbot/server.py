#
# HTTP Server for search bot (provides configuration to user)
# 
from http import server
from os import path
from .camera import Camera

import io
import logging
import socketserver
from threading import Condition
#from functools import partial

#class RequestHandler(server.SimpleHTTPRequestHandler):
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, directory = 'dist', **kwargs)
#    
#    def do_GET(self):
#        super().do_GET()

#class Server:
#    def __init__(self, port: int = 8000):
#        self.httpd = server.ThreadingHTTPServer(('', port), RequestHandler)
#        self.httpd.serve_forever()

# new stuff

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

class Server:
    def __init__(self, port: int=8000):
        self.camera = Camera()
        try:
            self.camera.setOutput(StreamingOutput())
            self.camera.startRecording()
            global output
            output = self.camera.getOutput()
            #handler = partial(StreamingHandler, output=self.output)
            #handler.setOutput(self.output)
            self.httpd = StreamingServer(('', port), StreamingHandler)
            self.httpd.serve_forever()
            
        finally:
            self.camera.stopRecording()

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

# class StreamingHandler(server.BaseHTTPRequestHandler):
#     def do_GET(self):
#         if self.path == '/':
#             self.send_response(301)
#             self.send_header('Location', '/index.html')
#             self.end_headers()
#         elif self.path == '/index.html':
#             with open('././dist/index.html', 'rt') as f:
#                 file_content = f.read()
#             content = file_content.encode('utf-8')
#             self.send_response(200)
#             self.send_header('Content-type', 'text/html')
#             self.send_header('Content-length', len(content))
#             self.end_headers()
#             self.wfile.write(content)
#         elif self.path == '/stream.mjpg':
#             self.send_response(200)
#             self.send_header('Age', 0)
#             self.send_header('Cache-Control', 'no-cache, private')
#             self.send_header('Pragma', 'no-cache')
#             self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
#             self.end_headers()
#             try:
#                 while True:
#                     with output.condition:
#                         output.condition.wait()
#                         frame = output.frame
#                     self.wfile.write(b'--FRAME\r\n')
#                     self.send_header('Content-Type', 'image/jpeg')
#                     self.send_header('Content-Length', len(frame))
#                     self.end_headers()
#                     self.wfile.write(frame)
#                     self.wfile.write(b'\r\n')
#             except Exception as e:
#                 logging.warning(
#                     'Removed streaming client %s: %s',
#                     self.client_address, str(e))
#         else:
#             self.send_error(404)
#             self.end_headers()

class StreamingHandler(server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory = 'dist', **kwargs)
        #self.output = output
        
    def do_GET(self):
        if self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            super().do_GET()
