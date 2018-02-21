import cherrypy

from threading import Thread

class BroadcastThread(Thread):
    def __init__(self, converter):
        super(BroadcastThread, self).__init__()
        self.converter = converter

    def run(self):
        try:
            while True:
                buf = self.converter.stdout.read(512)
                if buf:
                    cherrypy.engine.publish('websocket-broadcast', buf, binary=True)
                elif self.converter.poll() is not None:
                    break
        finally:
            self.converter.stdout.close()
