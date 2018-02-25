import logging
import picamera

from datetime import datetime

METER_MODE = 'spot'
RESOLUTION = (640, 480)
FRAMERATE = 24
VFLIP = False
HFLIP = False

class PiCameraWrapper(object):
    def __init__(self, resolution=RESOLUTION, meter_mode='spot', iso=200, exposure_mode='auto'):
        self.camera = picamera.PiCamera()
        self.camera.resolution = resolution
        self.camera.meter_mode = meter_mode
        self.camera.framerate = FRAMERATE
        self.camera.exposure_mode = exposure_mode
        self.camera.iso = iso
        self.camera.vflip = VFLIP
        self.camera.hflip = HFLIP
        self.camera.start_preview()
        logging.info('Camera setup: Resoltuion[%s] | Meter mode[%s] | Frame rate[%s] | Exposure mode[%s] | ISO[%s]', resolution, meter_mode, FRAMERATE, exposure_mode, iso)

    def start_streaming(self, output):
        logging.info('Starting video capture')
        self.camera.start_recording(output, format='yuv')

    def stop_streaming(self):
        logging.info('Stopping video capture')
        self.camera.stop_recording()

    def snap(self):
        logging.info('Camera recording status: %s' % self.camera.recording)

        if self.camera.recording:
            logging.info('Stopping camera')
            self.stop_streaming()
            logging.info('Camera stopped!')

        file_name = '/tmp/%s.png' % datetime.now().strftime('%Y%m%d%H%M%S')
        logging.info('Capturing image to "%s"', file_name)

        self.camera.capture(file_name, format='png')
