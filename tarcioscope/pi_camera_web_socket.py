from struct import Struct
from ws4py.websocket import WebSocket

from logger import log
from pi_camera_wrapper import PiCameraWrapper
from broadcast_output import BroadcastOutput

JSMPEG_MAGIC = b'jsmp'
JSMPEG_HEADER = Struct('>4sHH')

class PiCameraWebSocket(WebSocket):
    picamera = PiCameraWrapper()
    output = BroadcastOutput(picamera)

    def opened(self):
        jsmpeg_header = JSMPEG_HEADER.pack(JSMPEG_MAGIC, self.picamera.camera.resolution[0], self.picamera.camera.resolution[1])
        log("Connection opened. Sending header '%s'" % jsmpeg_header)
        self.send(jsmpeg_header, binary=True)

    def closed(self, code, reason=None):
        log('Closing socket. Reason: %s' % reason)
        self.picamera.stop_streaming()

    def received_message(self, message):
        log('Received message %s' % message.data)
