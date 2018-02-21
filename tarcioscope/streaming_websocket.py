import cherrypy

from struct import Struct
from ws4py.websocket import WebSocket

JSMPEG_MAGIC = b'jsmp'
JSMPEG_HEADER = Struct('>4sHH')

class StreamingWebSocket(WebSocket):
    def opened(self):
        ws_header = JSMPEG_HEADER.pack(JSMPEG_MAGIC, 1920, 1080)
        cherrypy.engine.publish('websocket-broadcast', ws_header, binary=True)
