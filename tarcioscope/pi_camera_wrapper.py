import picamera

from logger import log
from datetime import datetime

METER_MODE = 'spot'
RESOLUTION = (640, 480)
FRAMERATE = 24
VFLIP = False
HFLIP = False

class PiCameraWrapper(object):
    class __PiCameraWrapper:
        def __init__(self, resolution, meter_mode, iso, exposure_mode):
            self.camera = picamera.PiCamera()
            self.camera.resolution = resolution
            self.camera.meter_mode = meter_mode
            self.camera.framerate = FRAMERATE
            self.camera.exposure_mode = exposure_mode
            self.camera.iso = iso
            self.camera.vflip = VFLIP
            self.camera.hflip = HFLIP
            self.camera.start_preview()
            log('##### CAMERA SETUP #####')
            log('# Resolution[%s x %s]' % resolution[:2])
            log('# Meter mode[%s]' % meter_mode)
            log('# Frame rate[%s]' % FRAMERATE)
            log('# Exposure mode[%s]' % exposure_mode)
            log('# ISO[%s]' % iso)
            log('########################')

        def start_streaming(self, output):
            log('Starting video capture')

            if self.camera.recording:
                log('Camera already recording. Stopping...')
                self.stop_streaming()

            self.camera.start_recording(output, format='yuv')

        def stop_streaming(self):
            log('Stopping video capture')
            self.camera.stop_recording()

        def snap(self):
            log('Camera recording status: %s' % self.camera.recording)

            if self.camera.recording:
                log('Stopping camera')
                self.stop_streaming()

            file_name = '/tmp/%s.png' % datetime.now().strftime('%Y%m%d%H%M%S')
            log('Capturing image to "%s"' % file_name)

            self.camera.capture(file_name, format='png')

    instance = None

    def __new__(self, resolution=RESOLUTION, meter_mode='spot', iso=200, exposure_mode='auto'):
        if not PiCameraWrapper.instance:
            PiCameraWrapper.instance = PiCameraWrapper.__PiCameraWrapper(resolution, meter_mode, iso, exposure_mode)
        return PiCameraWrapper.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)
