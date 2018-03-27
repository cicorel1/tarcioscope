from wsgiref.simple_server import make_server

from lib import pi_camera_web_application


HOST = '0.0.0.0'
PORT = 8000


if __name__ == '__main__':
    ws_server = make_server(HOST, PORT, pi_camera_web_application.PiCameraWebApplication())
    ws_server.serve_forever()
