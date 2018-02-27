from geventwebsocket import WebSocketServer, Resource

from logger import log
from pi_camera_web_application import handle_config_endpoint
from pi_camera_stream_application import PiCameraStreamApplication

HOST = '0.0.0.0'
WS_PORT = 9000

resource = Resource([
    ('/', PiCameraStreamApplication),
    ('/config', handle_config_endpoint)
])

if __name__ == '__main__':
    ws_server = WebSocketServer((HOST, WS_PORT), resource, debug=False)
    ws_server.serve_forever()
