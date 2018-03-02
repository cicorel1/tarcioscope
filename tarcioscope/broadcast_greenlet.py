from logger import log
from gevent import Greenlet

class BroadcastGreenlet(Greenlet):
    def __init__(self, converter, websocket):
        Greenlet.__init__(self)
        self.converter = converter
        self.websocket = websocket

    def _run(self):
        try:
            while True:
                buf = self.converter.stdout.read(512)
                if buf:
                    self.websocket.send(buf, binary=True)
                elif self.converter.poll() is not None:
                    break
        except BrokenPipeError:
            pass
        finally:
            log('WebSocket stream is unavailable. Closing socket.')
            self.converter.stdout.close()
