from struct import Struct
from ws4py.websocket import WebSocket

from logger import log
from broadcast_thread import BroadcastThread
from pi_camera_wrapper import FRAME_WIDTH, FRAME_HEIGHT

JSMPEG_MAGIC = b'jsmp'
JSMPEG_HEADER = Struct('>4sHH')

class PiCameraWebSocket(WebSocket):
    def opened(self):
        app = self.environ['ws4py.app']

        jsmpeg_header = JSMPEG_HEADER.pack(JSMPEG_MAGIC, FRAME_WIDTH, FRAME_HEIGHT)
        log("Connection opened. Sending header '%s'" % jsmpeg_header)

        self.broadcast_thread = BroadcastThread(app.picamera, self)
        self.send(jsmpeg_header, binary=True)
        self.broadcast_thread.start()

    def closed(self, code, reason=None):
        log('Closing socket. Reason: %s' % reason)
        self.broadcast_thread.join()
