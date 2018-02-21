from pi_camera_stream_application import PiCameraStreamApplication

if __name__ == "__main__":
    from geventwebsocket import WebSocketServer, Resource

    websocket_server = WebSocketServer(('', 9000), Resource([
        ('/', PiCameraStreamApplication)
    ]))
    websocket_server.serve_forever()

