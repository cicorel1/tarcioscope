import cherrypy

from ws4py.websocket import WebSocket
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool

from camera import Camera
from broadcast_output import BroadcastOutput

cherrypy.config.update({ 'server.socket_host': '0.0.0.0', 'server.socket_port': 9000 })
WebSocketPlugin(cherrypy.engine).subscribe()
cherrypy.tools.websocket = WebSocketTool()

class StreamingWebSocket(WebSocket):
    def __init__(self):
        self.camera = Camera()

    def opened(self):
        while True:
            output = BroadcastOuput(self.camera.camera)
            self.camera.start_streaming(self)

class App(object):
    @cherrypy.expose
    def index(self):
        return """<video src="/ws"></video>"""
      
    @cherrypy.expose
    def ws(self):
        cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))

cherrypy.quickstart(App(), '/', config={'/ws': {'tools.websocket.on': True,
                                                 'tools.websocket.handler_cls': StreamingWebSocket}})
