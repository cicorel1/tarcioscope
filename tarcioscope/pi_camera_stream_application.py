import logging

from time import sleep
from struct import Struct
from geventwebsocket import WebSocketApplication

from pi_camera_wrapper import PiCameraWrapper
from broadcast_output import BroadcastOutput
from broadcast_greenlet import BroadcastGreenlet

JSMPEG_MAGIC = b'jsmp'
JSMPEG_HEADER = Struct('>4sHH')
FRAME_WIDTH = 320
FRAME_HEIGHT = 240

class PiCameraStreamApplication(WebSocketApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.picamera = PiCameraWrapper(resolution=(FRAME_WIDTH, FRAME_HEIGHT))
        self.output = BroadcastOutput(self.picamera)
        self.broadcast_greenlet = BroadcastGreenlet(self.output.converter, self.ws)
        sleep(1) # camera warm-up
        logging.info('Camera warmed up.')

    def on_open(self):
        jsmpeg_header = JSMPEG_HEADER.pack(JSMPEG_MAGIC, FRAME_WIDTH, FRAME_HEIGHT)
        logging.info("Connection opened. Sending header '%s'", jsmpeg_header)
        self.ws.send(jsmpeg_header)

        try:
            self.picamera.start_streaming(self.output)
            self.broadcast_greenlet.start()
            self.broadcast_greenlet.join()

            while True:
                self.picamera.camera.wait_recording(1)
        except KeyboardInterrupt:
            pass
        finally:
            self.on_close(None)

    def on_close(self, reason):
        logging.info('Closing socket. Reason: %s', reason)
        self.picamera.stop_streaming()
