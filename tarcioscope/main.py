import logging

from pi_camera_stream_application import PiCameraStreamApplication

WS_HOST = '0.0.0.0'
WS_PORT = 9000

if __name__ == "__main__":
    from geventwebsocket import WebSocketServer, Resource

    resource = Resource([('/', PiCameraStreamApplication)])
    websocket_server = WebSocketServer((WS_HOST, WS_PORT), resource)

    logging.info('Starting WebSocket server at %s:%s', WS_HOST, WS_PORT)

    websocket_server.serve_forever()
