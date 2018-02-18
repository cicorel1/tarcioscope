from struct import Struct
from ws4py.websocket import WebSocket

from pi_camera_wrapper import PiCameraWrapper
from broadcast_output import BroadcastOutput

class StreamingWebSocket(WebSocket):
    JSMPEG_MAGIC = b'jsmp'
    JSMPEG_HEADER = Struct('>4sHH')

    def __init__(self):
        super(StreamingWebSocket, self).__init__()
        camera = PiCameraWrapper()
        broadcast = BroadcastOutput()

    def received_message(self, message):
        try:
            while True:
                buf = self.broadcast.converter.stdout.read(512)
                if buf:
                    # cherrypy.engine.publish('websocket-broadcast', buf, binary=True)
                    self.send(buf, binary=True)
                elif self.broadcast.converter.poll() is not None:
                    break
        finally:
            self.broadcast.converter.stdout.close()

    def opened(self):
        self.send(self.JSMPEG_HEADER.pack(self.JSMPEG_MAGIC, 320, 240), binary=True)


