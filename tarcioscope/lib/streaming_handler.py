import json
from http import server

from . import logger
from . import pi_camera_wrapper

PICAMERA = pi_camera_wrapper.PiCameraWrapper()


class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response_only(200)


    def do_POST(self):
        if self.path == '/config':
            logger.log('Received CONFIG CHANGE request')
            content_len = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_len)

            json_body = json.loads(post_body.decode('gbk'))

            for key in json_body.keys():
                if key == 'exposure_mode':
                    PICAMERA.camera.exposure_mode = json_body[key]
                elif key == 'iso':
                    PICAMERA.camera.iso = int(json_body[key])
                else:
                    PICAMERA.camera.meter_mode = json_body[key]

            body_response = self.camera_configuration().encode('gbk')

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', len(body_response))
            self.end_headers()
            self.wfile.write(body_response)


    def do_GET(self):
        if self.path == '/snap':
            logger.log('Received SNAP request')
            file_name = PICAMERA.snap()
            data = open(file_name, 'rb').read()

            self.send_response(200)

            self.send_header('Content-Type', 'image/png')
            self.send_header('Content-Length', len(data))
            self.end_headers()

            self.wfile.write(data)
            return

        if self.path == '/config':
            logger.log('Received CONFIG request')
            body_response = self.camera_configuration().encode('gbk')

            self.send_response(200)

            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', len(body_response))
            self.end_headers()

            self.wfile.write(body_response)
            return

        if self.path == '/stream.mjpg':
            self.send_response(200)

            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()

            try:
                while True:
                    with PICAMERA.output.condition:
                        PICAMERA.output.condition.wait()
                        frame = PICAMERA.output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()

                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                PICAMERA.stop_streaming()
                logger.log('Removed streaming client %s: %s', self.client_address, str(e))

        self.send_error(404)
        self.end_headers()
        return

    def camera_configuration(self):
        return json.dumps({
            'meter_mode': PICAMERA.camera.meter_mode,
            'iso': PICAMERA.camera.iso,
            'exposure_mode': PICAMERA.camera.exposure_mode,
        })
