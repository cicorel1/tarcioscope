from time import sleep
from struct import Struct
from geventwebsocket import WebSocketApplication

from logger import log
from pi_camera_wrapper import PiCameraWrapper
from broadcast_output import BroadcastOutput
from broadcast_greenlet import BroadcastGreenlet

JSMPEG_MAGIC = b'jsmp'
JSMPEG_HEADER = Struct('>4sHH')

class PiCameraStreamApplication(WebSocketApplication):
    picamera = PiCameraWrapper()
    output = BroadcastOutput(picamera)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.broadcast_greenlet = BroadcastGreenlet(self.output.converter, self.ws)

    def on_open(self):
        jsmpeg_header = JSMPEG_HEADER.pack(JSMPEG_MAGIC, self.picamera.camera.resolution)
        log("Connection opened. Sending header '%s'" % jsmpeg_header)
        self.ws.send(jsmpeg_header)

        # try:
        self.picamera.start_streaming(self.output)
        self.broadcast_greenlet.start()
        self.broadcast_greenlet.join()

            # while True:
            #     self.picamera.camera.wait_recording(1)
        # except KeyboardInterrupt:
        #     pass
        # finally:
        #     self.on_close(None)

    def on_close(self, reason):
        log('Closing socket. Reason: %s' % reason)
        self.ws.close()
        self.broadcast_greenlet.kill(block=False)
        self.picamera.stop_streaming()
