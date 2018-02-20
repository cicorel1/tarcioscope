import cherrypy

from struct import Struct
from ws4py.websocket import WebSocket

JSMPEG_MAGIC = b'jsmp'
JSMPEG_HEADER = Struct('>4sHH')

class StreamingWebSocket(WebSocket):
    def opened(self):
        self.send(JSMPEG_HEADER.pack(JSMPEG_MAGIC, 1920, 1080), binary=True)
