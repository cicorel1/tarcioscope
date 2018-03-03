from ws4py.server.geventserver import WSGIServer

from logger import log
from pi_camera_web_socket import PiCameraWebSocket
from pi_camera_wrapper import PiCameraWrapper
from pi_camera_web_application import PiCameraWebApplication

HOST = '0.0.0.0'
PORT = 8000

if __name__ == '__main__':
    ws_server = WSGIServer((HOST, PORT), PiCameraWebApplication(HOST, PORT))
    ws_server.serve_forever()
