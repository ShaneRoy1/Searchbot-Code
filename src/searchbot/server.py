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

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

class Server:
    def __init__(self, port: int=8000):
    
        #camera is initialized here, rather than in main, so output can be saved and referenced later
        self.camera = Camera()
        try:
            self.camera.setOutput(StreamingOutput())
            self.camera.startRecording()
            global output
            output = self.camera.getOutput()
            self.httpd = StreamingServer(('', port), StreamingHandler)
            self.httpd.serve_forever()
            
        finally:
            self.camera.stopRecording()

#camera outputs to this
class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


# basic http server
class StreamingHandler(server.SimpleHTTPRequestHandler):

    # dont think this constructor is actually needed (?)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory = 'dist', **kwargs)
        
    def do_GET(self):

        # mapping for the mjpeg stream
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
        #everything else is handled in super
        else:
            super().do_GET()
