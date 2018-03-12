import picamera
from datetime import datetime

from logger import log
from broadcast_output import BroadcastOutput

FRAME_WIDTH = 320
FRAME_HEIGHT = 240

class PiCameraWrapper(object):
    class __PiCameraWrapper:
        def __init__(self):
            self.camera = picamera.PiCamera()
            self.camera.resolution = (FRAME_WIDTH, FRAME_HEIGHT)
            self.camera.meter_mode = 'spot'
            self.camera.framerate = 24
            self.camera.exposure_mode = 'auto'
            self.camera.iso = 100
            log('##### CAMERA SETUP #####')
            log('# Resolution[%s x %s]' % self.camera.resolution[:2])
            log('# Meter mode[%s]' % self.camera.meter_mode)
            log('# Exposure mode[%s]' % self.camera.exposure_mode)
            log('# ISO[%s]' % self.camera.iso)
            log('########################')


        def start_streaming(self):
            log('Starting video capture')
            self.stop_streaming()

            broadcast_output = BroadcastOutput(self)
            self.camera.start_recording(broadcast_output, format='yuv')


        def stop_streaming(self):
            log('Stopping video capture...')
            if not self.camera.recording:
                self.camera.stop_recording()
            else:
                log('Camera already stopped. Doing nothing.')


        def snap(self):
            log('Camera recording status: %s' % self.camera.recording)
            self.stop_streaming()

            file_name = '/tmp/%s.png' % datetime.now().strftime('%Y%m%d%H%M%S')
            log('Capturing image to "%s"' % file_name)

            self.camera.resolution = 'FHD'
            self.camera.capture(file_name, format='png')
            self.camera.resolution = (FRAME_WIDTH, FRAME_HEIGHT)
            self.start_streaming()
            return file_name


    instance = None


    def __new__(self):
        if not PiCameraWrapper.instance:
            PiCameraWrapper.instance = PiCameraWrapper.__PiCameraWrapper()
        return PiCameraWrapper.instance


    def __getattr__(self, name):
        return getattr(self.instance, name)
