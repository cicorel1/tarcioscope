import picamera

from struct import Struct
from time import sleep, time
from datetime import datetime

METER_MODE = 'spot'
RESOLUTION = (640, 480)
FRAMERATE = 24
VFLIP = True
HFLIP = True

class PiCameraWrapper(object):
    def __init__(self, meter_mode='spot', iso=200, exposure_mode='auto'):
        self.camera = picamera.PiCamera()
        self.camera.resolution = RESOLUTION
        self.camera.meter_mode = meter_mode
        self.camera.framerate = FRAMERATE
        self.camera.exposure_mode = exposure_mode
        self.camera.iso = iso
        self.camera.vflip = VFLIP
        self.camera.hflip = HFLIP
        self.camera.start_preview()

    def start_streaming(self, output):
        print('Starting video capture')
        self.camera.start_recording(output, format='yuv')

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
