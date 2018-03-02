from logger import log
from gevent import Greenlet

class BroadcastGreenlet(Greenlet):
    def __init__(self, converter, websocket):
        Greenlet.__init__(self)
        self.converter = converter
        self.websocket = websocket

    def _run(self):
        try:
            while self.websocket.stream is not None:
                buf = self.converter.stdout.read(512)
                if buf:
                    self.websocket.send(buf)
                elif self.converter.poll() is not None:
                    break
        finally:
            log('WebSocket stream is unavailable. Closing socket.')
            self.websocket.close()
            self.converter.stdout.close()
            # calling the above is no guarantee that the application on_close will be invoked
            # thus forcing a call here so we can close it all up
            self.websocket.current_app.on_close('Could not read from stream anymore.')
