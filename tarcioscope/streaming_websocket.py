import cherrypy

from struct import Struct
from ws4py.websocket import WebSocket

from pi_camera_wrapper import PiCameraWrapper
from broadcast_output import BroadcastOutput
from broadcast_thread import BroadcastThread


JSMPEG_MAGIC = b'jsmp'
JSMPEG_HEADER = Struct('>4sHH')


class StreamingWebSocket(WebSocket):
    # def __init__(self):
    #    super(StreamingWebSocket, self).__init__()
    #    self.picamera = PiCameraWrapper()
    #    self.output = BroadcastOutput(self.picamera.camera)
    #    self.broadcast_thread = BroadcastThread(self.output.converter, cherrypy.engine)

    # def received_message(self, message):
    #     BroadcastThread(self.output.converter, cherrypy.engine)
    #picamera = PiCameraWrapper()
    #output = BroadcastOutput(picamera)
    #broadcast_thread = BroadcastThread(output.converter, cherrypy.engine)
    #broadcast_thread.start()
    #picamera.start_streaming(output)
 
    def opened(self):
        self.send(JSMPEG_HEADER.pack(JSMPEG_MAGIC, 320, 240), binary=True)
