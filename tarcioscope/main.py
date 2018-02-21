import cherrypy
import logging

from ws4py import configure_logger
configure_logger(level=logging.DEBUG)

from streaming_websocket import StreamingWebSocket
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool

from pi_camera_wrapper import PiCameraWrapper
from broadcast_output import BroadcastOutput
from broadcast_thread import BroadcastThread

cherrypy.config.update({ 'server.socket_host': '0.0.0.0', 'server.socket_port': 9000 })
WebSocketPlugin(cherrypy.engine).subscribe()
cherrypy.tools.websocket = WebSocketTool()

class App(object):
    @cherrypy.expose
    def ws(self):
        cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))

        picamera = PiCameraWrapper()
        output = BroadcastOutput(picamera)
        broadcast_thread = BroadcastThread(output.converter, cherrypy.request.ws_handler)
        picamera.start_streaming(output)
        broadcast_thread.start()
        #while True:
        #    picamera.camera.wait_recording(1)


cherrypy.quickstart(App(), '/', config={'/ws': {'tools.websocket.on': True,
                                                 'tools.websocket.handler_cls': StreamingWebSocket}})
