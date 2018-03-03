import json

from ws4py.server.wsgiutils import WebSocketWSGIApplication

from broadcast_output import BroadcastOutput
from pi_camera_wrapper import PiCameraWrapper
from pi_camera_web_socket import PiCameraWebSocket

RESPONSE_HEADERS = [('Content-Type', 'application/json')]

class PiCameraWebApplication(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.picamera = PiCameraWrapper()
        self.output = BroadcastOutput(self.picamera)
        self.ws = WebSocketWSGIApplication(handler_cls=PiCameraWebSocket)
        # keep track of connected websocket clients
        # so that we can brodcasts messages sent by one
        # to all of them. Aren't we cool?
        self.clients = []

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'] == '/ws':
            environ['ws4py.app'] = self
            self.picamera.start_streaming(self.output)
            return self.ws(environ, start_response)

        return self.webapp(environ, start_response)

    def webapp(self, env, start_response):
        body = ''
        content_length = int(env.get('CONTENT_LENGTH')) if env.get('CONTENT_LENGTH') else 0

        start_response('200 OK', RESPONSE_HEADERS)

        if (content_length == 0):
            # start_response('400 Bad Request', RESPONSE_HEADERS)
            start_response('200 OK', RESPONSE_HEADERS)
            json_response = json.dumps({
                'resolution': self.picamera.camera.resolution,
                'meter_mode': self.picamera.camera.meter_mode,
                'iso': self.picamera.camera.iso,
                'exposure_mode': self.picamera.camera.exposure_mode,
            })
            body = json_response.encode('gbk')
        else:
            body = env['wsgi.input'].read(content_length)

        yield body
