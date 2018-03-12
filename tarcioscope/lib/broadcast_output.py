import io
import os


from subprocess import Popen, PIPE


from . import logger


class BroadcastOutput(object):
    def __init__(self, picamera):
        logger.log('Spawning background conversion process')
        self.converter = Popen([
            'avconv',
            '-f', 'rawvideo',
            '-pix_fmt', 'yuv420p',
            '-s', '%dx%d' % picamera.camera.resolution,
            '-r', str(float(picamera.camera.framerate)),
            '-i', '-',
            '-f', 'mpeg1video',
            '-b', '800k',
            '-r', str(float(picamera.camera.framerate)),
            '-'],
            stdin=PIPE, stdout=PIPE, stderr=io.open(os.devnull, 'wb'),
            shell=False, close_fds=True)


    def write(self, b):
        self.converter.stdin.write(b)


    def flush(self):
        logger.log('Terminating the conversion process.')
        self.converter.stdin.close()
        self.converter.terminate()
