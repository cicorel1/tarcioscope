import cherrypy

from streaming_websocket import StreamingWebSocket
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool

cherrypy.config.update({ 'server.socket_host': '0.0.0.0', 'server.socket_port': 9000 })
WebSocketPlugin(cherrypy.engine).subscribe()
cherrypy.tools.websocket = WebSocketTool()

class App(object):
    @cherrypy.expose
    def ws(self):
        cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))

cherrypy.quickstart(App(), '/', config={'/ws': {'tools.websocket.on': True,
                                                 'tools.websocket.handler_cls': StreamingWebSocket}})
