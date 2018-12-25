import json
from flask import Flask, request, jsonify, stream_with_context, Response

from lib import logger
from lib import pi_camera_wrapper

PICAMERA = pi_camera_wrapper.PiCameraWrapper()
PICAMERA.start_streaming()

app = Flask(__name__)

@app.route('/snap')
def snap():
    data = open(PICAMERA.snap(), 'rb').read()
    return (data, {'Content-Type': 'image/png', 'Content-Length': len(data)})
 
@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        json_body = request.get_json()

        for key in json_body.keys():
            if key == 'exposure_mode':
                PICAMERA.camera.exposure_mode = json_body[key]
            elif key == 'iso':
                PICAMERA.camera.iso = int(json_body[key])
            else:
                PICAMERA.camera.meter_mode = json_body[key]

    return jsonify(camera_configuration())

@app.route('/stream.mjpg')
def stream():

    @stream_with_context
    def generate():
        try:
            while True:
                with PICAMERA.output.condition:
                    PICAMERA.output.condition.wait()
                    frame = PICAMERA.output.frame
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            logger.log('Error: %s' % str(e))

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

def camera_configuration():
    return {
        'meter_mode': PICAMERA.camera.meter_mode,
        'iso': PICAMERA.camera.iso,
        'exposure_mode': PICAMERA.camera.exposure_mode,
    }
