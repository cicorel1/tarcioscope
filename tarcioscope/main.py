import cherrypy

from ws4py.websocket import WebSocket
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool

from camera import Camera

cherrypy.config.update({ 'server.socket_port': 9000 })
WebSocketPlugin(cherrypy.engine).subscribe()
cherrypy.tools.websocket = WebSocketTool()

class StreamingWebSocket(WebSocket):
    def opened(self):
        # self.send(JSMPEG_HEADER.pack(JSMPEG_MAGIC, WIDTH, HEIGHT), binary=True)
        self.send()

class App(object):
    def __init__(self):
        self.picamera = Camera()

    @cherrypy.expose
    def ws(self):
        cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))

cherrypy.quickstart(App(), '/', config={'/ws': {'tools.websocket.on': True,
                                                 'tools.websocket.handler_cls': StreamingWebSocket}})
