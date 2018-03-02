from gevent import monkey
monkey.patch_all()

# from geventwebsocket import WebSocketServer, Resource

from ws4py.server.geventserver import WSGIServer
from ws4py.server.wsgiutils import WebSocketWSGIApplication

from logger import log
from pi_camera_web_socket import PiCameraWebSocket
from pi_camera_wrapper import PiCameraWrapper
from pi_camera_web_application import handle_config_endpoint

HOST = '0.0.0.0'
WS_PORT = 8000

# resource = Resource([
#     ('/', PiCameraStreamApplication),
#     ('/config', handle_config_endpoint)
# ])

if __name__ == '__main__':
    ws_server = WSGIServer((HOST, WS_PORT), WebSocketWSGIApplication(handler_cls=PiCameraWebSocket))
    # ws_server = WebSocketServer((HOST, WS_PORT), resource, debug=False)
    ws_server.serve_forever()
