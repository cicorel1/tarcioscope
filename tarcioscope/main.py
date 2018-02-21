import cherrypy

from streaming_websocket import StreamingWebSocket
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool

class App(object):
    @cherrypy.expose
    def ws(self):
        cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))

if __name__ == '__main__':
    import logging

    from ws4py import configure_logger
    configure_logger(level=logging.DEBUG)

    cherrypy.config.update({ 'server.socket_host': '0.0.0.0', 'server.socket_port': 9000 })
    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()

    cherrypy.quickstart(App(), '/', config={
        '/ws': {
            'tools.websocket.on': True,
            'tools.websocket.handler_cls': StreamingWebSocket
            }
        }
    )

    from pi_camera_wrapper import PiCameraWrapper
    from broadcast_output import BroadcastOutput
    from broadcast_thread import BroadcastThread

    try:
        picamera = PiCameraWrapper()
        output = BroadcastOutput(picamera)
        broadcast_thread = BroadcastThread(output.converter)
        picamera.start_streaming(output)
        broadcast_thread.start()

        while True:
            picamera.camera.wait_recording(1)
    except KeyboardInterrupt:
        pass
    finally:
        print('Stopping recording')
        picamera.stop_streaming()
        print('Waiting for broadcast thread to finish')
        broadcast_thread.join()
