import json
from pi_camera_wrapper import PiCameraWrapper

RESPONSE_HEADERS = [('Content-Type', 'application/json')]

def handle_config_endpoint(env, start_response):
    body = ''
    content_length = int(env.get('CONTENT_LENGTH')) if env.get('CONTENT_LENGTH') else 0

    picamera = PiCameraWrapper()

    start_response('200 OK', RESPONSE_HEADERS)

    if (content_length == 0):
        # start_response('400 Bad Request', RESPONSE_HEADERS)
        start_response('200 OK')
        body = json.dumps({ 'resolution': picamera.camera.resolution })
    else:
        body = env['wsgi.input'].read(content_length)

    yield body
