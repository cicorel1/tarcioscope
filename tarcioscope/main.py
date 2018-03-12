from ws4py.server.geventserver import WSGIServer
from lib import pi_camera_web_application


HOST = '0.0.0.0'
PORT = 8000


if __name__ == '__main__':
    ws_server = WSGIServer((HOST, PORT), pi_camera_web_application.PiCameraWebApplication(HOST, PORT))
    ws_server.serve_forever()
