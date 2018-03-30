import socketserver
from http import server

from lib import streaming_handler
from lib import pi_camera_wrapper

HOST = '0.0.0.0'
PORT = 8000

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

if __name__ == '__main__':
    try:
        picamera = pi_camera_wrapper.PiCameraWrapper()
        picamera.start_streaming()

        server = StreamingServer((HOST, PORT), streaming_handler.StreamingHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print ('Interrupt recieved; closing server socket')
        picamera.stop_streaming()
        server.socket.close()
