#
# Searchbot camera
#
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

class Camera:
    def __init__(self):
        self.picam2 = Picamera2()
        self.encoder = JpegEncoder()
        config = self.picam2.create_preview_configuration(main={"size": (640, 480)})
        self.output = None
        self.picam2.configure(config)
        
    def startRecording(self):
        self.picam2.start_recording(self.encoder, FileOutput(self.output))

    def stopRecording(self):
        self.picam2.stop_recording()

    def setOutput(self, output):
        self.output = output

    def getOutput(self):
        return self.output

