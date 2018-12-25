import picamera
from datetime import datetime

from tarcioscope.lib import logger
from tarcioscope.lib import streaming_output

FRAME_WIDTH = 640
FRAME_HEIGHT = 480

class PiCameraWrapper:
    class __PiCameraWrapper:
        def __init__(self):
            self.camera = picamera.PiCamera()
            self.camera.resolution = (FRAME_WIDTH, FRAME_HEIGHT)
            self.camera.meter_mode = 'spot'
            self.camera.exposure_mode = 'auto'
            self.camera.iso = 100
            self.camera.framerate = 24
            self.output = streaming_output.StreamingOutput()
            logger.log('##### CAMERA SETUP #####')
            logger.log('# Resolution[%s x %s]' % self.camera.resolution[:2])
            logger.log('# Meter mode[%s]' % self.camera.meter_mode)
            logger.log('# Exposure mode[%s]' % self.camera.exposure_mode)
            logger.log('# ISO[%s]' % self.camera.iso)
            logger.log('########################')

        def start_streaming(self):
            self.stop_streaming()
            logger.log('Starting video capture')
            self.camera.start_recording(self.output, format='mjpeg')

        def stop_streaming(self):
            if self.camera.recording:
                logger.log('Stopping video capture...')
                self.camera.stop_recording()
            else:
                logger.log('Camera already stopped. Nothing to do.')

        def snap(self):
            self.stop_streaming()

            file_name = '/tmp/%s.png' % datetime.now().strftime('%Y%m%d%H%M%S')
            logger.log('Capturing Full HD image to "%s".' % file_name)

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

