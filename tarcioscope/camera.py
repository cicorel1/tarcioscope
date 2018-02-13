import picamera

from struct import Struct
from time import sleep, time
from datetime import datetime

METER_MODE = 'spot'
RESOLUTION = 'FHD'
FRAMERATE = 24
VFLIP = True
HFLIP = True


class Camera(object):
    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = RESOLUTION
        self.camera.meter_mode = METER_MODE
        self.camera.framerate = FRAMERATE
        self.camera.vflip = VFLIP # flips image rightside up, as needed
        self.camera.hflip = HFLIP # flips image left-right, as needed
        self.camera.start_preview()
 
    def start_streaming(self, websocket):
        print('Starting video capture')
        self.camera.start_recording(websocket.connection, format='mjpeg', resize='HD')
        while True:
            self.camera.wait_recording(1)

    def stop_streaming(self):
        print('Stopping video capture')
        self.camera.stop_recording()

    def snap(self):
        print('Camera recording status: %s' % self.camera.recording)

        if self.camera.recording:
            print('Stopping camera', end='...')
            self.stop_streaming()
            print('done!')

        file_name = '/tmp/%s.png' % datetime.now().strftime('%Y%m%d%H%M%S')
        print('Capturing image to "%s"' % file_name)

        sleep(2)

        self.camera.capture(file_name, format='png')

# camera = Camera()
# camera.start_streaming('/tmp/myvideo.h264')
# camera.snap()
