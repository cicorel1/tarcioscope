from struct import Struct
from ws4py.websocket import WebSocket


from . import logger
from . import broadcast_thread
from .pi_camera_wrapper import FRAME_WIDTH, FRAME_HEIGHT


JSMPEG_MAGIC = b'jsmp'
JSMPEG_HEADER = Struct('>4sHH')


class PiCameraWebSocket(WebSocket):
    def opened(self):
        app = self.environ['ws4py.app']

        jsmpeg_header = JSMPEG_HEADER.pack(JSMPEG_MAGIC, FRAME_WIDTH, FRAME_HEIGHT)
        logger.log("Connection opened. Sending header '%s'" % jsmpeg_header)

        self.bthread = broadcast_thread.BroadcastThread(app.picamera, self)
        self.send(jsmpeg_header, binary=True)
        self.bthread.start()


    def closed(self, code, reason=None):
        logger.log('Socket closed. Reason: %s. Joining broadcast thread.' % reason)
        self.bthread.join()
