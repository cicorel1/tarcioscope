import cherrypy

from struct import Struct
from ws4py.websocket import WebSocket

JSMPEG_MAGIC = b'jsmp'
JSMPEG_HEADER = Struct('>4sHH')

class StreamingWebSocket(WebSocket):
    def closed(self, code, reason=None):
        print(code)
        print(reason)

    def received_message(self, message):
        print('received message')
        print(message)

    def opened(self):
        ws_header = JSMPEG_HEADER.pack(JSMPEG_MAGIC, 1920, 1080)
        print('Sending jsmp header')
        cherrypy.engine.publish('websocket-broadcast', ws_header, binary=True)
        #self.send(ws_header, binary=True)
