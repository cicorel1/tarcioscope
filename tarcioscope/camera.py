import picamera

from struct import Struct
from time import sleep, time

WIDTH = 640
HEIGHT = 480
FRAMERATE = 24
JSMPEG_MAGIC = b'jsmp'
JSMPEG_HEADER = Struct('>4sHH')
VFLIP = False
HFLIP = False


class Camera(object):
    def __init__(self):
        with picamera.PiCamera() as self.camera:
            self.camera.resolution = (WIDTH, HEIGHT)
            self.camera.framerate = FRAMERATE
            self.camera.vflip = VFLIP # flips image rightside up, as needed
            self.camera.hflip = HFLIP # flips image left-right, as needed
            sleep(1) # camera warm-up time

    def start(self, outputstream):
        self.camera.start_recording(outputstream, format='mjpeg')
