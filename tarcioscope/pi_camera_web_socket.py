from struct import Struct
from ws4py.websocket import WebSocket

from logger import log
from broadcast_output import BroadcastOutput
from pi_camera_wrapper import PiCameraWrapper
from broadcast_greenlet import BroadcastGreenlet

FRAME_WIDTH = 320
FRAME_HEIGHT = 240
JSMPEG_MAGIC = b'jsmp'
JSMPEG_HEADER = Struct('>4sHH')

class PiCameraWebSocket(WebSocket):
    picamera = PiCameraWrapper(resolution=(FRAME_WIDTH, FRAME_HEIGHT))
    heartbeat_freq = 1

    def opened(self):
        jsmpeg_header = JSMPEG_HEADER.pack(JSMPEG_MAGIC, FRAME_WIDTH, FRAME_HEIGHT)
        log("Connection opened. Sending header '%s'" % jsmpeg_header)
        self.output = BroadcastOutput(self.picamera)
        self.picamera.start_streaming(self.output)
        self.broadcast_greenlet = BroadcastGreenlet(self.output.converter, self)
        self.send(jsmpeg_header, binary=True)
        self.broadcast_greenlet.start()
        self.broadcast_greenlet.join()

    def closed(self, code, reason=None):
        log('Closing socket. Reason: %s' % reason)
        self.output.flush()
        self.picamera.stop_streaming()
        self.broadcast_greenlet.kill(block=False)

    def received_message(self, message):
        log('Received message %s' % message.data)
