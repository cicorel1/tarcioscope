from time import sleep
from struct import Struct
from geventwebsocket import WebSocketApplication
from gevent import kill

from logger import log
from pi_camera_wrapper import PiCameraWrapper
from broadcast_output import BroadcastOutput
from broadcast_greenlet import BroadcastGreenlet

JSMPEG_MAGIC = b'jsmp'
JSMPEG_HEADER = Struct('>4sHH')
FRAME_WIDTH = 320
FRAME_HEIGHT = 240

class PiCameraStreamApplication(WebSocketApplication):
    picamera = PiCameraWrapper(resolution=(FRAME_WIDTH, FRAME_HEIGHT))
    output = BroadcastOutput(picamera)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.broadcast_greenlet = BroadcastGreenlet(self.output.converter, self.ws)
        # sleep(1) # camera warm-up
        # log('Camera warmed up.')

    def on_open(self):
        jsmpeg_header = JSMPEG_HEADER.pack(JSMPEG_MAGIC, FRAME_WIDTH, FRAME_HEIGHT)
        log("Connection opened. Sending header '%s'" % jsmpeg_header)
        self.ws.send(jsmpeg_header)

        try:
            self.picamera.start_streaming(self.output)
            self.broadcast_greenlet.start_later(1)
            # self.broadcast_greenlet.join()

            while True:
                self.picamera.camera.wait_recording(1)
        except KeyboardInterrupt:
            pass
        finally:
            self.on_close(None)

    def on_close(self, reason):
        log('Closing socket. Reason: %s' % reason)
        kill(self.broadcast_greenlet)
        self.picamera.stop_streaming()
