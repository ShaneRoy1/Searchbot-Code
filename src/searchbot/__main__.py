from .server import Server
from .camera import Camera

def main():
    try:
        camera = Camera()
        server = Server(camera, port = 8000)
        camera.startRecording()
    finally:
        camera.stopRecording()

if __name__ == "__main__":
    main()
