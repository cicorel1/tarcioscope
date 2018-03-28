import json
from http import server

from . import logger
from . import streaming_output
from . import pi_camera_wrapper


class StreamingHandler(server.BaseHTTPRequestHandler):
    def __init__(self):
        self.output = streaming_output.StreamingOutput()
        self.picamera = pi_camera_wrapper.PiCameraWrapper()
        self.picamera.start_streaming(self.output)


    def do_OPTIONS(self):
        self.send_response(200)


    def do_POST(self):
        if self.path == '/config':
            content_len = int(self.headers.getheader('Content-Length', 0))
            post_body = self.rfile.read(content_len)

            json_body = json.loads(post_body.decode('gbk'))

            for key in json_body.keys():
                if key == 'exposure_mode':
                    self.picamera.camera.exposure_mode = json_body[key]
                elif key == 'iso':
                    self.picamera.camera.iso = int(json_body[key])
                else:
                    self.picamera.camera.meter_mode = json_body[key]

            body_response = self.camera_configuration().encode('gbk')

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', len(body_response))
            self.end_headers()
            self.wfile.write(body_response)


    def do_GET(self):
        if self.path == '/snap':
            file_name = self.picamera.snap()
            data = open(file_name, 'rb').read()
            self.send_header('Content-Type', 'image/png')
            self.send_header('Content-Length', len(data))
            self.end_headers()
            self.wfile.write(data)
        elif self.path == '/config':
            body_response = self.camera_configuration().encode('gbk')

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', len(body_response))
            self.end_headers()
            self.wfile.write(body_response)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with self.output.condition:
                        self.output.condition.wait()
                        frame = self.output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                self.picamera.stop_streaming()
                logger.log('Removed streaming client %s: %s', self.client_address, str(e))

    def camera_configuration(self):
        return json.dumps({
            'meter_mode': self.picamera.camera.meter_mode,
            'iso': self.picamera.camera.iso,
            'exposure_mode': self.picamera.camera.exposure_mode,
        })
