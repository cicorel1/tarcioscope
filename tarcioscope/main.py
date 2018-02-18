import cherrypy

from struct import Struct

from ws4py.websocket import WebSocket
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool

from camera import Camera
from broadcast_output import BroadcastOutput

cherrypy.config.update({ 'server.socket_host': '0.0.0.0', 'server.socket_port': 9000 })
WebSocketPlugin(cherrypy.engine).subscribe()
cherrypy.tools.websocket = WebSocketTool()

class StreamingWebSocket(WebSocket):
    JSMPEG_MAGIC = b'jsmp'
    JSMPEG_HEADER = Struct('>4sHH')

    def opened(self):
        self.send(self.JSMPEG_HEADER.pack(self.JSMPEG_MAGIC, 320, 240), binary=True)
        broadcast = BroadcastOutput(Camera())
        try:
            while True:
                buf = broadcast.converter.stdout.read(512)
                if buf:
                    cherrypy.engine.publish('websocket-broadcast', buf, binary=True)
                elif broadcast.converter.poll() is not None:
                    break
        finally:
            broadcast.converter.stdout.close()

class App(object):
    @cherrypy.expose
    def ws(self):
        cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))

cherrypy.quickstart(App(), '/', config={'/ws': {'tools.websocket.on': True,
                                                 'tools.websocket.handler_cls': StreamingWebSocket}})
