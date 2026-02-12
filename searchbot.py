#!/usr/bin/python3

# Web server to host picamera2 picture after object processing

# Import http for http server
from http import server
from os import path

# Numpy for overlay stuff
import numpy as np

# Threading condition to syncronize http server with picamera
from threading import Condition

# Import Picamera2 library
from picamera2 import Picamera2

# The main architecture looks like this
# +-----------------------------------+
# | Picamera2 (Generates video frame) | (Producer)
# +-----------------------------------+
#                  |
#                  V (Consumer)
# +----------------------------------------+     +--------------------------------------+
# | Preview implementation that takes this |     | HTTP server connects to preview      |
# | and gives it to libav to output video  | <-- | and uses data for WebRTC connections |
# | for the webserver for WebRTC.          |     |                                      |
# +----------------------------------------+     +--------------------------------------+
#                              (Producer)            (Consumer)

# Preview implementation


# HTTP Server Request Handler
class ServerRequestHandler(server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory = 'dist', **kwargs)
    
    def do_GET(self):
        super().do_GET()

# HTTP Server initialization
httpd = server.ThreadingHTTPServer(('', 8000), ServerRequestHandler)
httpd.serve_forever()

# Picamera 2 initialization

