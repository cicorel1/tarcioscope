from flask import Blueprint, stream_with_context, Response

from tarcioscope.lib.logger import log
from tarcioscope.lib.pi_camera_wrapper import PiCameraWrapper

PICAMERA = PiCameraWrapper()
PICAMERA.start_streaming()

bp = Blueprint('api', __name__, url_prefix='/')

@bp.route('/snap')
def snap():
    """Snaps a picture in HIRES"""
    data = open(PICAMERA.snap(), 'rb').read()
    return (data, {'Content-Type': 'image/png', 'Content-Length': len(data)})

@bp.route('/stream.mjpg')
def stream():
    """Stream contents of the camera boundary frames"""

    @stream_with_context
    def generate():
        """Generator function that yields a frame with a content type"""
        try:
            while True:
                with PICAMERA.output.condition:
                    PICAMERA.output.condition.wait()
                    frame = PICAMERA.output.frame
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as err:
            log('Error: %s' % str(err))

    mime_type = 'multipart/x-mixed-replace; boundary=frame'
    return Response(generate(), mimetype=mime_type)

