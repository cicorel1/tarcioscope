import io
import os
import logging

from subprocess import Popen, PIPE

class BroadcastOutput(object):
    def __init__(self, picamera):
        logging.info('Spawning background conversion process')
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
        logging.info('Waiting for background conversion process to exit')
        self.converter.stdin.close()
        self.converter.wait()
