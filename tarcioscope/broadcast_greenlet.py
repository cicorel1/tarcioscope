from logger import log
from gevent import Greenlet

class BroadcastGreenlet(Greenlet):
    def __init__(self, converter, websocket):
        super().__init__()
        self.converter = converter
        self.websocket = websocket

    def _run(self):
        if not self.websocket.closed:
            log('WebSocket connection is open. Streaming...')
            try:
                while True:
                    buf = self.converter.stdout.read(512)
                    if buf:
                        self.websocket.send(buf)
                    elif self.converter.poll() is not None:
                        break
            finally:
                log('Could not write to websocket. Status: %s' % self.websocket.closed)
                # self.converter.stdout.close()
