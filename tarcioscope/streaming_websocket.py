from struct import Struct
from ws4py.websocket import WebSocket

from pi_camera_wrapper import PiCameraWrapper
from broadcast_output import BroadcastOutput
from broadcast_thread import BroadcastThread

class StreamingWebSocket(WebSocket):
    JSMPEG_MAGIC = b'jsmp'
    JSMPEG_HEADER = Struct('>4sHH')

    def __init__(self):
        super(StreamingWebSocket, self).__init__()
        self.picamera = PiCameraWrapper()
        self.output = BroadcastOutput(self.picamera.camera)
        self.broadcast_thread = BroadcastThread(self.output.converter, cherrypy.engine)

    # def received_message(self, message):
    #     BroadcastThread(self.output.converter, cherrypy.engine)

    def opened(self):
        self.send(self.JSMPEG_HEADER.pack(self.JSMPEG_MAGIC, 320, 240), binary=True)
        self.broadcast_thread.start()
        self.picamera.start_streaming(self.output)
