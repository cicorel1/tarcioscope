import json

from ws4py.server.wsgiutils import WebSocketWSGIApplication

from pi_camera_wrapper import PiCameraWrapper
from pi_camera_web_socket import PiCameraWebSocket

HTTP_200_OK = '200 OK'
CONTENT_TYPE = 'Content-Type'
CONTENT_LENGTH = 'Content-Length'

class PiCameraWebApplication(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.picamera = PiCameraWrapper()
        self.ws = WebSocketWSGIApplication(handler_cls=PiCameraWebSocket)
        # keep track of connected websocket clients
        # so that we can brodcasts messages sent by one
        # to all of them. Aren't we cool?
        self.clients = []

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'] == '/ws':
            environ['ws4py.app'] = self
            self.picamera.start_streaming()
            return self.ws(environ, start_response)

        if environ['PATH_INFO'] == '/snap':
            return self.take_snap(environ, start_response)

        return self.webapp(environ, start_response)

    def headers(self, data_length=0, content_type='application/json'):
        return [
            (CONTENT_TYPE, content_type),
            (CONTENT_LENGTH, str(data_length)),
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
            ('Access-Control-Allow-Headers', '%s, %s' % (CONTENT_TYPE, CONTENT_LENGTH))
        ]

    def take_snap(self, env, start_response):
        file_name = self.picamera.snap()
        data = open(file_name, 'rb').read()
        start_response(HTTP_200_OK, self.headers(data_length=len(data), content_type='image/png'))
        return [data]

    def webapp(self, env, start_response):
        body = ''
        content_length = int(env.get('CONTENT_LENGTH')) if env.get('CONTENT_LENGTH') else 0

        if (env.get('REQUEST_METHOD') == 'OPTIONS'):
            start_response(HTTP_200_OK, self.headers(data_length=0))
            return

        if (content_length != 0):
            body = env['wsgi.input'].read(content_length)
            json_body = json.loads(body.decode('gbk'))
            for key in json_body.keys():
                if key == 'exposure_mode':
                    self.picamera.camera.exposure_mode = json_body[key]
                elif key == 'iso':
                    self.picamera.camera.iso = int(json_body[key])
                else:
                    self.picamera.camera.meter_mode = json_body[key]

        json_response = json.dumps({
            'resolution': self.picamera.camera.resolution,
            'meter_mode': self.picamera.camera.meter_mode,
            'iso': self.picamera.camera.iso,
            'exposure_mode': self.picamera.camera.exposure_mode,
        })

        body = json_response.encode('gbk')

        start_response(HTTP_200_OK, self.headers(data_length=len(body)))
        return body
