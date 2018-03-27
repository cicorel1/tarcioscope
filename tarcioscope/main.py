from wsgiref.simple_server import make_server
from ws4py.server.wsgirefserver import WSGIServer, WebSocketWSGIRequestHandler
from ws4py.server.wsgiutils import WebSocketWSGIApplication

from lib import pi_camera_web_application


HOST = '0.0.0.0'
PORT = 8000


if __name__ == '__main__':
    ws_server = make_server(HOST, PORT, server_class=WSGIServer,
                            handler_class=WebSocketWSGIRequestHandler,
                            app=pi_camera_web_application.PiCameraWebApplication())
    ws_server.initialize_websockets_manager()
    ws_server.serve_forever()
