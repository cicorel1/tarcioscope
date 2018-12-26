from flask import Blueprint, request, jsonify

from tarcioscope.lib.pi_camera_wrapper import PiCameraWrapper

PICAMERA = PiCameraWrapper()

bp = Blueprint('config', __name__, url_prefix='/')

@bp.route('/config', methods=['GET', 'POST'])
def config():
    """Handles both setting and getting the camera's configuration"""
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

def camera_configuration():
    """Builds a dict out of current camera settings"""
    return {
        'meter_mode': PICAMERA.camera.meter_mode,
        'iso': PICAMERA.camera.iso,
        'exposure_mode': PICAMERA.camera.exposure_mode,
    }

